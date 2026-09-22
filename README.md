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
│   ├── utils.py
│   └── requirements.txt
│
├── main.py
└── README.md
