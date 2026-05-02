"""
Data models for the Tidebreak news aggregation package.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Article:
    """Represents a single news article."""

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
    """Result of news aggregation for a country."""

    country_code: str
    country_name: str
    articles: list[Article] = field(default_factory=list)
    sources_queried: int = 0
    sources_successful: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert result to dictionary with articles serialized."""
        data = asdict(self)
        data["articles"] = [article.to_dict() for article in self.articles]
        data["timestamp"] = self.timestamp.isoformat()
        return data
