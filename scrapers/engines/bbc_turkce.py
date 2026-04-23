"""Scraper engine for BBC Türkçe (bbc.com/turkce).

BBC's page uses React with CSS-in-JS class hashes; Playwright is used for reliable rendering.
"""

import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.base_engine import BaseEngine
from scrapers.utils import fetch_dynamic_html

logger = logging.getLogger(__name__)

_BASE_URL   = "https://www.bbc.com"
_TARGET_URL = "https://www.bbc.com/turkce"

_LINK_CLASSES = ["css-1i4ie53", "eq53xv90"]

# Two known class combinations for the headline <h3>; both share ez3pb4d0.
_H3_VARIANTS: list[list[str]] = [
    ["css-kiiel0", "ez3pb4d0"],
    ["css-g0mr8l",  "ez3pb4d0"],
]


class BbcTurkceEngine(BaseEngine):
    name = "bbc_turkce"
    url  = _TARGET_URL

    def scrape(self) -> list[dict]:
        logger.info(f"Fetching {_TARGET_URL}")
        html = fetch_dynamic_html(_TARGET_URL)
        return self._parse_articles(html)

    def _parse_articles(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        seen_urls: set[str] = set()
        articles: list[dict] = []

        for div in soup.find_all("div", class_="promo-text"):
            link_el = div.find("a", class_=_LINK_CLASSES)
            if not link_el:
                continue

            raw_href = link_el.get("href", "").strip()
            if not raw_href:
                continue

            url = urljoin(_BASE_URL, raw_href)
            if url in seen_urls:
                continue

            # Try each h3 variant in definition order; stop at the first match.
            h3 = None
            for h3_classes in _H3_VARIANTS:
                h3 = div.find("h3", class_=h3_classes)
                if h3:
                    break

            if not h3:
                continue

            text = h3.get_text(strip=True)
            if text:
                seen_urls.add(url)
                articles.append({"text": text, "url": url})

        logger.debug(f"Parsed {len(articles)} articles.")
        return articles
