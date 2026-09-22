from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

from scraper.config import (
    AUCTION_URL,
    AUCTION_OUTPUT_FILE
)

from scraper.auction_parser import (
    extract_auction_tables
)


def scrape_auction():

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        )
    )

    driver.maximize_window()

    print("Opening auction page...")

    driver.get(AUCTION_URL)

    # Wait for page to finish loading
    WebDriverWait(driver, 15).until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )

    print("Page loaded successfully.")

    # Get page HTML
    html = driver.page_source

    driver.quit()

    # Extract all auction sets
    df = extract_auction_tables(html)

    print("\nAuction Dataset:")
    print(df.head())

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nAuction Sets:")
    print(
        df["Auction_Set"].value_counts(
            dropna=False
        )
    )

    # Save raw auction data
    df.to_csv(
        AUCTION_OUTPUT_FILE,
        index=False
    )

    print("\nSaved to:")
    print(AUCTION_OUTPUT_FILE)


if __name__ == "__main__":
    scrape_auction()