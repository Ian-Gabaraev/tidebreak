"""Optional live integration tests against real upstream sources.

These tests are skipped unless TIDEBREAK_RUN_LIVE_TESTS=1 is set.

Run all countries:
    TIDEBREAK_RUN_LIVE_TESTS=1 python -m pytest tests/test_live_sources.py -v

Run a single country:
    TIDEBREAK_RUN_LIVE_TESTS=1 python -m pytest tests/test_live_sources.py -v -k "US"
"""

import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest

from tidebreak import get_news_by_country
from tidebreak.country_mappings import get_all_supported_countries

_LIVE = os.getenv("TIDEBREAK_RUN_LIVE_TESTS", "0") == "1"

# All supported country codes with human-readable test IDs
_ALL_COUNTRIES = sorted(get_all_supported_countries().items())


def _assert_serialized_item_shape(item: dict) -> None:
    """Verify a single serialized article has the expected schema."""
    assert set(item.keys()) == {"ID", "Title", "URL", "Source Name", "Summary"}
    assert isinstance(item["ID"], str) and item["ID"]
    assert isinstance(item["Title"], str) and item["Title"]
    assert isinstance(item["URL"], str) and item["URL"].startswith("http")
    assert isinstance(item["Source Name"], str) and item["Source Name"]


def _fetch_country(code: str) -> tuple[str, list[dict] | None, str | None]:
    """Fetch articles for a country, returning (code, articles, error)."""
    try:
        items = get_news_by_country(code, timeout=15)
        return (code, items, None)
    except Exception as e:
        return (code, None, str(e))


# ── Threaded all-countries live test ──────────────────────────────────────────


@pytest.mark.skipif(not _LIVE, reason="Set TIDEBREAK_RUN_LIVE_TESTS=1 to run live tests")
def test_live_all_countries_return_articles():
    """Every supported country must return at least one well-formed article (threaded)."""
    results: dict[str, tuple[list[dict] | None, str | None]] = {}

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(_fetch_country, code): (code, name) for code, name in _ALL_COUNTRIES
        }
        for future in as_completed(futures):
            code, items, error = future.result()
            results[code] = (items, error)

    failures = []
    for code, name in _ALL_COUNTRIES:
        items, error = results[code]
        if error:
            failures.append(f"{code} ({name}): raised {error[:100]}")
            continue
        if not items:
            failures.append(f"{code} ({name}): returned 0 articles")
            continue
        for item in items:
            _assert_serialized_item_shape(item)

    if failures:
        msg = f"{len(failures)}/{len(_ALL_COUNTRIES)} countries failed:\n" + "\n".join(failures)
        pytest.fail(msg)


# ── Per-country parametrized live test (optional, for targeted debugging) ─────


@pytest.mark.skipif(not _LIVE, reason="Set TIDEBREAK_RUN_LIVE_TESTS=1 to run live tests")
@pytest.mark.parametrize(
    "country_code,country_name",
    _ALL_COUNTRIES,
    ids=[f"{code}-{name}" for code, name in _ALL_COUNTRIES],
)
def test_live_country_returns_articles(country_code: str, country_name: str):
    """Each supported country must return at least one well-formed article."""
    items = get_news_by_country(country_code, timeout=15)

    assert isinstance(items, list), f"{country_code} ({country_name}) did not return a list"
    assert len(items) >= 1, (
        f"{country_code} ({country_name}) returned 0 articles — "
        "all configured sources may be unreachable"
    )

    for item in items:
        _assert_serialized_item_shape(item)


# ── Thailand-specific content quality checks ──────────────────────────────────


@pytest.mark.skipif(not _LIVE, reason="Set TIDEBREAK_RUN_LIVE_TESTS=1 to run live tests")
def test_live_thailand_no_non_latin_script():
    """Thailand articles must be English-only (no Thai/Cyrillic script)."""
    items = get_news_by_country("TH", timeout=15)

    assert len(items) >= 1
    for item in items:
        _assert_serialized_item_shape(item)
        text = f"{item['Title']} {item['Summary'] or ''}"
        assert "<" not in text and ">" not in text, f"HTML tags in TH article: {text[:120]}"
        assert not re.search(
            r"[\u0400-\u04FF\u0E00-\u0E7F]", text
        ), f"Non-Latin script in TH article: {text[:120]}"
