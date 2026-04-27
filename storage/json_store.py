"""Reads and writes per-engine scrape results to rotating JSON history files."""

import json
import logging
import os
from datetime import datetime

from config import OUTPUT_DIR, HISTORY_LIMIT
from exceptions import CriticalScraperError, ExitCode

logger = logging.getLogger(__name__)


def _output_path(engine_name: str) -> str:
    return os.path.join(OUTPUT_DIR, f"{engine_name}.json")


def _load_history(path: str) -> list[dict]:
    """Returns the existing run history for one engine, or an empty list if the file is new."""
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_history(history: list[dict], path: str) -> None:
    """Persists a run history to disk, creating parent directories as needed."""
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except OSError as e:
        raise CriticalScraperError(
            f"Cannot write to output file '{path}': {e}",
            ExitCode.STORAGE_ERROR,
        )


def append_run(engine_name: str, articles: list[dict]) -> str:
    """
    Appends a new scrape run for the given engine and prunes entries beyond HISTORY_LIMIT.

    Returns the path of the file that was written.
    """
    path = _output_path(engine_name)
    history = _load_history(path)

    history.append({
        "scraped_at": datetime.now().isoformat(timespec="seconds"),
        "article_count": len(articles),
        "articles": articles,
    })

    if len(history) > HISTORY_LIMIT:
        history = history[-HISTORY_LIMIT:]

    _save_history(history, path)
    logger.info(f"[{engine_name}] Saved {len(articles)} articles. History: {len(history)}/{HISTORY_LIMIT}.")
    return path
