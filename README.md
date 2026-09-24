# Data-Driven Player Valuation and Auction Strategy for T20 Franchises in IPL

## Problem Statement

Franchise T20 cricket teams operate under strict salary caps but
frequently overpay for marquee players based on emotional bias, media
hype, and traditional reputations during auctions. This reliance on
intuition rather than granular data leads to the "winner's curse",
resulting in imbalanced squads and inefficient budget allocation.
Existing valuation approaches typically stop at classifying players
into broad performance tiers, without explicitly relating performance
to cost — leaving the question of value (not just quality) largely
unanswered.

The objective of this project is to develop a predictive
classification model using scraped performance metrics to objectively
identify high-impact players, and extend this with a
performance-price efficiency framework that maps each player's
on-field output against their auction cost. By clustering players
along this performance-vs-price frontier, the model distinguishes
"undervalued gems" (high performance, low cost), "fairly priced
elite" players, and "overpriced" picks driven by reputation rather
than output. This provides management with a data-driven strategy to
not only shortlist high-impact players, but to explicitly target
budget-efficient acquisitions — optimising their auction purse and
assembling a balanced, highly competitive team while systematically
avoiding the winner's curse.

## Objectives

1. Develop a predictive classification model using scraped
   performance statistics to classify IPL players into Low, Medium
   and High performance tiers.
2. Build a performance-vs-price efficiency framework that maps each
   player's measured performance against the 2025 IPL auction price
   and identifies value-efficiency clusters.
3. Translate the clusters and a per-player value ranking into
   shortlists and role- and franchise-level breakdowns that inform
   auction strategy.

## Data Collection

Data was collected through web scraping.

* **Player performance data.** Batting and bowling career statistics
  for IPL players scraped from ESPNcricinfo Statsguru using Selenium
  and BeautifulSoup. The scraper paginates through the results table
  and stores each row in `data/raw/ipl_batting_raw.csv` and
  `data/raw/ipl_bowling_raw.csv`.
* **2025 IPL auction data.** Player name, country, role, base price,
  auctioned price and buying franchise scraped from the
  "List of 2025 Indian Premier League personnel changes" page on
  Wikipedia; stored in `data/raw/ipl_2025_auction_raw.csv`.
* **Integration.** A dedicated name-matching module aligns the
  abbreviated Statsguru names (for example `I Kishan`) with the full
  Wikipedia names (`Ishan Kishan`) using normalisation,
  initial-surname patterns and manual overrides for ambiguous cases.
  Retained players are excluded because their retention value is not
  comparable to an auction purchase price.

Raw scraped volume: 808 batting rows + 808 bowling rows + 180 auction
rows. The integrated analytical dataset contains **164 auction
acquisitions × 43 attributes** after cleaning and feature
engineering.

## Analytics Methods

* **Data preparation.** Placeholder `-` values separated into
  structural zeros (count columns) and undefined values (rate
  columns). Highest score parsed into a numeric column and a not-out
  flag. Price columns cast to numeric; auction price log-transformed
  to control right-skew.
* **Feature engineering.** Per-match and per-innings rates
  (`Runs_per_Inns`, `Wkts_per_Mat`, `Boundary_Rate`,
  `Bowling_Contribution`), participation flags (`Has_Batting`,
  `Has_Bowling`), country flag (`Is_Overseas`) and small-sample flag
  (`Low_Sample`).
* **Performance score.** Role-weighted average of z-scored batting
  and bowling features. Overall score split into Low, Medium and
  High tiers using tertile cuts.
* **Classification.** Logistic Regression (interpretable baseline)
  and Random Forest (non-linear comparison) on the raw performance
  features. Evaluated with 5-fold stratified cross-validation and a
  stratified 80/20 holdout.
* **Clustering.** K-Means on the standardised performance score and
  standardised `log(Auction_Price_Lakh)`. Number of clusters
  (`k = 4`) chosen from elbow and silhouette diagnostics and aligned
  with the four value quadrants described in the problem statement.
* **Value ranking.** A per-player
  `Value_Gap = z(Overall_Score) − z(log Auction_Price)` surfaces the
  largest positive and negative deviations for shortlisting.

## Key Results

Classification performance (5-fold stratified cross-validation):

| Model               | Accuracy       | Macro F1       |
|---|---:|---:|
| Logistic Regression | 0.805 ± 0.059  | 0.803 ± 0.058  |
| Random Forest       | 0.836 ± 0.048  | 0.832 ± 0.054  |

K-Means value clusters (`k = 4`):

| Cluster                       | Size | Mean score | Median price |
|---|---:|---:|---:|
| Undervalued / High-value      | 22   | +1.45      | ₹6.9 Cr      |
| High-performing but Expensive | 40   | +0.41      | ₹7.5 Cr      |
| Fair-value Mid-market         | 52   | +0.06      | ₹1.7 Cr      |
| Low-cost / Low-impact         | 50   | −0.37      | ₹0.3 Cr      |

* **Role-level finding.** 41% of wicket-keepers and 32% of batters
  fall in the *Undervalued / High-value* cluster, compared with 8% of
  bowlers and 2% of all-rounders.
* **Franchise-level finding.** Punjab Kings captured the highest
  absolute number of Undervalued acquisitions (4 of 20 buys), Kolkata
  Knight Riders led on share (3 of 13 = 23%), and Mumbai Indians
  captured none.

Ranked artefacts produced for the auction desk:

