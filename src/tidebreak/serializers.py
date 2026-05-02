"""Serialization helpers for Tidebreak public output."""

from urllib.parse import urlparse

from tidebreak.models import Article


def source_name_from_url(url: str) -> str:
    """Extract normalized source hostname from URL."""
    host = urlparse(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host or "unknown"


def serialize_article(article: Article, country_code: str, index: int) -> dict[str, str | None]:
    """Serialize one article into the standard API payload shape."""
    return {
        "ID": f"{country_code}-{index}",
        "Title": article.title,
        "URL": article.link,
        "Source Name": source_name_from_url(article.source or article.link),
        "Summary": article.summary if article.summary != "No summary available" else None,
    }


def serialize_articles(articles: list[Article], country_code: str) -> list[dict[str, str | None]]:
    """Serialize a list of articles into the standard API payload shape."""
    return [
        serialize_article(article=article, country_code=country_code, index=index)
        for index, article in enumerate(articles, start=1)
    ]

