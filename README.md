# IPL Player Valuation

A Business Analytics case study that analyses IPL player performance
alongside the 2025 auction price paid for each player and produces a
data-driven view of value efficiency at franchise level.

## Problem statement

Franchise T20 cricket teams operate under strict salary caps but
frequently overpay for marquee players based on reputation and
intuition. Existing valuation approaches typically stop at
classifying players into performance tiers without relating measured
performance to the amount actually paid. This project builds a
performance-vs-price framework that identifies players who delivered
more (or less) performance than the paid price would suggest, and
translates the finding into a shortlist an auction desk can act on.

## Objectives

1. Classify IPL players into performance tiers using scraped batting
   and bowling statistics.
2. Compare each player's measured performance against the 2025 auction
   price and identify value-efficiency clusters.
3. Produce ranked shortlists and role- and franchise-level breakdowns
   that inform future auction strategy.

## Data sources

* **Player performance:** batting and bowling statistics scraped from
  ESPNcricinfo Statsguru using Selenium and BeautifulSoup.
* **Auction prices:** the 2025 IPL personnel and auction tables on
  Wikipedia.

The scraper pipeline collects and integrates the data — no ready-made
Kaggle, UCI or GitHub dataset is used as the primary source.

## Dataset

The integrated dataset contains **164 auction acquisitions** with
batting statistics, bowling statistics, auction price, base price,
role, country and buying franchise. Retained players are excluded
because their retention value is not comparable to an auction purchase
price.

## Analytics methods

* Descriptive statistics and visual EDA on batting, bowling and
  auction-price distributions.
* Feature engineering to construct a transparent, role-weighted
  performance score from standardised batting and bowling metrics.
* Supervised classification (Logistic Regression and Random Forest)
  to predict Low / Medium / High performance tiers with 5-fold
  stratified cross-validation and an 80/20 holdout.
* Unsupervised clustering (K-Means on the standardised performance
  score and log auction price) to group players into four
  value-efficiency clusters.

## Key results

* **Random Forest** achieves 5-fold CV accuracy of **0.836 ± 0.048**
  (macro F1 0.832) on tier classification; Logistic Regression
  achieves 0.805 ± 0.059.
* K-Means clustering (`k = 4`, chosen from elbow and silhouette
  diagnostics) yields the following value clusters:

| Cluster                       | Size | Mean score | Median price |
|---|---:|---:|---:|
| Undervalued / High-value      | 22   | +1.45      | ₹6.9 Cr      |
| High-performing but Expensive | 40   | +0.41      | ₹7.5 Cr      |
| Fair-value Mid-market         | 52   | +0.06      | ₹1.7 Cr      |
| Low-cost / Low-impact         | 50   | −0.37      | ₹0.3 Cr      |

* **Role-level finding.** 41% of wicket-keepers and 32% of batters
  land in the *Undervalued / High-value* cluster, versus 8% of bowlers
  and 2% of all-rounders.
* **Franchise-level finding.** Punjab Kings captured the highest
  absolute number of Undervalued acquisitions (4); Kolkata Knight
  Riders led on share (23%). Mumbai Indians captured zero.

Full tables and figures are in `notebooks/analysis.ipynb` and
`notebooks/figures/`.

## Repository structure

```text
ipl-player-valuation/
├── data/
│   ├── raw/         # Scraped batting, bowling and auction CSVs
│   ├── processed/   # Cleaned, scored, clustered and shortlisted CSVs
│   └── final/       # Integrated dataset used as the notebook input
├── notebooks/
│   ├── analysis.ipynb
│   └── figures/     # PNGs exported from the notebook
├── report/          # Case study report PDF
├── scraper/
│   ├── __init__.py
│   ├── auction_parser.py
│   ├── auction_scraper.py
│   ├── build_final_dataset.py
│   ├── config.py
│   ├── merge_data.py
│   ├── parser.py
│   ├── player_matching.py
│   ├── requirements.txt
│   ├── scraper.py
│   └── utils.py
├── main.py
└── README.md
```

## How to reproduce

```powershell
# 1. Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r scraper/requirements.txt
pip install scikit-learn matplotlib seaborn jupyter ipykernel

# 3. Rebuild the raw and integrated datasets (optional)
python main.py

# 4. Open the analysis notebook
jupyter lab notebooks/analysis.ipynb
```

## References

See `report/Case_Study_Report.pdf` for the state-of-the-art comparison
and full reference list.
