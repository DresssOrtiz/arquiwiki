#!/usr/bin/env python3
"""Corre el experimento comparativo KB-A (LLM Wiki) vs KB-B (RAG) con el mismo modelo.

Uso:
  python3 experiment/run.py --brazo ambos --ids todas --reps 3
  python3 experiment/run.py --brazo A --ids P01,P02 --reps 1 --dry-run
  python3 experiment/run.py --brazo ambos --ids todas --reps 3 --orden aleatorio --semilla 42
  python3 experiment/run.py --overhead 3

Solo biblioteca estándar. Las respuestas de referencia (las claves) NUNCA se leen aquí.
Toda la generación usa `claude -p` (suscripción), con el mismo modelo en ambos brazos.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import shlex
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime
from pathlib import Path
from string import Template

EXP = Path(__file__).resolve().parent
REPO = EXP.parent
RESULTS = EXP / "results"
PROMPTS = EXP / "prompts"
sys.path.insert(0, str(REPO / "kb-wiki" / "agents"))
import run_agent as ra  # noqa: E402

BASELINE_TAG = "kb-a-baseline"
VAULT_IN_CONTAINER = "/vault"
WORKTREE_CONSULTOR = "/worktrees/consultor"
GIT_IN_GATEWAY = ["git", "-c", "safe.directory=*"]
EMPTY_MCP_JSON = '{"mcpServers":{}}'
OVERHEAD_PROMPT = "Responde solo: ok"
OVERHEAD_SYSTEM = "Responde exactamente lo que se te pide, sin usar herramientas."
BRAZOS = ("A", "B")


class ExperimentError(Exception):
    """Error que invalida la corrida (no de una pregunta concreta)."""


class BaselineError(ExperimentError):
    """El vault de KB-A ya no está en la línea base: la comparación dejaría de ser válida."""


# --------------------------------------------------------------------------- utilidades

def now_iso() -> str:
    return ra._now().strftime("%Y-%m-%dT%H:%M:%SZ")


def load_questions(ids: list[str] | None = None) -> list[dict]:
    """Lee SOLO preguntas.json (id, tipo, texto); las claves no se cargan nunca."""
    qs = json.loads((EXP / "preguntas.json").read_text(encoding="utf-8"))
    if ids is None:
        return qs
    by_id = {q["id"]: q for q in qs}
    missing = [i for i in ids if i not in by_id]
    if missing:
        raise ExperimentError(f"Preguntas inexistentes: {', '.join(missing)}")
    return [by_id[i] for i in ids]


def resolve_model(cli_model: str | None, env_file: dict[str, str]) -> str:
    return cli_model or ra.get_config("KBA_MODEL", env_file, ra.DEFAULT_MODEL)


def tokens_from_usage(usage: dict) -> dict:
    inp = int(usage.get("input_tokens") or 0)
    cc = int(usage.get("cache_creation_input_tokens") or 0)
    cr = int(usage.get("cache_read_input_tokens") or 0)
    return {"input_tokens": inp, "cache_creation_input_tokens": cc, "cache_read_input_tokens": cr,
            "output_tokens": int(usage.get("output_tokens") or 0), "total_input_tokens": inp + cc + cr}


# --------------------------------------------------------------------------- plan / orden

def build_plan(ids: list[str], brazos: list[str], reps: int, orden: str = "intercalado",
               semilla: int | None = None) -> list[dict]:
    """Lista de (pregunta, brazo, rep) en orden de ejecución.

    intercalado: por pregunta y repetición se ejecutan A y B seguidos; el brazo que va primero se
    alterna en cada par para que ninguno quede siempre antes (calentamiento, hora del día).
    aleatorio: baraja todos los ítems con random.Random(semilla): reproducible.
    """
    items: list[dict] = []
    pair = 0
    for qid in ids:
        for rep in range(1, reps + 1):
            order = list(brazos)
            if len(order) == 2 and pair % 2 == 1:
                order.reverse()
            pair += 1
            for b in order:
                items.append({"question_id": qid, "brazo": b, "rep": rep})
    if orden == "aleatorio":
        if semilla is None:
            raise ExperimentError("--orden aleatorio requiere --semilla")
        random.Random(semilla).shuffle(items)
    for i, it in enumerate(items, 1):
        it["orden_idx"] = i
    return items


# --------------------------------------------------------------------------- restauración de KB-A

def default_runner(cmd: list[str], timeout: int = 120) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def _gw(*git_args: str) -> list[str]:
    return ["docker", "compose", "exec", "-T", "mcp-gateway", *GIT_IN_GATEWAY, *git_args]


def reset_kba(runner=default_runner) -> dict:
    """Restaura KB-A a la línea base ANTES de cada pregunta.

    1. main del vault debe ser == etiqueta kb-a-baseline; si no, BaselineError (nada se resetea).
    2. La rama del consultor vuelve a la línea base (reset --hard + clean -fd en su worktree; si no
       hay worktree pero sí rama, la rama se mueve a la etiqueta).
    Todo va por `docker compose exec` porque el .git de los worktrees apunta a rutas del contenedor.
    `runner(cmd) -> (rc, stdout, stderr)` es inyectable para las pruebas.
    """
    rc, out, err = runner(_gw("-C", VAULT_IN_CONTAINER, "rev-parse", "main"))
    if rc != 0:
        raise BaselineError(f"No se pudo leer main del vault (¿gateway arriba?): {err.strip() or out.strip()}")
    main = out.strip()
    rc, out, err = runner(_gw("-C", VAULT_IN_CONTAINER, "rev-parse", f"{BASELINE_TAG}^{{commit}}"))
    if rc != 0:
        raise BaselineError(f"No existe la etiqueta {BASELINE_TAG} en el vault: {err.strip() or out.strip()}")
    base = out.strip()
    if main != base:
        raise BaselineError(
            f"main del vault ({main[:12]}) difiere de {BASELINE_TAG} ({base[:12]}): alguien fusionó cambios "
            f"después de la línea base. Restaura con `git reset --hard {BASELINE_TAG}` en el vault "
            f"(ver experiment/README.md) y reindexa KB-B antes de continuar.")
    rc, _, _ = runner(["docker", "compose", "exec", "-T", "mcp-gateway", "test", "-d", WORKTREE_CONSULTOR])
    if rc == 0:
        for cmd in (_gw("-C", WORKTREE_CONSULTOR, "reset", "--hard", BASELINE_TAG),
                    _gw("-C", WORKTREE_CONSULTOR, "clean", "-fd")):
            rc, out, err = runner(cmd)
            if rc != 0:
                raise BaselineError(f"Falló la restauración del consultor ({' '.join(cmd[-4:])}): {err.strip()}")
        action = "worktree_reset"
    else:
        rc, _, _ = runner(_gw("-C", VAULT_IN_CONTAINER, "rev-parse", "--verify", "-q", "refs/heads/agent/consultor"))
        if rc == 0:
            rc, _, err = runner(_gw("-C", VAULT_IN_CONTAINER, "branch", "-f", "agent/consultor", BASELINE_TAG))
            if rc != 0:
                raise BaselineError(f"No se pudo mover agent/consultor a la línea base: {err.strip()}")
            action = "branch_reset"
        else:
            action = "sin_worktree"
    return {"baseline": base, "accion": action}


# --------------------------------------------------------------------------- KB-B: recuperación y prompt

def rag_base_url(env_file: dict[str, str], override: str | None = None) -> str:
    if override:
        return override.rstrip("/")
    return f"http://127.0.0.1:{ra.get_config('RAG_PORT', env_file, '8001')}"


def http_post_json(url: str, payload: dict, timeout: int = 120) -> dict:
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def consultar_rag(base_url: str, question: str, k: int, question_id: str, post=http_post_json) -> tuple[dict, int]:
    """POST /query con use_llm:false. Devuelve (respuesta, ms de reloj)."""
    t0 = time.perf_counter()
    data = post(f"{base_url}/query", {"question": question, "k": k, "question_id": question_id, "use_llm": False})
    return data, int((time.perf_counter() - t0) * 1000)


def format_fragments(fragments: list[dict]) -> str:
    parts = []
    for i, f in enumerate(fragments, 1):
        parts.append(f"### Fragmento {i}\nFuente: {f.get('source')}\nEncabezado: {f.get('heading')}\n\n{f.get('text', '').strip()}")
    return "\n\n".join(parts) if parts else "(la recuperación no devolvió fragmentos)"


def build_prompt_b(question: str, fragments_text: str) -> str:
    tpl = Template((PROMPTS / "kbb.md").read_text(encoding="utf-8"))
    return tpl.safe_substitute(pregunta=question, fragmentos=fragments_text,
                               fecha=datetime.now().strftime("%Y-%m-%d"))


def system_prompt_b() -> str:
    return (PROMPTS / "kbb_system.md").read_text(encoding="utf-8").strip()


def build_command_b(prompt: str, model: str, system: str | None = None) -> list[str]:
    """Misma configuración aislada que build_command de run_agent, pero sin herramientas ni MCP."""
    return [
        "claude", "-p", prompt, "--output-format", "json", "--model", model,
        "--tools", "", "--strict-mcp-config", "--mcp-config", EMPTY_MCP_JSON,
        "--setting-sources", "", "--disable-slash-commands", "--no-session-persistence",
        "--system-prompt", system_prompt_b() if system is None else system,
    ]


# --------------------------------------------------------------------------- ejecución de claude -p

def run_claude(cmd: list[str], env_extra: dict | None = None, timeout: int = 600) -> dict:
    """Ejecuta `cmd` en un directorio temporal vacío (0700) y devuelve stdout/stderr/rc/wall_ms."""
    tmpdir = Path(tempfile.mkdtemp(prefix="exp-"))
    os.chmod(tmpdir, 0o700)
    stdout = stderr = ""
    rc: int | None = None
    t0 = time.monotonic()
    try:
        env = {k: v for k, v in os.environ.items() if not k.startswith("GATEWAY_TOKEN_")}
        env.update(env_extra or {})
        try:
            p = subprocess.run(cmd, cwd=tmpdir, env=env, capture_output=True, text=True, timeout=timeout)
            stdout, stderr, rc = p.stdout, p.stderr, p.returncode
        except subprocess.TimeoutExpired as e:
            stdout = (e.stdout.decode() if isinstance(e.stdout, bytes) else e.stdout) or ""
            stderr = f"Tiempo agotado tras {timeout} s"
        except FileNotFoundError:
            stderr = "No se encontró el ejecutable 'claude' en el PATH"
    finally:
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)
    return {"stdout": stdout, "stderr": stderr, "returncode": rc, "wall_ms": int((time.monotonic() - t0) * 1000)}


def parse_claude_output(res: dict, secrets: list[str] | None = None) -> dict:
    """Mismos campos y criterios que run_agent.run_agent (que no expone esta lógica como función)."""
    secrets = secrets or []
    data = None
    try:
        parsed = json.loads(res["stdout"])
        if isinstance(parsed, dict):
            data = parsed
    except (json.JSONDecodeError, ValueError):
        pass
    if data is None:
        raw = ra._redact(f"[stdout]\n{res['stdout']}\n[stderr]\n{res['stderr']}\n[returncode] {res['returncode']}\n", secrets)
        return {**tokens_from_usage({}), "num_turns": None, "duration_ms": None, "duration_api_ms": None,
                "cost_usd_equiv": None, "is_error": True, "respuesta": raw,
                "error": ra._redact(res["stderr"].strip() or "Salida no JSON de claude", secrets)[:2000]}
    return {**tokens_from_usage(data.get("usage") or {}),
            "num_turns": data.get("num_turns"), "duration_ms": data.get("duration_ms"),
            "duration_api_ms": data.get("duration_api_ms"), "cost_usd_equiv": data.get("total_cost_usd"),
            "is_error": bool(data.get("is_error")) or res["returncode"] != 0,
            "respuesta": ra._redact(str(data.get("result") or ""), secrets), "error": None}


# --------------------------------------------------------------------------- un ítem (pregunta, brazo, rep)

def respuesta_path(qid: str, brazo: str, rep: int, run_id: str) -> Path:
    return RESULTS / "respuestas" / f"{qid}-{brazo}-r{rep}-{run_id}.md"


def _guardar_respuesta(path: Path, texto: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    ra._write_exclusive(path, texto)
    return str(path.relative_to(REPO)) if path.is_relative_to(REPO) else str(path)


def run_item_a(q: dict, item: dict, ctx: dict) -> dict:
    baseline = ctx["reset"]()  # BaselineError aborta toda la corrida
    rec = ra.run_agent("consultor", "consulta", modo="experimento", pregunta=q["texto"],
                       question_id=q["id"], model=ctx["model"], timeout=ctx.get("timeout"))
    run_id = rec["run_id"]
    texto = rec.get("respuesta") or ""
    if rec.get("is_error") and not texto:
        texto = f"[ERROR] {rec.get('error', '')}"
    path = _guardar_respuesta(respuesta_path(q["id"], "A", item["rep"], run_id), texto)
    keys = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens",
            "total_input_tokens", "num_turns", "duration_api_ms", "cost_usd_equiv", "is_error", "model")
    return {"run_id": run_id, **{k: rec.get(k) for k in keys}, "wall_ms": rec.get("wall_ms"),
            "latencia_total_ms": rec.get("wall_ms"), "retrieval_ms": None, "retrieval_wall_ms": None,
            "fragmentos": None, "retrieved_tokens": None, "respuesta_path": path,
            "error": rec.get("error"), "baseline_ok": True, "baseline": baseline.get("baseline"),
            "reset": baseline.get("accion")}


def run_item_b(q: dict, item: dict, ctx: dict) -> dict:
    run_id = uuid.uuid4().hex[:12]
    data, rwall = consultar_rag(ctx["rag_url"], q["texto"], ctx["k"], q["id"], ctx.get("rag_post", http_post_json))
    frags = data.get("fragments") or []
    prompt = build_prompt_b(q["texto"], format_fragments(frags))
    res = run_claude(build_command_b(prompt, ctx["model"]), timeout=ctx.get("timeout") or 600)
    p = parse_claude_output(res)
    texto = p["respuesta"] if not p["is_error"] or p["respuesta"] else f"[ERROR] {p['error']}"
    path = _guardar_respuesta(respuesta_path(q["id"], "B", item["rep"], run_id), texto)
    lat = data.get("latency_ms") or {}
    return {"run_id": run_id, **{k: p[k] for k in ("input_tokens", "cache_creation_input_tokens",
            "cache_read_input_tokens", "output_tokens", "total_input_tokens", "num_turns",
            "duration_api_ms", "cost_usd_equiv", "is_error", "error")},
            "model": ctx["model"], "wall_ms": res["wall_ms"], "latencia_total_ms": rwall + res["wall_ms"],
            "retrieval_ms": lat.get("retrieval_ms"), "retrieval_wall_ms": rwall,
            "fragmentos": [{"source": f.get("source"), "heading": f.get("heading"), "score": f.get("score")}
                           for f in frags],
            "retrieved_tokens": data.get("retrieved_tokens"), "respuesta_path": path,
            "baseline_ok": None}


def run_item(q: dict, item: dict, ctx: dict) -> dict:
    """Ejecuta un ítem y devuelve la fila del registro unificado. Errores de la pregunta se registran."""
    base = {"ts": now_iso(), "brazo": item["brazo"], "question_id": q["id"], "tipo": q["tipo"],
            "rep": item["rep"], "orden_idx": item.get("orden_idx"), "orden": ctx.get("orden"),
            "semilla": ctx.get("semilla"), "model": ctx["model"]}
    try:
        fn = run_item_a if item["brazo"] == "A" else run_item_b
        out = fn(q, item, ctx)
    except (BaselineError, KeyboardInterrupt):
        raise
    except (ra.AgentError, urllib.error.URLError, OSError, ValueError, KeyError) as e:
        out = {"run_id": uuid.uuid4().hex[:12], "is_error": True, "error": f"{type(e).__name__}: {e}"[:2000]}
    row = {**base, **out}
    if row.get("is_error") is None:
        row["is_error"] = False
    return row


def ejecutar(plan: list[dict], questions: dict[str, dict], ctx: dict, log=print) -> list[dict]:
    out_path = RESULTS / "experimento.jsonl"
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in plan:
        q = questions[item["question_id"]]
        log(f"[{item['orden_idx']}/{len(plan)}] {q['id']} brazo={item['brazo']} rep={item['rep']} ...")
        row = run_item(q, item, ctx)
        ra._append_jsonl(out_path, row)
        rows.append(row)
        estado = "ERROR " + str(row.get("error")) if row.get("is_error") else \
            f"ok entrada={row.get('total_input_tokens')} salida={row.get('output_tokens')} total={row.get('latencia_total_ms')} ms"
        log(f"    {estado}")
    return rows


def resumen(rows: list[dict]) -> str:
    lines = ["", "== Resumen =="]
    for b in BRAZOS:
        rs = [r for r in rows if r["brazo"] == b]
        if not rs:
            continue
        ok = [r for r in rs if not r.get("is_error")]
        lat = sorted(r["latencia_total_ms"] for r in ok if r.get("latencia_total_ms") is not None)
        med = lat[len(lat) // 2] if lat else None
        lines.append(f"Brazo {b}: {len(rs)} ejecuciones, {len(ok)} ok, {len(rs) - len(ok)} con error; "
                     f"latencia total mediana={med} ms; "
                     f"entrada total={sum(r.get('total_input_tokens') or 0 for r in ok)}; "
                     f"salida={sum(r.get('output_tokens') or 0 for r in ok)}")
    for r in rows:
        if r.get("is_error"):
            lines.append(f"  ERROR {r['question_id']} {r['brazo']} r{r['rep']}: {str(r.get('error'))[:200]}")
    return "\n".join(lines)


# --------------------------------------------------------------------------- overhead fijo del CLI

def overhead_item(config: str, model: str, rep: int, env_file: dict[str, str], timeout: int = 300) -> dict:
    """Mide un prompt trivial. B-sin-herramientas: configuración de B. A-mcp-sin-pregunta: configuración de A
    (MCP + herramientas de solo lectura), con prompt y system prompt triviales para que no lea nada."""
    token = None
    cfg = None
    tmp = None
    try:
        if config == "A-mcp-sin-pregunta":
            token = ra.get_config(ra.TOKEN_VARS["consultor"], env_file)
            if not token:
                raise ra.AgentError(f"Falta {ra.TOKEN_VARS['consultor']} en el entorno o en .env")
            tmp = Path(tempfile.mkdtemp(prefix="exp-oh-"))
            os.chmod(tmp, 0o700)
            cfg = tmp / "mcp.json"
            fd = os.open(cfg, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "w") as f:
                json.dump(ra.mcp_config(token, ra.get_config("GATEWAY_PORT", env_file, "8002")), f)
            cmd = ra.build_command("consultor", "consulta", "experimento", OVERHEAD_PROMPT, cfg, model)
            cmd[cmd.index("--system-prompt") + 1] = OVERHEAD_SYSTEM
        else:
            cmd = build_command_b(OVERHEAD_PROMPT, model, system=OVERHEAD_SYSTEM)
        res = run_claude(cmd, timeout=timeout)
    finally:
        if tmp:
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)
    p = parse_claude_output(res, [token] if token else [])
    return {"ts": now_iso(), "run_id": uuid.uuid4().hex[:12], "config": config, "rep": rep, "model": model,
            "prompt": OVERHEAD_PROMPT, **{k: p[k] for k in ("input_tokens", "cache_creation_input_tokens",
            "cache_read_input_tokens", "output_tokens", "total_input_tokens", "num_turns", "duration_api_ms",
            "cost_usd_equiv", "is_error", "error")}, "wall_ms": res["wall_ms"]}


def run_overhead(n: int, model: str, env_file: dict[str, str], log=print) -> list[dict]:
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows = []
    for rep in range(1, n + 1):
        for config in ("B-sin-herramientas", "A-mcp-sin-pregunta"):
            try:
                row = overhead_item(config, model, rep, env_file)
            except ra.AgentError as e:
                row = {"ts": now_iso(), "run_id": uuid.uuid4().hex[:12], "config": config, "rep": rep,
                       "model": model, "is_error": True, "error": str(e)}
            ra._append_jsonl(RESULTS / "overhead.jsonl", row)
            rows.append(row)
            log(f"overhead {config} r{rep}: entrada_total={row.get('total_input_tokens')} "
                f"error={row.get('error')}")
    return rows


# --------------------------------------------------------------------------- CLI

def print_plan(plan, questions, model, k, rag_url, orden, semilla) -> None:
    print(f"# DRY-RUN: no se ejecuta nada. modelo={model} k={k} orden={orden} semilla={semilla}")
    print(f"# {len(plan)} ejecuciones. Resultados irían a {RESULTS / 'experimento.jsonl'}")
    for it in plan:
        print(f"{it['orden_idx']:>3}. {it['question_id']} brazo={it['brazo']} rep={it['rep']}")
    brazos = {it["brazo"] for it in plan}
    if "A" in brazos:
        print("\n# Antes de CADA ejecución del brazo A (reset del estado):")
        for cmd in (_gw("-C", VAULT_IN_CONTAINER, "rev-parse", "main"),
                    _gw("-C", VAULT_IN_CONTAINER, "rev-parse", f"{BASELINE_TAG}^{{commit}}"),
                    _gw("-C", WORKTREE_CONSULTOR, "reset", "--hard", BASELINE_TAG),
                    _gw("-C", WORKTREE_CONSULTOR, "clean", "-fd")):
            print("  " + " ".join(shlex.quote(c) for c in cmd))
        print("# Comando brazo A (cwd: dir temporal vacío; el token va en mcp.json, aquí redactado):")
        prompt = ra.build_prompt("consulta", "experimento", "<pregunta>", None)
        print("  " + " ".join(shlex.quote(c) for c in ra.build_command(
            "consultor", "consulta", "experimento", prompt, "<tmpdir>/mcp.json", model)))
        print(f"  mcp-config: {json.dumps(ra.mcp_config('***', '<GATEWAY_PORT>'))}")
    if "B" in brazos:
        print(f"\n# Brazo B: POST {rag_url}/query " + json.dumps(
            {"question": "<pregunta>", "k": k, "question_id": "<id>", "use_llm": False}))
        print("# Comando brazo B (cwd: dir temporal vacío, sin herramientas ni MCP):")
        prompt = build_prompt_b("<pregunta>", "<fragmentos recuperados>")
        print("  " + " ".join(shlex.quote(c) for c in build_command_b(prompt, model)))


def parse_ids(s: str, all_ids: list[str]) -> list[str]:
    if s.strip().lower() == "todas":
        return all_ids
    ids = [x.strip().upper() for x in s.split(",") if x.strip()]
    bad = [i for i in ids if i not in all_ids]
    if bad:
        raise ExperimentError(f"Preguntas inexistentes: {', '.join(bad)}")
    return ids


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Experimento KB-A vs KB-B (mismo modelo, claude -p)")
    ap.add_argument("--brazo", choices=["A", "B", "ambos"], default="ambos")
    ap.add_argument("--ids", default="todas", help="P01,P02 o 'todas'")
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--orden", choices=["intercalado", "aleatorio"], default="intercalado")
    ap.add_argument("--semilla", type=int)
    ap.add_argument("--model", help="por defecto KBA_MODEL o claude-sonnet-5-5 (el mismo en A y B)")
    ap.add_argument("--k", type=int, help="top-k de KB-B (por defecto RAG_TOP_K de .env o 5)")
    ap.add_argument("--rag-url", help="por defecto http://127.0.0.1:${RAG_PORT:-8001}")
    ap.add_argument("--timeout", type=int, help="s por ejecución de claude (por defecto 600)")
    ap.add_argument("--overhead", type=int, metavar="N", help="mide N veces el overhead fijo del CLI y sale")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    try:
        env_file = ra.load_env(REPO / ".env")
        model = resolve_model(a.model, env_file)
        if os.environ.pop("ANTHROPIC_API_KEY", None):  # que claude use la suscripción, no una API de pago
            print("AVISO: se ignoró ANTHROPIC_API_KEY del entorno (el experimento usa la suscripción).",
                  file=sys.stderr)
        k = a.k or int(ra.get_config("RAG_TOP_K", env_file, "5"))
        rag_url = rag_base_url(env_file, a.rag_url)

        if a.overhead:
            if a.dry_run:
                print(f"# DRY-RUN overhead x{a.overhead}, modelo={model}: prompt {OVERHEAD_PROMPT!r} con la "
                      f"configuración de B y la de A (MCP, sin pregunta) -> {RESULTS / 'overhead.jsonl'}")
                print("  " + " ".join(shlex.quote(c) for c in build_command_b(OVERHEAD_PROMPT, model, OVERHEAD_SYSTEM)))
                return 0
            run_overhead(a.overhead, model, env_file)
            return 0

        if a.reps < 1:
            raise ExperimentError("--reps debe ser >= 1")
        all_q = load_questions()
        ids = parse_ids(a.ids, [q["id"] for q in all_q])
        brazos = list(BRAZOS) if a.brazo == "ambos" else [a.brazo]
        semilla = a.semilla
        if a.orden == "aleatorio" and semilla is None:
            semilla = random.SystemRandom().randrange(2**31)
            print(f"AVISO: sin --semilla; se usa {semilla} (queda registrada).", file=sys.stderr)
        plan = build_plan(ids, brazos, a.reps, a.orden, semilla)
        questions = {q["id"]: q for q in all_q}

        if a.dry_run:
            print_plan(plan, questions, model, k, rag_url, a.orden, semilla)
            return 0

        if "B" in brazos:  # solo lectura
            try:
                with urllib.request.urlopen(f"{rag_url}/health", timeout=10) as r:
                    r.read()
            except (urllib.error.URLError, OSError) as e:
                raise ExperimentError(f"KB-B no responde en {rag_url}/health: {e}") from e
        ctx = {"model": model, "k": k, "rag_url": rag_url, "reset": reset_kba, "timeout": a.timeout,
               "orden": a.orden, "semilla": semilla}
        rows = ejecutar(plan, questions, ctx)
        print(resumen(rows))
        return 1 if any(r.get("is_error") for r in rows) else 0
    except BaselineError as e:
        print(f"\nABORTADO por la línea base de KB-A: {e}", file=sys.stderr)
        return 3
    except ExperimentError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
