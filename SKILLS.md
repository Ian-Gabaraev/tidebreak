# Skills & Best Practices

This document tracks techniques, patterns, and best practices discovered during Tidebreak development.

## Python Packaging & Distribution

### Building Wheels
- Use `pyproject.toml` for modern Python packaging (PEP 517/518)
- Use `setuptools.build_meta` as build backend
- Pin dependencies with version specifications
- Use `python -m build` for cross-platform wheel building
- Wheel files are platform-independent for pure Python packages

### Dependency Management
- Separate `requirements.txt` (production) and `requirements-dev.txt` (development)
- Use semantic versioning for dependencies
- Keep dependencies minimal for smaller package footprint
- Document all direct dependencies clearly

## Web Scraping & API Integration

### RSS Feed Parsing
- Use `feedparser` library for robust RSS/Atom parsing
- `feedparser.parse()` is flexible and handles malformed feeds
- Check `feed.bozo` and `feed.bozo_exception` for parsing warnings
- Entries may not have all fields - use `.get()` with defaults

### HTTP Requests Best Practices
- Create reusable `requests.Session` for connection pooling
- Implement retry logic with exponential backoff via `urllib3.util.retry.Retry`
- Set reasonable timeouts (10s default for news feeds)
- Use proper User-Agent headers to identify your client
- Handle HTTP errors gracefully (429, 500-504 for retries)

### Error Handling & Resilience
- Create a custom exception hierarchy for domain-specific errors
- Allow partial failures: get articles from successful sources even if others fail
- Log errors at appropriate levels (debug, warning, error)
- Return meaningful error messages in the result context

## Data Models & Type Safety

### Dataclasses vs Pydantic
- Use `dataclasses` for lightweight models with built-in `.asdict()` serialization
- Include `to_dict()` methods for custom serialization logic
- Use `field(default_factory=...)` for mutable defaults (lists, dicts)
- Type hints provide IDE support and documentation

