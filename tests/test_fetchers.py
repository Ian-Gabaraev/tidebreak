"""
Tests for the fetchers module.
"""

import pytest
import responses
from tidebreak.fetchers import (
    create_session_with_retries,
    fetch_articles_from_source,
    fetch_rss_feed,
)
from tidebreak.exceptions import FetchError, ParseError

SAMPLE_RSS_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>Test Feed</title>
        <link>https://example.com</link>
        <description>A test feed</description>
        <item>
            <title>Article 1</title>
            <link>https://example.com/article1</link>
            <description>Summary of article 1</description>
        </item>
        <item>
            <title>Article 2</title>
            <link>https://example.com/article2</link>
            <description>Summary of article 2</description>
        </item>
    </channel>
</rss>
"""

SAMPLE_VN_HTML = """
<html>
  <body>
    <article>
      <a href="/economy/vietnam-economy-expands-2026.html">Vietnam economy expands in early 2026 with stronger exports</a>
      <p>Growth is supported by rising manufacturing activity and stronger demand.</p>
    </article>
    <article>
      <a href="https://vietnamnews.vn/society/health-system-upgrades.html">Health system upgrades improve access in rural provinces</a>
      <p>New digital services help patients reach care more efficiently.</p>
    </article>
  </body>
</html>
"""

SAMPLE_VN_HTML_MIXED_QUALITY = """
<html>
  <body>
    <nav>
      <a href="/middle-east-conflict/topic-28712.html">Middle East conflict</a>
      <a href="/tag/economy">Economy Tag</a>
      <a href="/video">Video</a>
    </nav>
    <section>
      <a href="/vietnam/new-trade-corridor-opens-2026-260502.html">
        Vietnam opens new trade corridor to boost regional exports in 2026
      </a>
      <p>
        The new logistics route is expected to reduce shipping times and support
        manufacturing growth across major industrial provinces.
      </p>
    </section>
    <section>
      <a href="/business/renewable-investment-accelerates-2026-260503.html">
        Renewable investment accelerates as Vietnamese firms expand clean energy projects
      </a>
      <p>
        Analysts expect additional foreign direct investment in solar and grid infrastructure.
      </p>
    </section>
  </body>
</html>
"""

SAMPLE_TH_HTML = """
<html>
  <body>
    <article>
      <a href="/thailand/general/12345/bangkok-launches-new-flood-prevention-plan-for-rainy-season">Bangkok launches new flood prevention plan for rainy season</a>
      <p>Officials say drainage upgrades and emergency teams are being deployed citywide.</p>
    </article>
    <article>
      <a href="https://bangkokpost.com/business/67890/tourism-recovery-continues-with-strong-arrivals">Tourism recovery continues with strong arrivals and airline capacity growth</a>
      <p>Industry data points to steady demand from regional and long-haul markets.</p>
    </article>
  </body>
</html>
"""

SAMPLE_TH_HTML_MIXED_QUALITY = """
<html>
  <body>
    <nav>
      <a href="/topic/politics">Politics Topic</a>
      <a href="/tag/tourism">Tourism Tag</a>
      <a href="/video">Video</a>
    </nav>
    <section>
      <a href="/thailand/politics/98765/cabinet-approves-major-infrastructure-budget-for-2026">
        Cabinet approves major infrastructure budget package for 2026 projects
      </a>
      <p>
        The package prioritizes rail modernization, regional logistics and climate resilience.
      </p>
    </section>
  </body>
</html>
"""

SAMPLE_TH_RSS_MIXED_LANGUAGE = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>Thailand Feed</title>
        <item>
            <title>Thailand plans new digital visa process for international tourists</title>
            <link>https://thethaiger.com/news/national/digital-visa-process</link>
            <description><![CDATA[<p>The new <strong>digital</strong> process will reduce airport wait times.</p>]]></description>
        </item>
        <item>
            <title>Таиланд обсуждает новые правила туризма</title>
            <link>https://thethaiger.com/news/russian/non-english-item</link>
            <description><![CDATA[<p>Это статья не на английском языке.</p>]]></description>
        </item>
    </channel>
</rss>
"""


@responses.activate
def test_fetch_rss_feed_success():
    """Test successfully fetching and parsing an RSS feed."""
    responses.add(
        responses.GET,
        "https://example.com/feed.rss",
        body=SAMPLE_RSS_FEED,
        status=200,
    )

    articles = fetch_rss_feed("https://example.com/feed.rss")

    assert len(articles) == 2
    assert articles[0].title == "Article 1"
    assert articles[0].link == "https://example.com/article1"
    assert articles[1].title == "Article 2"


