# Business Analytics Individual Case Study — Project Continuation Documentation

## 1. Purpose of This Document

This document is a handoff document for a new AI agent/contributor. It contains the project requirements, selected topic, problem statement, objectives, data sources, current implementation, files/code already created, important decisions, known issues, and the exact next steps.

The new agent should continue from the current stage rather than redesigning the project from scratch.

---

# 2. Project Overview

## Project Domain

**Sports Analytics / T20 Franchise Management**

## Working Title

**Data-Driven Player Valuation and Auction Strategy for T20 Franchise Cricket Using Business Analytics**

The project focuses on IPL/T20 franchise cricket auctions and uses player performance statistics together with auction prices to study player value and budget efficiency.

## Core Business Problem

T20 franchise teams operate under strict auction/salary budgets. Auction decisions can be influenced by player reputation, media attention, and traditional perceptions rather than a systematic comparison of performance and cost.

The project aims to use data to answer two related questions:

1. How can players be objectively classified according to their cricket performance?
2. How does a player's performance compare with the amount paid for that player at auction?

The second question is the central business-analysis component. It allows the project to identify players who provide relatively high performance for their auction cost and players whose auction prices are high relative to measured performance.

---

# 3. Refined Problem Statement

The current refined problem statement is:

> Franchise T20 cricket teams operate under strict salary caps but frequently overpay for marquee players based on emotional bias, media hype, and traditional reputations during auctions. This reliance on intuition rather than granular data leads to the “winner’s curse,” resulting in imbalanced squads and inefficient budget allocation. Existing valuation approaches typically stop at classifying players into broad performance tiers, without explicitly relating performance to cost — leaving the question of value (not just quality) largely unanswered. The objective of this project is to develop a predictive classification model using scraped performance metrics to objectively identify high-impact players, and extend this with a performance-price efficiency framework that maps each player’s on-field output against their auction cost. By clustering players along this performance-vs-price frontier, the model distinguishes “undervalued gems” (high performance, low cost), “fairly priced elite” players, and “overpriced” picks driven by reputation rather than output. This provides management with a data-driven strategy to not only shortlist high-impact players, but to explicitly target budget-efficient acquisitions — optimizing their auction purse and assembling a balanced, highly competitive team while systematically avoiding the winner’s curse.

Important: do not claim guaranteed savings, guaranteed competitive success, or actual ROI unless the analysis provides evidence.

---

# 4. Objectives

The project has three main objectives.

### Objective 1 — Performance Classification

Classify IPL players into performance tiers using scraped batting and bowling statistics.

### Objective 2 — Performance-Price Efficiency

Develop a performance-vs-price analysis that identifies players whose measured performance is relatively high or low compared with their 2025 auction price.

### Objective 3 — Auction Strategy

Translate the performance-price analysis into practical auction-budget recommendations for franchise management.

The recommendations should be presented as data-supported decision support, not as guaranteed predictions.

---

# 5. Required Assignment / Report Structure

The individual Business Analytics case study requires the report to cover:

1. **Problem Statement and Objectives**
2. **Data Collection / Dataset Description**
   - Source
   - Number of records
   - Attributes
   - Variables
3. **Data Preparation and Exploratory Data Analysis**
4. **Analytics Method**
5. **Comparison with State-of-the-Art**
   - At least 3 recent published studies
   - Required comparison fields:
     - Study
     - Year
     - Dataset
     - Method
     - Metric
     - Key Result
     - Comparison with this project
6. **Results / Business Insights / Recommendations**
7. **Conclusion**
8. **References**

Report target: **8–10 pages excluding references/appendix.**

GitHub Classroom should contain:

```text
README.md
data/
analysis.ipynb
report PDF
```

The project also needs the actual data collection/scraping implementation because ready-made Kaggle/UCI/GitHub datasets are prohibited.

---

# 6. Dataset Requirement

The assignment requires the dataset to be collected through:

- Questionnaire/survey, OR
- Web scraping.

A ready-made Kaggle/UCI/GitHub dataset should NOT be presented as the primary dataset.

This project therefore uses **real web scraping**.

The scraper uses:

- Selenium
- BeautifulSoup
- pandas

The project is NOT using Apify.

---

# 7. Data Sources

## 7.1 IPL Performance Data

Source:

**ESPNcricinfo Statsguru**

