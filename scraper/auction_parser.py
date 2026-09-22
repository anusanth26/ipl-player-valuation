from bs4 import BeautifulSoup
import pandas as pd


def extract_auction_tables(html):

    soup = BeautifulSoup(html, "lxml")

    tables = soup.find_all("table")

    all_players = []

    for table in tables:

        # Get table headers
        header_row = table.find("tr")

        if not header_row:
            continue

        headers = [
            cell.get_text(
                " ",
                strip=True
            )
            for cell in header_row.find_all(
                ["th", "td"]
            )
        ]

        # Normalize header names
        header_text = " ".join(
            headers
        ).lower()

        # Identify auction player tables
        if (
            "name" not in header_text
            or "base price" not in header_text
            or "auctioned price" not in header_text
        ):
            continue

        rows = []

        for tr in table.find_all("tr")[1:]:

            cells = tr.find_all(
                ["td", "th"]
            )

            if not cells:
                continue

            row = [
                cell.get_text(
                    " ",
                    strip=True
                )
                for cell in cells
            ]

            # Make sure row matches header count
            if len(row) != len(headers):
                continue

            rows.append(row)

        if not rows:
            continue

        df = pd.DataFrame(
            rows,
            columns=headers
        )

        # Print information about this auction table
        print("\nAuction table found")
        print("Headers:", headers)
        print("Rows:", len(rows))

        all_players.append(df)

    if not all_players:
        raise Exception(
            "No IPL auction tables found!"
        )

    # Combine all auction sets
    final_df = pd.concat(
        all_players,
        ignore_index=True
    )

    return final_df