"""Shared HTML fetch utilities used by scraper engines.

Engines that scrape JS-rendered pages call fetch_dynamic_html().
Engines that scrape server-rendered pages call fetch_static_html().
"""

import logging

import requests
from playwright.sync_api import sync_playwright

from exceptions import CriticalScraperError, ExitCode

logger = logging.getLogger(__name__)

_REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def fetch_static_html(url: str, timeout: int = 15) -> str:
    """Fetches a server-rendered page via requests. Raises requests.HTTPError on non-2xx responses."""
    response = requests.get(url, headers=_REQUEST_HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.text


def fetch_dynamic_html(url: str) -> str:
    """Renders a JS-heavy page with headless Chromium and returns the full page HTML.

    Raises CriticalScraperError if the browser binary cannot be launched.
    Page-load failures (timeouts, network errors) are left to propagate so the
    scheduler can log them as non-fatal and continue.
    """
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
        except Exception as e:
            raise CriticalScraperError(
                f"Chromium browser could not be launched: {e}",
                ExitCode.BROWSER_ERROR,
            )

        try:
            page = browser.new_page()
            # networkidle waits until there are no active network connections for 500 ms.
            page.goto(url, wait_until="networkidle")
            html = page.content()
        finally:
            browser.close()

    return html