Two separate datasets are scraped:

### Batting

Current URL:

```text
https://stats.cricinfo.com/ci/engine/stats/index.html?class=6;filter=advanced;orderby=runs;size=200;template=results;tournament_type=5;trophy=117;type=batting
```

Output:

```text
data/raw/ipl_batting_raw.csv
```

### Bowling

Current URL:

```text
https://stats.cricinfo.com/ci/engine/stats/index.html?class=6;filter=advanced;orderby=matches;size=200;template=results;tournament_type=5;trophy=117;type=bowling
```

Output:

```text
data/raw/ipl_bowling_raw.csv
```

Both currently contain approximately **808 unique players**.

---

# 8. Batting Dataset

Current scraped batting dataset:

```text
ipl_batting_raw.csv
```

Approximate shape:

```text
808 rows × 16 columns
```

The extra column `Unnamed: 15` is an unwanted CSV/index-like column and should be removed during merging/cleaning.

Main batting columns:

```text
Player
Span
Mat
Inns
NO
Runs
HS
Ave
BF
SR
100
50
0
4s
6s
```

Examples of players appearing near the top include:

```text
V Kohli
RG Sharma
S Dhawan
DA Warner
KL Rahul
```

---

# 9. Bowling Dataset

Current scraped bowling dataset:

```text
ipl_bowling_raw.csv
```

Approximate shape:

```text
808 rows × 15 columns
```

The extra column `Unnamed: 14` is an unwanted CSV/index-like column.

Main bowling columns:

```text
Player
Span
Mat
Inns
Overs
Mdns
Runs
Wkts
BBI
Ave
Econ
SR
4
5
```

Important:

- `Mdns` (maidens) should be retained.
- `BBI` contains strings such as `2/25`, `4/6`, `5/16`.
- `BBI` should remain a string unless a later analysis specifically needs to split it into best wickets/best runs.
- Do not accidentally let Excel's date formatting change the actual CSV value.
- `Mat` exists in both batting and bowling, so only one match-count column is needed after merging.

---

# 10. Combined Performance Dataset

The current merge combines batting and bowling by player.

The intended final combined raw structure is:

```text
Player
Span
Mat
Bat_Inns
NO
Bat_Runs
HS
Bat_Ave
BF
Bat_SR
100
50
0
4s
6s
Bowl_Inns
Overs
Mdns
Bowl_Runs
Wkts
BBI
Bowl_Ave
Econ
Bowl_SR
4W
5W
```

The intended output is:

```text
data/raw/ipl_combined_raw.csv
```

Expected shape after removing duplicate/extra span information is approximately:

```text
808 × 26
```

The merge is an outer join because a player may have batting statistics, bowling statistics, or both.

---

# 11. Current Merge Code

Current working merge approach:

```python
import pandas as pd
from scraper.config import DATA_DIR

def merge_batting_bowling():
    batting_file = DATA_DIR / "ipl_batting_raw.csv"
    bowling_file = DATA_DIR / "ipl_bowling_raw.csv"

    batting_df = pd.read_csv(batting_file)
    bowling_df = pd.read_csv(bowling_file)

    print("Batting dataset:", batting_df.shape)
    print("Bowling dataset:", bowling_df.shape)

    batting_df = batting_df.rename(columns={
        "Inns": "Bat_Inns",
        "Runs": "Bat_Runs",
        "Ave": "Bat_Ave",
        "SR": "Bat_SR"
    })

    bowling_df = bowling_df.rename(columns={
        "Inns": "Bowl_Inns",
        "Runs": "Bowl_Runs",
        "Ave": "Bowl_Ave",
        "SR": "Bowl_SR",
        "4": "4W",
        "5": "5W"
    })

    batting_df = batting_df.drop(
        columns=["Unnamed: 15"],
        errors="ignore"
    )

    bowling_df = bowling_df.drop(
        columns=["Unnamed: 14"],
        errors="ignore"
    )

    bowling_df = bowling_df.drop(
        columns=["Mat", "Span"],
        errors="ignore"
    )

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

    output_file = DATA_DIR / "ipl_combined_raw.csv"
    combined_df.to_csv(output_file, index=False)

    print("\nSaved to:")
    print(output_file)


if __name__ == "__main__":
    merge_batting_bowling()
```

---

# 12. Auction Price Dataset

## Source

Current source:

