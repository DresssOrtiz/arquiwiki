#!/usr/bin/env python3
"""Mide el costo de actualizar un documento fuente en KB-A y KB-B (protocolo 4.4, paso 6).

ADVERTENCIA: se ejecuta DESPUÉS del experimento principal. Modifica `raw/` del vault de ejecución
(.runtime/vault) con un commit en main y fusiona el trabajo del ingestor, así que CAMBIA la línea base
`kb-a-baseline`. Para volver al estado original: `python3 experiment/costo_actualizacion.py --restaurar`.

  python3 experiment/costo_actualizacion.py --archivo raw/2-2-atributos-de-calidad-1.md --dry-run
  python3 experiment/costo_actualizacion.py --archivo raw/2-2-atributos-de-calidad-1.md --yes
  python3 experiment/costo_actualizacion.py --restaurar --yes

Cómo se modifica el archivo: se añade una diapositiva marcada al final de la copia de `raw/<x>.md` que
hay en el vault de ejecución (la semilla versionada kb-wiki/vault/ no se toca). El gateway no puede
escribir en raw/ (es de solo lectura para los agentes), así que la escritura la hace este script desde
el host en `.runtime/vault` y el commit en main se hace dentro del contenedor mcp-gateway
(`docker compose exec ... git -c safe.directory='*'`), con el mismo git que usa el vault.
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
import time
import uuid
from pathlib import Path

EXP = Path(__file__).resolve().parent
REPO = EXP.parent
RESULTS = EXP / "results"
sys.path.insert(0, str(REPO / "kb-wiki" / "agents"))
import run_agent as ra  # noqa: E402

VAULT_HOST = REPO / ".runtime" / "vault"
BASELINE_TAG = "kb-a-baseline"
ROLES = ("ingestor", "consultor", "auditor")
GIT = ["git", "-c", "safe.directory=*", "-c", "user.name=arquiwiki-experimento",
       "-c", "user.email=experimento@arquiwiki.local"]


class ActualizacionError(Exception):
    pass


def default_runner(cmd: list[str], timeout: int = 300) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def gw(*args: str) -> list[str]:
    return ["docker", "compose", "exec", "-T", "mcp-gateway", *GIT, *args]


def validar_archivo(archivo: str) -> str:
    if not re.fullmatch(r"raw/[A-Za-z0-9._-]+\.md", archivo):
        raise ActualizacionError(f"--archivo debe ser raw/<nombre>.md (recibido {archivo!r})")
    return archivo


def bloque_marcado(texto_actual: str, marcador: str) -> str:
    """Diapositiva nueva al final, con un dato único y fácil de buscar en consultas."""
    nums = [int(n) for n in re.findall(r"(?m)^## Diapositiva (\d+)\s*$", texto_actual)]
    n = (max(nums) if nums else 0) + 1
    return (f"\n## Diapositiva {n}\n\n[ACTUALIZACION CONTROLADA DEL EXPERIMENTO] "
            f"El código de verificación de esta diapositiva añadida es {marcador}.\n")


def modificar_vault(archivo: str, marcador: str, runner=default_runner, vault: Path = VAULT_HOST) -> str:
    """Añade la diapositiva marcada y hace commit en main. Devuelve el hash del commit."""
    path = vault / archivo
    if not path.is_file():
        raise ActualizacionError(f"No existe {path}")
    path.write_text(path.read_text(encoding="utf-8") + bloque_marcado(path.read_text(encoding="utf-8"), marcador),
                    encoding="utf-8")
    for cmd in (gw("-C", "/vault", "add", archivo),
                gw("-C", "/vault", "commit", "-q", "-m", f"experimento: actualización controlada de {archivo}")):
        rc, out, err = runner(cmd)
        if rc != 0:
            raise ActualizacionError(f"Falló {' '.join(cmd[-3:])} en el contenedor: {err.strip() or out.strip()}. "
                                     f"Alternativa documentada: git -C .runtime/vault desde el host.")
    rc, out, err = runner(gw("-C", "/vault", "rev-parse", "HEAD"))
    return out.strip()


def _post(url: str, payload: dict, timeout: int = 300) -> dict:
    import urllib.request
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"},
                                 method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def actualizar_b(archivo: str, marcador: str, rag_url: str, k: int, post=_post) -> dict:
    t0 = time.perf_counter()
    res = post(f"{rag_url}/index", {"path": archivo})
    elapsed = int((time.perf_counter() - t0) * 1000)
    q = post(f"{rag_url}/query", {"question": f"código de verificación {marcador}", "k": k,
                                  "question_id": "ACT", "use_llm": False})
    refleja = any(marcador in (f.get("text") or "") for f in q.get("fragments", []))
    return {"brazo": "B", "modo": res.get("mode"), "files_changed": res.get("files_changed"),
            "chunks_written": res.get("chunks_written"), "embedded_tokens": res.get("embedded_tokens"),
            "llm_total_input_tokens": 0, "llm_output_tokens": 0,
            "elapsed_ms": res.get("elapsed_ms", elapsed), "elapsed_wall_ms": elapsed, "refleja": refleja,
            "is_error": False}


def actualizar_a(archivo: str, marcador: str, runner=default_runner, agent=ra.run_agent, model: str | None = None) -> dict:
    t0 = time.perf_counter()
    rec = agent("ingestor", "ingesta", modo="demo", fuente=archivo, model=model)
    merge = runner([str(REPO / "scripts" / "merge-agents.sh")])
    elapsed = int((time.perf_counter() - t0) * 1000)
    rc, out, _ = runner(gw("-C", "/vault", "grep", "-l", marcador, "main", "--", "wiki"))
    return {"brazo": "A", "run_id_agente": rec.get("run_id"), "model": rec.get("model"),
            "llm_total_input_tokens": rec.get("total_input_tokens"),
            "llm_input_tokens": rec.get("input_tokens"),
            "llm_cache_creation_input_tokens": rec.get("cache_creation_input_tokens"),
            "llm_cache_read_input_tokens": rec.get("cache_read_input_tokens"),
            "llm_output_tokens": rec.get("output_tokens"), "num_turns": rec.get("num_turns"),
            "agente_wall_ms": rec.get("wall_ms"), "elapsed_ms": elapsed, "embedded_tokens": 0,
            "merge_rc": merge[0], "refleja": rc == 0 and bool(out.strip()),
            "paginas_con_marcador": out.strip().replace("main:", "").splitlines(),
            "is_error": bool(rec.get("is_error")) or merge[0] != 0,
            "error": rec.get("error") or (merge[2].strip() if merge[0] != 0 else None)}


def restaurar(rag_url: str, runner=default_runner, post=_post, dry: bool = False) -> list[list[str]]:
    """Devuelve el vault a kb-a-baseline y reindexa KB-B con force. Requiere --yes."""
    cmds = [gw("-C", "/vault", "reset", "--hard", BASELINE_TAG), gw("-C", "/vault", "clean", "-fd")]
    for rol in ROLES:
        cmds.append(["docker", "compose", "exec", "-T", "mcp-gateway", "sh", "-c",
                     f"if [ -d /worktrees/{rol} ]; then git -c safe.directory='*' -C /worktrees/{rol} reset --hard "
                     f"{BASELINE_TAG} && git -c safe.directory='*' -C /worktrees/{rol} clean -fd; "
                     f"else git -c safe.directory='*' -C /vault branch -f agent/{rol} {BASELINE_TAG} 2>/dev/null || true; fi"])
    if dry:
        return cmds
    for cmd in cmds:
        rc, out, err = runner(cmd)
        if rc != 0:
            raise ActualizacionError(f"Falló la restauración ({shlex.join(cmd[-3:])}): {err.strip()}")
    post(f"{rag_url}/index", {"force": True})
    return cmds


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Costo de actualización KB-A vs KB-B (ejecutar tras el experimento)")
    ap.add_argument("--archivo", default="raw/2-2-atributos-de-calidad-1.md")
    ap.add_argument("--model")
    ap.add_argument("--k", type=int)
    ap.add_argument("--rag-url")
    ap.add_argument("--restaurar", action="store_true", help="vuelve el vault a kb-a-baseline y reindexa KB-B")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--yes", action="store_true", help="confirma que el experimento principal ya terminó")
    a = ap.parse_args(argv)
    env = ra.load_env(REPO / ".env")
    rag_url = (a.rag_url or f"http://127.0.0.1:{ra.get_config('RAG_PORT', env, '8001')}").rstrip("/")
    k = a.k or int(ra.get_config("RAG_TOP_K", env, "5"))
    model = a.model or ra.get_config("KBA_MODEL", env, ra.DEFAULT_MODEL)
    try:
        if a.restaurar:
            cmds = restaurar(rag_url, dry=a.dry_run) if (a.dry_run or a.yes) else None
            if cmds is None:
                raise ActualizacionError("Restaurar descarta el trabajo posterior a kb-a-baseline: añade --yes")
            if a.dry_run:
                print("# DRY-RUN restaurar:")
                for c in cmds:
                    print("  " + shlex.join(c))
                print(f"  POST {rag_url}/index " + json.dumps({"force": True}))
            else:
                print("Vault restaurado a kb-a-baseline y KB-B reindexado (force).")
            return 0
        archivo = validar_archivo(a.archivo)
        marcador = f"ACT-{uuid.uuid4().hex[:8]}"
        if a.dry_run:
            print("# DRY-RUN (no se ejecuta nada). ADVERTENCIA: la ejecución real cambia la línea base kb-a-baseline.")
            print(f"1. Añadir una diapositiva marcada ({marcador}) a .runtime/vault/{archivo} y commit en main:")
            print("   " + shlex.join(gw("-C", "/vault", "add", archivo)))
            print("   " + shlex.join(gw("-C", "/vault", "commit", "-q", "-m", "experimento: actualización controlada")))
            print(f"2. KB-B: POST {rag_url}/index " + json.dumps({"path": archivo}) + "  (registra rag_builds.jsonl, incremental)")
            print(f"   y POST {rag_url}/query use_llm=false para comprobar que el marcador se recupera")
            print(f"3. KB-A: run_agent('ingestor','ingesta',modo='demo',fuente={archivo!r}, model={model!r}) + scripts/merge-agents.sh")
            print(f"   y git grep del marcador en wiki/ de main")
            print(f"4. Salida: {RESULTS / 'actualizacion.jsonl'}")
            print("5. Restaurar después: python3 experiment/costo_actualizacion.py --restaurar --yes")
            return 0
        if not a.yes:
            raise ActualizacionError("Esto cambia la línea base de KB-A. Confirma que el experimento principal "
                                     "terminó y repite con --yes")
        commit = modificar_vault(archivo, marcador)
        base = {"ts": ra._now().strftime("%Y-%m-%dT%H:%M:%SZ"), "archivo": archivo, "marcador": marcador,
                "commit": commit}
        RESULTS.mkdir(parents=True, exist_ok=True)
        for fn in (lambda: actualizar_b(archivo, marcador, rag_url, k),
                   lambda: actualizar_a(archivo, marcador, model=model)):
            try:
                row = fn()
            except Exception as e:  # se registra y se sigue con el otro brazo
                row = {"brazo": "?", "is_error": True, "error": f"{type(e).__name__}: {e}"[:2000]}
            row = {**base, "run_id": uuid.uuid4().hex[:12], **row}
            ra._append_jsonl(RESULTS / "actualizacion.jsonl", row)
            print(json.dumps(row, ensure_ascii=False))
        return 0
    except ActualizacionError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
