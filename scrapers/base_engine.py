"""Abstract base class that every scraper engine must implement."""

from abc import ABC, abstractmethod


class BaseEngine(ABC):
    """
    Contract for a scraper engine.

    Subclasses must define:
      - `name`  — unique snake_case identifier; becomes the output filename stem (data/{name}.json)
      - `url`   — primary target URL; used in log messages
      - `scrape()` — fetches and returns a list of {"text": str, "url": str} dicts
    """

    name: str
    url: str

    @abstractmethod
    def scrape(self) -> list[dict]:
        """Return a list of {"text": str, "url": str} dicts for this source."""
        ...