```text
https://en.wikipedia.org/wiki/List_of_2025_Indian_Premier_League_personnel_changes
```

The page contains multiple IPL auction tables.

A Selenium + BeautifulSoup scraper successfully extracted approximately:

```text
180 auction records
```

The current raw file is:

```text
data/raw/ipl_2025_auction_raw.csv
```

Current raw columns were:

```text
No.
Name
Country
Role
No. of IPL matches
Category
Base price ( ₹ lakhs )
2025 IPL team
Auctioned price ( ₹ lakhs )
2024 IPL team
Auction_Set
```

However, **Auction_Set is NOT required for the business analysis**.

The project explicitly decided not to spend time tracking auction sets such as Marquee Set 1, Set 2, etc.

---

# 13. Intended Clean Auction Dataset

The auction data should eventually be reduced to useful fields:

```text
Player
Country
Role
Base_Price_Lakh
Auction_Price_Lakh
Auction_Team
```

The most important fields for this project are:

```text
Player
Auction_Price_Lakh
```

Country, role, base price, and team are useful for segmentation and interpretation.

Auction prices on the scraped Wikipedia tables are already represented in **₹ lakhs**, so no crore/lakh conversion is required.

Example values encountered:

```text
Jos Buttler       1575
Shreyas Iyer      2675
Rishabh Pant      2700
Kagiso Rabada     1075
Arshdeep Singh    1800
```

These examples are only examples of the scraped format; they are not intended as analytical conclusions.

---

# 14. Important Auction Data Issue

The current auction dataset has fewer records than the 808-player Statsguru dataset.

This is expected to some degree because:

- Statsguru contains a much broader population of IPL players.
- Not every IPL player participated in the 2025 auction.
- Some players may have been unsold.
- Some players may have been retained rather than bought at auction.
- Some records may be missing from the currently scraped auction tables.
- Wikipedia player names are often full names, while Statsguru commonly uses abbreviated names.

Therefore, **do not simply merge the two datasets using exact player names and assume the result is correct.**

---

# 15. Immediate Next Task — Player Matching

This is the current point where the project stopped.

We need to compare:

```text
808 Statsguru players
        ↓
name matching
        ↓
~180 auction records
```

The major problem is name representation.

Examples:

```text
Statsguru:
V Kohli
RG Sharma
JJ Bumrah

Wikipedia:
Virat Kohli
Rohit Sharma
Jasprit Bumrah
```

There can also be symbols such as:

```text
Arshdeep Singh †
```

Therefore, exact matching will not be sufficient.

## Recommended matching procedure

### Step 1

Normalize names:

- lowercase
- remove symbols such as `†`
- remove unnecessary punctuation
- normalize whitespace

### Step 2

Perform exact normalized matching.

### Step 3

For unmatched names, generate candidate matches using:

- surname
- first-name initial
- remaining initials
- possibly country/role where useful

### Step 4

Review ambiguous matches rather than blindly accepting fuzzy matching.

The goal is to avoid false matches between players with similar names.

---

# 16. Missing Auction Prices — Important Rule

Do NOT automatically fill missing 2025 auction prices using older auction prices.

For example:

```text
2024 auction price ≠ 2025 auction price
```

If a player has no 2025 auction price, determine why.

Possible categories:

### A. Sold in 2025

If the player was sold and a price exists, recover the correct 2025 price from a reliable 2025 source or a historical version of the page if necessary.

### B. Unsold

If the player was part of the auction but remained unsold, there is no auction purchase price.

Keep this as missing/NaN for the price-efficiency analysis rather than inventing a number.

### C. Retained / Not Auctioned

The player should not be treated as having a 2025 auction purchase price.

### D. Missing from Current Web Page

If evidence suggests a player was sold but the current page lacks the record, inspect page history/previous versions or another reliable source to recover the 2025 price.

**Previous versions are a verification/recovery mechanism, not a source for substituting older-year prices.**

---

# 17. Critical Temporal Issue to Resolve

There is an important methodological issue that must be considered before final modeling.

The current Statsguru URLs return career statistics that can include matches after the 2025 auction, potentially including 2026 data.

But the auction prices are from the **2025 IPL auction**.

Therefore, using current career statistics to explain a player's 2025 auction price could introduce temporal leakage.

For example:

```text
2025 auction price
        ↑
should ideally use performance information
available BEFORE the 2025 auction
```

