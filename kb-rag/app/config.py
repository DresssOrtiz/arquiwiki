import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    database_url: str
    corpus_dir: Path
    results_dir: Path
    embedding_model: str
    anthropic_api_key: str
    anthropic_model: str
    top_k: int
    chunk_max_tokens: int
    answer_max_tokens: int


def load_settings() -> Settings:
    # La URL puede venir con el prefijo de SQLAlchemy ("postgresql+psycopg://").
    url = os.getenv("DATABASE_URL", "postgresql://arquiwiki:change-me@localhost:5432/arquiwiki")
    return Settings(
        database_url=url.replace("postgresql+psycopg://", "postgresql://"),
        corpus_dir=Path(os.getenv("CORPUS_DIR", "/vault/raw")),
        results_dir=Path(os.getenv("RESULTS_DIR", "/results")),
        embedding_model=os.getenv(
            "EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        ),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        anthropic_model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5"),
        top_k=int(os.getenv("RAG_TOP_K", "5")),
        # El modelo de embeddings multilingüe rinde mejor con fragmentos cortos.
        chunk_max_tokens=int(os.getenv("RAG_CHUNK_TOKENS", "200")),
        answer_max_tokens=int(os.getenv("RAG_ANSWER_MAX_TOKENS", "600")),
    )
