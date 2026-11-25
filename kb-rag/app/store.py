"""Acceso a pgvector. El servicio depende del protocolo `Store`, no de Postgres."""

import json
from dataclasses import dataclass
from typing import Protocol

import psycopg
from pgvector.psycopg import register_vector

from app.chunker import Chunk


@dataclass(frozen=True)
class Hit:
    path: str
    heading: str
    text: str
    tokens: int
    score: float  # similitud coseno, 1 = idéntico


class Store(Protocol):
    def document_hashes(self) -> dict[str, str]: ...

    def replace_document(
        self, path: str, sha256: str, chunks: list[Chunk], vectors: list[list[float]]
    ) -> None: ...

    def delete_document(self, path: str) -> None: ...

    def search(self, vector: list[float], k: int) -> list[Hit]: ...

    def stats(self) -> dict: ...

    def log(self, kind: str, data: dict) -> None: ...


class PgStore:
    def __init__(self, database_url: str, dim: int):
        self._url = database_url
        self._dim = dim
        self._init_schema()

    def _connect(self) -> psycopg.Connection:
        conn = psycopg.connect(self._url, autocommit=True)
        register_vector(conn)
        return conn

    def _init_schema(self) -> None:
        # La extensión la crea infra/postgres/init.sql; aquí se asegura por si se usa otra base.
        with psycopg.connect(self._url, autocommit=True) as conn:
            conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
            conn.execute("CREATE SCHEMA IF NOT EXISTS rag")
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS rag.documents (
                    path text PRIMARY KEY,
                    sha256 text NOT NULL,
                    chunk_count int NOT NULL,
                    updated_at timestamptz NOT NULL DEFAULT now()
                )"""
            )
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS rag.chunks (
                    id bigserial PRIMARY KEY,
                    path text NOT NULL REFERENCES rag.documents(path) ON DELETE CASCADE,
                    ord int NOT NULL,
                    heading text NOT NULL,
                    content text NOT NULL,
                    tokens int NOT NULL,
                    embedding vector({self._dim}) NOT NULL
                )"""
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS chunks_embedding_hnsw "
                "ON rag.chunks USING hnsw (embedding vector_cosine_ops)"
            )
            for table in ("build_log", "query_log"):
                conn.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS rag.{table} (
                        id bigserial PRIMARY KEY,
                        ts timestamptz NOT NULL DEFAULT now(),
                        data jsonb NOT NULL
                    )"""
                )
            actual = conn.execute(
                "SELECT atttypmod FROM pg_attribute "
                "WHERE attrelid = 'rag.chunks'::regclass AND attname = 'embedding'"
            ).fetchone()
            if actual and actual[0] != self._dim:
                raise RuntimeError(
                    f"rag.chunks usa vectores de {actual[0]} dimensiones y el modelo produce "
                    f"{self._dim}. Si cambiaste EMBEDDING_MODEL, elimina el esquema rag y reindexa."
                )

    def document_hashes(self) -> dict[str, str]:
        with self._connect() as conn:
            return dict(conn.execute("SELECT path, sha256 FROM rag.documents").fetchall())

    def replace_document(self, path, sha256, chunks, vectors) -> None:
        with self._connect() as conn, conn.transaction():
            conn.execute("DELETE FROM rag.documents WHERE path = %s", (path,))
            conn.execute(
                "INSERT INTO rag.documents (path, sha256, chunk_count) VALUES (%s, %s, %s)",
                (path, sha256, len(chunks)),
            )
            with conn.cursor() as cur:
                cur.executemany(
                    "INSERT INTO rag.chunks (path, ord, heading, content, tokens, embedding) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    [
                        (path, c.ord, c.heading, c.text, c.tokens, v)
                        for c, v in zip(chunks, vectors, strict=True)
                    ],
                )

    def delete_document(self, path: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM rag.documents WHERE path = %s", (path,))

    def search(self, vector: list[float], k: int) -> list[Hit]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT path, heading, content, tokens, 1 - (embedding <=> %s::vector) AS score "
                "FROM rag.chunks ORDER BY embedding <=> %s::vector LIMIT %s",
                (vector, vector, k),
            ).fetchall()
        return [Hit(*row) for row in rows]

    def stats(self) -> dict:
        with self._connect() as conn:
            docs, chunks, tokens = conn.execute(
                "SELECT (SELECT count(*) FROM rag.documents), count(*), coalesce(sum(tokens), 0) "
                "FROM rag.chunks"
            ).fetchone()
        return {"documents": docs, "chunks": chunks, "indexed_tokens": int(tokens)}

    def log(self, kind: str, data: dict) -> None:
        table = {"build": "build_log", "query": "query_log"}[kind]
        with self._connect() as conn:
            conn.execute(f"INSERT INTO rag.{table} (data) VALUES (%s)", (json.dumps(data),))
