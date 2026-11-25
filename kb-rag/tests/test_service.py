import json

import pytest
from fastapi.testclient import TestClient
from tests.helpers import FakeEmbedder, FakeLLM, MemoryStore

from app.main import app
from app.service import RagService


@pytest.fixture()
def corpus(tmp_path):
    raw = tmp_path / "vault" / "raw"
    raw.mkdir(parents=True)
    (raw / "atam.md").write_text("# ATAM\n\nMétodo para evaluar arquitecturas y sus tradeoffs.\n")
    (raw / "mani.md").write_text("# MANI\n\nSistema de inventario con requisitos de rendimiento.\n")
    return raw


@pytest.fixture()
def service(corpus, tmp_path):
    return RagService(
        store=MemoryStore(),
        embedder=FakeEmbedder(),
        llm=FakeLLM(),
        corpus_dir=corpus,
        results_dir=tmp_path / "results",
    )


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def test_indexacion_completa_registra_el_build(service, tmp_path):
    rec = service.index()
    assert rec["mode"] == "full"
    assert rec["files_total"] == rec["files_changed"] == 2
    assert rec["chunks_written"] == 2
    assert rec["embedded_tokens"] > 0
    assert rec["llm_tokens"] == 0
    assert read_jsonl(tmp_path / "results" / "rag_builds.jsonl")[0]["mode"] == "full"


def test_reindexar_sin_cambios_no_reprocesa(service):
    service.index()
    rec = service.index()
    assert rec["mode"] == "incremental"
    assert rec["files_changed"] == 0
    assert rec["embedded_tokens"] == 0


def test_actualizar_un_documento_solo_reprocesa_ese(service, corpus):
    service.index()
    (corpus / "atam.md").write_text("# ATAM\n\nTexto nuevo sobre el método de evaluación.\n")
    rec = service.index()
    assert rec["files_changed"] == 1
    assert rec["chunks_written"] == 1


def test_borrar_un_archivo_lo_quita_del_indice(service, corpus):
    service.index()
    (corpus / "mani.md").unlink()
    rec = service.index()
    assert rec["files_removed"] == 1
    assert set(service.store.docs) == {"raw/atam.md"}


def test_indexar_un_archivo_inexistente(service):
    with pytest.raises(FileNotFoundError):
        service.index("raw/no-existe.md")


def test_consulta_devuelve_fuentes_tokens_y_registro(service, tmp_path):
    service.index()
    out = service.query("método para evaluar arquitecturas", question_id="P01")
    assert out["fragments"][0]["source"] == "raw/atam.md"
    assert out["sources"][0] == "raw/atam.md"
    assert out["llm"] == "anthropic"
    assert out["usage"] == {"input_tokens": 123, "output_tokens": 45}
    assert out["retrieved_tokens"] > 0
    assert set(out["latency_ms"]) == {"retrieval_ms", "generation_ms", "total_ms"}

    rec = read_jsonl(tmp_path / "results" / "rag_queries.jsonl")[0]
    assert rec["question_id"] == "P01"
    assert rec["input_tokens"] == 123 and rec["output_tokens"] == 45
    assert rec["sources"][0] == "raw/atam.md"
    assert service.store.logs[-1][0] == "query"


def test_consulta_sin_llm_solo_recupera(service):
    service.index()
    out = service.query("inventario", use_llm=False)
    assert out["answer"] is None and out["llm"] == "disabled"
    assert out["usage"] == {"input_tokens": 0, "output_tokens": 0}
    assert service.llm.calls == []


def test_consulta_sin_clave_configurada(corpus, tmp_path):
    svc = RagService(MemoryStore(), FakeEmbedder(), None, corpus, tmp_path / "r")
    svc.index()
    assert svc.query("inventario")["llm"] == "disabled"


def test_un_directorio_de_resultados_no_escribible_no_rompe(corpus, tmp_path):
    bloqueado = tmp_path / "archivo"
    bloqueado.write_text("x")  # un archivo donde debería haber directorio
    svc = RagService(MemoryStore(), FakeEmbedder(), None, corpus, bloqueado / "sub")
    assert svc.index()["files_changed"] == 2


def test_api_http(service):
    app.state.service = service
    try:
        with TestClient(app) as client:
            assert client.get("/health").json() == {"status": "ok"}
            assert client.post("/index", json={}).json()["mode"] == "full"
            assert client.get("/stats").json()["documents"] == 2
            r = client.post("/query", json={"question": "inventario", "k": 1, "use_llm": False})
            assert r.status_code == 200 and len(r.json()["fragments"]) == 1
            assert client.post("/index", json={"path": "raw/x.md"}).status_code == 404
            assert client.post("/query", json={"question": ""}).status_code == 422
    finally:
        app.state.service = None
