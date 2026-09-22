from bs4 import BeautifulSoup
import pandas as pd


def extract_table(html, table_type):
    """
    Extract batting or bowling statistics table
    from the Statsguru page.
    """

    soup = BeautifulSoup(html, "lxml")
    tables = soup.find_all("table", class_="engineTable")

    selected_table = None

    for table in tables:

        headers = [
            th.get_text(strip=True)
            for th in table.find_all("th")
        ]

        # Find batting table
        if table_type == "batting":
            if (
                "Player" in headers
                and "Runs" in headers
                and "BF" in headers
            ):
                selected_table = table
                break

        # Find bowling table
        elif table_type == "bowling":
            if (
                "Player" in headers
                and "Wkts" in headers
                and "Overs" in headers
                and "Econ" in headers
            ):
                selected_table = table
                break

    if selected_table is None:
        raise Exception(
            f"{table_type.capitalize()} statistics table not found!"
        )

    headers = [
        th.get_text(strip=True)
        for th in selected_table.find_all("th")
    ]

    rows = []

    for tr in selected_table.find_all("tr")[1:]:

        cols = tr.find_all("td")

        if len(cols) != len(headers):
            continue

        row = [
            col.get_text(" ", strip=True)
            for col in cols
        ]

        rows.append(row)

    df = pd.DataFrame(rows, columns=headers)

    return df