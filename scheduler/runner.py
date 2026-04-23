"""Registers and drives the periodic scraping job across all engines."""

import logging
import time

import schedule

from config import SCRAPE_INTERVAL_MINUTES
from exceptions import CriticalScraperError
from logger.file_logger import create_run_logger
from scrapers.registry import ENGINES
from storage.json_store import append_run

logger = logging.getLogger(__name__)


def _run_scrape_job() -> None:
    """
    Runs every registered engine once and writes results to their respective JSON files.

    One log file is created per scheduler tick and shared across all engines in that tick.
    A CriticalScraperError from any engine terminates the process immediately.
    Any other exception is logged and the remaining engines continue normally.
    """
    run_log = create_run_logger()
    logger.info(f"Scrape job started — {len(ENGINES)} engine(s) registered.")

    for engine in ENGINES:
        try:
            articles = engine.scrape()
            output_path = append_run(engine.name, articles)
            run_log.log_success(engine.url, len(articles), output_path)
            logger.info(f"[{engine.name}] Scraped {len(articles)} articles.")
        except CriticalScraperError as e:
            logger.critical(str(e))
            run_log.log_critical(str(e), e.exit_code)  # calls sys.exit()
        except Exception as e:
            logger.exception(f"[{engine.name}] Scrape failed.")
            run_log.log_error(f"[{engine.name}] {e}")


def start() -> None:
    """Runs all engines once immediately, then repeats every SCRAPE_INTERVAL_MINUTES minutes."""
    logger.info(f"Scheduler initialised — interval: every {SCRAPE_INTERVAL_MINUTES} minute(s).")

    _run_scrape_job()

    schedule.every(SCRAPE_INTERVAL_MINUTES).minutes.do(_run_scrape_job)

    while True:
        schedule.run_pending()
        time.sleep(1)
