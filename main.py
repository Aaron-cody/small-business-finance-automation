"""Run the full small-business finance automation workflow."""

from src.analyze_finance import analyze_finance
from src.clean_data import clean_data
from src.generate_report import generate_report
from src.generate_sample_data import generate_sample_data


def main() -> None:
    print("1/4 Generating messy sample finance data...")
    generate_sample_data()

    print("2/4 Cleaning and validating data...")
    clean_data()

    print("3/4 Calculating finance metrics...")
    analyze_finance()

    print("4/4 Generating dashboard-ready charts...")
    generate_report()

    print("Pipeline complete. Review the generated files in outputs/.")


if __name__ == "__main__":
    main()

