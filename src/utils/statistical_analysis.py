import numpy as np
import pandas as pd
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


def statistical_analysis(df):
    results = {}

    duration_groups = [
        group["view_count"].values for name, group in df.groupby("duration_category")
    ]
    f_stat, p_value_anova = stats.f_oneway(*duration_groups)

    results["anova"] = {
        "f_stat": f_stat,
        "p_value": p_value_anova,
        "significant": p_value_anova < 0.05,
    }

    for category in df["duration_category"].unique():
        if pd.notna(category):
            subset = df[df["duration_category"] == category]
            results[f"duration_{category}"] = {
                "mean_views": subset["view_count"].mean(),
                "std_views": subset["view_count"].std(),
                "count": len(subset),
            }

    sentiment_score_corr = df["sentiment_score"].corr(df["view_count"])
    sentiment_likes_corr = df["sentiment_score"].corr(df["like_count"])

    n = len(df.dropna(subset=["sentiment_score", "view_count"]))
    t_stat = sentiment_score_corr * np.sqrt((n - 2) / (1 - sentiment_score_corr**2))
    p_value_corr = 2 * (1 - stats.t.cdf(abs(t_stat), n - 2))

    results["correlation"] = {
        "sentiment_views": sentiment_score_corr,
        "sentiment_likes": sentiment_likes_corr,
        "t_stat": t_stat,
        "p_value": p_value_corr,
        "significant": p_value_corr < 0.05,
    }

    for sentiment in df["comment_sentiment"].unique():
        if pd.notna(sentiment):
            subset = df[df["comment_sentiment"] == sentiment]
            results[f"sentiment_{sentiment}"] = {
                "mean_views": subset["view_count"].mean(),
                "mean_likes": subset["like_count"].mean(),
                "count": len(subset),
            }

    df_reg = df.copy()
    df_reg = pd.get_dummies(
        df_reg, columns=["duration_category", "time_of_day"], prefix=["dur", "time"]
    )

    predictors = [
        "duration_minutes",
        "title_length",
        "description_length",
        "tags_count",
        "total_astro_terms",
        "sentiment_score",
    ]

    dummy_cols = [col for col in df_reg.columns if col.startswith(("dur_", "time_"))]
    predictors.extend(dummy_cols)
    available_predictors = [col for col in predictors if col in df_reg.columns]
    df_clean = df_reg[available_predictors + ["log_views"]].dropna()

    if len(df_clean) > 10:
        X = df_clean[available_predictors]
        y = df_clean["log_views"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )

        model = LinearRegression()
        model.fit(X_train, y_train)

        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        r2_train = r2_score(y_train, y_pred_train)
        r2_test = r2_score(y_test, y_pred_test)

        feature_importance = pd.DataFrame(
            {
                "feature": available_predictors,
                "coefficient": model.coef_,
                "abs_coefficient": np.abs(model.coef_),
            }
        ).sort_values("abs_coefficient", ascending=False)

        results["regression"] = {
            "r2_train": r2_train,
            "r2_test": r2_test,
            "feature_importance": feature_importance,
        }

    return results
