"""
Player Name Matching Report

Matches auction player names (Wikipedia full names) to
Statsguru abbreviated names. This script is READ-ONLY --
it does not modify any existing CSV files.

Usage:
    python -m scraper.player_matching
"""

import pandas as pd
import re
import difflib
from pathlib import Path

from scraper.config import DATA_DIR


def normalize_name(name):
    """Normalize a player name for comparison."""
    if not isinstance(name, str):
        return ""

    name = name.strip()

    # Remove symbols like †, *, etc.
    name = re.sub(r'[†*#]', '', name)

    # Remove content in parentheses
    name = re.sub(r'\([^)]*\)', '', name)

    # Normalize whitespace
    name = re.sub(r'\s+', ' ', name).strip()

    # Lowercase
    name = name.lower()

    return name


def extract_surname_and_initial(name):
    """
    Extract surname and first initial from a name.

    Returns (surname, first_initial, all_initials)
    """
    parts = name.split()

    if len(parts) == 0:
        return ("", "", "")

    if len(parts) == 1:
        return (parts[0], "", "")

    surname = parts[-1]
    first_initial = parts[0][0] if parts[0] else ""

    # Collect all initials from non-surname parts
    all_initials = "".join(
        p[0] for p in parts[:-1] if p
    )

    return (surname, first_initial, all_initials)


def match_statsguru_pattern(statsguru_name, surname, first_initial):
    """
    Check if a Statsguru name matches a surname + first initial.

    Statsguru names follow patterns like:
        V Kohli, RG Sharma, JJ Bumrah, DPMD Jayawardene
    """
    parts = statsguru_name.split()

    if len(parts) < 2:
        return False

    sg_surname = parts[-1]
    sg_initials = "".join(parts[:-1])

    # Surname must match
    if sg_surname != surname:
        return False

    # First initial must match
    if not sg_initials or not first_initial:
        return False

    if sg_initials[0] != first_initial:
        return False

    return True


