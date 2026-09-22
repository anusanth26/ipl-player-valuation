**IPL Player Valuation**
A Business Analytics case study on evaluating IPL player performance in relation to 2025 auction prices.
Overview
This project analyzes IPL player performance statistics and 2025 auction prices to study performance-price efficiency in franchise cricket.
The analysis has two main components:
1. Player Performance Classification — classify players into performance tiers using batting and bowling statistics.
2. Performance-Price Analysis — compare player performance with auction price to identify relatively high-value and high-cost acquisitions.
The results are intended to provide data-driven insights that can support player shortlisting and auction budget planning.
Objectives
- Classify IPL players based on their observed performance.
- Analyze the relationship between player performance and 2025 auction price.
- Identify performance-price patterns that can support auction decision-making.
Data Sources
Player performance data is collected from ESPNcricinfo Statsguru using Selenium and BeautifulSoup.
Auction information is collected from the 2025 IPL personnel and auction tables on Wikipedia.
The project uses publicly available data and does not use a ready-made Kaggle, UCI, or similar dataset as its primary data source.
Methodology
The project follows this workflow:
Web Scraping
     ↓
Data Cleaning
     ↓
Data Integration
     ↓
Exploratory Data Analysis
     ↓
Performance Scoring
     ↓
Performance Classification
     ↓
Performance vs Price Analysis
     ↓
Clustering
     ↓
Business Insights
The planned machine learning methods include Logistic Regression / Random Forest for performance classification and K-Means clustering for performance-price analysis.
Dataset
The integrated dataset contains player-level batting, bowling, and auction information.
Key performance variables include:
- Runs
- Batting average
- Strike rate
- Wickets
- Bowling average
- Economy rate
- Bowling strike rate
- Fours and sixes
- 4-wicket and 5-wicket hauls
- Maidens
Auction-related variables include:
- Base price
- 2025 auction price
- 2025 IPL team
- Player role
- Country
The current integrated dataset contains 164 matched players.
Project Structure
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
│   ├── config.py
│   ├── scraper.py
│   ├── parser.py
│   ├── auction_scraper.py
│   ├── auction_parser.py
│   ├── merge_data.py
│   ├── utils.py
│   └── requirements.txt
│
├── main.py
└── README.md
Key Output
The analysis aims to produce a player-level view containing:
- Performance score
- Performance tier
- 2025 auction price
- Performance-price cluster
- Value interpretation
The project is a retrospective analysis of observed performance and auction price. It is intended to support future auction decisions rather than predict future player performance.
Note
Retained players are treated separately from players purchased during the 2025 auction, since retained players do not have a 2025 auction purchase price.
Tools & Technologies
- Python
- Pandas
- NumPy
- Scikit-learn
- BeautifulSoup
- Selenium
- Matplotlib
- Jupyter Notebook
Status
In progress
Current work is focused on finalizing the integrated dataset, data preprocessing, exploratory analysis, and the performance-price analysis.
