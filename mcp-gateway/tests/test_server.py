"""Pruebas de extremo a extremo con el cliente MCP real sobre HTTP."""

import json
import socket
import threading
import time
from contextlib import asynccontextmanager

import httpx
import pytest
import uvicorn
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from app.audit import Audit
from app.roles import TokenTable
from app.server import create_app

TOKENS = {
    "GATEWAY_TOKEN_INGESTOR": "tok-ing",
    "GATEWAY_TOKEN_CONSULTOR": "tok-con",
    "GATEWAY_TOKEN_AUDITOR": "tok-aud",
}


@pytest.fixture()
def gateway(vault, tmp_path):
    audit_path = tmp_path / "audit.jsonl"
    app = create_app(vault, TokenTable.from_env(TOKENS), Audit(audit_path))
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    for _ in range(100):
        if server.started:
            break
        time.sleep(0.05)
    yield f"http://127.0.0.1:{port}", audit_path
    server.should_exit = True
    thread.join(timeout=5)


@asynccontextmanager
async def connect(base, token):
    async with streamablehttp_client(f"{base}/mcp", headers={"Authorization": f"Bearer {token}"}) as (r, w, _):
        async with ClientSession(r, w) as session:
            await session.initialize()
            yield session


def text(result):
    return result.content[0].text


async def test_sin_token_o_con_token_falso_da_401(gateway):
    base, _ = gateway
    async with httpx.AsyncClient() as c:
        assert (await c.post(f"{base}/mcp", json={})).status_code == 401
        r = await c.post(f"{base}/mcp", json={}, headers={"Authorization": "Bearer falso"})
        assert r.status_code == 401
        assert (await c.get(f"{base}/health")).json() == {"status": "ok"}


async def test_lista_las_herramientas(gateway):
    base, _ = gateway
    async with connect(base, "tok-ing") as s:
        nombres = {t.name for t in (await s.list_tools()).tools}
    assert nombres == {
        "whoami", "list_notes", "read_note", "search_notes", "write_note", "commit_changes", "sync_main",
    }


async def test_el_rol_sale_del_token(gateway):
    base, _ = gateway
    for token, rol in [("tok-ing", "ingestor"), ("tok-con", "consultor"), ("tok-aud", "auditor")]:
        async with connect(base, token) as s:
            assert json.loads(text(await s.call_tool("whoami", {})))["role"] == rol


async def test_escribir_en_raw_se_deniega_y_queda_auditado(gateway):
    base, audit_path = gateway
    async with connect(base, "tok-ing") as s:
        r = await s.call_tool("write_note", {"path": "raw/atam.md", "content": "pisado"})
        assert r.isError and "solo lectura" in text(r)
        leido = await s.call_tool("read_note", {"path": "raw/atam.md"})
        assert "pisado" not in text(leido)

    entradas = [json.loads(line) for line in audit_path.read_text().splitlines()]
    denegada = next(e for e in entradas if e["tool"] == "write_note")
    assert denegada["role"] == "ingestor" and denegada["allowed"] is False
    lectura = next(e for e in entradas if e["tool"] == "read_note")
    assert lectura["allowed"] is True and lectura["chars_returned"] > 0


async def test_flujo_del_consultor(gateway):
    base, audit_path = gateway
    async with connect(base, "tok-con") as s:
        ok = await s.call_tool("write_note", {"path": "wiki/consultas/p01.md", "content": "# P01\n"})
        assert not ok.isError
        mal = await s.call_tool("write_note", {"path": "wiki/atam.md", "content": "x"})
        assert mal.isError and "consultor" in text(mal)
        commit = await s.call_tool("commit_changes", {"message": "consulta p01"})
        assert "agent/consultor" in text(commit)
        resultado = await s.call_tool("search_notes", {"query": "evaluación"})
        # las listas llegan como un bloque de contenido por elemento
        hits = [json.loads(c.text) for c in resultado.content]
        assert hits[0]["path"] == "raw/atam.md"

    escritura = next(
        json.loads(line) for line in audit_path.read_text().splitlines() if '"allowed": true' in line and "write_note" in line
    )
    assert escritura["bytes_written"] == len("# P01\n")
