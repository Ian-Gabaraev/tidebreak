"""HTTP fetcher and source parsers for news sources."""

import logging
import re
from html import unescape
from typing import Optional
from urllib.parse import urljoin, urlparse

import feedparser
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from tidebreak.exceptions import FetchError, ParseError
from tidebreak.models import Article

logger = logging.getLogger(__name__)

# Default timeout for HTTP requests (seconds)
DEFAULT_TIMEOUT = 10

# Default User-Agent to be a good web citizen
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

_VIETNAM_HTML_DOMAINS = {
    "vietnamnews.vn",
    "en.baodanang.vn",
    "e.vnexpress.net",
    "news.tuoitre.vn",
    "en.vietnamplus.vn",
}

_ALJAZEERA_WHERE_PREFIX = "https://www.aljazeera.com/where/"

_THAILAND_HTML_DOMAINS = {
    "bangkokpost.com",
    "nationthailand.com",
    "khaosodenglish.com",
    "thaipbsworld.com",
    "world.thaipbs.or.th",
    "thethaiger.com",
    "pattayamail.com",
}

_THAILAND_SOURCE_HOSTS = {
    "nationthailand.com",
    "world.thaipbs.or.th",
    "thethaiger.com",
    "khaosodenglish.com",
}

_VIETNAM_NEGATIVE_URL_TOKENS = {
    "/topic",
    "/tag",
    "/tags",
    "/category",
    "/categories",
    "/video",
    "/videos",
    "/photo",
    "/photos",
    "/gallery",
    "/multimedia",
    "/podcast",
    "/search",
    "/author",
    "/authors",
    "/contact",
    "/about",
    "/advertise",
    "/rss",
}

_VIETNAM_POSITIVE_URL_TOKENS = {
    "/news",
    "/vietnam",
    "/economy",
    "/business",
    "/world",
    "/society",
    "/politics",
    "/travel",
}

_THAILAND_NEGATIVE_URL_TOKENS = {
    "/topic",
    "/tag",
    "/tags",
    "/category",
    "/categories",
    "/video",
    "/videos",
    "/photo",
    "/photos",
    "/gallery",
    "/multimedia",
    "/podcast",
    "/search",
    "/author",
    "/authors",
    "/contact",
    "/about",
    "/advertise",
    "/rss",
}

_THAILAND_POSITIVE_URL_TOKENS = {
    "/thailand",
    "/bangkok",
    "/news",
    "/economy",
    "/business",
    "/politics",
    "/tourism",
    "/travel",
    "/world",
}


