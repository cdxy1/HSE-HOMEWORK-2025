from googleapiclient.discovery import build

from src.config import BATCH_SIZE, SEARCH_TERMS


def setup_youtube_api(api_key):
    return build("youtube", "v3", developerKey=api_key)


def search_astrology_videos(youtube, max_results):
    all_video_ids = []

    for term in SEARCH_TERMS:
        try:
            search_response = (
                youtube.search()
                .list(
                    q=term,
                    part="id",
                    maxResults=min(25, max_results // len(SEARCH_TERMS)),
                    type="video",
                    regionCode="RU",
                    relevanceLanguage="ru",
                    order="relevance",
                )
                .execute()
            )

            video_ids = [item["id"]["videoId"] for item in search_response["items"]]
            all_video_ids.extend(video_ids)

        except Exception:
            pass

    unique_video_ids = list(set(all_video_ids))
    return unique_video_ids[:max_results]


def get_video_details(youtube, video_ids):
    videos_data = []

    for i in range(0, len(video_ids), BATCH_SIZE):
        batch_ids = video_ids[i : i + BATCH_SIZE]

        try:
            videos_response = (
                youtube.videos()
                .list(
                    part="snippet,statistics,contentDetails,topicDetails",
                    id=",".join(batch_ids),
                )
                .execute()
            )

            for item in videos_response["items"]:
                video_data = extract_video_info(item)
                videos_data.append(video_data)

        except Exception:
            pass

    return videos_data


def extract_video_info(item):
    snippet = item["snippet"]
    statistics = item["statistics"]
    content_details = item["contentDetails"]

    video_info = {
        "kind": item["kind"],
        "video_id": item["id"],
        "published_at": snippet["publishedAt"],
        "channel_id": snippet["channelId"],
        "channel_title": snippet["channelTitle"],
        "title": snippet["title"],
        "description": snippet.get("description", ""),
        "tags": snippet.get("tags", []),
        "category_id": snippet.get("categoryId", ""),
        "duration": content_details["duration"],
        "view_count": int(statistics.get("viewCount", 0)),
        "like_count": int(statistics.get("likeCount", 0)),
        "comment_count": int(statistics.get("commentCount", 0)),
    }

    if "topicDetails" in item:
        video_info["topic_categories"] = item["topicDetails"].get("topicCategories", [])
    else:
        video_info["topic_categories"] = []

    return video_info


def get_video_comments(youtube, video_id, max_comments=20):
    try:
        comments_response = (
            youtube.commentThreads()
            .list(
                part="snippet",
                videoId=video_id,
                maxResults=max_comments,
                order="relevance",
            )
            .execute()
        )

        comments = []
        for item in comments_response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append(
                {
                    "text": comment["textDisplay"],
                    "like_count": comment["likeCount"],
                    "published_at": comment["publishedAt"],
                }
            )

        return comments

    except Exception:
        return []
