"""Tests for ORM storage layer."""

from pathlib import Path

from app.storage import ORMStorage, RequestLog


def test_orm_storage_creates_table_and_inserts_row(tmp_path: Path):
    db_path = tmp_path / "api_test.db"
    storage = ORMStorage(str(db_path))
    storage.init_db()

    storage.log_request(country_code="VN", article_count=4, from_cache=False)

    with storage.session_factory() as session:
        rows = session.query(RequestLog).all()

    assert len(rows) == 1
    row = rows[0]
    assert row.country_code == "VN"
    assert row.article_count == 4
    assert row.from_cache is False
    assert row.created_at is not None


def test_orm_storage_seeds_country_sources(tmp_path: Path):
    db_path = tmp_path / "api_test.db"
    storage = ORMStorage(str(db_path))
    storage.init_db()
    storage.seed_country_sources()

    vn_sources = storage.get_country_sources("VN")
    th_sources = storage.get_country_sources("TH")

    assert len(vn_sources) >= 1
    assert len(th_sources) >= 1


def test_orm_storage_article_backup_roundtrip(tmp_path: Path):
    db_path = tmp_path / "api_test.db"
    storage = ORMStorage(str(db_path))
    storage.init_db()

    payload = [
        {
            "ID": "VN-1",
            "Title": "Example title",
            "URL": "https://example.com/story",
            "Source Name": "example.com",
            "Summary": "Example summary",
        }
    ]

    storage.store_article_backup("VN", payload)
    restored = storage.get_article_backup("VN")

    assert restored == payload


