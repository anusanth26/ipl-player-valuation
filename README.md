# IPL Player Valuation

A Business Analytics project that analyzes IPL player performance and 2025 auction prices to study player value and performance-price relationships.

## Project Overview

Player auctions in franchise cricket involve decisions about performance, reputation, and budget allocation. This project uses publicly available IPL data to analyze player performance in relation to their 2025 auction price.

The project combines batting and bowling statistics with auction information to develop a data-driven view of player performance and price efficiency.

The analysis focuses on:

- Classifying players based on their observed performance
- Comparing player performance with their auction price
- Identifying performance-price patterns
- Generating insights that can support auction planning and player shortlisting

## Objectives

1. Classify IPL players into performance tiers using batting and bowling statistics.
2. Analyze the relationship between player performance and their 2025 auction price.
3. Identify players and performance-price patterns that can provide useful insights for auction decision-making.

## Data Sources

### Player Performance Data

Player batting and bowling statistics are collected from **ESPNcricinfo Statsguru** using web scraping with Selenium and BeautifulSoup.

### Auction Data

2025 IPL auction information is collected from the **2025 IPL personnel and auction tables on Wikipedia**.

The project collects and integrates the data instead of using a ready-made Kaggle, UCI, or GitHub dataset as the primary dataset.

## Dataset

The integrated dataset contains player-level batting, bowling, and auction information.

### Batting Attributes

- Matches
- Innings
- Runs
- Highest Score
- Batting Average
- Balls Faced
- Strike Rate
- Centuries
- Half-centuries
- Fours
- Sixes

### Bowling Attributes

- Innings
- Overs
- Maidens
- Runs Conceded
- Wickets
- Best Bowling
- Bowling Average
- Economy Rate
- Bowling Strike Rate
- 4-Wicket Hauls
- 5-Wicket Hauls

### Auction Attributes

- Player
- Country
- Role
- Base Price
- 2025 Auction Price
- Auction Team

The current integrated dataset contains **164 matched players**.

## Methodology

The project follows the following workflow:

1. **Data Collection**
   - Scrape IPL batting and bowling statistics
   - Collect 2025 auction information

2. **Data Preprocessing**
   - Clean column names and values
   - Handle missing values
   - Remove unnecessary columns
   - Integrate batting, bowling, and auction data

3. **Exploratory Data Analysis**
   - Analyze player performance distributions
   - Examine relationships between performance variables
   - Analyze auction price distributions
   - Study the relationship between performance and price

4. **Performance Analysis**
   - Construct performance measures using relevant batting and bowling statistics
   - Classify players into performance tiers

5. **Performance-Price Analysis**
   - Compare player performance with 2025 auction price
   - Identify different performance-price patterns
   - Apply clustering to analyze player groups

6. **Business Insights**
   - Identify high-value performance-price combinations
   - Analyze expensive players in relation to their observed performance
   - Derive insights relevant to auction planning

## Project Structure

```text
ipl-player-valuation/
│
├── data/
│   ├── raw/
│   ├── processed/
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
│   ├── player_matching.py
│   ├── build_final_dataset.py
│   ├── utils.py
│   └── requirements.txt
│
├── main.py
└── README.md
```

## Scope Decisions (Frozen)

To keep the case study consistent with the approved problem statement,
the following decisions are treated as fixed unless the teacher explicitly
requires a change:

1. **Analytical unit is a player.** The final dataset contains
   **164 players × 31 columns**, representing every player for whom
   both scraped performance statistics and a 2025 auction purchase
   price could be matched.
2. **Retained players are separated from auction purchases.** Only
   players who were bought at the 2025 auction hold a value in
   `Auction_Price_Lakh`. Retention values are not used as a substitute
   for auction price.
3. **The "≥10,000 records" teacher remark** is addressed by reporting
   the underlying raw scraped volume (approximately 808 batting rows
   + 808 bowling rows + 180 auction rows ≈ 1,796 raw records) while
   keeping the analytical dataset at 164 integrated player-level rows.
   The dataset is not artificially inflated by duplicating players.
4. **This is a retrospective performance-vs-price analysis**, not a
   future-performance prediction model. Findings are used to inform
   future auction strategy, not to forecast future player output.
5. **Auction-set tracking is out of scope.** Only auction price,
   base price, buying team, role, and country are used from the
   auction source.

## Analytics Methods

The project applies the following methods from the Business Analytics
syllabus:

- **Descriptive statistics and visual EDA** on batting, bowling and
  auction-price distributions.
- **Feature engineering** to construct a transparent, role-aware
  performance score from standardised batting and bowling metrics.
- **Supervised classification** (Logistic Regression and Random Forest)
  to classify players into Low / Medium / High performance tiers, with
  stratified cross-validation because of the small sample size.
- **Unsupervised clustering** (K-Means on standardised performance
  score and log auction price) to group players into value-efficiency
  clusters such as *Undervalued*, *High-performing but Expensive*,
  *Potentially Overpriced* and *Low-cost / Low-impact*.

## Results

*To be filled after the notebook analysis is complete.*

Planned outputs:

- Player performance tier classifications and model evaluation table.
- Value-efficiency cluster table with per-cluster narrative.
- Shortlist tables (top undervalued acquisitions, potentially
  overpriced picks) with role and franchise breakdowns.

## Business Recommendations

*To be filled after clustering results are interpreted.*

## References

*To be filled during report writing, together with at least three
recent published studies for the state-of-the-art comparison.*

## How to Reproduce

```powershell
# Install dependencies
pip install -r scraper/requirements.txt

# Run the full scrape + match + build pipeline
python main.py

# Open the analysis notebook
jupyter lab notebooks/analysis.ipynb
```
