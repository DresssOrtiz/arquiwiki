FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 UV_COMPILE_BYTECODE=1 \
    FASTEMBED_CACHE_PATH=/models
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /srv
COPY pyproject.toml ./
RUN uv sync --no-dev --no-install-project
ENV PATH="/srv/.venv/bin:$PATH"

# El modelo se descarga al construir la imagen: la demo funciona sin red.
ARG EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
RUN python -c "from fastembed import TextEmbedding; TextEmbedding(model_name='${EMBEDDING_MODEL}')" \
    && chmod -R a+rX /models

COPY app ./app

# El usuario real lo fija docker-compose (HOST_UID/HOST_GID) para poder escribir en experiment/results.
USER 10001
EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
