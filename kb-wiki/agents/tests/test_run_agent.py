"""Pruebas de run_agent.py con un `claude` falso (nunca se ejecuta el real)."""
import json
import os
import stat
import sys
import textwrap
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_agent as ra  # noqa: E402

TOKENS = {"INGESTOR": "tok-ingestor-SECRETO1", "CONSULTOR": "tok-consultor-SECRETO2",
          "AUDITOR": "tok-auditor-SECRETO3"}

FAKE = textwrap.dedent('''\
    #!/usr/bin/env python3
    import json, os, sys
    a = sys.argv[1:]
    def opt(n): return a[a.index(n) + 1]
    cap = {"args": a, "cwd": os.getcwd(), "cwd_listing": sorted(os.listdir(os.getcwd())),
           "mcp_path": opt("--mcp-config"), "mcp": json.load(open(opt("--mcp-config"))),
           "mcp_mode": oct(os.stat(opt("--mcp-config")).st_mode & 0o777),
           "cwd_mode": oct(os.stat(os.getcwd()).st_mode & 0o777),
           "env_tokens": [k for k in os.environ if k.startswith("GATEWAY_TOKEN_")]}
    open(os.environ["FAKE_CAPTURE"], "w").write(json.dumps(cap))
    for flag in ("--strict-mcp-config", "--no-session-persistence", "--disable-slash-commands"):
        assert flag in a, flag
    assert opt("--tools") == "" and opt("--setting-sources") == ""
    assert opt("--output-format") == "json"
    auth = cap["mcp"]["mcpServers"]["arquiwiki"]["headers"]["Authorization"]
    mode = os.environ.get("FAKE_MODE", "ok")
    if mode == "crash":
        sys.stderr.write("boom con " + auth)
        sys.exit(3)
    if mode == "garbage":
        print("esto no es json " + auth)
        sys.exit(0)
    out = {"type": "result", "is_error": mode == "iserror", "result": "respuesta de prueba",
           "num_turns": 4, "duration_ms": 1234, "duration_api_ms": 1000, "total_cost_usd": 0.0123,
           "session_id": "s", "usage": {"input_tokens": 10, "cache_creation_input_tokens": 200,
           "cache_read_input_tokens": 3000, "output_tokens": 55}, "modelUsage": {}}
    print(json.dumps(out))
''')


