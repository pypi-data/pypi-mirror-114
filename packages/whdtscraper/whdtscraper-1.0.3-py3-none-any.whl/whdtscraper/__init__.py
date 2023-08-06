import warnings
warnings.simplefilter('always', DeprecationWarning)
warnings.warn("Note: this package is deprecated in favour of mhdscraper", DeprecationWarning)

from whdtscraper.whdtscraper import fetch_latest_version, fetch_versions, fetch_wikies, fetch_dumps, WIKI_URL
