# Tidebreak 🌊

A Python wheel package that aggregates news articles by country code. Simply provide an ISO country code and get back relevant news articles with titles, links, and summaries.

## Features

✨ **What it does:**
- Accepts ISO 3166-1 Alpha-2 country codes (e.g., "US", "GB", "FR")
- Maps countries to multiple news sources
- Randomly selects 5 news sources
- Fetches and parses RSS feeds
- Returns up to 5 articles with titles, links, and summaries
- Graceful error handling with partial failures

## Installation

```bash
pip install tidebreak-0.1.0-py3-none-any.whl
```

## Quick Start

```python
from tidebreak import get_news_by_country

# Get news for a country
result = get_news_by_country("US")

# Result is a list[dict] with required keys
for article in result:
    print(article["ID"])
    print(article["Title"])
    print(f"Link: {article['URL']}")
    print(f"Source: {article['Source Name']}")
    print(f"Summary: {article['Summary']}\n")
```

## Supported Countries

80+ countries including:
- North America: US, CA, MX
- Europe: GB, FR, DE, ES, IT, PL, and more
- Asia: JP, CN, IN, SG, TH, and more
- Africa: ZA, KE, NG, and more
- Oceania: AU, NZ

See full list in `src/tidebreak/country_mappings.py`

## Project Structure

```
tidebreak/
├── src/tidebreak/          # Main package code
│   ├── __init__.py         # Package exports
│   ├── aggregator.py       # Main news aggregation logic
│   ├── fetchers.py         # HTTP and RSS parsing
│   ├── models.py           # Data models
│   ├── country_mappings.py # Country codes and news sources
│   └── exceptions.py       # Custom exceptions
├── tests/                  # Comprehensive test suite
├── pyproject.toml          # Modern Python packaging
├── setup.py                # Setup configuration
├── requirements.txt        # Production dependencies
└── example_usage.py        # Usage examples
```

## Development

See **SKILLS.md**, **PROJECT_LOG.md**, and **REFERENCES.md** for development notes.

## Testing

```bash
pytest tests/ -v --cov=tidebreak
```

Run optional live source checks (network required):

```bash
TIDEBREAK_RUN_LIVE_TESTS=1 pytest tests/test_live_sources.py -v
```

Current coverage: **95%**

## License

MIT License - See LICENSE file for details

**Author:** Ian Gabaraev (2026)

