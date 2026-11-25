"""Registro de métricas del experimento: archivos JSONL en RESULTS_DIR."""

import json
import logging
from datetime import UTC, datetime
from pathlib import Path

log = logging.getLogger("rag.metrics")

FILES = {"build": "rag_builds.jsonl", "query": "rag_queries.jsonl"}


def now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def append_jsonl(results_dir: Path, kind: str, record: dict) -> None:
    """Agrega una línea. Si el directorio no es escribible solo se avisa: la métrica
    queda igual en la tabla rag.*_log."""
    try:
        results_dir.mkdir(parents=True, exist_ok=True)
        with (results_dir / FILES[kind]).open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as exc:
        log.warning("No se pudo escribir %s: %s", FILES[kind], exc)
