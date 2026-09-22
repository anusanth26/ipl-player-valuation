from pathlib import Path

# IPL Batting Stats
BATTING_URL = (
    "https://stats.cricinfo.com/ci/engine/stats/index.html?"
    "class=6;filter=advanced;orderby=runs;"
    "size=200;template=results;"
    "tournament_type=5;trophy=117;type=batting"
)

# IPL Bowling Stats
BOWLING_URL = (
    "https://stats.cricinfo.com/ci/engine/stats/index.html?"
    "class=6;filter=advanced;orderby=matches;"
    "size=200;template=results;"
    "tournament_type=5;trophy=117;type=bowling"
)

# IPL 2025 Auction
AUCTION_URL = (
    "https://en.wikipedia.org/wiki/"
    "List_of_2025_Indian_Premier_League_personnel_changes"
)

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "raw"

BATTING_OUTPUT_FILE = DATA_DIR / "ipl_batting_raw.csv"
BOWLING_OUTPUT_FILE = DATA_DIR / "ipl_bowling_raw.csv"
AUCTION_OUTPUT_FILE = DATA_DIR / "ipl_2025_auction_raw.csv"

WAIT_TIME = 3
