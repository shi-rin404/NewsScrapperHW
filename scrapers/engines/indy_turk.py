"""Scraper engine for IndyTurk (indyturk.com)."""

import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.base_engine import BaseEngine
from scrapers.utils import fetch_static_html

logger = logging.getLogger(__name__)

_BASE_URL   = "https://www.indyturk.com"
_TARGET_URL = "https://www.indyturk.com"


class IndyTurkEngine(BaseEngine):
    name = "indy_turk"
    url  = _TARGET_URL

    def scrape(self) -> list[dict]:
        logger.info(f"Fetching {_TARGET_URL}")
        html = fetch_static_html(_TARGET_URL)
        return self._parse_articles(html)

    def _parse_articles(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        seen_urls: set[str] = set()
        articles: list[dict] = []

        for div in soup.find_all("div", class_="article-item-title"):
            links = div.find_all("a")

            if len(links) != 1:
                logger.error(
                    f"[indy_turk] Expected exactly 1 <a> inside .article-item-title, "
                    f"found {len(links)} — skipping element."
                )
                continue

            link_el = links[0]
            raw_href = link_el.get("href", "").strip()
            if not raw_href:
                continue

            url = urljoin(_BASE_URL, raw_href)
            if url in seen_urls:
                continue

            text = div.get_text(strip=True)
            if text:
                seen_urls.add(url)
                articles.append({"text": text, "url": url})

        logger.debug(f"Parsed {len(articles)} articles.")
        return articles
