import pandas as pd

from src.utils.youtube_api import (
    get_video_comments,
    get_video_details,
    search_astrology_videos,
    setup_youtube_api,
)

from src.utils.data_processing import analyze_comment_sentiment, create_derived_variables
from src.config import COMMENTS_ANALYSIS_LIMIT, MAX_COMMENTS_PER_VIDEO


def collect_youtube_data(api_key, max_videos=120):
    youtube = setup_youtube_api(api_key)
    video_ids = search_astrology_videos(youtube, max_videos)

    if not video_ids:
        return None

    videos_data = get_video_details(youtube, video_ids)

    if not videos_data:
        return None

    df = pd.DataFrame(videos_data)

    all_comments = []
    comment_sentiments = []

    for idx, video_id in enumerate(df["video_id"].head(COMMENTS_ANALYSIS_LIMIT)):
        comments = get_video_comments(
            youtube, video_id, max_comments=MAX_COMMENTS_PER_VIDEO // 2
        )
        all_comments.append(comments)

        sentiment, score = analyze_comment_sentiment(comments)
        comment_sentiments.append({"sentiment": sentiment, "score": score})

    df_comments = pd.DataFrame(comment_sentiments)
    if len(df_comments) > 0:
        df.loc[: len(df_comments) - 1, "comment_sentiment"] = df_comments["sentiment"]
        df.loc[: len(df_comments) - 1, "sentiment_score"] = df_comments["score"]

    df["comment_sentiment"] = df["comment_sentiment"].fillna("нейтральная")
    df["sentiment_score"] = df["sentiment_score"].fillna(0)
    df = create_derived_variables(df)

    return df
