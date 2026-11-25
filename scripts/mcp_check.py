"""Verifica el gateway MCP real: autenticación, roles y permisos.

Uso: uv run --with "mcp<2" python scripts/mcp_check.py   (lee tokens de .env o del entorno)
"""

import asyncio
import json
import os
import sys
from pathlib import Path

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


def load_env() -> dict[str, str]:
    env = dict(os.environ)
    dotenv = Path(".env")
    if dotenv.exists():
        for line in dotenv.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, _, v = line.partition("=")
                env.setdefault(k.strip(), v.strip())
    return env


ENV = load_env()
BASE = f"http://127.0.0.1:{ENV.get('GATEWAY_PORT', '8002')}"
FAILS: list[str] = []


def check(ok: bool, label: str) -> None:
    print(("  ok   " if ok else "  FALLA ") + label)
    if not ok:
        FAILS.append(label)


async def session_for(role: str):
    token = ENV[f"GATEWAY_TOKEN_{role.upper()}"]
    return streamablehttp_client(f"{BASE}/mcp", headers={"Authorization": f"Bearer {token}"})


async def main() -> int:
    r = httpx.post(f"{BASE}/mcp", json={})
    check(r.status_code == 401, "sin token: 401")

    for role, writable in [("ingestor", "wiki/smoke-ingestor.md"), ("consultor", "wiki/consultas/smoke.md"), ("auditor", "wiki/auditoria/smoke.md")]:
        print(f"rol {role}")
        async with await session_for(role) as (read, write, _):
            async with ClientSession(read, write) as s:
                await s.initialize()
                who = json.loads((await s.call_tool("whoami", {})).content[0].text)
                check(who["role"] == role, "whoami devuelve el rol del token")
                notas = [c.text for c in (await s.call_tool("list_notes", {"prefix": "raw/"})).content]
                check(len(notas) > 0, f"lee raw/ ({len(notas)} notas)")
                res = await s.call_tool("write_note", {"path": "raw/smoke.md", "content": "x"})
                check(res.isError, "escribir en raw/ es denegado")
                res = await s.call_tool("write_note", {"path": "../fuera.md", "content": "x"})
                check(res.isError, "ruta con .. es denegada")
                res = await s.call_tool("write_note", {"path": writable, "content": f"# Prueba de {role}\n"})
                check(not res.isError, f"escribe en {writable}")
                res = await s.call_tool("commit_changes", {"message": f"smoke: {role}"})
                check(not res.isError and f"agent/{role}" in res.content[0].text, "commit en su propia rama")

    # El consultor no puede escribir en el área del ingestor
    async with await session_for("consultor") as (read, write, _):
        async with ClientSession(read, write) as s:
            await s.initialize()
            res = await s.call_tool("write_note", {"path": "wiki/otra.md", "content": "x"})
            check(res.isError, "consultor no escribe fuera de wiki/consultas/")

    print("RESULTADO:", "OK" if not FAILS else f"{len(FAILS)} fallas")
    return 1 if FAILS else 0


sys.exit(asyncio.run(main()))
