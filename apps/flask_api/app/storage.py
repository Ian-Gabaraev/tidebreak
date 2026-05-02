"""SQLAlchemy ORM persistence for request logs, source mappings, and API backups."""

from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import Boolean, DateTime, Integer, String, create_engine, delete, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.pool import NullPool

from tidebreak.country_mappings import get_all_supported_countries, get_news_sources


class Base(DeclarativeBase):
    pass


class RequestLog(Base):
    __tablename__ = "request_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False, index=True)
    article_count: Mapped[int] = mapped_column(Integer, nullable=False)
    from_cache: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class CountrySourceMap(Base):
    __tablename__ = "country_source_map"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False, index=True)
    country_name: Mapped[str] = mapped_column(String(128), nullable=False)
    source_url: Mapped[str] = mapped_column(String(1024), nullable=False)


class ArticleBackup(Base):
    __tablename__ = "article_backup"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False, index=True)
    article_id: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(1024), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str | None] = mapped_column(String(4096), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ORMStorage:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        self.engine = create_engine(
            f"sqlite:///{self.db_path}",
            future=True,
            pool_pre_ping=True,
            poolclass=NullPool,
        )
        self.session_factory = sessionmaker(bind=self.engine, future=True)

    def init_db(self) -> None:
        Base.metadata.create_all(self.engine)

    def seed_country_sources(self) -> None:
        countries = get_all_supported_countries()

        with self.session_factory() as session:
            existing_codes = {
                row[0]
                for row in session.execute(select(CountrySourceMap.country_code).distinct()).all()
            }

            for code, name in countries.items():
                if code in existing_codes:
                    continue

                sources = get_news_sources(code)
                if not sources:
                    continue

                for source_url in sources:
                    session.add(
                        CountrySourceMap(
                            country_code=code,
                            country_name=name,
                            source_url=source_url,
                        )
                    )

            session.commit()

    def log_request(self, country_code: str, article_count: int, from_cache: bool) -> None:
        with self.session_factory() as session:
            session.add(
                RequestLog(
                    country_code=country_code,
                    article_count=article_count,
                    from_cache=from_cache,
                    created_at=datetime.now(timezone.utc),
                )
            )
            session.commit()

    def get_country_sources(self, country_code: str) -> list[str]:
        with self.session_factory() as session:
            rows = session.execute(
                select(CountrySourceMap.source_url).where(CountrySourceMap.country_code == country_code)
            ).all()
        return [row[0] for row in rows]

    def store_article_backup(self, country_code: str, articles: list[dict[str, str | None]]) -> None:
        with self.session_factory() as session:
            session.execute(
                delete(ArticleBackup).where(ArticleBackup.country_code == country_code)
            )

            for item in articles:
                session.add(
                    ArticleBackup(
                        country_code=country_code,
                        article_id=str(item.get("ID") or ""),
                        title=str(item.get("Title") or ""),
                        url=str(item.get("URL") or ""),
                        source_name=str(item.get("Source Name") or "unknown"),
                        summary=item.get("Summary"),
                        created_at=datetime.now(timezone.utc),
                    )
                )

            session.commit()

    def get_article_backup(self, country_code: str) -> list[dict[str, str | None]]:
        with self.session_factory() as session:
            rows = session.execute(
                select(ArticleBackup)
                .where(ArticleBackup.country_code == country_code)
                .order_by(ArticleBackup.id.asc())
            ).scalars().all()

        return [
            {
                "ID": row.article_id,
                "Title": row.title,
                "URL": row.url,
                "Source Name": row.source_name,
                "Summary": row.summary,
            }
            for row in rows
        ]

