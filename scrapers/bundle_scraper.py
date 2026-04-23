"""Fetches and parses trending news articles from the Bundle website."""

import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from config import BASE_URL, TARGET_URL, ARTICLE_LINK_CLASSES, ARTICLE_TEXT_CLASSES
from exceptions import CriticalScraperError, ExitCode

logger = logging.getLogger(__name__)


def _fetch_rendered_html() -> str:
    """Launches a headless browser, waits for JS to finish, and returns the full page HTML."""
    with sync_playwright() as p:
        # A launch failure (e.g. missing Chromium binary) is unrecoverable — escalate immediately.
        try:
            browser = p.chromium.launch(headless=True)
        except Exception as e:
            raise CriticalScraperError(
                f"Chromium browser could not be launched: {e}",
                ExitCode.BROWSER_ERROR,
            )

        try:
            page = browser.new_page()
            # networkidle waits until there are no more than 0 network connections for 500ms,
            # which is necessary for JS-rendered (React/Next.js) pages.
            page.goto(TARGET_URL, wait_until="networkidle")
            html = page.content()
        finally:
            # Always close the browser, even if page.goto() raises (e.g. network timeout).
            browser.close()

    return html


def _parse_articles(html: str) -> list[dict]:
    """Extracts article text and URLs from rendered HTML using BeautifulSoup."""
    soup = BeautifulSoup(html, "html.parser")
    articles = []

    # Find all <a> containers that carry every class in ARTICLE_LINK_CLASSES.
    # BeautifulSoup's class_ list argument performs a subset match (all classes must be present).
    link_elements = soup.find_all("a", class_=ARTICLE_LINK_CLASSES)

    for link_el in link_elements:
        raw_href = link_el.get("href", "").strip()
        if not raw_href:
            continue

        # urljoin handles both absolute hrefs (returned as-is) and relative paths.
        url = urljoin(BASE_URL, raw_href)

        # Each article container holds exactly one headline <p>; take the first match.
        text_el = link_el.find("p", class_=ARTICLE_TEXT_CLASSES)
        if not text_el:
            continue

        text = text_el.get_text(strip=True)
        if text:
            articles.append({"text": text, "url": url})

    logger.debug(f"Parsed {len(articles)} articles from HTML.")
    return articles


def scrape_articles() -> list[dict]:
    """Public entry point: renders the page and returns a list of {text, url} dicts."""
    logger.info(f"Fetching {TARGET_URL}")
    html = _fetch_rendered_html()
    return _parse_articles(html)
