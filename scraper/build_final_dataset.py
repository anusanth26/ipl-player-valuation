import pandas as pd
from pathlib import Path
from scraper.config import DATA_DIR
import numpy as np

def build_final_dataset():
    """
    Builds the final analysis-ready dataset by merging the combined
    performance data with the auction data using the confirmed name mappings.
    """
    combined_file = DATA_DIR / "ipl_combined_raw.csv"
    auction_file = DATA_DIR / "ipl_2025_auction_raw.csv"
    matching_file = DATA_DIR.parent / "processed" / "matching_report.csv"

    print("Loading datasets...")
    perf_df = pd.read_csv(combined_file)
    auction_df = pd.read_csv(auction_file)
    matches_df = pd.read_csv(matching_file)

    # 1. Keep only confirmed matches (exact and initial)
    matched_only = matches_df[matches_df["Match_Type"].isin(["exact", "initial"])].copy()
    
    # 2. Add our manual resolutions for ambiguous/fuzzy matches
    manual_resolutions = {
        "Jitesh Sharma": "JM Sharma",
        "Ashutosh Sharma": "AR Sharma",
        "Karn Sharma": "KV Sharma",
        "Shubham Dubey": "SB Dubey",
        "Prasidh Krishna": "M Prasidh Krishna",
        "Rasikh Salam Dar": "Rasikh Salam",
        "Sai Kishore †": "R Sai Kishore",
        "Dushmantha Chameera": "PVD Chameera",
        "Wanindu Hasaranga": "PW Hasaranga"
    }

    # Remove any existing rows for the manual resolutions to avoid duplicates
    matched_only = matched_only[~matched_only["Auction_Name"].isin(manual_resolutions.keys())]

    # Append manual resolutions
    manual_rows = pd.DataFrame([
        {
            "Auction_Name": k,
            "Statsguru_Name": v,
            "Match_Type": "manual_resolution",
            "Confidence": "high"
        }
        for k, v in manual_resolutions.items()
    ])
    
    final_matches = pd.concat([matched_only, manual_rows], ignore_index=True)
    
    # Create mapping dictionary
    name_map = dict(zip(final_matches["Auction_Name"], final_matches["Statsguru_Name"]))

    # 3. Clean auction data
    print("\nCleaning auction data...")
    # Normalize column names to exact matches to handle potential trailing spaces
    auction_df.columns = auction_df.columns.str.strip()
    
    # Clean the Name column of trailing spaces
    auction_df["Name"] = auction_df["Name"].str.strip()
    
    # Keep only the players we mapped
    auction_matched = auction_df[auction_df["Name"].isin(name_map.keys())].copy()
    
    # Rename columns to standard names
    rename_dict = {
        "Name": "Auction_Name",
        "Country": "Country",
        "Role": "Role",
        "Base price ( ₹ lakhs )": "Base_Price_Lakh",
        "Auctioned price ( ₹ lakhs )": "Auction_Price_Lakh",
        "2025 IPL team": "Auction_Team"
    }
    
    # Only keep the columns we need
    auction_clean = auction_matched[list(rename_dict.keys())].rename(columns=rename_dict)
    
    # Apply the name mapping so we can merge with Statsguru data
    auction_clean["Player"] = auction_clean["Auction_Name"].map(name_map)
    
    # Drop Auction_Name as we now have Player
    auction_clean = auction_clean.drop(columns=["Auction_Name"])
    
    # Convert Auction_Price_Lakh to numeric, coercing errors to NaN (handles "— N/a")
    auction_clean["Auction_Price_Lakh"] = pd.to_numeric(auction_clean["Auction_Price_Lakh"], errors="coerce")
    auction_clean["Base_Price_Lakh"] = pd.to_numeric(auction_clean["Base_Price_Lakh"], errors="coerce")
    
    # 4. Merge datasets
    print("\nMerging datasets...")
    # Inner join because we only want players who have BOTH performance data and auction data
    final_df = pd.merge(perf_df, auction_clean, on="Player", how="inner")
    
    # 5. Save final dataset
    output_file = DATA_DIR.parent / "final" / "ipl_player_dataset.csv"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    final_df.to_csv(output_file, index=False)
    
    print("=" * 60)
    print("FINAL DATASET SUMMARY")
    print("=" * 60)
    print(f"Statsguru players: {len(perf_df)}")
    print(f"Auction players: {len(auction_df)}")
    print(f"Matched players: {len(final_df)}")
    print(f"\nFinal columns ({len(final_df.columns)}):")
    for col in final_df.columns:
        print(f" - {col}")
    
    print(f"\nMissing auction prices: {final_df['Auction_Price_Lakh'].isna().sum()}")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    build_final_dataset()