def run_matching():
    """Run the full matching pipeline and produce a report."""

    # Load datasets
    combined_file = DATA_DIR / "ipl_combined_raw.csv"
    auction_file = DATA_DIR / "ipl_2025_auction_raw.csv"

    combined_df = pd.read_csv(combined_file)
    auction_df = pd.read_csv(auction_file)

    print("=" * 60)
    print("PLAYER NAME MATCHING REPORT")
    print("=" * 60)
    print(f"\nStatsguru players: {len(combined_df)}")
    print(f"Auction players:   {len(auction_df)}")

    # Get player name lists
    statsguru_players = combined_df["Player"].tolist()
    auction_players = auction_df["Name"].tolist()

    # Normalize all names
    sg_normalized = {
        p: normalize_name(p) for p in statsguru_players
    }
    auc_normalized = {
        p: normalize_name(p) for p in auction_players
    }

    # Build reverse lookup: normalized → original
    sg_by_normalized = {}
    for orig, norm in sg_normalized.items():
        sg_by_normalized.setdefault(norm, []).append(orig)

    # ---- STEP 1: Exact normalized match ----
    exact_matches = {}       # auction_name → statsguru_name
    unmatched_auction = []   # auction names not yet matched

    for auc_orig, auc_norm in auc_normalized.items():
        if auc_norm in sg_by_normalized:
            exact_matches[auc_orig] = sg_by_normalized[auc_norm][0]
        else:
            unmatched_auction.append(auc_orig)

    print(f"\n--- Step 1: Exact normalized match ---")
    print(f"Matched: {len(exact_matches)}")
    print(f"Unmatched: {len(unmatched_auction)}")

    # ---- STEP 2: Surname + Initial match ----
    initial_matches = {}
    ambiguous_matches = {}
    still_unmatched = []

    for auc_name in unmatched_auction:
        auc_norm = auc_normalized[auc_name]
        surname, first_init, all_inits = extract_surname_and_initial(auc_norm)

        if not surname or not first_init:
            still_unmatched.append(auc_name)
            continue

        candidates = []
        for sg_orig, sg_norm in sg_normalized.items():
            if match_statsguru_pattern(sg_norm, surname, first_init):
                candidates.append(sg_orig)

        if len(candidates) == 1:
            initial_matches[auc_name] = candidates[0]
        elif len(candidates) > 1:
            ambiguous_matches[auc_name] = candidates
        else:
            still_unmatched.append(auc_name)

    print(f"\n--- Step 2: Surname + Initial match ---")
    print(f"Matched: {len(initial_matches)}")
    print(f"Ambiguous: {len(ambiguous_matches)}")
    print(f"Still unmatched: {len(still_unmatched)}")

    # ---- STEP 3: Fuzzy match for remaining ----
    fuzzy_candidates = {}
    truly_unmatched = []

    sg_norm_list = list(sg_normalized.values())
    sg_orig_list = list(sg_normalized.keys())

    for auc_name in still_unmatched:
        auc_norm = auc_normalized[auc_name]

        # Use SequenceMatcher for fuzzy matching
        best_matches = difflib.get_close_matches(
            auc_norm,
            sg_norm_list,
            n=3,
            cutoff=0.55
        )

        if best_matches:
            candidates = []
            for match in best_matches:
                idx = sg_norm_list.index(match)
                candidates.append(
                    (sg_orig_list[idx], match,
                     difflib.SequenceMatcher(
                         None, auc_norm, match
                     ).ratio())
                )
            fuzzy_candidates[auc_name] = candidates
        else:
            truly_unmatched.append(auc_name)

    print(f"\n--- Step 3: Fuzzy candidates ---")
    print(f"With candidates: {len(fuzzy_candidates)}")
    print(f"No match at all: {len(truly_unmatched)}")

    # ---- DETAILED REPORT ----
    print("\n" + "=" * 60)
    print("DETAILED RESULTS")
    print("=" * 60)

    # Print exact matches
    print(f"\n{'-' * 40}")
    print(f"EXACT MATCHES ({len(exact_matches)})")
    print(f"{'-' * 40}")
    for auc, sg in sorted(exact_matches.items()):
        print(f"  {auc:35s} -> {sg}")

    # Print initial-based matches
    print(f"\n{'-' * 40}")
    print(f"INITIAL-BASED MATCHES ({len(initial_matches)})")
    print(f"{'-' * 40}")
    for auc, sg in sorted(initial_matches.items()):
        print(f"  {auc:35s} -> {sg}")

    # Print ambiguous matches
    if ambiguous_matches:
        print(f"\n{'-' * 40}")
        print(f"!! AMBIGUOUS MATCHES ({len(ambiguous_matches)})")
        print(f"{'-' * 40}")
        for auc, candidates in sorted(ambiguous_matches.items()):
            print(f"  {auc}:")
            for c in candidates:
                print(f"    - {c}")

    # Print fuzzy candidates
    if fuzzy_candidates:
        print(f"\n{'-' * 40}")
        print(f"FUZZY CANDIDATES ({len(fuzzy_candidates)})")
        print(f"{'-' * 40}")
        for auc, candidates in sorted(fuzzy_candidates.items()):
            print(f"  {auc}:")
            for sg_orig, sg_norm, score in candidates:
                print(f"    - {sg_orig:30s} (score: {score:.2f})")

    # Print truly unmatched
    if truly_unmatched:
        print(f"\n{'-' * 40}")
        print(f"TRULY UNMATCHED AUCTION PLAYERS ({len(truly_unmatched)})")
        print(f"{'-' * 40}")
        for name in sorted(truly_unmatched):
            # Check if this is a newcomer (— N/a matches)
            row = auction_df[auction_df["Name"] == name].iloc[0]
            ipl_matches = row.get("No. of IPL matches", "")
            print(f"  {name:35s} (IPL matches: {ipl_matches})")

    # ---- Unmatched Statsguru summary ----
    all_matched_sg = set(exact_matches.values()) | set(initial_matches.values())
    unmatched_sg = [
        p for p in statsguru_players if p not in all_matched_sg
    ]
    print(f"\n{'-' * 40}")
    print(f"STATSGURU PLAYERS WITHOUT AUCTION DATA")
    print(f"{'-' * 40}")
    print(f"  Total: {len(unmatched_sg)} out of {len(statsguru_players)}")
    print(f"  (This is expected -- most historical players")
    print(f"   were not part of the 2025 auction)")

    # ---- SUMMARY ----
    total_confirmed = len(exact_matches) + len(initial_matches)
    print(f"\n{'=' * 60}")
    print(f"MATCHING SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Auction players total:        {len(auction_players)}")
    print(f"  Exact matches:                {len(exact_matches)}")
    print(f"  Initial-based matches:        {len(initial_matches)}")
    print(f"  Confirmed matches total:      {total_confirmed}")
    print(f"  Ambiguous (need review):      {len(ambiguous_matches)}")
    print(f"  Fuzzy candidates (review):    {len(fuzzy_candidates)}")
    print(f"  Truly unmatched:              {len(truly_unmatched)}")
    print(f"{'=' * 60}")

    # Save matching results to a CSV for reference
    results = []

    for auc, sg in exact_matches.items():
        results.append({
            "Auction_Name": auc,
            "Statsguru_Name": sg,
            "Match_Type": "exact",
            "Confidence": "high"
        })

    for auc, sg in initial_matches.items():
        results.append({
            "Auction_Name": auc,
            "Statsguru_Name": sg,
            "Match_Type": "initial",
            "Confidence": "high"
        })

    for auc, candidates in ambiguous_matches.items():
        for c in candidates:
            results.append({
                "Auction_Name": auc,
                "Statsguru_Name": c,
                "Match_Type": "ambiguous",
                "Confidence": "review"
            })

    for auc, candidates in fuzzy_candidates.items():
        for sg_orig, sg_norm, score in candidates:
            results.append({
                "Auction_Name": auc,
                "Statsguru_Name": sg_orig,
                "Match_Type": "fuzzy",
                "Confidence": f"score={score:.2f}"
            })

    for name in truly_unmatched:
        results.append({
            "Auction_Name": name,
            "Statsguru_Name": "",
            "Match_Type": "unmatched",
            "Confidence": "none"
        })

    results_df = pd.DataFrame(results)
    output_path = DATA_DIR.parent / "processed" / "matching_report.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)
    print(f"\nMatching report saved to: {output_path}")

    return {
        "exact": exact_matches,
        "initial": initial_matches,
        "ambiguous": ambiguous_matches,
        "fuzzy": fuzzy_candidates,
        "unmatched": truly_unmatched
    }


if __name__ == "__main__":
    run_matching()
