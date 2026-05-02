"""Optional live integration tests against real upstream sources.

These tests are skipped unless TIDEBREAK_RUN_LIVE_TESTS=1 is set.
"""

import os

import pytest

from tidebreak import get_news_by_country


def _live_tests_enabled() -> bool:
    return os.getenv("TIDEBREAK_RUN_LIVE_TESTS", "0") == "1"


def _assert_serialized_item_shape(item: dict) -> None:
    assert set(item.keys()) == {"ID", "Title", "URL", "Source Name", "Summary"}
    assert isinstance(item["ID"], str) and item["ID"]
    assert isinstance(item["Title"], str) and item["Title"]
    assert isinstance(item["URL"], str) and item["URL"].startswith("http")
    assert isinstance(item["Source Name"], str) and item["Source Name"]


@pytest.mark.skipif(not _live_tests_enabled(), reason="Set TIDEBREAK_RUN_LIVE_TESTS=1 to run live tests")
def test_live_vietnam_returns_articles():
    items = get_news_by_country("VN")

    assert isinstance(items, list)
    assert len(items) >= 1
    _assert_serialized_item_shape(items[0])


@pytest.mark.skipif(not _live_tests_enabled(), reason="Set TIDEBREAK_RUN_LIVE_TESTS=1 to run live tests")
def test_live_thailand_returns_articles():
    items = get_news_by_country("TH")

    assert isinstance(items, list)
    assert len(items) >= 1
    _assert_serialized_item_shape(items[0])

