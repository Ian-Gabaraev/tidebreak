FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN mkdir -p /data

COPY apps/flask_api/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY dist/tidebreak-0.1.0-py3-none-any.whl /app/tidebreak-0.1.0-py3-none-any.whl
RUN pip install /app/tidebreak-0.1.0-py3-none-any.whl

COPY apps/flask_api /app

ENV SQLITE_PATH=/data/tidebreak_api.db \
    REDIS_URL=redis://redis:6379/0 \
    CACHE_TTL_SECONDS=300

EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi:app"]

