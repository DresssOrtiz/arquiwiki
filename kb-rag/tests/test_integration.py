"""Prueba contra pgvector real y el modelo de embeddings de verdad.

Se salta si no hay TEST_DATABASE_URL. Ejemplo:
  TEST_DATABASE_URL=postgresql://arquiwiki:change-me@localhost:5432/arquiwiki uv run pytest -m integration
"""

import os

import pytest

from app.embedder import FastEmbedder
from app.service import RagService
from app.store import PgStore

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not os.getenv("TEST_DATABASE_URL"), reason="sin TEST_DATABASE_URL"),
]


def test_indexa_y_recupera_la_fuente_correcta(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    (raw / "atam.md").write_text(
        "# ATAM\n\nATAM es un método para evaluar una arquitectura frente a sus objetivos de negocio.\n"
    )
    (raw / "inventario.md").write_text(
        "# MANI\n\nMANI registra productos, movimientos de bodega y alertas de existencias mínimas.\n"
    )
    embedder = FastEmbedder("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    store = PgStore(os.environ["TEST_DATABASE_URL"], embedder.dim)
    # base limpia para que la prueba sea repetible
    for path in list(store.document_hashes()):
        store.delete_document(path)

    svc = RagService(store, embedder, None, raw, tmp_path / "results")
    assert svc.index()["mode"] == "full"
    assert svc.index()["files_changed"] == 0

    out = svc.query("¿Cómo se evalúa una arquitectura de software?", k=2, use_llm=False)
    assert out["sources"][0] == "raw/atam.md"
    out = svc.query("alertas de existencias en bodega", k=2, use_llm=False)
    assert out["sources"][0] == "raw/inventario.md"
