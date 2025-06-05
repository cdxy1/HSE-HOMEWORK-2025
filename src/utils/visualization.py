import matplotlib.pyplot as plt


def create_visualizations(df):
    plt.style.use("default")
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle(
        "Анализ YouTube контента по астрологии", fontsize=16, fontweight="bold"
    )

    axes[0, 0].hist(
        df["log_views"], bins=30, alpha=0.7, color="skyblue", edgecolor="black"
    )
    axes[0, 0].set_title("Распределение просмотров (log)")
    axes[0, 0].set_xlabel("Логарифм просмотров")
    axes[0, 0].set_ylabel("Частота")

    duration_views = df.groupby("duration_category")["view_count"].mean()
    axes[0, 1].bar(
        duration_views.index,
        duration_views.values,
        color=["lightcoral", "lightgreen", "lightblue"],
    )
    axes[0, 1].set_title("Средние просмотры по категориям длительности")
    axes[0, 1].set_ylabel("Среднее количество просмотров")
    axes[0, 1].tick_params(axis="x", rotation=45)

    time_views = df.groupby("time_of_day")["view_count"].mean()
    axes[0, 2].bar(
        time_views.index, time_views.values, color=["gold", "orange", "red", "purple"]
    )
    axes[0, 2].set_title("Средние просмотры по времени суток")
    axes[0, 2].set_ylabel("Среднее количество просмотров")

    corr_data = df[
        ["view_count", "like_count", "comment_count", "duration_minutes"]
    ].corr()
    axes[1, 0].imshow(corr_data, cmap="coolwarm", aspect="auto", vmin=-1, vmax=1)
    axes[1, 0].set_xticks(range(len(corr_data.columns)))
    axes[1, 0].set_yticks(range(len(corr_data.columns)))
    axes[1, 0].set_xticklabels(corr_data.columns, rotation=45)
    axes[1, 0].set_yticklabels(corr_data.columns)
    axes[1, 0].set_title("Корреляционная матрица")

    for i in range(len(corr_data.columns)):
        for j in range(len(corr_data.columns)):
            axes[1, 0].text(
                j,
                i,
                f"{corr_data.iloc[i, j]:.2f}",
                ha="center",
                va="center",
                color="white" if abs(corr_data.iloc[i, j]) > 0.5 else "black",
            )

    axes[1, 1].scatter(
        df["total_astro_terms"], df["log_views"], alpha=0.6, color="mediumpurple"
    )
    axes[1, 1].set_xlabel("Количество астрологических терминов")
    axes[1, 1].set_ylabel("Логарифм просмотров")
    axes[1, 1].set_title("Термины vs Популярность")

    sentiment_counts = df["comment_sentiment"].value_counts()
    axes[1, 2].pie(
        sentiment_counts.values,
        labels=sentiment_counts.index,
        autopct="%1.1f%%",
        colors=["lightgreen", "lightcoral", "lightgray"],
    )
    axes[1, 2].set_title("Тональность комментариев")

    plt.tight_layout()
    plt.show()
