import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from app.config import load_settings
from app.service import RagService


@asynccontextmanager
async def lifespan(app: FastAPI):
    if getattr(app.state, "service", None) is None:  # las pruebas inyectan el suyo
        from app.embedder import FastEmbedder
        from app.llm import AnthropicLLM
        from app.store import PgStore

        s = load_settings()
        embedder = FastEmbedder(s.embedding_model)
        llm = (
            AnthropicLLM(s.anthropic_api_key, s.anthropic_model, s.answer_max_tokens)
            if s.anthropic_api_key
            else None
        )
        chunk_max = min(s.chunk_max_tokens, embedder.max_seq_len)
        if chunk_max < s.chunk_max_tokens:
            logging.getLogger("rag").warning(
                "RAG_CHUNK_TOKENS=%d supera la ventana del modelo (%d); se usa %d",
                s.chunk_max_tokens, embedder.max_seq_len, chunk_max,
            )
        app.state.service = RagService(
            store=PgStore(s.database_url, embedder.dim),
            embedder=embedder,
            llm=llm,
            corpus_dir=s.corpus_dir,
            results_dir=s.results_dir,
            chunk_max_tokens=chunk_max,
            top_k=s.top_k,
        )
    yield


app = FastAPI(
    title="ArquiWiki RAG (KB-B)",
    version="1.0.0",
    description="Fragmenta, indexa en pgvector y consulta el corpus registrando tokens y latencia.",
    lifespan=lifespan,
)


def _service(request: Request) -> RagService:
    return request.app.state.service


class IndexRequest(BaseModel):
    path: str | None = Field(default=None, description="Ruta raw/... de un solo archivo")
    force: bool = Field(default=False, description="Reprocesar aunque el hash no haya cambiado")


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)
    k: int | None = Field(default=None, ge=1, le=20)
    question_id: str | None = Field(default=None, description="Id de la pregunta del experimento")
    use_llm: bool = Field(default=True, description="false: solo recuperación, sin gastar tokens")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/stats")
def stats(request: Request):
    return _service(request).store.stats()


@app.post("/index")
def index(body: IndexRequest, request: Request):
    try:
        return _service(request).index(body.path, body.force)
    except FileNotFoundError:
        raise HTTPException(404, f"No existe {body.path} en el corpus")


@app.post("/query")
def query(body: QueryRequest, request: Request):
    return _service(request).query(body.question, body.k, body.question_id, body.use_llm)
