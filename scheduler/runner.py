"""Registers and drives the periodic scraping job."""

import logging
import time

import schedule

from config import SCRAPE_INTERVAL_MINUTES, TARGET_URL, OUTPUT_FILE
from exceptions import CriticalScraperError
from logger.file_logger import create_run_logger
from scrapers.bundle_scraper import scrape_articles
from storage.json_store import append_run

logger = logging.getLogger(__name__)


def _run_scrape_job() -> None:
    """Executes one full scrape-and-store cycle."""
    run_log = create_run_logger()
    logger.info("Scrape job started.")

    try:
        articles = scrape_articles()
        append_run(articles)
        run_log.log_success(TARGET_URL, len(articles), OUTPUT_FILE)
        logger.info(f"Scraped {len(articles)} articles.")
    except CriticalScraperError as e:
        # Unrecoverable — log to file and exit with the appropriate code.
        logger.critical(str(e))
        run_log.log_critical(str(e), e.exit_code)
    except Exception as e:
        # Non-fatal — record the error and let the scheduler continue.
        logger.exception("Scrape job failed.")
        run_log.log_error(str(e))


def start() -> None:
    """Runs the scraper once immediately, then repeats it every SCRAPE_INTERVAL_MINUTES minutes."""
    logger.info(f"Scheduler initialised — interval: every {SCRAPE_INTERVAL_MINUTES} minute(s).")

    # Fire immediately so there is data from the moment the process starts.
    _run_scrape_job()

    schedule.every(SCRAPE_INTERVAL_MINUTES).minutes.do(_run_scrape_job)

    while True:
        schedule.run_pending()
        time.sleep(1)
