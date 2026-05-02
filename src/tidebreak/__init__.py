"""
Tidebreak - News aggregation by country code.

A Python package that accepts a country code, fetches news from relevant sources,
and returns structured article data.
"""

__version__ = "0.1.0"
__author__ = "Ian Gabaraev"
__license__ = "MIT"

from tidebreak.aggregator import get_news_by_country
from tidebreak.models import Article, CountryAggregationResult

__all__ = [
    "get_news_by_country",
    "Article",
    "CountryAggregationResult",
]
