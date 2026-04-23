"""Scraper engine for the trending news page on bundle.app."""

import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.base_engine import BaseEngine
from scrapers.utils import fetch_dynamic_html

logger = logging.getLogger(__name__)

_BASE_URL   = "https://www.bundle.app"
_TARGET_URL = "https://www.bundle.app/tr/gundem"

# Each tuple is (link_classes, text_classes) — a unique subset of Tailwind classes that
# identifies one article card layout. Multiple layouts exist on the same page.
_SELECTOR_PAIRS: list[tuple[list[str], list[str]]] = [
    # Horizontal card (fixed 280 px width)
    (["font-barlow", "min-w-[280px]", "w-[280px]"],       ["line-clamp-3", "font-semibold"]),
    # Vertical card (rounded, white background)
    (["font-barlow", "rounded-[20px]", "cursor-pointer"],  ["font-semibold", "text-[17px]"]),
]


class BundleGundemEngine(BaseEngine):
    name = "bundle_gundem"
    url  = _TARGET_URL

    def scrape(self) -> list[dict]:
        logger.info(f"Fetching {_TARGET_URL}")
        html = fetch_dynamic_html(_TARGET_URL)
        return self._parse_articles(html)

    def _parse_articles(self, html: str) -> list[dict]:
        """Iterates over every selector pair so all card layouts on the page are covered.

        Results are deduplicated by URL to prevent duplicates when layouts overlap.
        """
        soup = BeautifulSoup(html, "html.parser")
        seen_urls: set[str] = set()
        articles: list[dict] = []

        for link_classes, text_classes in _SELECTOR_PAIRS:
            for link_el in soup.find_all("a", class_=link_classes):
                raw_href = link_el.get("href", "").strip()
                if not raw_href:
                    continue

                url = urljoin(_BASE_URL, raw_href)
                if url in seen_urls:
                    continue

                text_el = link_el.find("p", class_=text_classes)
                if not text_el:
                    continue

                text = text_el.get_text(strip=True)
                if text:
                    seen_urls.add(url)
                    articles.append({"text": text, "url": url})

        logger.debug(f"Parsed {len(articles)} articles across {len(_SELECTOR_PAIRS)} selector pair(s).")
        return articles
