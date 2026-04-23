"""Reads and writes scrape results to the JSON history file."""

import json
import logging
import os
from datetime import datetime

from config import OUTPUT_FILE, HISTORY_LIMIT
from exceptions import CriticalScraperError, ExitCode

logger = logging.getLogger(__name__)


def _load_history() -> list[dict]:
    """Returns the existing run history from disk, or an empty list if the file does not exist."""
    if not os.path.exists(OUTPUT_FILE):
        return []

    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_history(history: list[dict]) -> None:
    """Persists the run history to disk, creating parent directories as needed."""
    parent_dir = os.path.dirname(OUTPUT_FILE)
    try:
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except OSError as e:
        raise CriticalScraperError(
            f"Cannot write to output file '{OUTPUT_FILE}': {e}",
            ExitCode.STORAGE_ERROR,
        )


def append_run(articles: list[dict]) -> None:
    """Appends a new scrape run to the history and drops the oldest entry if HISTORY_LIMIT is exceeded."""
    history = _load_history()

    entry = {
        "scraped_at": datetime.now().isoformat(timespec="seconds"),
        "article_count": len(articles),
        "articles": articles,
    }

    history.append(entry)

    # Trim from the front so only the most recent N runs are kept.
    if len(history) > HISTORY_LIMIT:
        history = history[-HISTORY_LIMIT:]

    _save_history(history)
    logger.info(f"Saved run with {len(articles)} articles. History depth: {len(history)}/{HISTORY_LIMIT}.")
