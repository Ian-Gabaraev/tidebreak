"""
Tests for the country_mappings module.
"""

import pytest

from tidebreak.country_mappings import (
    get_country_name,
    get_news_sources,
    is_valid_country_code,
    get_all_supported_countries,
)


def test_get_country_name_valid():
    """Test getting country name with valid code."""
    assert get_country_name("US") == "United States"
    assert get_country_name("GB") == "United Kingdom"
    assert get_country_name("FR") == "France"


def test_get_country_name_invalid():
    """Test getting country name with invalid code."""
    with pytest.raises(ValueError):
        get_country_name("XX")


def test_get_news_sources_valid():
    """Test getting news sources for valid country."""
    sources = get_news_sources("US")
    assert isinstance(sources, list)
    assert len(sources) > 0


def test_get_news_sources_vietnam():
    """Test Vietnam has the configured 5 source URLs."""
    sources = get_news_sources("VN")
    assert len(sources) == 5
    assert "https://vietnamnews.vn/" in sources
    assert "https://en.baodanang.vn/" in sources
    assert "https://e.vnexpress.net/" in sources
    assert "https://news.tuoitre.vn/vietnam-news.htm" in sources
    assert "https://en.vietnamplus.vn/" in sources


def test_get_news_sources_thailand():
    """Test Thailand has the configured 5 source URLs."""
    sources = get_news_sources("TH")
    assert len(sources) == 5
    assert "https://www.nationthailand.com/" in sources
    assert "https://www.nationthailand.com/thailand" in sources
    assert "https://world.thaipbs.or.th/feed/" in sources
    assert "https://thethaiger.com/feed/" in sources
    assert "https://khaosodenglish.com/feed/" in sources


def test_get_news_sources_no_sources():
    """Test getting news sources for country with no configured sources."""
    # Use a country that exists but has no sources
    sources = get_news_sources("AO")  # Angola
    assert isinstance(sources, list)
    assert len(sources) == 0


def test_get_news_sources_invalid():
    """Test getting news sources with invalid code."""
    with pytest.raises(ValueError):
        get_news_sources("XX")


def test_is_valid_country_code():
    """Test validating country codes."""
    assert is_valid_country_code("US") is True
    assert is_valid_country_code("GB") is True
    assert is_valid_country_code("XX") is False
    assert is_valid_country_code("") is False


def test_get_all_supported_countries():
    """Test getting all supported countries."""
    countries = get_all_supported_countries()

    assert isinstance(countries, dict)
    assert "US" in countries
    assert "GB" in countries
    assert len(countries) > 50  # Should have many countries
