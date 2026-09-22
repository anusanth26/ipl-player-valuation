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
        service=Service(ChromeDriverManager().install())
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

        df = extract_table(html, table_type)

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

            next_url = next_button.get_attribute("href")

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

    # Remove duplicate players
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