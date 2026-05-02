"""Smoke tests for Flask API endpoints."""

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