@responses.activate
def test_fetch_rss_feed_network_error():
    """Test handling of network errors."""
    responses.add(
        responses.GET,
        "https://example.com/feed.rss",
        status=500,
    )

    with pytest.raises(FetchError):
        fetch_rss_feed("https://example.com/feed.rss")


@responses.activate
def test_fetch_rss_feed_not_found():
    """Test handling of 404 errors."""
    responses.add(
        responses.GET,
        "https://example.com/feed.rss",
        status=404,
    )

    with pytest.raises(FetchError):
        fetch_rss_feed("https://example.com/feed.rss")


def test_create_session_with_retries():
    """Test creating a session with retries."""
    session = create_session_with_retries()

    assert session is not None
    assert "User-Agent" in session.headers


@responses.activate
def test_fetch_articles_from_source_rss():
    """Test dispatching to RSS parsing when content is RSS."""
    responses.add(
        responses.GET,
        "https://example.com/feed.rss",
        body=SAMPLE_RSS_FEED,
        status=200,
        content_type="application/rss+xml",
    )

    articles = fetch_articles_from_source("https://example.com/feed.rss")

    assert len(articles) == 2
    assert articles[0].title == "Article 1"


@responses.activate
def test_fetch_articles_from_source_vietnam_html():
    """Test parsing Vietnam HTML pages with article links and summaries."""
    responses.add(
        responses.GET,
        "https://vietnamnews.vn/",
        body=SAMPLE_VN_HTML,
        status=200,
        content_type="text/html",
    )

    articles = fetch_articles_from_source("https://vietnamnews.vn/")

    assert len(articles) == 2
    assert articles[0].title.startswith("Vietnam economy expands")
    assert articles[0].link == "https://vietnamnews.vn/economy/vietnam-economy-expands-2026.html"
    assert "Growth is supported" in articles[0].summary


@responses.activate
def test_fetch_articles_from_source_unsupported_html_raises_parse_error():
    """Test unsupported non-RSS/non-Vietnam HTML sources."""
    responses.add(
        responses.GET,
        "https://example.com/news",
        body="<html><body><h1>News</h1></body></html>",
        status=200,
        content_type="text/html",
    )

    with pytest.raises(ParseError):
        fetch_articles_from_source("https://example.com/news")


@responses.activate
def test_fetch_articles_from_source_vietnam_html_prefers_article_links():
    """Test that scoring prefers article-like links over topic/tag/video pages."""
    responses.add(
        responses.GET,
        "https://e.vnexpress.net/",
        body=SAMPLE_VN_HTML_MIXED_QUALITY,
        status=200,
        content_type="text/html",
    )

    articles = fetch_articles_from_source("https://e.vnexpress.net/")

    assert len(articles) == 2
    assert all("/topic" not in article.link for article in articles)
    assert all("/tag" not in article.link for article in articles)
    assert all("/video" not in article.link for article in articles)
    assert articles[0].title.startswith("Vietnam opens new trade corridor")


@responses.activate
def test_fetch_articles_from_source_thailand_html():
    """Test parsing Thailand HTML pages with article links and summaries."""
    responses.add(
        responses.GET,
        "https://bangkokpost.com/",
        body=SAMPLE_TH_HTML,
        status=200,
        content_type="text/html",
    )

    articles = fetch_articles_from_source("https://bangkokpost.com/")

    assert len(articles) == 2
    assert articles[0].title.startswith("Bangkok launches new flood prevention plan")
    assert "/thailand/general/12345" in articles[0].link
    assert "Officials say drainage upgrades" in articles[0].summary


@responses.activate
def test_fetch_articles_from_source_thailand_html_prefers_article_links():
    """Test Thailand scoring prefers article links over topic/tag/video pages."""
    responses.add(
        responses.GET,
        "https://nationthailand.com/",
        body=SAMPLE_TH_HTML_MIXED_QUALITY,
        status=200,
        content_type="text/html",
    )

    articles = fetch_articles_from_source("https://nationthailand.com/")

    assert len(articles) == 1
    assert all("/topic" not in article.link for article in articles)
    assert all("/tag" not in article.link for article in articles)
    assert all("/video" not in article.link for article in articles)
    assert articles[0].title.startswith("Cabinet approves major infrastructure budget")


@responses.activate
def test_fetch_articles_from_source_thailand_rss_filters_non_english_and_strips_html():
    """Test Thailand RSS output is English-only and plain text."""
    responses.add(
        responses.GET,
        "https://thethaiger.com/feed/",
        body=SAMPLE_TH_RSS_MIXED_LANGUAGE,
        status=200,
        content_type="application/rss+xml",
    )

    articles = fetch_articles_from_source("https://thethaiger.com/feed/")

    assert len(articles) == 1
    assert articles[0].title.startswith("Thailand plans new digital visa process")
    assert "<" not in articles[0].summary
    assert "strong" not in articles[0].summary.lower()
