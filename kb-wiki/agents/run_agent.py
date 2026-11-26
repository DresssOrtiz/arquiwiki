#!/usr/bin/env python3
"""Ejecuta un agente de KB-A (ingestor, consultor, auditor) sin interfaz con `claude -p`.

El agente accede al vault solo por el gateway MCP del proyecto. Cada ejecución
registra tokens, tiempos y costo equivalente en experiment/results/kba_runs.jsonl.

Uso:
  python3 kb-wiki/agents/run_agent.py consultor --op consulta --modo experimento \
      --pregunta "¿Qué es un estilo arquitectónico?" --question-id P01
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from string import Template

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent  # raíz del repo (los tests la sustituyen)
PROMPTS_DIR = HERE / "prompts"

DEFAULT_MODEL = "claude-sonnet-5-5"
ALL_TOOLS = ["whoami", "list_notes", "read_note", "search_notes", "write_note", "commit_changes", "sync_main"]
READ_ONLY_TOOLS = [t for t in ALL_TOOLS if t not in ("write_note", "commit_changes")]
SCHEMA_FILE = {"ingestor": "CLAUDE.md", "consultor": "AGENTS.md", "auditor": "GEMINI.md"}
OP_ROLE = {"ingesta": "ingestor", "correccion": "ingestor", "consulta": "consultor", "lint": "auditor"}
TOKEN_VARS = {r: f"GATEWAY_TOKEN_{r.upper()}" for r in SCHEMA_FILE}
MODES = ("demo", "experimento")


class AgentError(Exception):
    """Error de configuración o de entorno (no del agente)."""


def load_env(path: Path) -> dict[str, str]:
    """Parser simple de .env. No exporta nada al entorno."""
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.removeprefix("export ").strip()
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        values[key] = val
    return values


def get_config(name: str, env_file: dict[str, str], default: str | None = None) -> str | None:
    """Las variables del entorno tienen prioridad sobre .env."""
    return os.environ.get(name) or env_file.get(name) or default


def allowed_tools(rol: str, modo: str) -> list[str]:
    tools = READ_ONLY_TOOLS if (rol == "consultor" and modo == "experimento") else ALL_TOOLS
    return [f"mcp__arquiwiki__{t}" for t in tools]


def system_prompt(rol: str) -> str:
    esquema = SCHEMA_FILE[rol]
    return (
        f"Eres el agente {rol} de ArquiWiki. Accedes al vault solo mediante las herramientas MCP arquiwiki. "
        f"Antes de actuar, lee con read_note el esquema {esquema} y CONVENCIONES.md y síguelos al pie de la letra."
    )


def build_prompt(op: str, modo: str, pregunta: str | None, fuente: str | None) -> str:
    tpl = Template((PROMPTS_DIR / f"{op}.md").read_text(encoding="utf-8"))
    return tpl.safe_substitute(
        pregunta=pregunta or "(sin pregunta)",
        fuente=fuente or "(ninguna)",
        modo=modo,
        fecha=datetime.now().strftime("%Y-%m-%d"),
        instruccion_modo=MODO_INSTRUCCION.get(modo, ""),
    )


# Solo se envía la instrucción del modo activo: en el experimento no debe haber texto
# sobre archivar que cambie la conducta ni infle los tokens.
MODO_INSTRUCCION = {
    "experimento": "Modo experimento: solo respondes; no escribas ni hagas commit.",
    "demo": "Modo demo: además, archiva la consulta en `wiki/consultas/` según tu esquema y haz `commit_changes`.",
}


def build_command(rol: str, op: str, modo: str, prompt: str, mcp_config_path: str | Path,
                  model: str | None = None) -> list[str]:
    """Comando `claude` sin interfaz. No contiene el token (va en el archivo mcp-config)."""
    return [
        "claude", "-p", prompt, "--output-format", "json",
        "--model", model or os.environ.get("KBA_MODEL") or DEFAULT_MODEL,
        "--mcp-config", str(mcp_config_path), "--strict-mcp-config", "--tools", "",
        "--allowedTools", ",".join(allowed_tools(rol, modo)),
        "--setting-sources", "", "--disable-slash-commands", "--no-session-persistence",
        "--system-prompt", system_prompt(rol),
    ]


def mcp_config(token: str, port: str) -> dict:
    return {"mcpServers": {"arquiwiki": {
        "type": "http", "url": f"http://127.0.0.1:{port}/mcp",
        "headers": {"Authorization": f"Bearer {token}"},
    }}}


def _redact(text: str, secrets: list[str]) -> str:
    for s in secrets:
        if s:
            text = text.replace(s, "***")
    return text


def _validate(rol: str, op: str, modo: str, pregunta: str | None) -> None:
    if rol not in SCHEMA_FILE:
        raise AgentError(f"Rol desconocido: {rol}")
    if op not in OP_ROLE:
        raise AgentError(f"Operación desconocida: {op}")
    if OP_ROLE[op] != rol:
        raise AgentError(f"La operación '{op}' corresponde al rol '{OP_ROLE[op]}', no a '{rol}'")
    if modo not in MODES:
        raise AgentError(f"Modo inválido: {modo} (demo|experimento)")
    if op == "consulta" and not pregunta:
        raise AgentError("La operación consulta requiere --pregunta")


def _results_dir() -> Path:
    d = ROOT / "experiment" / "results"
    try:
        (d / "kba_runs").mkdir(parents=True, exist_ok=True)
        probe = d / ".write_probe"
        probe.touch()
        probe.unlink()
    except PermissionError as e:
        raise AgentError(
            f"No se puede escribir en {d} ({e}). Si lo creó root (por ejemplo, un contenedor), "
            f"corrige los permisos: sudo chown -R $(id -un) '{d}'"
        ) from e
    return d


def _now() -> datetime:
    """Reloj del registro (las pruebas lo sustituyen)."""
    return datetime.now(timezone.utc)


def _write_exclusive(path: Path, text: str) -> None:
    """Crea el archivo y falla si ya existe: nunca sobrescribe una respuesta anterior."""
    with open(path, "x", encoding="utf-8") as f:
        f.write(text)


def _append_jsonl(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def run_agent(rol: str, op: str, modo: str = "experimento", pregunta: str | None = None,
              fuente: str | None = None, question_id: str | None = None,
              model: str | None = None, timeout: int | None = None) -> dict:
    """Ejecuta el agente y devuelve el registro (también se añade a kba_runs.jsonl)."""
    _validate(rol, op, modo, pregunta)
    env_file = load_env(ROOT / ".env")
    token = get_config(TOKEN_VARS[rol], env_file)
    if not token:
        raise AgentError(f"Falta {TOKEN_VARS[rol]} en el entorno o en .env")
    port = get_config("GATEWAY_PORT", env_file, "8002")
    model = model or get_config("KBA_MODEL", env_file, DEFAULT_MODEL)
    timeout = timeout or (1800 if op == "ingesta" else 600)
    results = _results_dir()

    prompt = build_prompt(op, modo, pregunta, fuente)
    now = _now()
    ts = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    run_id = uuid.uuid4().hex[:12]  # único por ejecución, aunque coincida el segundo
    resp_name = f"{stamp}-{rol}-{op}" + (f"-{question_id}" if question_id else "") + f"-{run_id}.md"
    resp_rel = f"experiment/results/kba_runs/{resp_name}"

    record: dict = {
        "run_id": run_id, "ts": ts, "rol": rol, "motor": "claude", "op": op, "modo": modo,
        "question_id": question_id, "fuente": fuente, "model": model,
    }
    tmpdir = Path(tempfile.mkdtemp(prefix="kba-"))
    os.chmod(tmpdir, 0o700)
    stdout = stderr = ""
    returncode: int | None = None
    wall_start = time.monotonic()
    try:
        cfg = tmpdir / "mcp.json"
        fd = os.open(cfg, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w") as f:
            json.dump(mcp_config(token, port), f)
        cmd = build_command(rol, op, modo, prompt, cfg, model)
        child_env = {k: v for k, v in os.environ.items() if not k.startswith("GATEWAY_TOKEN_")}
        try:
            proc = subprocess.run(cmd, cwd=tmpdir, env=child_env, capture_output=True, text=True,
                                  timeout=timeout)
            stdout, stderr, returncode = proc.stdout, proc.stderr, proc.returncode
        except subprocess.TimeoutExpired as e:
            stdout = (e.stdout.decode() if isinstance(e.stdout, bytes) else e.stdout) or ""
            stderr = f"Tiempo agotado tras {timeout} s"
        except FileNotFoundError:
            stderr = "No se encontró el ejecutable 'claude' en el PATH"
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    wall_ms = int((time.monotonic() - wall_start) * 1000)

    data = None
    try:
        parsed = json.loads(stdout)
        if isinstance(parsed, dict):
            data = parsed
    except (json.JSONDecodeError, ValueError):
        pass

    secrets = [token]
    if data is not None:
        usage = data.get("usage") or {}
        inp = int(usage.get("input_tokens") or 0)
        cc = int(usage.get("cache_creation_input_tokens") or 0)
        cr = int(usage.get("cache_read_input_tokens") or 0)
        result_text = _redact(str(data.get("result") or ""), secrets)
        is_error = bool(data.get("is_error")) or returncode != 0
        record.update({
            "input_tokens": inp, "cache_creation_input_tokens": cc, "cache_read_input_tokens": cr,
            "output_tokens": int(usage.get("output_tokens") or 0),
            "total_input_tokens": inp + cc + cr,
            "num_turns": data.get("num_turns"), "duration_ms": data.get("duration_ms"),
            "duration_api_ms": data.get("duration_api_ms"), "wall_ms": wall_ms,
            "cost_usd_equiv": data.get("total_cost_usd"), "is_error": is_error,
        })
        _write_exclusive(results / "kba_runs" / resp_name, result_text)
        record["respuesta_path"] = resp_rel
        record["respuesta"] = result_text
    else:
        raw = _redact(f"[stdout]\n{stdout}\n[stderr]\n{stderr}\n[returncode] {returncode}\n", secrets)
        _write_exclusive(results / "kba_runs" / resp_name, raw)
        record.update({
            "input_tokens": 0, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0,
            "output_tokens": 0, "total_input_tokens": 0, "num_turns": None, "duration_ms": None,
            "duration_api_ms": None, "wall_ms": wall_ms, "cost_usd_equiv": None, "is_error": True,
            "respuesta_path": resp_rel,
            "error": _redact(stderr.strip() or "Salida no JSON de claude", secrets)[:2000],
        })
    # `respuesta` (texto) se devuelve al llamador pero no se duplica en el jsonl.
    _append_jsonl(results / "kba_runs.jsonl", {k: v for k, v in record.items() if k != "respuesta"})
    return record


def _dry_run(rol: str, op: str, modo: str, pregunta, fuente, model) -> int:
    _validate(rol, op, modo, pregunta)
    prompt = build_prompt(op, modo, pregunta, fuente)
    cmd = build_command(rol, op, modo, prompt, "<tmpdir>/mcp.json", model or get_config(
        "KBA_MODEL", load_env(ROOT / ".env"), DEFAULT_MODEL))
    port = get_config("GATEWAY_PORT", load_env(ROOT / ".env"), "8002")
    print("# Comando (cwd: dir temporal vacío)")
    print(" ".join(shlex.quote(c) for c in cmd))
    print(f"# mcp-config: {json.dumps(mcp_config('***', port))}")
    print("# Prompt")
    print(prompt)
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Ejecuta un agente de KB-A con claude -p")
    p.add_argument("rol", choices=list(SCHEMA_FILE))
    p.add_argument("--op", required=True, choices=list(OP_ROLE))
    p.add_argument("--modo", choices=MODES, default="experimento",
                   help="solo afecta al consultor: experimento (sin escritura) o demo")
    p.add_argument("--pregunta")
    p.add_argument("--fuente", help="p. ej. raw/x.md")
    p.add_argument("--question-id")
    p.add_argument("--model")
    p.add_argument("--timeout", type=int)
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args(argv)
    try:
        if a.dry_run:
            return _dry_run(a.rol, a.op, a.modo, a.pregunta, a.fuente, a.model)
        rec = run_agent(a.rol, a.op, a.modo, a.pregunta, a.fuente, a.question_id, a.model, a.timeout)
    except AgentError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    print(f"rol={rec['rol']} op={rec['op']} modo={rec['modo']} model={rec['model']}")
    print(f"tokens: entrada_total={rec['total_input_tokens']} (nuevos={rec['input_tokens']}, "
          f"cache_creacion={rec['cache_creation_input_tokens']}, cache_lectura={rec['cache_read_input_tokens']}) "
          f"salida={rec['output_tokens']}")
    print(f"duración: wall={rec['wall_ms']} ms api={rec['duration_api_ms']} ms turnos={rec['num_turns']} "
          f"costo_equiv=${rec['cost_usd_equiv']}")
    print(f"respuesta guardada en: {rec['respuesta_path']}")
    if rec["is_error"]:
        print(f"ERROR: {rec.get('error', 'el agente terminó con is_error')}", file=sys.stderr)
    print("---")
    print(rec.get("respuesta") or "")
    return 1 if rec["is_error"] else 0


if __name__ == "__main__":
    sys.exit(main())
