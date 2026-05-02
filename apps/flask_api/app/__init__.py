"""Flask app factory for Tidebreak API service."""

from flask import Flask

from app.cache import CacheClient
from app.config import Config
from app.routes import api_bp
from app.storage import ORMStorage


def create_app(config: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    storage = ORMStorage(app.config["SQLITE_PATH"])
    storage.init_db()
    storage.seed_country_sources()

    cache = CacheClient(
        redis_url=app.config["REDIS_URL"],
        default_ttl=app.config["CACHE_TTL_SECONDS"],
    )

    app.extensions["storage"] = storage
    app.extensions["cache"] = cache

    app.register_blueprint(api_bp)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
