from config import API_KEY, MAX_VIDEOS_DEFAULT
from utils.data_collector import collect_youtube_data
from utils.data_processing import additional_analysis, describe_dataset
from utils.report_generator import generate_reports
from utils.statistical_analysis import statistical_analysis
from utils.visualization import create_visualizations


def main():
    df = collect_youtube_data(API_KEY, max_videos=MAX_VIDEOS_DEFAULT)

    if df is None:
        return

    dataset_stats = describe_dataset(df)

    create_visualizations(df)

    analysis_results = statistical_analysis(df)

    additional_results = additional_analysis(df)

    generate_reports(df)

    return df, dataset_stats, analysis_results, additional_results


if __name__ == "__main__":
    results = main()
