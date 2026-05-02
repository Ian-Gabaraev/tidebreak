# Project Log

Development progress and decisions for the Tidebreak project.

## Timeline

### May 2, 2026

#### Session 1: Project Setup
- Created reference files for documentation and tracking
- Set up README.md, SKILLS.md, PROJECT_LOG.md, REFERENCES.md
- **Status**: Ready to start building

#### Session 2: Complete Package Implementation (COMPLETED ✓)

**Architecture & Design:**
- Created modular package structure with 6 core modules:
  - `models.py` - Data models (Article, CountryAggregationResult)
  - `country_mappings.py` - Country codes and news source mappings
  - `exceptions.py` - Custom exception hierarchy
  - `fetchers.py` - HTTP client and RSS parser
  - `aggregator.py` - Main orchestrator function
  - `__init__.py` - Public API exports

**Implementation Details:**
- **Fetchers Module**: Robust HTTP client with:
  - Connection pooling via requests.Session
  - Automatic retry logic with exponential backoff (Retry strategy)
  - Configurable timeouts (10s default)
  - Proper User-Agent headers
  - Error handling and logging

- **Aggregator Function**: `get_news_by_country(country_code)`
  - Validates country code against known list
  - Retrieves available news sources for country
  - Randomly selects 5 sources (or fewer if not available)
  - Fetches and parses RSS feeds in parallel session
  - Collects up to 5 articles per successful source
  - Gracefully handles partial failures
  - Returns structured CountryAggregationResult

- **Data Models**: Type-safe with JSON serialization
  - Article: title, link, summary, source, published_date
  - CountryAggregationResult: metadata + articles list

**Testing:**
- Created comprehensive test suite (19 tests)
- Achieved 95% code coverage
- Test modules: test_aggregator.py, test_models.py, test_fetchers.py, test_country_mappings.py
- Mocked external HTTP calls with `responses` library
- All tests passing ✓

**Packaging & Distribution:**
- Modern `pyproject.toml` with setuptools configuration
- Created `setup.py` for legacy compatibility
- Built wheel distribution: `tidebreak-0.1.0-py3-none-any.whl` (8.4 KB)
- Also built source distribution: `tidebreak-0.1.0.tar.gz` (10 KB)
- Fixed deprecation warnings for pyproject.toml license format
- Wheel tested and verified working in clean environment ✓

**Country & News Sources:**
- Mapped 80+ ISO country codes to country names
- Pre-configured news sources for: US, GB, FR, DE, CA, AU
- Other countries ready for source mapping
- Extensible architecture for adding more sources

**Documentation:**
- Comprehensive README with features and quick start
- API documentation in docstrings
- Example usage script (example_usage.py)
- Updated SKILLS.md with patterns and best practices
- Updated REFERENCES.md with code snippets

**Demo/Verification:**
- Tested wheel installation in clean environment
- Successfully fetched real news articles from multiple sources
- Gracefully handled mixed success/failure scenarios (1 feed failed, returned 4 articles)

**Status**: ✅ COMPLETE - Ready for production use

#### Session 3: Vietnam Parser Implementation (COMPLETED ✓)

**Goal:** Implement parsing for Vietnam sources provided by user:
- `https://vietnamnews.vn/`
- `https://en.baodanang.vn/`
- `https://e.vnexpress.net/`
- `https://news.tuoitre.vn/vietnam-news.htm`
- `https://en.vietnamplus.vn/`

**Code Changes:**
- Added `VN` source entries in `src/tidebreak/country_mappings.py`
- Added `fetch_articles_from_source()` dispatcher in `src/tidebreak/fetchers.py`
- Kept RSS support and added VN HTML page parsing path
- Added VN domain allowlist + same-host link filtering to improve extraction quality
- Updated aggregator to call new dispatcher (`fetch_articles_from_source`)

**Testing:**
- Updated `tests/test_aggregator.py` to patch new dispatcher function
- Added VN mapping test in `tests/test_country_mappings.py`
- Added fetcher tests for:
  - RSS dispatch path
  - Vietnam HTML extraction path
  - Unsupported HTML parse error path
- Test run result: **23 passed**

**Live Verification:**
- Ran `get_news_by_country("VN")`
- Result: 5 sources queried, 5 successful, 5 articles returned

**Status**: ✅ Vietnam parsing integrated and verified

#### Session 4: Vietnam Article Quality Ranking (COMPLETED ✓)

**Goal:** Reduce low-value HTML picks (topic/tag/navigation links) and prioritize real stories.

**Code Changes:**
- Added URL/token quality scoring in `src/tidebreak/fetchers.py`
- Added penalties for non-article patterns (topic/tag/video/search/etc.)
- Added positive signals for article-like links (path/title/summary characteristics)
- Tightened paragraph-summary extraction to only nearby text before the next anchor