rather than:

```text
2025 auction price
        ↑
career statistics through 2026
```

Before finalizing the analysis, investigate whether Statsguru can be configured with an appropriate date cutoff, ideally ending before the 2025 auction.

If feasible, use pre-auction performance data.

If not feasible within the project constraints, explicitly describe the analysis as retrospective performance-price analysis and state the temporal limitation in the methodology/limitations section.

Do NOT silently claim that the model predicts the 2025 auction decision if post-auction statistics are included.

---

# 18. Planned Data Processing

After the player matching issue is resolved:

1. Clean batting data.
2. Clean bowling data.
3. Clean auction data.
4. Match player names.
5. Merge performance + auction data.
6. Identify missing values.
7. Convert relevant fields to numeric.
8. Handle zero/undefined statistics appropriately.
9. Remove irrelevant columns.
10. Save a final analysis-ready dataset.

Target file:

```text
data/final/ipl_player_dataset.csv
```

---

# 19. Planned Exploratory Data Analysis

EDA should be straightforward and business-oriented.

Potential analyses:

### Auction Price Distribution

Study how auction prices are distributed.

### Performance vs Auction Price

Plot performance score against auction price.

### Batting Performance vs Price

Study relationships involving:

```text
Runs
Average
Strike Rate
100s
50s
4s
6s
```

### Bowling Performance vs Price

Study relationships involving:

```text
Wickets
Economy
Bowling Average
Bowling Strike Rate
4-wicket hauls
5-wicket hauls
Maidens
```

### Role vs Price

Compare auction prices by player role.

### Correlation

Examine relationships between relevant performance metrics and auction price.

Do not create unnecessary charts simply to increase the number of plots. Each visualization should answer a business question.

---

# 20. Performance Score

The project intends to construct a transparent overall performance score.

Conceptually:

```text
Batting Performance
        +
Bowling Performance
        ↓
Overall Performance Score
```

The exact formula has NOT yet been finalized.

Do not arbitrarily choose weights without examining the data and explaining the rationale.

Potentially relevant variables include:

### Batting

```text
Bat_Runs
Bat_Ave
Bat_SR
100
50
4s
6s
```

### Bowling

```text
Wkts
Bowl_Ave
Econ
Bowl_SR
4W
5W
Mdns
```

The score should be normalized appropriately because these variables have very different scales.

---

# 21. Performance Classification

The planned modeling stage includes performance-tier classification.

Possible models:

```text
Logistic Regression
Random Forest
```

The project originally considered other models such as XGBoost/SVM, but the current plan is to keep the modeling manageable and interpretable.

Potential target:

```text
Low Performance
Medium Performance
High Performance
```

However, the exact target-generation method has NOT yet been finalized.

The new agent should first establish a defensible way to define the performance classes rather than arbitrarily assigning labels.

Evaluation may include:

```text
Accuracy
Precision
Recall
F1-score
Confusion Matrix
```

Use metrics appropriate to the final target and class distribution.

---

# 22. Performance-Price Efficiency Analysis

This is the central contribution of the project.

The conceptual relationship is:

```text
                 HIGH PERFORMANCE
                       ↑
                       │
     High-value        │       High-cost
     / efficient       │       elite
                       │
LOW PRICE ─────────────┼────────────── HIGH PRICE
                       │
     Low performance   │       Potentially
     / low cost        │       overpriced
                       │
                       ↓
                 LOW PERFORMANCE
```

The exact labels should only be applied after examining the actual cluster characteristics.

The analysis should distinguish:

- performance
- cost
- relative efficiency

The key idea is:

> A player should not be evaluated only by how good they are, but also by how their measured performance compares with their auction cost.

---

# 23. K-Means Clustering

The current plan is to use K-Means for the performance-price analysis.

Potential inputs:

```text
Performance Score
Auction Price / normalized price
```

The number of clusters should be justified based on the analysis rather than automatically assumed.

After clustering, inspect:

- cluster centroids
- average performance
- average auction price
- number of players
- player roles
- representative players

Only then assign business-friendly descriptions to the clusters.

Do not claim that K-Means itself proves a player is “overpriced” in an absolute economic sense. It identifies groups based on the variables provided.

---

# 24. Business Insights

The analysis should ultimately answer questions such as:

### Question 1

