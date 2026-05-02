"""
Tests for the aggregator module.
"""

import pytest
from unittest.mock import patch

from tidebreak.aggregator import get_news_by_country
from tidebreak.exceptions import InvalidCountryError
from tidebreak.models import Article


def test_get_news_by_country_valid_code():
    """Test getting news with a valid country code."""
    with patch("tidebreak.aggregator.fetch_articles_from_source") as mock_fetch:
        # Mock articles from feeds
        mock_fetch.return_value = [
            Article(
                title="Test Article 1",
                link="https://example.com/1",
                summary="Summary 1",
                source="https://example.com/feed",
            )
        ]
        
        result = get_news_by_country("US")
        
        assert isinstance(result, list)
        assert len(result) >= 1
        assert set(result[0].keys()) == {"ID", "Title", "URL", "Source Name", "Summary"}
        assert result[0]["Title"] == "Test Article 1"


def test_get_news_by_country_invalid_code():
    """Test that invalid country code raises InvalidCountryError."""
    with pytest.raises(InvalidCountryError):
        get_news_by_country("XX")


def test_get_news_by_country_no_sources():
    """Test country with no configured news sources."""
    # This would be for a country in the mapping but with no sources
    result = get_news_by_country("ET")  # Ethiopia has no sources configured
    
    assert result == []


def test_get_news_by_country_fetch_error():
    """Test handling of fetch errors."""
    with patch("tidebreak.aggregator.fetch_articles_from_source") as mock_fetch:
        from tidebreak.exceptions import FetchError
        
        mock_fetch.side_effect = FetchError("Network error")
        
        result = get_news_by_country("US")
        
        assert result == []


def test_get_news_by_country_deduplicates_same_story_across_sources():
    """Test syndicated duplicates from different sites are returned once."""
    source_a = "https://site-a.example/news"
    source_b = "https://site-b.example/news"

    with (
        patch("tidebreak.aggregator.random.sample", return_value=[source_a, source_b]),
        patch("tidebreak.aggregator.fetch_articles_from_source") as mock_fetch,
    ):
        mock_fetch.side_effect = [
            [
                Article(
                    title="Vietnamese PM hosts welcome ceremony for Japanese counterpart",
                    link="https://site-a.example/story-1",
                    summary="Story summary from source A.",
                    source=source_a,
                )
            ],
            [
                Article(
                    title="Vietnamese PM hosts welcome ceremony for Japanese counterpart",
                    link="https://site-b.example/story-2",
                    summary="Same story syndicated by source B.",
                    source=source_b,
                )
            ],
        ]

        result = get_news_by_country("VN", num_sources=2)

        assert len(result) == 1
        assert result[0]["URL"] == "https://site-a.example/story-1"


def test_get_news_by_country_deduplicates_near_duplicate_titles():
    """Test near-duplicate syndicated titles are collapsed into one result."""
    source_a = "https://site-a.example/news"
    source_b = "https://site-b.example/news"

    with (
        patch("tidebreak.aggregator.random.sample", return_value=[source_a, source_b]),
        patch("tidebreak.aggregator.fetch_articles_from_source") as mock_fetch,
    ):
        mock_fetch.side_effect = [
            [
                Article(
                    title="Vietnamese PM hosts welcome ceremony for Japanese counterpart",
                    link="https://site-a.example/story-1",
                    summary="Story summary from source A.",
                    source=source_a,
                )
            ],
            [
                Article(
                    title="Vietnamese PM hosts ceremony for Japanese counterpart",
                    link="https://site-b.example/story-2",
                    summary="Same story with slight title variation.",
                    source=source_b,
                )
            ],
        ]

        result = get_news_by_country("VN", num_sources=2)

        assert len(result) == 1
        assert result[0]["URL"] == "https://site-a.example/story-1"


