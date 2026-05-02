"""
Tests for the models module.
"""

from datetime import datetime
from tidebreak.models import Article, CountryAggregationResult


def test_article_creation():
    """Test creating an Article."""
    article = Article(
        title="Test Article",
        link="https://example.com/test",
        summary="Test summary",
        source="https://example.com/feed",
    )
    
    assert article.title == "Test Article"
    assert article.link == "https://example.com/test"
    assert article.summary == "Test summary"


def test_article_to_dict():
    """Test converting Article to dictionary."""
    article = Article(
        title="Test",
        link="https://example.com",
        summary="Summary",
    )
    
    article_dict = article.to_dict()
    
    assert isinstance(article_dict, dict)
    assert article_dict["title"] == "Test"
    assert article_dict["link"] == "https://example.com"


def test_country_aggregation_result_creation():
    """Test creating CountryAggregationResult."""
    articles = [
        Article(title="Article 1", link="https://example.com/1", summary="Summary 1"),
        Article(title="Article 2", link="https://example.com/2", summary="Summary 2"),
    ]
    
    result = CountryAggregationResult(
        country_code="US",
        country_name="United States",
        articles=articles,
        sources_queried=5,
        sources_successful=3,
    )
    
    assert result.country_code == "US"
    assert len(result.articles) == 2
    assert result.sources_queried == 5
    assert result.sources_successful == 3


def test_country_aggregation_result_to_dict():
    """Test converting CountryAggregationResult to dictionary."""
    articles = [
        Article(title="Article 1", link="https://example.com/1", summary="Summary 1"),
    ]
    
    result = CountryAggregationResult(
        country_code="US",
        country_name="United States",
        articles=articles,
    )
    
    result_dict = result.to_dict()
    
    assert isinstance(result_dict, dict)
    assert result_dict["country_code"] == "US"
    assert len(result_dict["articles"]) == 1
    assert isinstance(result_dict["timestamp"], str)

