FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 UV_COMPILE_BYTECODE=1
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /srv
COPY pyproject.toml ./
RUN uv sync --no-dev --no-install-project
ENV PATH="/srv/.venv/bin:$PATH"

COPY app ./app

# El usuario real lo fija docker-compose (HOST_UID/HOST_GID) para escribir en el vault.
USER 10001
EXPOSE 8002
CMD ["python", "-m", "app"]
