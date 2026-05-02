"""
Main news aggregator module.
"""

import logging
import random
import re
from difflib import SequenceMatcher

from tidebreak.country_mappings import (
    get_country_name,
    get_news_sources,
    is_valid_country_code,
)
from tidebreak.fetchers import create_session_with_retries, fetch_articles_from_source
from tidebreak.models import Article
from tidebreak.serializers import serialize_articles
from tidebreak.exceptions import InvalidCountryError, FetchError

logger = logging.getLogger(__name__)


def _normalize_for_dedupe(value: str) -> str:
    """Normalize text so syndicated copies can be matched reliably."""
    lowered = value.lower().strip()
    without_punctuation = re.sub(r"[^\w\s]", " ", lowered)
    return " ".join(without_punctuation.split())


def _title_token_set(value: str) -> set[str]:
    """Extract comparable title tokens while dropping tiny/common glue words."""
    stopwords = {
        "a",
        "an",
        "and",
        "at",
        "by",
        "for",
        "from",
        "in",
        "of",
        "on",
        "the",
        "to",
        "with",
    }
    tokens = [token for token in _normalize_for_dedupe(value).split() if len(token) >= 3]
    return {token for token in tokens if token not in stopwords}


def _is_near_duplicate_title(left_title: str, right_title: str) -> bool:
    left = _normalize_for_dedupe(left_title)
    right = _normalize_for_dedupe(right_title)

    if not left or not right:
        return False
    if left == right:
        return True

    left_tokens = _title_token_set(left)
    right_tokens = _title_token_set(right)
    if left_tokens and right_tokens:
        overlap = len(left_tokens & right_tokens)
        min_size = min(len(left_tokens), len(right_tokens))
        union_size = len(left_tokens | right_tokens)
        overlap_ratio = overlap / min_size
        jaccard = overlap / union_size
        if overlap_ratio >= 0.9 and jaccard >= 0.72:
            return True

    return SequenceMatcher(None, left, right).ratio() >= 0.93


def _article_dedupe_key(article) -> str:
    title_key = _normalize_for_dedupe(article.title)
    if title_key:
        return f"title:{title_key}"

    link_key = _normalize_for_dedupe(article.link)
    return f"link:{link_key}"


def _dedupe_articles(articles):
    seen: set[str] = set()
    deduped = []
    kept_titles: list[str] = []

    for article in articles:
        key = _article_dedupe_key(article)
        if key in seen:
            continue

        normalized_title = _normalize_for_dedupe(article.title)
        if normalized_title and any(
            _is_near_duplicate_title(normalized_title, existing_title)
            for existing_title in kept_titles
        ):
            continue

        seen.add(key)
        deduped.append(article)
        if normalized_title:
            kept_titles.append(normalized_title)

    return deduped


def get_news_by_country(
    country_code: str,
    num_sources: int = 5,
    articles_per_source: int = 1,
    timeout: int = 10,
) -> list[dict[str, str | None]]:
    """
    Get news articles for a specific country.
    
    This function:
    1. Validates the country code
    2. Retrieves available news sources for that country
    3. Randomly selects the specified number of sources
    4. Fetches and parses articles from those sources
    5. Returns structured article data
    
    Args:
        country_code: ISO 3166-1 Alpha-2 country code (e.g., 'US', 'GB')
        num_sources: Number of news sources to query (default: 5)
        articles_per_source: Articles to extract per source (default: 1, up to 5 max)
        timeout: Request timeout in seconds (default: 10)
        
    Returns:
        List of dictionaries with: ID, Title, URL, Source Name, Summary
        
    Raises:
        InvalidCountryError: If country code is not valid
    """
    # Validate country code
    if not is_valid_country_code(country_code):
        raise InvalidCountryError(f"Invalid country code: {country_code}")
    
    country_name = get_country_name(country_code)
    logger.info(f"Fetching news for {country_name} ({country_code})")
    
    # Get available news sources for this country
    available_sources = get_news_sources(country_code)
    
    if not available_sources:
        logger.warning(f"No news sources configured for {country_code}")
        return []
    
    # Randomly select sources
    sources_to_query = random.sample(
        available_sources,
        min(num_sources, len(available_sources)),
    )
    
    logger.info(f"Selected {len(sources_to_query)} sources for {country_code}")
    
    collected_articles: list[Article] = []
    sources_successful = 0
    
    # Create session for reuse
    session = create_session_with_retries(timeout=timeout)
    
    # Fetch articles from each source
    for source_url in sources_to_query:
        try:
            logger.debug(f"Fetching from {source_url}")
            articles = fetch_articles_from_source(source_url, timeout=timeout, session=session)
            collected_articles.extend(articles[:articles_per_source])
            sources_successful += 1
            
        except FetchError as e:
            logger.warning(f"Failed to fetch from {source_url}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error fetching from {source_url}: {e}")
    
    # Drop syndicated duplicates before enforcing final max size.
    deduped_articles = _dedupe_articles(collected_articles)
    deduped_articles = deduped_articles[:5]
    
    logger.info(
        f"Successfully retrieved {len(deduped_articles)} articles "
        f"from {sources_successful}/{len(sources_to_query)} sources"
    )

    return serialize_articles(articles=deduped_articles, country_code=country_code)