* `data/processed/top_value_shortlist.csv` — 15 players with the
  largest positive Value Gap.
* `data/processed/overpriced_watchlist.csv` — 10 players with the
  largest negative Value Gap.

Full tables and figures are in `notebooks/analysis.ipynb` and
`notebooks/figures/`.

## State-of-the-Art Comparison

Five recent published studies on IPL player valuation and performance
analytics are compared with this case study below.

| Published Study / Year | Dataset | Method Used | Evaluation Metric | Key Result | Comparison with Your Work |
|---|---|---|---|---|---|
| Karnik (2010), *Journal of Sports Economics* | 2008 IPL auction — 78 auctioned players and their pre-auction international / domestic record | Hedonic price regression with player attributes (batting average, bowling average, age, nationality, all-rounder status) as regressors | Adjusted R² and OLS coefficient significance | Batting performance, nationality and all-rounder status significantly explain auction prices; the model formalises the intuition that observable performance drives bidding | Foundational hedonic baseline. This case study replaces the linear regression on price with a role-weighted performance score and a K-Means partition of the score-vs-price plane, so the emergent groups are unsupervised rather than derived from regression residuals. |
| Rani et al. (2020), *IEEE ICCE* | IPL player statistics; players clustered by past performance and matched to a target playing XI | Two-stage pipeline — unsupervised clustering followed by ensemble classifiers (Bagging, Boosting, Random Forest) to predict inclusion in the playing XI | Classification accuracy on the held-out set | Ensembles outperformed individual classifiers on player-selection accuracy; the clustering step reduced label sparsity for the classifier | Both studies use a cluster-then-classify design and Random Forest. Their target is playing-XI selection, whereas this case study predicts Low / Medium / High performance tier and then applies a separate value-efficiency cluster on the score-price plane, so the outputs support auction shortlisting rather than match-day team selection. |
| Malhotra (2022), *Journal of Sports Analytics* | IPL auction prices and player performance across multiple seasons | Hedonic pricing model with linear regression; economic value estimated as the gap between predicted and actual auction price | Coefficient of determination (R²) and predicted-vs-actual price comparison | Hedonic model explains a substantial share of auction-price variance; players with large positive residuals are identified as economic value creators | Same value-vs-price framing, but based on a parametric regression fit to price. This case study substitutes a role-weighted performance score and K-Means clustering on the score-price plane, so the value groups emerge from unsupervised structure rather than from residuals of a fitted price equation. |
| Mansurali et al. (2022), *Springer* | IPL batting and bowling statistics for retained and auctioned players | K-Means and hierarchical clustering on standardised performance features to profile players by playing style | Silhouette score and cluster-size validation | Cricketers grouped into distinct performance archetypes (aggressive batter, anchor, pace bowler, spinner, etc.) with strong within-cluster homogeneity | Same K-Means backbone and silhouette-based cluster validation. Their clustering input is a performance-only feature space that yields playing-style archetypes; this case study clusters on a two-dimensional score-vs-price plane, so the emergent groups carry economic meaning (undervalued, expensive, mid-market, low-cost) rather than tactical style. |
| Chittibabu & Sundararaman (2023), *Journal of Sports Analytics* | Player performance and auction records from IPL mega-auction seasons | Supervised regression / classification with Decision Trees and related machine-learning algorithms to predict player base price | Prediction accuracy and RMSE against actual base prices | Decision-tree-based models achieve competitive base-price prediction; the study argues for a data-driven base-price policy for franchises | Both studies use tree-based ML on scraped performance data. Their target is the *base price* set before the auction (a franchise-side decision), whereas this case study uses the *realised auction price* to build a value-efficiency ranking, so the outputs address different stages of the auction workflow. |

## References

**Published studies**

1. Karnik, A. (2010). *Valuing cricketers using hedonic price models*.
   Journal of Sports Economics, 11(4), 456–469.
   DOI: 10.1177/1527002509350442.
2. Rani, P. J., Kamath, A. V., Menon, A., Chithrapriya, S. B., &
   Nithya, M. (2020). *Selection of players and team for an Indian
   Premier League cricket match using ensembles of classifiers*. In
   2020 IEEE International Conference for Convergence in Engineering
   (ICCE). DOI: 10.1109/ICCE50343.2020.9198371.
3. Malhotra, G. (2022). *A comprehensive approach to predict auction
   prices and economic value creation of cricketers in the Indian
   Premier League (IPL)*. Journal of Sports Analytics, 8(1), 3–28.
   DOI: 10.3233/JSA-200580.
4. Mansurali, A., Harish, V., Hussain, S., Swamynathan, S., & Perinba
   Selvin Raj, P. (2022). *Profiling the IPL Players — Sports
   Analytics Through Clustering Algorithms*. In Workshop on Mining
   Data for Financial Applications, Lecture Notes in Networks and
   Systems, Springer. DOI: 10.1007/978-981-99-1620-7_5.
5. Chittibabu, V., & Sundararaman, M. (2023). *Base price
   determination for IPL mega auctions: A player performance-based
   approach*. Journal of Sports Analytics, 9(3).
   DOI: 10.3233/JSA-220633.

**Data sources**

* ESPNcricinfo Statsguru — IPL batting and bowling statistics.
  <https://stats.cricinfo.com/ci/engine/stats/index.html?class=6;trophy=117>
* Wikipedia — *List of 2025 Indian Premier League personnel changes*.
  <https://en.wikipedia.org/wiki/List_of_2025_Indian_Premier_League_personnel_changes>


