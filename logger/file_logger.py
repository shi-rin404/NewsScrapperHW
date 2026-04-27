"""Creates and manages per-run rotating log files under the logs directory."""

import os
import re
import sys
from datetime import datetime

from config import LOGS_DIR, LOG_HISTORY_LIMIT


def _existing_log_files() -> list[str]:
    """Returns log filenames in the logs directory sorted by their numeric index (ascending)."""
    os.makedirs(LOGS_DIR, exist_ok=True)
    files = [f for f in os.listdir(LOGS_DIR) if re.match(r"^log_\d+\.txt$", f)]
    return sorted(files, key=lambda f: int(re.search(r"\d+", f).group()))


def _prune_old_logs(existing: list[str]) -> None:
    """Removes the oldest log files so the total stays below LOG_HISTORY_LIMIT."""
    # Delete from the front (smallest index = oldest) until there is room for the new file.
    while len(existing) >= LOG_HISTORY_LIMIT:
        oldest = existing.pop(0)
        os.remove(os.path.join(LOGS_DIR, oldest))


def _next_log_number(existing: list[str]) -> int:
    """Returns the next sequential log number based on the highest existing index."""
    if not existing:
        return 1
    last_n = int(re.search(r"\d+", existing[-1]).group())
    return last_n + 1


class RunLogger:
    """Writes structured log entries for a single scrape run to its dedicated log file."""

    def __init__(self, log_path: str):
        self._path = log_path

    def _write(self, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self._path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")

    def log_success(self, url: str, article_count: int, json_path: str) -> None:
        self._write(
            f"Data scrapped from {url}. "
            f"{article_count} articles has found. "
            f"Saved into {json_path}."
        )

    def log_error(self, message: str) -> None:
        """Logs a non-fatal error. The scheduler will continue to the next run."""
        self._write(f"ERROR: {message}")

    def log_critical(self, message: str, exit_code: int) -> None:
        """Logs a fatal error and terminates the process with the given exit code."""
        self._write(f"CRITICAL: {message} — Exiting with code {exit_code}.")
        sys.exit(exit_code)


def create_run_logger() -> RunLogger:
    """
    Creates a fresh log file for the upcoming scrape run and returns a RunLogger bound to it.

    Prunes the oldest log file first if the history limit has been reached.
    """
    existing = _existing_log_files()
    _prune_old_logs(existing)
    n = _next_log_number(existing)
    log_path = os.path.join(LOGS_DIR, f"log_{n}.txt")
    return RunLogger(log_path)
