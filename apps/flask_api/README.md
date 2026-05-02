# Tidebreak Flask API

A standalone Flask service that wraps `tidebreak` and exposes country-based article retrieval.

## API

- `GET /health`
- `GET /api/v1/articles/<country_code>`

Example:

```bash
curl http://localhost:8000/api/v1/articles/VN
```

Response is a JSON array of article objects with keys:
- `ID`
- `Title`
- `URL`
- `Source Name`
- `Summary`

## Local Run (without Docker)

From repository root:

```bash
cd /Users/iangabaraev/repos/tidebreak
source venv/bin/activate
python -m pip install -e .
python -m pip install -r apps/flask_api/requirements.txt
gunicorn -c apps/flask_api/gunicorn.conf.py --chdir apps/flask_api wsgi:app
```

Then:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/articles/TH
```

## Docker Run (Gunicorn + Redis + SQLite)

From repository root:

```bash
cd /Users/iangabaraev/repos/tidebreak
docker compose up --build -d
```

Smoke test:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/articles/VN
curl http://localhost:8000/api/v1/articles/TH
```

If port 8000 is already in use on your machine, use the mapped Docker host port:

```bash
curl http://localhost:8001/health
curl http://localhost:8001/api/v1/articles/VN
curl http://localhost:8001/api/v1/articles/TH
```

Stop:

```bash
docker compose down
```


