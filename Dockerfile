FROM python:3.12.8-slim as builder


ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev

WORKDIR /build

RUN pip install poetry==2.0.1

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main


FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /build/.venv /app/./venv
COPY . .

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
