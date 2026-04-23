"""Central configuration for the Bundle news scraper project."""

# --- Target ---
BASE_URL = "https://www.bundle.app"
TARGET_URL = "https://www.bundle.app/tr/gundem"

# --- HTML Element Identifiers ---
# Subset of classes that uniquely identify the <a> container for each article.
# Using a subset rather than the full class string makes matching resilient to minor markup changes.
ARTICLE_LINK_CLASSES = ["font-barlow", "min-w-[280px]", "w-[280px]"]

# Subset of classes that uniquely identify the <p> headline inside each article container.
ARTICLE_TEXT_CLASSES = ["line-clamp-3", "font-semibold"]

# --- Storage ---
OUTPUT_FILE = "data/news.json"

# Maximum number of scrape runs to retain in the history file (oldest are dropped first).
HISTORY_LIMIT = 10

# --- Logging ---
LOGS_DIR = "logs"

# Maximum number of per-run log files to keep on disk (oldest are deleted first).
LOG_HISTORY_LIMIT = 10

# --- Scheduler ---
SCRAPE_INTERVAL_MINUTES = 5
