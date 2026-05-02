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

## How Duplicate Detection Works

News syndication means the same story can appear across multiple outlets with slightly different wording. Tidebreak runs a deduplication pass before returning the final list.

### 1) Text normalization

Before comparing titles, Tidebreak normalizes them by:
- lowercasing
- removing punctuation
- collapsing extra whitespace

This makes small formatting differences compare correctly.

### 2) Exact duplicate check

If two normalized titles are exactly the same, they are considered duplicates.

### 3) Near-duplicate check

If titles are not exact matches, Tidebreak applies similarity heuristics:
- token overlap ratio (shared important words)
- Jaccard similarity (shared words vs total unique words)
- sequence similarity (overall string closeness)
- leading phrase match (same first few words) for syndicated paraphrases

This catches cases like:
- "Vietnam requests US to deliver objective, balanced assessment..."
- "Vietnam requests US to make objective assessment..."

### 4) Stable retention rule

When duplicates are found, Tidebreak keeps the first seen article and drops later duplicates. This keeps output deterministic and avoids noisy repeats.

### Notes

- Deduplication runs before the final top-5 trim.
- It is title-based, which works well for syndicated headlines.
- Very aggressive dedupe can hide legitimately distinct but similar stories; thresholds are tuned to balance that risk.

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

## Flask API Service

A separate Flask API service is available in `apps/flask_api`.

- Endpoint: `GET /api/v1/articles/<country_code>`
- Stack: Gunicorn + Redis cache + SQLite request logging
- Dockerized via root `docker-compose.yml`

See `apps/flask_api/README.md` for run and smoke-test commands.

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