@pytest.fixture
def env(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    (root / ".env").write_text(
        "# comentario\nGATEWAY_PORT=9999\n"
        + "".join(f"GATEWAY_TOKEN_{k}={v}\n" for k, v in TOKENS.items()))
    bindir = tmp_path / "bin"
    bindir.mkdir()
    fake = bindir / "claude"
    fake.write_text(FAKE)
    fake.chmod(fake.stat().st_mode | stat.S_IEXEC)
    capture = tmp_path / "capture.json"
    monkeypatch.setattr(ra, "ROOT", root)
    monkeypatch.setenv("PATH", f"{bindir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("FAKE_CAPTURE", str(capture))
    monkeypatch.delenv("FAKE_MODE", raising=False)
    for k in TOKENS:
        monkeypatch.delenv(f"GATEWAY_TOKEN_{k}", raising=False)
    monkeypatch.delenv("GATEWAY_PORT", raising=False)
    monkeypatch.delenv("KBA_MODEL", raising=False)
    return root, capture


def cap(capture):
    return json.loads(capture.read_text())


def tools_of(c):
    return c["args"][c["args"].index("--allowedTools") + 1].split(",")


def last_row(root):
    return json.loads((root / "experiment/results/kba_runs.jsonl").read_text().splitlines()[-1])


def test_consultor_experimento_sin_escritura(env):
    _, capture = env
    ra.run_agent("consultor", "consulta", "experimento", pregunta="¿Qué es X?", question_id="P01")
    t = tools_of(cap(capture))
    assert "mcp__arquiwiki__write_note" not in t and "mcp__arquiwiki__commit_changes" not in t
    assert "mcp__arquiwiki__read_note" in t and "mcp__arquiwiki__search_notes" in t


@pytest.mark.parametrize("rol,op,modo", [("consultor", "consulta", "demo"),
                                         ("ingestor", "ingesta", "demo"),
                                         ("auditor", "lint", "demo")])
def test_roles_con_todas_las_herramientas(env, rol, op, modo):
    _, capture = env
    ra.run_agent(rol, op, modo, pregunta="p")
    assert set(tools_of(cap(capture))) == {f"mcp__arquiwiki__{x}" for x in ra.ALL_TOOLS}


@pytest.mark.parametrize("rol,op,esquema", [("ingestor", "ingesta", "CLAUDE.md"),
                                            ("consultor", "consulta", "AGENTS.md"),
                                            ("auditor", "lint", "GEMINI.md")])
def test_system_prompt_cita_esquema(env, rol, op, esquema):
    _, capture = env
    ra.run_agent(rol, op, "demo", pregunta="p")
    a = cap(capture)["args"]
    sp = a[a.index("--system-prompt") + 1]
    assert f"agente {rol}" in sp and esquema in sp and "CONVENCIONES.md" in sp
    assert not any(o in sp for o in {"CLAUDE.md", "AGENTS.md", "GEMINI.md"} - {esquema})


def test_config_mcp_aislamiento_y_borrado(env):
    _, capture = env
    ra.run_agent("auditor", "lint", "demo")
    c = cap(capture)
    srv = c["mcp"]["mcpServers"]["arquiwiki"]
    assert srv["url"] == "http://127.0.0.1:9999/mcp"
    assert srv["headers"]["Authorization"] == f"Bearer {TOKENS['AUDITOR']}"
    assert c["mcp_mode"] == "0o600" and c["cwd_mode"] == "0o700"
    assert c["cwd_listing"] == ["mcp.json"]
    assert not Path(c["cwd"]).exists() and not Path(c["mcp_path"]).exists()
    assert c["env_tokens"] == []
    assert c["args"][c["args"].index("--model") + 1] == "claude-sonnet-5-5"


def test_registro_y_total_input_tokens(env):
    root, _ = env
    rec = ra.run_agent("consultor", "consulta", "experimento", pregunta="q", question_id="P07")
    assert rec["total_input_tokens"] == 10 + 200 + 3000
    assert rec["output_tokens"] == 55 and rec["cost_usd_equiv"] == 0.0123 and rec["motor"] == "claude"
    row = last_row(root)
    assert row["question_id"] == "P07" and row["total_input_tokens"] == 3210 and row["wall_ms"] >= 0
    assert row["is_error"] is False and row["num_turns"] == 4 and "respuesta" not in row
    assert (root / row["respuesta_path"]).read_text() == "respuesta de prueba"
    assert row["respuesta_path"].endswith(f"-consultor-consulta-P07-{row['run_id']}.md")


def test_run_id_unico_con_misma_marca_de_tiempo(env, monkeypatch):
    from datetime import datetime, timezone
    root, _ = env
    monkeypatch.setattr(ra, "_now", lambda: datetime(2026, 11, 25, 10, 0, 0, tzinfo=timezone.utc))
    r1 = ra.run_agent("consultor", "consulta", "experimento", pregunta="q", question_id="P01")
    monkeypatch.setenv("FAKE_MODE", "garbage")  # segunda corrida con otro contenido
    r2 = ra.run_agent("consultor", "consulta", "experimento", pregunta="q", question_id="P01")
    assert r1["run_id"] != r2["run_id"] and r1["respuesta_path"] != r2["respuesta_path"]
    rows = [json.loads(l) for l in (root / "experiment/results/kba_runs.jsonl").read_text().splitlines()]
    assert [r["run_id"] for r in rows] == [r1["run_id"], r2["run_id"]]
    assert rows[0]["ts"] == rows[1]["ts"]
    assert r1["run_id"] in r1["respuesta_path"]
    assert (root / r1["respuesta_path"]).read_text() == "respuesta de prueba"
    assert "[stdout]" in (root / r2["respuesta_path"]).read_text()
    assert len(list((root / "experiment/results/kba_runs").iterdir())) == 2


def test_escritura_exclusiva_no_sobrescribe(tmp_path):
    f = tmp_path / "x.md"
    ra._write_exclusive(f, "a")
    with pytest.raises(FileExistsError):
        ra._write_exclusive(f, "b")
    assert f.read_text() == "a"


def test_token_nunca_aparece(env, capsys, monkeypatch):
    root, _ = env
    ra.main(["consultor", "--op", "consulta", "--pregunta", "q", "--dry-run"])
    ra.main(["consultor", "--op", "consulta", "--pregunta", "q"])
    for mode in ("crash", "garbage"):
        monkeypatch.setenv("FAKE_MODE", mode)
        ra.main(["consultor", "--op", "consulta", "--pregunta", "q"])
    out = capsys.readouterr()
    blob = out.out + out.err + (root / "experiment/results/kba_runs.jsonl").read_text()
    for f in (root / "experiment/results/kba_runs").iterdir():
        blob += f.read_text()
    assert not any(t in blob for t in TOKENS.values())
    assert "***" in out.out


def test_dry_run_no_ejecuta(env, capsys):
    root, capture = env
    assert ra.main(["ingestor", "--op", "ingesta", "--fuente", "raw/x.md", "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "raw/x.md" in out and "--allowedTools" in out
    assert not capture.exists() and not (root / "experiment").exists()


def test_error_is_error(env, monkeypatch):
    root, _ = env
    monkeypatch.setenv("FAKE_MODE", "iserror")
    assert ra.main(["auditor", "--op", "lint"]) == 1
    assert last_row(root)["is_error"] is True


def test_proceso_falla(env, monkeypatch):
    root, _ = env
    monkeypatch.setenv("FAKE_MODE", "crash")
    assert ra.main(["auditor", "--op", "lint"]) == 1
    row = last_row(root)
    assert row["is_error"] is True and "boom" in row["error"] and "SECRETO" not in row["error"]


def test_salida_no_json(env, monkeypatch):
    root, _ = env
    monkeypatch.setenv("FAKE_MODE", "garbage")
    rec = ra.run_agent("auditor", "lint", "demo")
    assert rec["is_error"] is True and rec["total_input_tokens"] == 0
    raw = (root / rec["respuesta_path"]).read_text()
    assert "esto no es json" in raw and "SECRETO" not in raw


def test_validaciones(env, capsys):
    assert ra.main(["consultor", "--op", "lint"]) == 2
    assert ra.main(["consultor", "--op", "consulta"]) == 2
    assert "Error" in capsys.readouterr().err


def test_falta_token(env):
    root, _ = env
    (root / ".env").write_text("GATEWAY_PORT=1\n")
    assert ra.main(["auditor", "--op", "lint"]) == 2


def test_entorno_tiene_prioridad_y_modelo(env, monkeypatch):
    _, capture = env
    monkeypatch.setenv("GATEWAY_TOKEN_AUDITOR", "otro-token-ENV")
    monkeypatch.setenv("GATEWAY_PORT", "7777")
    ra.run_agent("auditor", "lint", "demo", model="m-x")
    c = cap(capture)
    srv = c["mcp"]["mcpServers"]["arquiwiki"]
    assert srv["url"].endswith(":7777/mcp") and srv["headers"]["Authorization"] == "Bearer otro-token-ENV"
    assert c["args"][c["args"].index("--model") + 1] == "m-x"


def test_plantillas_sustituyen_variables():
    for op in ra.OP_ROLE:
        assert "$" not in ra.build_prompt(op, "demo", "¿Pregunta?", "raw/a.md")
    assert "¿Pregunta?" in ra.build_prompt("consulta", "demo", "¿Pregunta?", None)
    assert "raw/a.md" in ra.build_prompt("ingesta", "demo", None, "raw/a.md")
