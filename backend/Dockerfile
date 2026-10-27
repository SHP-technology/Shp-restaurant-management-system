# SHP Restaurant backend — Django + Channels (ASGI)
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps for psycopg / Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static into STATIC_ROOT (served by WhiteNoise)
RUN DJANGO_DEBUG=False DJANGO_SECRET_KEY=build-only-key \
    python manage.py collectstatic --noinput || true

EXPOSE 8000

# ASGI server (Uvicorn) so WebSockets/Channels work. Scale workers via WEB_CONCURRENCY.
CMD ["sh", "-c", "python manage.py migrate --noinput && uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --workers ${WEB_CONCURRENCY:-3}"]
