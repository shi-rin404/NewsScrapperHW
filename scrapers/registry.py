"""
Central registry of all active scraper engines.

To add a new source:
  1. Create a new engine in scrapers/engines/
  2. Import it here and append an instance to ENGINES
"""

from scrapers.engines.bbc_turkce   import BbcTurkceEngine
from scrapers.engines.bundle_gundem import BundleGundemEngine
from scrapers.engines.euronews_tr  import EuronewsTrEngine
from scrapers.engines.indy_turk    import IndyTurkEngine

ENGINES = [
    BundleGundemEngine(),
    BbcTurkceEngine(),
    IndyTurkEngine(),
    EuronewsTrEngine(),
]