Which players combine relatively high performance with relatively low auction cost?

### Question 2

Which players command high prices relative to their measured performance?

### Question 3

How does value differ across player roles?

### Question 4

Does auction price appear strongly associated with measured performance?

### Question 5

How could a franchise use these patterns to shortlist players before an auction?

---

# 25. Recommendations

Recommendations should be based directly on the observed analysis.

Possible recommendation categories:

### Player Shortlisting

Use performance-price analysis to identify budget-efficient candidates.

### Budget Allocation

Compare high-cost players against their measured performance rather than relying solely on reputation.

### Role Balance

Examine whether budget-efficient options exist across different roles.

### Pre-Auction Planning

Prepare a shortlist before the auction based on objective performance metrics.

Again, recommendations should be framed as **decision support**, not guaranteed outcomes.

---

# 26. State-of-the-Art Comparison

The report requires at least three recent published studies.

Studies identified during the planning stage include work related to:

1. IPL auction price prediction using machine learning.
2. Economic value creation in IPL.
3. Base-price determination for IPL mega auctions using modified hedonic approaches and XGBoost.

These studies must be properly verified before being included in the final report.

The final table should contain:

| Study | Year | Dataset | Method | Metric | Key Result | Comparison |
|---|---:|---|---|---|---|---|

The comparison should focus on methodological differences such as:

- auction price prediction
- player valuation
- performance classification
- performance-price efficiency
- clustering
- business decision support

Do not claim superiority simply because this project obtains a higher metric on a different dataset.

---

# 27. Project Folder Structure

Current intended structure:

```text
individual-case-study/
│
├── data/
│   ├── raw/
│   │   ├── ipl_batting_raw.csv
│   │   ├── ipl_bowling_raw.csv
│   │   ├── ipl_combined_raw.csv
│   │   └── ipl_2025_auction_raw.csv
│   │
│   ├── processed/
│   │
│   └── final/
│
├── notebooks/
│   └── analysis.ipynb
│
├── scraper/
│   ├── __init__.py
│   ├── config.py
│   ├── scraper.py
│   ├── parser.py
│   ├── auction_parser.py
│   ├── auction_scraper.py
│   ├── merge_data.py
│   ├── utils.py
│   └── requirements.txt
│
├── README.md
│
└── main.py
```

Avoid adding unnecessary architecture or files. The user prefers a simple, understandable implementation.

---

# 28. Current config.py

Current relevant configuration:

```python
from pathlib import Path

BATTING_URL = (
    "https://stats.cricinfo.com/ci/engine/stats/index.html?"
    "class=6;filter=advanced;orderby=runs;"
    "size=200;template=results;"
    "tournament_type=5;trophy=117;type=batting"
)

BOWLING_URL = (
    "https://stats.cricinfo.com/ci/engine/stats/index.html?"
    "class=6;filter=advanced;orderby=matches;"
    "size=200;template=results;"
    "tournament_type=5;trophy=117;type=bowling"
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"

BATTING_OUTPUT_FILE = DATA_DIR / "ipl_batting_raw.csv"
BOWLING_OUTPUT_FILE = DATA_DIR / "ipl_bowling_raw.csv"

WAIT_TIME = 3

AUCTION_URL = (
    "https://en.wikipedia.org/wiki/"
    "List_of_2025_Indian_Premier_League_personnel_changes"
)

AUCTION_OUTPUT_FILE = DATA_DIR / "ipl_2025_auction_raw.csv"
```

If the actual local file differs slightly, inspect it before modifying it.

---

# 29. Current Statsguru Parser

Current working parser:

```python
from bs4 import BeautifulSoup
import pandas as pd


def extract_table(html, table_type):
    soup = BeautifulSoup(html, "lxml")

    tables = soup.find_all("table", class_="engineTable")

    selected_table = None

    for table in tables:
        headers = [
            th.get_text(strip=True)
            for th in table.find_all("th")
        ]

        if table_type == "batting":
            if "Player" in headers and "Runs" in headers and "BF" in headers:
                selected_table = table
                break

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

    return pd.DataFrame(rows, columns=headers)
```

---

# 30. Current Statsguru Scraper

Current working approach:

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

from scraper.config import (
    BATTING_URL,
    BOWLING_URL,
    BATTING_OUTPUT_FILE,
    BOWLING_OUTPUT_FILE,
    WAIT_TIME
)

