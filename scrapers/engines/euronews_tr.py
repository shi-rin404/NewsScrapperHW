"""Scraper engine for Euronews Türkçe (tr.euronews.com/son-haberler)."""

import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.base_engine import BaseEngine
from scrapers.utils import fetch_dynamic_html

logger = logging.getLogger(__name__)

_BASE_URL   = "https://tr.euronews.com"
_TARGET_URL = "https://tr.euronews.com/son-haberler"


class EuronewsTrEngine(BaseEngine):
    name = "euronews_tr"
    url  = _TARGET_URL

    def scrape(self) -> list[dict]:
        logger.info(f"Fetching {_TARGET_URL}")
        html = fetch_dynamic_html(_TARGET_URL)
        return self._parse_articles(html)

    def _parse_articles(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        seen_urls: set[str] = set()
        articles: list[dict] = []

        for li in soup.find_all("li", class_="tc-justin-timeline__item"):
            h2 = li.find("h2", class_="tc-justin-timeline__article__title")
            if not h2:
                continue

            link_el = li.find("a", class_="tc-justin-timeline__article__link")
            if not link_el:
                continue

            raw_href = link_el.get("href", "").strip()
            if not raw_href:
                continue

            url = urljoin(_BASE_URL, raw_href)
            if url in seen_urls:
                continue

            text = h2.get_text(strip=True)
            if text:
                seen_urls.add(url)
                articles.append({"text": text, "url": url})

        logger.debug(f"Parsed {len(articles)} articles.")
        return articles
