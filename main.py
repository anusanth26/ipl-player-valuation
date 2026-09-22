from scraper.utils import create_directories
from scraper.scraper import scrape_batting, scrape_bowling
from scraper.auction_scraper import run_auction_scraper
from scraper.merge_data import merge_batting_bowling
from scraper.player_matching import run_matching
from scraper.build_final_dataset import build_final_dataset

def main():
    print("Starting IPL 2025 Data Pipeline...")
    create_directories()

    # Step 1: Scrape Statsguru
    print("\n--- Step 1: Scraping ESPNcricinfo ---")
    scrape_batting()
    scrape_bowling()
    merge_batting_bowling()

    # Step 2: Scrape Auction Data
    print("\n--- Step 2: Scraping Wikipedia Auction Data ---")
    run_auction_scraper()

    # Step 3: Match Players & Build Final Dataset
    print("\n--- Step 3: Matching Players ---")
    run_matching()
    
    print("\n--- Step 4: Building Final Dataset ---")
    build_final_dataset()
    
    print("\nPipeline execution completed successfully.")

if __name__ == "__main__":
    main()