from scraper.parser import extract_table


def scrape_stats(url, output_file, table_type):
    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        )
    )

    driver.maximize_window()
    driver.get(url)

    all_tables = []

    while True:

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "table.engineTable")
            )
        )

        html = driver.page_source

        df = extract_table(
            html,
            table_type
        )

        all_tables.append(df)

        print(
            f"{table_type.capitalize()}: "
            f"Collected {len(df)} rows"
        )

        try:

            next_button = driver.find_element(
                By.XPATH,
                "//a[contains(@class, 'PaginationLink') "
                "and normalize-space()='Next']"
            )

            next_url = next_button.get_attribute(
                "href"
            )

            print("Moving to next page...")

            driver.get(next_url)

            time.sleep(WAIT_TIME)

        except Exception:

            print("No more pages.")

            break

    driver.quit()

    final_df = pd.concat(
        all_tables,
        ignore_index=True
    )

    final_df = final_df.drop_duplicates(
        subset=["Player"],
        keep="first"
    )

    final_df.to_csv(
        output_file,
        index=False
    )

    print("\nFinal Dataset:")
    print(final_df.head())

    print("\nDataset Shape:")
    print(final_df.shape)

    print("\nColumns:")
    print(final_df.columns.tolist())


def scrape_batting():
    scrape_stats(
        BATTING_URL,
        BATTING_OUTPUT_FILE,
        "batting"
    )


def scrape_bowling():
    scrape_stats(
        BOWLING_URL,
        BOWLING_OUTPUT_FILE,
        "bowling"
    )
```

---

# 31. Auction Parser — Current Direction

The current auction parser successfully detects tables by looking for headers containing:

- Name
- Base price
- Auctioned price

The earlier parser also tracked auction-table numbers, but that was intentionally rejected as unnecessary.

The parser should now simply:

1. Find relevant auction tables.
2. Extract rows.
3. Concatenate them.
4. Standardize column names.
5. Remove unnecessary auction-set information.
6. Save the raw/clean auction dataset.

Do not spend time implementing auction-set identification unless a later analysis specifically requires it.

---

# 32. Auction Scraper — Current Direction

The scraper uses Selenium to load the Wikipedia page and then passes `page_source` to BeautifulSoup.

Earlier code:

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

from scraper.config import (
    AUCTION_URL,
    AUCTION_OUTPUT_FILE
)

from scraper.auction_parser import extract_auction_tables


def scrape_auction():

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        )
    )

    driver.maximize_window()

    print("Opening auction page...")

    driver.get(AUCTION_URL)

    WebDriverWait(driver, 15).until(
        lambda d:
        d.execute_script(
            "return document.readyState"
        ) == "complete"
    )

    print("Page loaded successfully.")

    html = driver.page_source

    driver.quit()

    df = extract_auction_tables(html)

    print("\nAuction Dataset:")
    print(df.head())

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    df.to_csv(
        AUCTION_OUTPUT_FILE,
        index=False
    )

    print("\nSaved to:")
    print(AUCTION_OUTPUT_FILE)


if __name__ == "__main__":
    scrape_auction()
```

The old `Auction_Set` printing/output must be removed.

---

# 33. main.py

During testing, `main.py` was temporarily configured to run only bowling:

```python
from scraper.utils import create_directories
from scraper.scraper import scrape_bowling


def main():
    create_directories()
    scrape_bowling()


if __name__ == "__main__":
    main()
```

Eventually, it can be changed to run the complete scraping/merging pipeline once the individual components are stable.

Do not unnecessarily rerun large scrapes if the existing raw files are already correct.

---

# 34. Utilities

Current `utils.py` contains:

```python
from pathlib import Path


def create_directories():

    project_root = Path(__file__).resolve().parent.parent

    folders = [
        project_root / "data" / "raw",
        project_root / "data" / "processed",
        project_root / "data" / "final",
        project_root / "logs"
    ]

    for folder in folders:
        folder.mkdir(
            parents=True,
            exist_ok=True
        )
```

The `logs` directory is not currently central to the project. Do not add a complex logging framework unless actually needed.

---

# 35. Important Decisions Already Made

These decisions should be preserved unless new evidence requires changing them.

### Decision 1

Use real Selenium + BeautifulSoup scraping.

### Decision 2

