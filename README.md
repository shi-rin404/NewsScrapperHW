# Turkish News Scraper

A modular, scheduled web scraper that collects trending news headlines from multiple Turkish news sources and persists them to rotating JSON history files.

---

## Sources

| Engine | Site | Method |
|---|---|---|
| `bundle_gundem` | [bundle.app/tr/gundem](https://www.bundle.app/tr/gundem) | Playwright (JS-rendered) |
| `bbc_turkce` | [bbc.com/turkce](https://www.bbc.com/turkce) | Playwright (JS-rendered) |
| `indy_turk` | [indyturk.com](https://www.indyturk.com) | requests (static) |
| `euronews_tr` | [tr.euronews.com/son-haberler](https://tr.euronews.com/son-haberler) | Playwright (JS-rendered) |

---

## Project Structure

```
├── config.py                   # All shared constants (interval, limits, paths)
├── exceptions.py               # CriticalScraperError + exit codes
├── main.py                     # Entry point
│
├── scrapers/
│   ├── base_engine.py          # Abstract base class all engines implement
│   ├── registry.py             # List of active engines — edit this to add sources
│   ├── utils.py                # Shared fetch helpers (static & dynamic)
│   └── engines/
│       ├── bundle_gundem.py
│       ├── bbc_turkce.py
│       ├── indy_turk.py
│       └── euronews_tr.py
│
├── storage/
│   └── json_store.py           # Per-engine JSON read / write / rotate
│
├── scheduler/
│   └── runner.py               # schedule-based hourly loop
│
└── logger/
    └── file_logger.py          # Per-run rotating log files
```

---

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download the Playwright browser binary (one-time)
playwright install chromium

# 4. Run
python main.py
```

---

## Configuration

All tuneable constants live in `config.py`.

| Constant | Default | Description |
|---|---|---|
| `SCRAPE_INTERVAL_MINUTES` | `60` | How often each source is scraped |
| `HISTORY_LIMIT` | `10` | Max scrape runs retained per source JSON file |
| `OUTPUT_DIR` | `"data"` | Directory for JSON output files |
| `LOGS_DIR` | `"logs"` | Directory for log files |
| `LOG_HISTORY_LIMIT` | `10` | Max log files kept on disk |

---

## Output

Each source writes to its own file under `data/`:

```
data/
├── bundle_gundem.json
├── bbc_turkce.json
├── indy_turk.json
└── euronews_tr.json
```

Each file holds a rolling list of up to 10 scrape runs:

```json
[
  {
    "scraped_at": "2026-04-23T13:00:00",
    "article_count": 14,
    "articles": [
      { "text": "Headline text", "url": "https://..." },
      ...
    ]
  }
]
```

---

## Logs

A new file is created in `logs/` for every scheduler tick, named `log_{n}.txt`. Oldest files are deleted once the count exceeds `LOG_HISTORY_LIMIT`.

```
[2026-04-23 13:00:01] Data scrapped from https://www.bundle.app/tr/gundem. 14 articles has found. Saved into data\bundle_gundem.json.
[2026-04-23 13:00:45] ERROR: [euronews_tr] net::ERR_CONNECTION_TIMED_OUT
[2026-04-23 13:01:00] CRITICAL: Chromium browser could not be launched — Exiting with code 3.
```

---

## Exit Codes

| Code | Meaning |
|---|---|
| `1` | Unknown critical error |
| `2` | Storage write failure (`OSError` on JSON output) |
| `3` | Browser launch failure (Playwright / Chromium not found) |

---

## Adding a New Source

**1.** Create `scrapers/engines/my_source.py`:

```python
from scrapers.base_engine import BaseEngine
from scrapers.utils import fetch_static_html  # or fetch_dynamic_html

class MySourceEngine(BaseEngine):
    name = "my_source"          # becomes data/my_source.json
    url  = "https://..."

    def scrape(self) -> list[dict]:
        html = fetch_static_html(self.url)
        # parse and return [{"text": "...", "url": "..."}]
```

**2.** Register it in `scrapers/registry.py`:

```python
from scrapers.engines.my_source import MySourceEngine

ENGINES = [
    ...
    MySourceEngine(),
]
```

No other changes needed — scheduling, logging, and JSON rotation are handled automatically.