### API Contract Design
- Define clear input/output data models upfront
- Include metadata in results (sources_queried, sources_successful, timestamps)
- Support serialization to dict/JSON for API responses
- Design for extensibility (new fields shouldn't break old code)

## Testing & Code Coverage

### Test Organization
- Separate test files by module (`test_models.py`, `test_fetchers.py`, etc.)
- Use `pytest` for flexible, powerful testing
- Mock external HTTP calls with `responses` library
- Aim for >90% code coverage

### Testing Best Practices
- Test happy path and error cases
- Mock external dependencies (network calls, third-party APIs)
- Use fixtures for common test data
- Property-based tests for robustness (parameterized tests)
- Test data models serialization/deserialization

## Logging

### Python Logging Setup
- Get logger per module: `logging.getLogger(__name__)`
- Use appropriate log levels: DEBUG, INFO, WARNING, ERROR
- Include context in log messages for debugging
- Avoid sensitive data in logs (API keys, tokens)

## Security Considerations

### Input Validation
- Validate country codes against a known list
- Raise meaningful exceptions for invalid input
- Use custom exception types for better error handling

### Web Scraping Ethics
- Use appropriate User-Agent headers
- Respect robots.txt and ToS
- Implement reasonable timeouts and retries
- Don't overload servers with requests

## Project Structure

### Src-Layout Package Structure
```
project/
├── src/packagename/
│   ├── __init__.py          # Exports public API
│   ├── core_module.py       # Main logic
│   ├── helpers.py           # Utilities
│   └── exceptions.py        # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_helpers.py
├── pyproject.toml           # Modern packaging config
└── setup.py                 # Legacy compatibility
```

**Benefits:**
- Cleaner separation of package code and tests
- Avoids import issues with `__pycache__`
- Ensures package installed in editable mode is properly isolated

## Session History

### Session 1 (May 2, 2026)
- Initialized project reference files
- Set up SKILLS.md, PROJECT_LOG.md, and REFERENCES.md for tracking progress

### Session 2 (May 2, 2026) — Complete Package Implementation
- Created modular package architecture with six core modules
- Implemented RSS feed fetching with retry logic and resilience
- Built comprehensive test suite (19 tests, 95% coverage)
- Created data models using dataclasses
- Set up modern Python packaging with pyproject.toml
- Successfully built and tested wheel distribution
- Achieved production-ready code with error handling and logging

### Session 3 (May 2, 2026) — Vietnam Source Parsing
- Added Vietnam country source mapping with five provided English-language sources
- Added a source dispatcher to support mixed RSS and HTML page parsing
- Implemented resilient HTML article extraction for VN domains using anchor and paragraph heuristics
- Added domain safety filters to keep extracted links on the same source host
- Extended test suite for VN mapping and HTML parser behavior
- Verified live run for `get_news_by_country("VN")`

### Session 4 (May 2, 2026) — Article Quality Ranking
- Added scoring-based ranking to prefer article-like links to topic/tag/navigation links
- Penalized low-value URL patterns (`/topic`, `/tag`, `/video`, `/search`, etc.)
- Rewarded article signals (headline length, rich summary text, article-like path structure)
- Tightened summary extraction scope to avoid nav links inheriting body text from later sections
- Added tests with mixed-quality VN HTML fixtures to verify garbage filtering behavior

### Session 5 (May 2, 2026) - Cross-Source Deduplication
- Added deterministic dedupe pass in aggregation output to remove syndicated duplicates
- Used normalized title as the primary fingerprint for cross-domain duplicate detection
- Kept first-seen item to preserve stable ordering and predictable API responses
- Added regression test for the same story appearing from two different websites

### Session 6 (May 2, 2026) - Near-Duplicate Title Matching
- Extended dedupe normalization to remove punctuation and normalize spacing/casing
- Added near-duplicate title matching using token overlap and sequence similarity heuristics
- Preserved deterministic behavior by retaining first-seen article in duplicate clusters
- Added a regression test for minor wording differences between syndicated titles

### Session 7 (May 2, 2026) — Output Contract Update
- Changed `get_news_by_country()` return type to `list[dict]`
- Standardized output keys: `ID`, `Title`, `URL`, `Source Name`, `Summary`
- Added source-name derivation from article/source URL hostname
- Kept dedupe + quality filtering while simplifying the consumer-facing payload format

### Session 8 (May 2, 2026) — Shared Serializer Layer
- Added reusable serializer module (`src/tidebreak/serializers.py`) for uniform output formatting
- Moved payload-shaping logic out of aggregator into serializer helpers
- Added dedicated serializer tests to lock output schema behavior
- Ensured all countries use the same serialization path via `get_news_by_country()`

### Session 9 (May 2, 2026) — Thailand Source Parsing
- Added an English-language Thailand source set under `TH`
- Extended fetch dispatch to support Thailand HTML domains
- Implemented Thailand HTML scoring heuristics to prioritize article-like links
- Added tests for TH mapping and TH parser quality filtering
- Verified `TH` path through public API with standardized serialized output

### Session 10 (May 2, 2026) — Live Reliability Testing
- Replaced low-success TH sources with more reachable English endpoints and feed URLs
- Added opt-in live integration tests (`tests/test_live_sources.py`) for `VN` and `TH`
- Used environment-gated live test execution (`TIDEBREAK_RUN_LIVE_TESTS=1`) to avoid CI flakiness by default
- Added README instructions for running live tests explicitly

### Session 11 (May 2, 2026) — Thailand Language/HTML Quality Gate
- Added Thailand-specific content rules to enforce English-like output
- Added Cyrillic/Thai script rejection for TH title/summary text
- Normalized RSS/HTML text through HTML tag stripping before serialization
- Added regression and live assertions to ensure TH payloads are plain text only

### Session 12 (May 2, 2026) - Flask API + Docker Stack
- Scaffolded a separate Flask service under `apps/flask_api` with app-factory structure
- Added Redis-backed response caching with a graceful fallback when Redis is unavailable
- Added SQLite request logging with auto-initialized schema
- Deployed Flask with Gunicorn and Docker Compose (`api` + `redis` services)
- Added service smoke tests and Dockerized local verification workflow

### Session 13 (May 2, 2026) — Paraphrase Duplicate Catching
- Strengthened near-duplicate title detection for syndicated paraphrases
- Added lead-token and overlap heuristic to catch close variants with minor wording changes
- Added regression test using the reported Vietnam IP-protection duplicate pair

### Session 14 (May 2, 2026) — Flask ORM Migration
- Migrated Flask app storage from raw `sqlite3` statements to SQLAlchemy ORM
- Added `RequestLog` declarative model and session-based persistence layer
- Kept existing route/storage interface stable while swapping implementation
- Added ORM storage tests and fixed SQLite connection lifecycle warnings

### Session 15 (May 2, 2026) — ORM Source Mapping + Backup Tables
- Added `country_source_map` ORM table to persist country-to-source URL mappings
- Added `article_backup` ORM table storing exact API response fields (`ID`, `Title`, `URL`, `Source Name`, `Summary`)
- Seeded source map from `tidebreak.country_mappings` at Flask app startup
- Implemented backup fallback in API route when fresh pull returns no articles