Use ESPNcricinfo Statsguru for IPL batting and bowling performance.

### Decision 3

Use the 2025 IPL auction information from the Wikipedia personnel-changes page as the initial auction-price source.

### Decision 4

Do NOT track auction-set identifiers.

### Decision 5

Do NOT substitute older auction prices for missing 2025 prices.

### Decision 6

Batting + bowling are sufficient for the current project. A separate fielding dataset is not currently required.

### Decision 7

Maidens (`Mdns`) should remain in the raw/combined data.

### Decision 8

Keep the implementation simple. Do not create unnecessary modules or abstractions.

### Decision 9

The final project should connect the analytics to a business decision: budget-efficient player acquisition.

---

# 36. Things NOT to Do

Do not:

- Download a Kaggle IPL dataset and use it instead of the scraper.
- Use Apify for scraping.
- Add auction-set information just because the source contains it.
- Fill missing 2025 auction prices with 2024/2023 prices.
- Blindly fuzzy-match all player names without reviewing ambiguous matches.
- Use every scraped feature automatically.
- Claim that a cluster objectively proves a player is overpriced in an absolute financial sense.
- Claim guaranteed savings or guaranteed team success.
- Claim the model predicts the 2025 auction if the performance data includes post-auction matches.
- Add unnecessary software architecture.
- Start writing the final report before the dataset and analysis are stable.

---

# 37. Exact Current Status

## Completed

### Project planning

- Domain selected.
- Project title selected.
- Problem statement developed.
- Three objectives defined.
- Business value/auction-efficiency direction established.

### Scraping

- Batting Statsguru scraper works.
- Bowling Statsguru scraper works.
- Batting raw dataset collected.
- Bowling raw dataset collected.
- Wikipedia auction scraper works.
- Auction data collected from multiple auction tables.

### Raw data

```text
ipl_batting_raw.csv       ✅
ipl_bowling_raw.csv       ✅
ipl_combined_raw.csv      ✅ initial merge
ipl_2025_auction_raw.csv  ✅ initial scrape
```

### Merge

- Batting/bowling merge has been implemented.
- Duplicate/extra columns have been identified.
- Final intended 26-column combined structure has been defined.

---

# 38. Current Incomplete Work

## Highest priority

### 1. Clean auction parser

Remove `Auction_Set` and standardize auction columns.

### 2. Player matching

Determine how many of the auction records match Statsguru players.

### 3. Missing auction-price investigation

For unmatched/missing players, determine:

- sold
- unsold
- retained/not auctioned
- missing record

Use previous Wikipedia versions only where necessary to recover/verify 2025 auction information.

### 4. Temporal validity

Determine whether Statsguru can be restricted to pre-2025-auction performance.

### 5. Final merged dataset

Create:

```text
data/final/ipl_player_dataset.csv
```

---

# 39. After the Data Pipeline

The remaining analytical work is:

```text
Final Dataset
      ↓
Data Cleaning
      ↓
EDA
      ↓
Performance Score
      ↓
Performance Classification
      ↓
Model Evaluation
      ↓
Performance vs Price
      ↓
K-Means
      ↓
Business Insights
      ↓
Recommendations
      ↓
State-of-the-Art Comparison
      ↓
Report
      ↓
README + GitHub Classroom
```

---

# 40. Recommended Immediate Action for the New Agent

Start with this exact task:

> Inspect the current auction CSV and Statsguru combined CSV, normalize the player names, and produce a matching report showing:
>
> 1. Number of auction players.
> 2. Number matched to Statsguru.
> 3. Number unmatched.
> 4. List of unmatched auction players.
> 5. List of Statsguru players without auction records.
> 6. Potential ambiguous name matches.
>
> Do NOT modify the data permanently until the matching results have been inspected.

After that, investigate missing 2025 prices only where necessary.

---

# 41. Final Goal

The finished project should demonstrate:

```text
Real web data
     ↓
Data preparation
     ↓
Exploratory analysis
     ↓
Player performance modeling
     ↓
Performance-price analysis
     ↓
Player value segmentation
     ↓
Auction strategy insights
```

The final business question is:

> **How can an IPL franchise use player performance and auction-price data to identify performance-efficient acquisition opportunities and make more systematic budget-allocation decisions during player auctions?**

The project should remain understandable, reproducible, and defensible for an undergraduate Business Analytics case study.

