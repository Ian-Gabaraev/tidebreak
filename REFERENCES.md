# Code References & Patterns

Useful code snippets and patterns for quick reference during development.

## Python Patterns

### Project Structure
```
tidebreak/
├── README.md
├── LICENSE
├── pyproject.toml        # Modern packaging config
├── setup.py              # Legacy compatibility
├── requirements.txt      # Production
├── requirements-dev.txt  # Development/testing
├── src/
│   └── tidebreak/
│       ├── __init__.py
│       ├── aggregator.py
│       ├── country_mappings.py
│       ├── exceptions.py
│       ├── fetchers.py
│       └── models.py
├── tests/
│   ├── __init__.py
│   ├── test_aggregator.py
│   ├── test_country_mappings.py
│   ├── test_fetchers.py
│   └── test_models.py
├── example_usage.py
├── SKILLS.md
├── PROJECT_LOG.md
└── REFERENCES.md
```

### Standard Imports
```python
# Type hints
from typing import Optional, List, Dict, Any

# Standard library
import logging
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime

# Web scraping
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import feedparser
```

### Logging Setup
```python
import logging

logger = logging.getLogger(__name__)

# Don't configure in library code, let users configure
# Testing can use caplog fixture
```

## Patterns Used in Tidebreak

### Custom Exception Hierarchy
```python
class TidebreakException(Exception):
    """Base exception for Tidebreak."""
    pass

class InvalidCountryError(TidebreakException):
    """Raised when an invalid country code is provided."""
    pass

class FetchError(TidebreakException):
    """Raised when there's an error fetching from a news source."""
    pass
```

### Dataclasses with Serialization
```python
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime

@dataclass
class Article:
    title: str
    link: str
    summary: str
    source: Optional[str] = None
    published_date: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert article to dictionary."""
        return asdict(self)

@dataclass
class CountryAggregationResult:
    country_code: str
    country_name: str
    articles: list[Article] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        data = asdict(self)
        data['articles'] = [a.to_dict() for a in self.articles]
        return data
```

### Requests Session with Retries
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session_with_retries(
    retries: int = 3,
    backoff_factor: float = 0.5,
) -> requests.Session:
    session = requests.Session()
    
    retry_strategy = Retry(
        total=retries,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"],
        backoff_factor=backoff_factor,
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (compatible; MyBot/1.0)"
    })
    
    return session
```

### RSS Feed Parsing
```python
import feedparser

def fetch_rss_feed(feed_url: str) -> list[Article]:
    """Parse RSS feed and extract articles."""
    try:
        response = requests.get(feed_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise FetchError(f"Failed to fetch feed from {feed_url}") from e
    
    try:
        feed = feedparser.parse(response.content)
        
        if feed.bozo and feed.bozo_exception:
            logger.warning(f"Feed parsing warning: {feed.bozo_exception}")
        
        articles = []
        for entry in feed.entries[:5]:  # Get up to 5 articles
            article = Article(
                title=entry.get("title", "No title"),
                link=entry.get("link", ""),
                summary=entry.get("summary", entry.get("description", "")),
                source=feed_url,
            )
            articles.append(article)
        
        return articles
    
    except Exception as e:
        raise ParseError(f"Failed to parse feed from {feed_url}") from e
```

### Main Aggregator Function Pattern
```python
def get_news_by_country(country_code: str) -> CountryAggregationResult:
    """
    Get news articles for a specific country.
    
    Process:
    1. Validate input
    2. Get available resources for country
    3. Randomly select subset of resources
    4. Fetch data from each resource
    5. Aggregate results with error handling
    """
    # 1. Validate
    if not is_valid_country_code(country_code):
        raise InvalidCountryError(f"Invalid country code: {country_code}")
    
    country_name = get_country_name(country_code)
    logger.info(f"Fetching news for {country_name}")
    
    # 2. Get resources
    available_sources = get_news_sources(country_code)
    
    if not available_sources:
        return CountryAggregationResult(
            country_code=country_code,
            country_name=country_name,
            articles=[],
            errors=[f"No news sources configured"],
        )
    
    # 3. Random selection
    sources_to_query = random.sample(
        available_sources,
        min(5, len(available_sources)),
    )
    
    # 4. Aggregate results with error handling
    result = CountryAggregationResult(
        country_code=country_code,
        country_name=country_name,
        sources_queried=len(sources_to_query),
    )
    
    session = create_session_with_retries()
    
    for source_url in sources_to_query:
        try:
            articles = fetch_rss_feed(source_url, session=session)
            result.articles.extend(articles)
            result.sources_successful += 1
        except FetchError as e:
            logger.warning(f"Failed to fetch from {source_url}: {e}")
            result.errors.append(str(e))
    
    return result
```

## Testing Patterns

### Mocking HTTP Requests
```python
import responses

@responses.activate
def test_fetch_rss_feed_success():
    """Test RSS feed fetching with mocked HTTP."""
    responses.add(
        responses.GET,
        "https://example.com/feed.rss",
        body=SAMPLE_RSS_FEED,
        status=200,
    )
    
    articles = fetch_rss_feed("https://example.com/feed.rss")
    assert len(articles) > 0
```

### Pytest Fixtures for Test Data
```python
import pytest

SAMPLE_RSS_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>Test Feed</title>
        <item>
            <title>Article 1</title>
            <link>https://example.com/article1</link>
            <description>Summary</description>
        </item>
    </channel>
</rss>
"""

@pytest.fixture
def sample_article():
    return Article(
        title="Test",
        link="https://example.com",
        summary="Summary"
    )
```

## Packaging Configuration

### pyproject.toml Essentials
```toml
[build-system]
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "package-name"
version = "0.1.0"
description = "..."
requires-python = ">=3.10"
license = {file = "LICENSE"}
dependencies = [
    "requests>=2.31.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
]
```

## Useful Commands

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install in editable mode
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests with coverage
pytest tests/ -v --cov=packagename

# Build distributions
python -m build

# Format code
black src/

# Lint code
ruff check .

# Type checking
mypy src/
```

## Security Best Practices Applied

✓ Input validation (country codes)
✓ Proper exception handling
✓ User-Agent headers for web requests
✓ Timeout management to prevent hanging
✓ Logging without sensitive data
✓ Dependency pinning with versions
✓ No hardcoded secrets or credentials

