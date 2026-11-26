import hashlib
import time
from pathlib import Path

from app.chunker import chunk_markdown
from app.embedder import Embedder
from app.llm import LLM
from app.metrics import append_jsonl, now_iso
from app.store import Store


class RagService:
    def __init__(
        self,
        store: Store,
        embedder: Embedder,
        llm: LLM | None,
        corpus_dir: Path,
        results_dir: Path,
        chunk_max_tokens: int = 120,
        top_k: int = 5,
    ):
        self.store = store
        self.embedder = embedder
        self.llm = llm
        self.corpus_dir = corpus_dir
        self.results_dir = results_dir
        self.chunk_max_tokens = chunk_max_tokens
        self.top_k = top_k

    # ------------------------------------------------------------------ indexación

    def _corpus_files(self) -> dict[str, Path]:
        base = self.corpus_dir
        return {
            f"raw/{p.relative_to(base).as_posix()}": p
            for p in sorted(base.rglob("*.md"))
            if p.is_file()
        }

    def index(self, path: str | None = None, force: bool = False) -> dict:
        """Indexa el corpus. Solo reprocesa los archivos cuyo hash cambió, de modo que el
        costo de actualizar un documento queda medido por separado del de construir todo."""
        started = time.perf_counter()
        files = self._corpus_files()
        if path is not None:
            if path not in files:
                raise FileNotFoundError(path)
            files = {path: files[path]}
        known = self.store.document_hashes()
        mode = "full" if not known or force else "incremental"

        changed = embedded_tokens = chunks_written = 0
        for rel, file in files.items():
            raw = file.read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            if not force and known.get(rel) == digest:
                continue
            chunks = chunk_markdown(
                raw.decode("utf-8"), self.embedder.count_tokens, self.chunk_max_tokens
            )
            vectors = self.embedder.embed([c.text for c in chunks]) if chunks else []
            self.store.replace_document(rel, digest, chunks, vectors)
            changed += 1
            chunks_written += len(chunks)
            embedded_tokens += sum(c.tokens for c in chunks)

        removed = 0
        if path is None:
            for gone in set(known) - set(files):
                self.store.delete_document(gone)
                removed += 1

        record = {
            "ts": now_iso(),
            "mode": mode,
            "files_total": len(files),
            "files_changed": changed,
            "files_removed": removed,
            "chunks_written": chunks_written,
            "embedded_tokens": embedded_tokens,
            "llm_tokens": 0,  # embeddings locales: no hay consumo de LLM al construir
            "elapsed_ms": round((time.perf_counter() - started) * 1000),
        }
        self.store.log("build", record)
        append_jsonl(self.results_dir, "build", record)
        return record

    # ------------------------------------------------------------------ consulta

    def query(
        self,
        question: str,
        k: int | None = None,
        question_id: str | None = None,
        use_llm: bool = True,
    ) -> dict:
        k = k or self.top_k
        t0 = time.perf_counter()
        vector = self.embedder.embed([question])[0]
        hits = self.store.search(vector, k)
        t1 = time.perf_counter()

        answer = None
        llm_mode = "disabled"
        if use_llm and self.llm is not None and hits:
            answer = self.llm.answer(question, hits)
            llm_mode = "anthropic"
        t2 = time.perf_counter()

        retrieved_tokens = sum(h.tokens for h in hits)
        latency = {
            "retrieval_ms": round((t1 - t0) * 1000),
            "generation_ms": round((t2 - t1) * 1000),
            "total_ms": round((t2 - t0) * 1000),
        }
        sources = list(dict.fromkeys(h.path for h in hits))
        usage = {
            "input_tokens": answer.input_tokens if answer else 0,
            "output_tokens": answer.output_tokens if answer else 0,
        }

        record = {
            "ts": now_iso(),
            "question_id": question_id,
            "question": question,
            "k": k,
            "llm": llm_mode,
            "model": answer.model if answer else None,
            **usage,
            "retrieved_tokens": retrieved_tokens,
            **latency,
            "sources": sources,
        }
        self.store.log("query", record)
        append_jsonl(self.results_dir, "query", record)

        return {
            "question": question,
            "answer": answer.text if answer else None,
            "llm": llm_mode,
            "model": record["model"],
            "fragments": [
                {
                    "source": h.path,
                    "heading": h.heading,
                    "score": round(h.score, 4),
                    "tokens": h.tokens,
                    "text": h.text,
                }
                for h in hits
            ],
            "usage": usage,
            "retrieved_tokens": retrieved_tokens,
            "latency_ms": latency,
            "sources": sources,
        }
