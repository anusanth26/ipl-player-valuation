import pandas as pd

from scraper.config import DATA_DIR


def merge_batting_bowling():

    batting_file = DATA_DIR / "ipl_batting_raw.csv"
    bowling_file = DATA_DIR / "ipl_bowling_raw.csv"

    batting_df = pd.read_csv(batting_file)
    bowling_df = pd.read_csv(bowling_file)

    print("Batting dataset:", batting_df.shape)
    print("Bowling dataset:", bowling_df.shape)

    # Rename batting columns
    batting_df = batting_df.rename(columns={
        "Inns": "Bat_Inns",
        "Runs": "Bat_Runs",
        "Ave": "Bat_Ave",
        "SR": "Bat_SR"
    })

    # Rename bowling columns
    bowling_df = bowling_df.rename(columns={
        "Inns": "Bowl_Inns",
        "Runs": "Bowl_Runs",
        "Ave": "Bowl_Ave",
        "SR": "Bowl_SR",
        "4": "4W",
        "5": "5W"
    })

    # Remove unnecessary columns
    batting_df = batting_df.drop(
        columns=["Unnamed: 15"],
        errors="ignore"
    )

    bowling_df = bowling_df.drop(
        columns=["Unnamed: 14"],
        errors="ignore"
    )

    # We already have Mat from batting
    bowling_df = bowling_df.drop(
        columns=["Mat","Span"],
        errors="ignore"
    )

    # Merge using Player
    combined_df = pd.merge(
        batting_df,
        bowling_df,
        on="Player",
        how="outer"
    )

    print("\nCombined dataset:")
    print(combined_df.head())

    print("\nCombined shape:")
    print(combined_df.shape)

    print("\nColumns:")
    print(combined_df.columns.tolist())

    # Save combined dataset
    output_file = DATA_DIR / "ipl_combined_raw.csv"

    combined_df.to_csv(
        output_file,
        index=False
    )

    print("\nSaved to:")
    print(output_file)


if __name__ == "__main__":
    merge_batting_bowling()