def create_session_with_retries(
    retries: int = 3,
    backoff_factor: float = 0.5,
    timeout: int = DEFAULT_TIMEOUT,
) -> requests.Session:
    """
    Create a requests session with automatic retries.

    Args:
        retries: Number of retries
        backoff_factor: Backoff factor for retries
        timeout: Request timeout in seconds

    Returns:
        Configured requests Session
    """
    session = requests.Session()

    retry_strategy = Retry(
        total=retries,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"],
        backoff_factor=backoff_factor,
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # Set default User-Agent
    session.headers.update({"User-Agent": DEFAULT_USER_AGENT})

    return session


def fetch_rss_feed(
    feed_url: str,
    timeout: int = DEFAULT_TIMEOUT,
    session: Optional[requests.Session] = None,
) -> list[Article]:
    """
    Fetch and parse an RSS feed.

    Args:
        feed_url: URL of the RSS feed
        timeout: Request timeout in seconds
        session: Optional requests Session (creates new if not provided)

    Returns:
        List of Article objects parsed from the feed

    Raises:
        FetchError: If there's an error fetching the feed
        ParseError: If there's an error parsing the feed
    """
    if session is None:
        session = create_session_with_retries(timeout=timeout)

    try:
        logger.debug(f"Fetching RSS feed from {feed_url}")
        response = session.get(feed_url, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch feed {feed_url}: {e}")
        raise FetchError(f"Failed to fetch feed from {feed_url}") from e

    try:
        articles = _parse_rss_content(response.content, source_url=feed_url)
        logger.debug(f"Successfully parsed {len(articles)} RSS articles from {feed_url}")
        return articles

    except Exception as e:
        logger.error(f"Failed to parse feed {feed_url}: {e}")
        raise ParseError(f"Failed to parse feed from {feed_url}") from e


def fetch_articles_from_source(
    source_url: str,
    timeout: int = DEFAULT_TIMEOUT,
    session: Optional[requests.Session] = None,
) -> list[Article]:
    """Fetch and parse articles from either RSS sources or supported HTML pages."""
    if session is None:
        session = create_session_with_retries(timeout=timeout)

    try:
        logger.debug(f"Fetching source page from {source_url}")
        response = session.get(source_url, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch source {source_url}: {e}")
        raise FetchError(f"Failed to fetch feed from {source_url}") from e

    content_type = response.headers.get("Content-Type", "").lower()
    content = response.content

    try:
        articles: list[Article]
        if _looks_like_rss(content, content_type):
            articles = _parse_rss_content(content, source_url=source_url)
            if _is_thailand_source(source_url):
                articles = _apply_thailand_content_rules(articles)
            return articles

        if _is_vietnam_html_source(source_url):
            articles = _parse_vietnam_html_page(
                source_url=source_url,
                html_text=response.text,
                limit=5,
            )
            return articles

        if _is_aljazeera_where_source(source_url):
            articles = _parse_aljazeera_where_page(
                source_url=source_url,
                html_text=response.text,
                limit=5,
            )
            return articles

        if _is_thailand_html_source(source_url):
            articles = _parse_thailand_html_page(
                source_url=source_url,
                html_text=response.text,
                limit=5,
            )
            return _apply_thailand_content_rules(articles)

        rss_fallback = _parse_rss_content(content, source_url=source_url)
        if rss_fallback:
            if _is_thailand_source(source_url):
                return _apply_thailand_content_rules(rss_fallback)
            return rss_fallback

        raise ParseError(f"Unsupported non-RSS source: {source_url}")
    except ParseError:
        raise
    except Exception as e:
        raise ParseError(f"Failed to parse source {source_url}") from e


def _looks_like_rss(content: bytes, content_type: str) -> bool:
    if "xml" in content_type or "rss" in content_type or "atom" in content_type:
        return True

    prefix = content[:512].decode("utf-8", errors="ignore").lower()
    return "<rss" in prefix or "<feed" in prefix


def _parse_rss_content(content: bytes, source_url: str) -> list[Article]:
    feed = feedparser.parse(content)

    if feed.bozo and feed.bozo_exception:
        logger.warning(f"Feed parsing warning for {source_url}: {feed.bozo_exception}")

    articles: list[Article] = []
    for entry in feed.entries[:5]:
        raw_title = entry.get("title", "No title")
        raw_summary = entry.get("summary", entry.get("description", "No summary available"))

        title = _clean_html_text(raw_title) or "No title"
        summary = _clean_html_text(raw_summary) or "No summary available"

        articles.append(
            Article(
                title=title,
                link=entry.get("link", ""),
                summary=summary,
                source=source_url,
                published_date=None,
            )
        )
    return articles


def _is_vietnam_html_source(source_url: str) -> bool:
    host = urlparse(source_url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host in _VIETNAM_HTML_DOMAINS


def _is_thailand_html_source(source_url: str) -> bool:
    host = _normalize_host(source_url)
    return host in _THAILAND_HTML_DOMAINS


def _is_thailand_source(source_url: str) -> bool:
    return _normalize_host(source_url) in _THAILAND_SOURCE_HOSTS


def _parse_vietnam_html_page(source_url: str, html_text: str, limit: int = 5) -> list[Article]:
    # Keep parsing permissive because these sites may change templates frequently.
    anchor_pattern = re.compile(
        r"<a\s+[^>]*href=[\"'](?P<href>[^\"']+)[\"'][^>]*>(?P<title>.*?)</a>",
        re.IGNORECASE | re.DOTALL,
    )
    paragraph_pattern = re.compile(r"<p[^>]*>(?P<text>.*?)</p>", re.IGNORECASE | re.DOTALL)

    candidates: list[tuple[int, Article]] = []
    seen_links: set[str] = set()
    source_host = urlparse(source_url).netloc.lower()

    for match in anchor_pattern.finditer(html_text):
        href = (match.group("href") or "").strip()
        raw_title = match.group("title") or ""

        if not href or href.startswith(("#", "javascript:", "mailto:")):
            continue

        link = urljoin(source_url, href)
        parsed_link = urlparse(link)
        if parsed_link.scheme not in {"http", "https"}:
            continue
        link_host = parsed_link.netloc.lower()
        if not (link_host == source_host or link_host.endswith(f".{source_host}")):
            continue
        if link.rstrip("/") == source_url.rstrip("/"):
            continue

        title = _clean_html_text(raw_title)
        if len(title) < 20:
            continue

        if link in seen_links:
            continue

        next_anchor_idx = html_text.find("<a", match.end())
        scan_end = match.end() + 400
        if next_anchor_idx != -1:
            scan_end = min(scan_end, next_anchor_idx)

        scan_window = html_text[match.end() : scan_end]
        paragraph_match = paragraph_pattern.search(scan_window)
        summary = _clean_html_text(paragraph_match.group("text")) if paragraph_match else ""
        if not summary:
            summary = "No summary available"

        article = Article(
            title=title,
            link=link,
            summary=summary,
            source=source_url,
            published_date=None,
        )

        score = _score_vietnam_candidate(article=article, source_url=source_url)
        if score >= 2:
            candidates.append((score, article))
        seen_links.add(link)

    if not candidates:
        raise ParseError(f"Could not extract articles from {source_url}")

    candidates.sort(key=lambda pair: pair[0], reverse=True)
    best_articles = [article for _, article in candidates[:limit]]
    return best_articles


def _parse_thailand_html_page(source_url: str, html_text: str, limit: int = 5) -> list[Article]:
    anchor_pattern = re.compile(
        r"<a\s+[^>]*href=[\"'](?P<href>[^\"']+)[\"'][^>]*>(?P<title>.*?)</a>",
        re.IGNORECASE | re.DOTALL,
    )
    paragraph_pattern = re.compile(r"<p[^>]*>(?P<text>.*?)</p>", re.IGNORECASE | re.DOTALL)

    candidates: list[tuple[int, Article]] = []
    seen_links: set[str] = set()
    source_host = urlparse(source_url).netloc.lower()

    for match in anchor_pattern.finditer(html_text):
        href = (match.group("href") or "").strip()
        raw_title = match.group("title") or ""

        if not href or href.startswith(("#", "javascript:", "mailto:")):
            continue

        link = urljoin(source_url, href)
        parsed_link = urlparse(link)
        if parsed_link.scheme not in {"http", "https"}:
            continue
        link_host = parsed_link.netloc.lower()
        if not (link_host == source_host or link_host.endswith(f".{source_host}")):
            continue
        if link.rstrip("/") == source_url.rstrip("/"):
            continue

        title = _clean_html_text(raw_title)
        if len(title) < 20:
            continue

        if link in seen_links:
            continue

        next_anchor_idx = html_text.find("<a", match.end())
        scan_end = match.end() + 400
        if next_anchor_idx != -1:
            scan_end = min(scan_end, next_anchor_idx)

        scan_window = html_text[match.end() : scan_end]
        paragraph_match = paragraph_pattern.search(scan_window)
        summary = _clean_html_text(paragraph_match.group("text")) if paragraph_match else ""
        if not summary:
            summary = "No summary available"

        article = Article(
            title=title,
            link=link,
            summary=summary,
            source=source_url,
            published_date=None,
        )

        score = _score_thailand_candidate(article=article, source_url=source_url)
        if score >= 2:
            candidates.append((score, article))
        seen_links.add(link)

    if not candidates:
        raise ParseError(f"Could not extract articles from {source_url}")

    candidates.sort(key=lambda pair: pair[0], reverse=True)
    best_articles = [article for _, article in candidates[:limit]]
    return best_articles


def _score_vietnam_candidate(article: Article, source_url: str) -> int:
    score = 0
    parsed_link = urlparse(article.link)
    path = parsed_link.path.lower()
    title = article.title.lower()
    summary = article.summary

    if len(article.title) >= 35:
        score += 3
    elif len(article.title) >= 24:
        score += 1

    if summary != "No summary available":
        score += 2
        if len(summary) >= 80:
            score += 2

    if path.endswith((".htm", ".html")):
        score += 3

    if re.search(r"\d{4}", path):
        score += 2

    slash_count = path.count("/")
    if slash_count >= 2:
        score += 1

    for token in _VIETNAM_POSITIVE_URL_TOKENS:
        if token in path:
            score += 1

    for token in _VIETNAM_NEGATIVE_URL_TOKENS:
        if token in path:
            score -= 6

    if re.fullmatch(r"(home|latest news|video|photos?)", title):
        score -= 6

    source_host = urlparse(source_url).netloc.lower()
    link_host = parsed_link.netloc.lower()
    if link_host != source_host:
        score -= 8

    return score


def _score_thailand_candidate(article: Article, source_url: str) -> int:
    score = 0
    parsed_link = urlparse(article.link)
    path = parsed_link.path.lower()
    title = article.title.lower()
    summary = article.summary

    if len(article.title) >= 35:
        score += 3
    elif len(article.title) >= 24:
        score += 1

    if summary != "No summary available":
        score += 2
        if len(summary) >= 80:
            score += 2

    if path.endswith((".htm", ".html")):
        score += 3

    if re.search(r"\d{4}", path):
        score += 2

    slash_count = path.count("/")
    if slash_count >= 2:
        score += 1

    for token in _THAILAND_POSITIVE_URL_TOKENS:
        if token in path:
            score += 1

    for token in _THAILAND_NEGATIVE_URL_TOKENS:
        if token in path:
            score -= 6

    if re.fullmatch(r"(home|latest news|video|photos?)", title):
        score -= 6

    source_host = urlparse(source_url).netloc.lower()
    link_host = parsed_link.netloc.lower()
    if link_host != source_host:
        score -= 8

    return score


def _apply_thailand_content_rules(articles: list[Article]) -> list[Article]:
    filtered: list[Article] = []

    for article in articles:
        article.title = _clean_html_text(article.title)
        article.summary = _clean_html_text(article.summary)

        if not _is_english_like(article.title):
            continue

        if _contains_forbidden_script(article.title) or _contains_forbidden_script(article.summary):
            continue

        if not article.summary:
            article.summary = "No summary available"

        filtered.append(article)

    return filtered


def _contains_forbidden_script(value: str) -> bool:
    return bool(re.search(r"[\u0400-\u04FF\u0E00-\u0E7F]", value or ""))


def _is_english_like(value: str) -> bool:
    text = value or ""
    letters = re.findall(r"[A-Za-z]", text)
    all_alpha = re.findall(r"[A-Za-z\u0400-\u04FF\u0E00-\u0E7F]", text)
    if not all_alpha:
        return False

    ratio = len(letters) / len(all_alpha)
    return ratio >= 0.85


def _normalize_host(source_url: str) -> str:
    host = urlparse(source_url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def _is_aljazeera_where_source(source_url: str) -> bool:
    return source_url.startswith(_ALJAZEERA_WHERE_PREFIX)


def _parse_aljazeera_where_page(source_url: str, html_text: str, limit: int = 5) -> list[Article]:
    """Parse an Al Jazeera /where/<country>/ listing page for article links."""
    anchor_pattern = re.compile(
        r"<a\s+[^>]*href=[\"'](?P<href>/news/[^\"']+)[\"'][^>]*>(?P<title>.*?)</a>",
        re.IGNORECASE | re.DOTALL,
    )

    articles: list[Article] = []
    seen_links: set[str] = set()

    for match in anchor_pattern.finditer(html_text):
        href = match.group("href").strip()
        raw_title = match.group("title")

        link = urljoin("https://www.aljazeera.com", href)
        if link in seen_links:
            continue

        title = _clean_html_text(raw_title)
        if len(title) < 15:
            continue

        articles.append(
            Article(
                title=title,
                link=link,
                summary="No summary available",
                source=source_url,
                published_date=None,
            )
        )
        seen_links.add(link)

        if len(articles) >= limit:
            break

    if not articles:
        raise ParseError(f"Could not extract articles from {source_url}")

    return articles


def _clean_html_text(value: str) -> str:
    no_tags = re.sub(r"<[^>]+>", " ", value)
    normalized = re.sub(r"\s+", " ", unescape(no_tags)).strip()
    return normalized
