"""
Central configuration for the Bundle news scraper project.

Engine-specific constants (URLs, CSS selectors) live inside each engine module,
not here. Only shared, cross-cutting settings belong in this file.
"""

# --- Storage ---
OUTPUT_DIR = "data"

# Maximum number of scrape runs to retain per source (oldest are dropped first).
HISTORY_LIMIT = 10

# --- Logging ---
LOGS_DIR = "logs"

# Maximum number of per-run log files to keep on disk (oldest are deleted first).
LOG_HISTORY_LIMIT = 10

# --- Scheduler ---
SCRAPE_INTERVAL_MINUTES = 60