**Testing & Verification:**
- Added mixed-quality parser test in `tests/test_fetchers.py`
- Full test run result: **24 passed**
- Live run for `get_news_by_country("VN")` returned 5 article-like links from 5/5 sources

**Status**: ✅ VN parser now favors higher-quality story links

#### Session 5: Duplicate Story Removal (COMPLETED ✓)

**Goal:** Avoid returning the same story twice when syndicated by multiple websites.

**Code Changes:**
- Added normalization + fingerprint helpers in `src/tidebreak/aggregator.py`
- Added `_dedupe_articles(...)` pass to remove duplicates before final result truncation
- Deduplication key uses normalized title, which catches common cross-site syndicated copies

**Testing:**
- Added regression test in `tests/test_aggregator.py` for duplicate titles from 2 different sources
- Ensures output keeps one copy and preserves stable first-seen ordering

**Status**: ✅ Duplicate syndicated stories are now filtered from response output

#### Session 6: Near-Duplicate Deduplication (COMPLETED ✓)

**Goal:** Catch duplicate stories even when titles differ slightly across sources.

**Code Changes:**
- Enhanced title normalization in `src/tidebreak/aggregator.py` (case, punctuation, whitespace)
- Added near-duplicate matcher based on token overlap and sequence similarity
- Kept deterministic first-seen retention logic

**Testing & Verification:**
- Added near-duplicate regression test in `tests/test_aggregator.py`
- Full suite result: **26 passed**
- Live VN sanity check confirmed output titles are unique after dedupe pass

**Status**: ✅ Stronger duplicate prevention active for exact and near-duplicate titles

#### Session 7: API Return Format Migration (COMPLETED ✓)

**Goal:** Return a consumer-friendly list of dictionaries rather than internal model object.

**Code Changes:**
- Updated `get_news_by_country()` in `src/tidebreak/aggregator.py` to return `list[dict]`
- Added output formatter with keys:
  - `ID`
  - `Title`
  - `URL`
  - `Source Name`
  - `Summary`
- Derived `Source Name` from article/source host (e.g., `e.vnexpress.net`)
- Preserved existing VN quality filters and dedupe logic

**Testing & Verification:**
- Updated `tests/test_aggregator.py` expectations for new payload shape
- Full suite result: **26 passed**
- Live check confirms returned value is `list` of dicts with required keys

**Status**: ✅ API now returns standardized list-of-dictionaries output

#### Session 8: Shared Serializer Standardization (COMPLETED ✓)

**Goal:** Centralize output shaping so all countries and flows use one serializer.

**Code Changes:**
- Added `src/tidebreak/serializers.py` with:
  - `source_name_from_url(...)`
  - `serialize_article(...)`
  - `serialize_articles(...)`
- Refactored `src/tidebreak/aggregator.py` to use shared serializer instead of inline formatting
- Added serializer-specific unit tests in `tests/test_serializers.py`

**Testing & Verification:**
- Full suite result: **29 passed**
- Live sanity run confirms API still returns `list[dict]` with required keys

**Status**: ✅ Serializer now provides a single standardized output path for all countries

#### Session 9: Thailand Support (COMPLETED ✓)

**Goal:** Add Thailand country support with English-language news sources and parser flow.

**Source Selection (English):**
- `https://bangkokpost.com/`
- `https://nationthailand.com/`
- `https://khaosodenglish.com/`
- `https://thaipbsworld.com/`
- `https://thethaiger.com/`

**Code Changes:**
- Added `TH` mapping in `src/tidebreak/country_mappings.py`
- Extended `src/tidebreak/fetchers.py` with:
  - Thailand domain allowlist and dispatch hook
  - Thailand HTML parser and scoring heuristics
  - Thailand positive/negative URL token sets for quality filtering

**Testing & Verification:**
- Added tests in `tests/test_country_mappings.py` for TH source mapping
- Added tests in `tests/test_fetchers.py` for TH HTML extraction and filtering
- Full suite result: **32 passed**
- Live `TH` run returned serialized article dictionaries; some sources can still fail at runtime due to site-level restrictions/template variance (handled gracefully)

**Status**: ✅ Thailand support added with resilient fallback behavior

#### Session 10: Thailand Reliability + Live Tests (COMPLETED ✓)

**Goal:** Increase real-world pull success and add explicit live checks.

**Code Changes:**
- Updated TH source list in `src/tidebreak/country_mappings.py` toward higher-success English endpoints:
  - `https://www.nationthailand.com/`
  - `https://www.nationthailand.com/news`
  - `https://world.thaipbs.or.th/feed/`
  - `https://thethaiger.com/feed/`
  - `https://www.pattayamail.com/feed/`
