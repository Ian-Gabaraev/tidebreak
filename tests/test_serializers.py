"""Tests for serializer helpers."""

from tidebreak.models import Article
from tidebreak.serializers import serialize_article, serialize_articles, source_name_from_url


def test_source_name_from_url_normalizes_www():
    assert source_name_from_url("https://www.example.com/news") == "example.com"


def test_serialize_article_standard_keys_and_summary_none():
    article = Article(
        title="Test headline",
        link="https://news.example.com/story-1",
        summary="No summary available",
        source="https://www.news.example.com/",
    )

    payload = serialize_article(article=article, country_code="VN", index=1)

    assert payload == {
        "ID": "VN-1",
        "Title": "Test headline",
        "URL": "https://news.example.com/story-1",
        "Source Name": "news.example.com",
        "Summary": None,
    }


def test_serialize_articles_assigns_incrementing_ids():
    articles = [
        Article(title="A", link="https://a.example/1", summary="s1", source="https://a.example"),
        Article(title="B", link="https://b.example/1", summary="s2", source="https://b.example"),
    ]

    payload = serialize_articles(articles=articles, country_code="US")

    assert payload[0]["ID"] == "US-1"
    assert payload[1]["ID"] == "US-2"
    assert set(payload[0].keys()) == {"ID", "Title", "URL", "Source Name", "Summary"}
