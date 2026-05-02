"""API routes for article retrieval by country code."""

import re

from flask import Blueprint, current_app, jsonify
from tidebreak import get_news_by_country

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

_COUNTRY_CODE_RE = re.compile(r"^[A-Z]{2}$")


@api_bp.get("/articles/<country_code>")
def get_articles(country_code: str):
    normalized_code = country_code.upper().strip()
    if not _COUNTRY_CODE_RE.fullmatch(normalized_code):
        return (
            jsonify({"error": "Invalid country code. Use ISO-3166 alpha-2 format, e.g. VN."}),
            400,
        )

    cache = current_app.extensions["cache"]
    storage = current_app.extensions["storage"]

    cache_key = f"articles:{normalized_code}"
    cached = cache.get_json(cache_key)
    if cached is not None:
        storage.log_request(normalized_code, len(cached), from_cache=True)
        return jsonify(cached), 200

    articles = get_news_by_country(normalized_code)

    # Backward compatibility for older tidebreak versions that may return model objects.
    if hasattr(articles, "articles"):
        articles = [
            {
                "id": f"{normalized_code}-{idx}",
                "title": item.title,
                "url": item.link,
                "sourceName": item.source or "unknown",
                "summary": item.summary,
            }
            for idx, item in enumerate(articles.articles, start=1)
        ]

    cache.set_json(cache_key, articles)
    storage.log_request(normalized_code, len(articles), from_cache=False)

    return jsonify(articles), 200
