import isodate
import numpy as np
import pandas as pd

from src.config import ASTRO_TERMS, NEGATIVE_WORDS, POSITIVE_WORDS


def parse_duration(duration_str):
    try:
        duration = isodate.parse_duration(duration_str)
        return duration.total_seconds() / 60
    except Exception:
        return 0


def categorize_duration(minutes):
    if minutes < 5:
        return "Короткие"
    elif minutes <= 20:
        return "Средние"
    else:
        return "Длинные"


def extract_astrology_terms(text):
    text_lower = text.lower()
    count = sum(1 for term in ASTRO_TERMS if term in text_lower)
    return count


def analyze_comment_sentiment(comments):
    if not comments:
        return "нейтральная", 0

    total_positive = 0
    total_negative = 0

    for comment in comments:
        text_lower = comment["text"].lower()
        total_positive += sum(1 for word in POSITIVE_WORDS if word in text_lower)
        total_negative += sum(1 for word in NEGATIVE_WORDS if word in text_lower)

    if total_positive > total_negative:
        return "позитивная", total_positive - total_negative
    elif total_negative > total_positive:
        return "негативная", total_negative - total_positive
    else:
        return "нейтральная", 0


def create_derived_variables(df):
    df["duration_minutes"] = df["duration"].apply(parse_duration)
    df["duration_category"] = df["duration_minutes"].apply(categorize_duration)
    df["title_length"] = df["title"].str.len()
    df["description_length"] = df["description"].str.len()
    df["description_words"] = df["description"].str.split().str.len()
    df["tags_count"] = df["tags"].apply(lambda x: len(x) if x else 0)
    df["astro_terms_title"] = df["title"].apply(extract_astrology_terms)
    df["astro_terms_desc"] = df["description"].apply(extract_astrology_terms)
    df["total_astro_terms"] = df["astro_terms_title"] + df["astro_terms_desc"]
    df["published_datetime"] = pd.to_datetime(df["published_at"]).dt.tz_localize(None)
    df["day_of_week"] = df["published_datetime"].dt.day_name()
    df["hour"] = df["published_datetime"].dt.hour
    df["month"] = df["published_datetime"].dt.month
    df["time_of_day"] = df["hour"].apply(
        lambda x: "Утро"
        if 6 <= x < 12
        else "День"
        if 12 <= x < 18
        else "Вечер"
        if 18 <= x < 24
        else "Ночь"
    )
    df["engagement_rate"] = (df["like_count"] + df["comment_count"]) / df[
        "view_count"
    ].replace(0, 1)
    df["like_rate"] = df["like_count"] / df["view_count"].replace(0, 1)
    df["comment_rate"] = df["comment_count"] / df["view_count"].replace(0, 1)
    df["log_views"] = np.log1p(df["view_count"])
    df["log_likes"] = np.log1p(df["like_count"])
    df["log_comments"] = np.log1p(df["comment_count"])

    return df


def describe_dataset(df):
    stats = {
        "videos_count": len(df),
        "variables_count": len(df.columns),
        "period_start": df["published_datetime"].min(),
        "period_end": df["published_datetime"].max(),
        "numeric_stats": df[
            ["view_count", "like_count", "comment_count", "duration_minutes"]
        ].describe(),
        "duration_distribution": df["duration_category"].value_counts(),
        "time_distribution": df["time_of_day"].value_counts(),
        "top_channels": df["channel_title"].value_counts().head(10),
    }
    return stats


def additional_analysis(df):
    results = {}

    day_stats = (
        df.groupby("day_of_week")
        .agg({"view_count": "mean", "engagement_rate": "mean", "video_id": "count"})
        .round(2)
    )
    results["day_stats"] = day_stats

    channel_stats = (
        df.groupby("channel_title")
        .agg({"view_count": "mean", "like_count": "mean", "video_id": "count"})
        .sort_values("view_count", ascending=False)
        .head()
    )
    results["channel_stats"] = channel_stats

    df["astro_terms_category"] = pd.cut(
        df["total_astro_terms"],
        bins=[0, 1, 3, float("inf")],
        labels=["Мало (0-1)", "Средне (2-3)", "Много (4+)"],
    )

    astro_analysis = (
        df.groupby("astro_terms_category")
        .agg({"view_count": "mean", "like_count": "mean", "engagement_rate": "mean"})
        .round(2)
    )
    results["astro_analysis"] = astro_analysis

    return results