- Extended Thailand domain allowlist in `src/tidebreak/fetchers.py` for relevant hosts
- Added optional live integration test file: `tests/test_live_sources.py`
- Added README command for live test execution via env flag

**Testing & Verification:**
- Full local suite (default): **32 passed, 2 skipped**
- Live suite (`TIDEBREAK_RUN_LIVE_TESTS=1`): **2 passed** (`VN`, `TH`)

**Status**: ✅ Live pull checks now exist and pass for VN/TH in current environment

#### Session 11: Thailand English + No-HTML Enforcement (COMPLETED ✓)

**Goal:** Ensure TH output is English-only and contains no raw HTML snippets.

**Code Changes:**
- Updated TH source list in `src/tidebreak/country_mappings.py` to remove lower-quality source and keep English-focused endpoints
- Added TH post-parse content rules in `src/tidebreak/fetchers.py`:
  - HTML stripping for titles/summaries
  - English-likeness check
  - Cyrillic/Thai script rejection
- Applied TH filtering for both RSS and HTML dispatch paths

**Testing & Verification:**
- Added TH RSS regression test to ensure non-English entries are filtered and HTML tags are removed
- Tightened live TH test assertions to reject HTML and forbidden scripts
- Full suite result: **33 passed, 2 skipped**
- Live strict TH test result: **1 passed**

**Status**: ✅ TH output now enforced as plain-text English-like data

#### Session 12: Flask API Service + Dockerization (COMPLETED ✓)

**Goal:** Build a separate Flask app in-repo that uses `tidebreak` as wheel dependency and runs with Gunicorn, Redis, and SQLite.

**Scaffold Created:**
- `apps/flask_api/app/__init__.py` (app factory)
- `apps/flask_api/app/routes.py` (`GET /api/v1/articles/<country_code>`)
- `apps/flask_api/app/cache.py` (Redis cache wrapper)
- `apps/flask_api/app/storage.py` (SQLite request logs)
- `apps/flask_api/app/config.py` (runtime config)
- `apps/flask_api/wsgi.py` (Gunicorn entrypoint)
- `apps/flask_api/gunicorn.conf.py`
- `apps/flask_api/requirements.txt`
- `apps/flask_api/tests/test_api.py`
- `apps/flask_api/README.md`
- Root `docker-compose.yml` (`api` + `redis`)

**Dependency Strategy:**
- Built fresh wheel: `dist/tidebreak-0.1.0-py3-none-any.whl`
- Docker image installs `tidebreak` from the local wheel file

**Docker/Runtime Verification:**
- Compose build and startup succeeded after resolving host-port conflicts (mapped API host port to `8001`)
- Smoke tested endpoints:
  - `GET /health` -> `{"status":"ok"}`
  - `GET /api/v1/articles/VN` -> JSON array of real article objects
  - `GET /api/v1/articles/TH` -> JSON array of real article objects
- Stack shutdown verified with `docker compose down`

**Tests Run:**
- Flask app tests: **2 passed** (`apps/flask_api/tests/test_api.py`)
- Existing suite still green: **33 passed, 2 skipped**

**Status**: ✅ Separate Flask API stack scaffolded, dockerized, and locally validated

#### Session 13: Duplicate Regression Fix for VN Paraphrase Pair (COMPLETED ✓)

**Goal:** Prevent very close duplicate stories with slightly different wording from passing dedupe.

**Code Changes:**
- Updated `_is_near_duplicate_title(...)` in `src/tidebreak/aggregator.py`
- Added lead-token + token-overlap heuristic for syndicated paraphrase detection

**Regression Coverage:**
- Added test in `tests/test_aggregator.py` using reported pair:
  - "Vietnam requests US to deliver objective, balanced assessment of IP protection efforts"
  - "Vietnam requests US to make objective assessment of IP rights protection efforts"

**Verification:**
- Aggregator tests: **7 passed**
- Full suite: **34 passed, 2 skipped**
- Direct function check for reported pair now returns `True` for near-duplicate matching

**Status**: ✅ Reported duplicate leakage case resolved

## Completed Features

- [x] Wheel distribution packaging
- [x] Country code to news source mapping
- [x] RSS feed fetching with retries
- [x] Article parsing and extraction
- [x] Structured result objects
- [x] Comprehensive error handling
- [x] Comprehensive test suite
- [x] API documentation
- [x] Example usage

## Next Steps (Future Enhancements)

- [ ] Add more news sources for each country
- [ ] Implement caching layer (Redis/file-based)
- [ ] Add configurable source limit
- [ ] Support for filtering by topic/keywords
- [ ] Rate limiting/throttling
- [ ] CLI tool for command-line usage
- [ ] Publish to PyPI
- [ ] Add GitHub Actions CI/CD
- [ ] Create async version for high-volume usage

