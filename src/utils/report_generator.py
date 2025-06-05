from datetime import datetime

import pandas as pd


def generate_reports(df):
    output_filename = (
        f"youtube_astrology_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )
    df.to_excel(output_filename, index=False, engine="openpyxl")

    summary_stats = pd.DataFrame(
        {
            "Метрика": [
                "Всего видео",
                "Средние просмотры",
                "Средние лайки",
                "Средние комментарии",
                "Средняя длительность (мин)",
                "Период анализа",
            ],
            "Значение": [
                len(df),
                f"{df['view_count'].mean():.0f}",
                f"{df['like_count'].mean():.0f}",
                f"{df['comment_count'].mean():.0f}",
                f"{df['duration_minutes'].mean():.1f}",
                f"{df['published_datetime'].min().date()} - {df['published_datetime'].max().date()}",
            ],
        }
    )

    category_analysis = (
        df.groupby("duration_category")
        .agg(
            {
                "view_count": ["count", "mean", "std"],
                "like_count": "mean",
                "engagement_rate": "mean",
            }
        )
        .round(2)
    )

    correlation_matrix = df[
        [
            "view_count",
            "like_count",
            "comment_count",
            "duration_minutes",
            "title_length",
            "total_astro_terms",
            "engagement_rate",
        ]
    ].corr()

    report_filename = (
        f"astrology_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )
    with pd.ExcelWriter(report_filename, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Основные данные", index=False)
        summary_stats.to_excel(writer, sheet_name="Сводная статистика", index=False)
        category_analysis.to_excel(writer, sheet_name="Анализ по категориям")
        correlation_matrix.to_excel(writer, sheet_name="Корреляции")

    return output_filename, report_filename
