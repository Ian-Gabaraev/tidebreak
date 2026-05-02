"""Smoke tests for Flask API endpoints."""

from unittest.mock import patch

from app import create_app


def test_health_endpoint():
    app = create_app()
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_articles_endpoint_bad_country_code():
    app = create_app()
    client = app.test_client()

    response = client.get("/api/v1/articles/XYZ")

    assert response.status_code == 400
    payload = response.get_json()
    assert "error" in payload


def test_articles_endpoint_uses_backup_when_fresh_fetch_empty():
    app = create_app()
    storage = app.extensions["storage"]
    storage.store_article_backup(
        "VN",
        [
            {
                "ID": "VN-1",
                "Title": "Backup headline",
                "URL": "https://backup.example/vn-1",
                "Source Name": "backup.example",
                "Summary": "Backup summary",
            }
        ],
    )

    client = app.test_client()

    with patch("app.routes.get_news_by_country", return_value=[]):
        response = client.get("/api/v1/articles/VN")

    assert response.status_code == 200
    payload = response.get_json()
    assert len(payload) == 1
    assert payload[0]["Title"] == "Backup headline"


def test_sources_endpoint_invalid_country_code():
    app = create_app()
    client = app.test_client()

    response = client.get("/api/v1/sources/XYZ")

    assert response.status_code == 400
    payload = response.get_json()
    assert "error" in payload
    assert "Invalid country code" in payload["error"]


def test_sources_endpoint_valid_country_with_sources():
    app = create_app()
    storage = app.extensions["storage"]

    # Seed some sources for VN
    storage.seed_country_sources()

    client = app.test_client()
    response = client.get("/api/v1/sources/VN")

    assert response.status_code == 200
    payload = response.get_json()
    assert "country_code" in payload
    assert payload["country_code"] == "VN"
    assert "sources" in payload
    assert isinstance(payload["sources"], list)
    # VN should have sources seeded
    assert len(payload["sources"]) > 0


def test_sources_endpoint_valid_country_no_sources():
    app = create_app()
    client = app.test_client()

    # Query a country that has no seeded sources
    response = client.get("/api/v1/sources/ZZ")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["country_code"] == "ZZ"
    assert payload["sources"] == []


def test_sources_endpoint_case_insensitive():
    app = create_app()
    storage = app.extensions["storage"]

    # Seed sources
    storage.seed_country_sources()

    client = app.test_client()

    # Test lowercase input normalization
    response_lower = client.get("/api/v1/sources/vn")
    response_upper = client.get("/api/v1/sources/VN")

    assert response_lower.status_code == 200
    assert response_upper.status_code == 200
    assert response_lower.get_json()["sources"] == response_upper.get_json()["sources"]
