"""Pruebas del experimento con `claude` falso y RAG falso (nunca se ejecuta el real)."""
import csv
import importlib.util
import json
import os
import stat
import sys
import textwrap
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

EXP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXP.parent / "kb-wiki" / "agents"))
import run_agent as ra  # noqa: E402


def _load(name):
    spec = importlib.util.spec_from_file_location(f"exp_{name}", EXP / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m


run = _load("run")
cal = _load("calificacion")
rep = _load("reporte")

FRAGS = [
    {"source": "raw/1-2-definiciones-1.md", "heading": "1.2 Definiciones 1 > Diapositiva 41", "score": 0.81,
     "tokens": 30, "text": "SRP: una clase tiene una sola razón FRAGMENTO-UNO"},
    {"source": "raw/1-2-definiciones-1.md", "heading": "1.2 Definiciones 1 > Diapositiva 42", "score": 0.7,
     "tokens": 20, "text": "DIP: depender de abstracciones FRAGMENTO-DOS"},
]

FAKE = textwrap.dedent('''\
    #!/usr/bin/env python3
    import json, os, sys
    a = sys.argv[1:]
    with open(os.environ["FAKE_CAPTURE"], "a") as f:
        f.write(json.dumps({"args": a, "cwd": os.getcwd(), "listing": os.listdir(os.getcwd())}) + "\\n")
    out = {"type": "result", "is_error": os.environ.get("FAKE_MODE") == "iserror",
           "result": "Respuesta falsa\\n\\n## Fuentes\\n- Raw: raw/x.md, diap. 1",
           "num_turns": 3, "duration_ms": 900, "duration_api_ms": 800, "total_cost_usd": 0.01,
           "usage": {"input_tokens": 5, "cache_creation_input_tokens": 100, "cache_read_input_tokens": 1000,
                     "output_tokens": 40}}
    print(json.dumps(out))
''')


@pytest.fixture
def env(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    (root / "experiment" / "results").mkdir(parents=True)
    (root / ".env").write_text("GATEWAY_PORT=9999\nGATEWAY_TOKEN_CONSULTOR=tok-consultor-SECRETO\n"
                               "GATEWAY_TOKEN_INGESTOR=tok-ing\nGATEWAY_TOKEN_AUDITOR=tok-aud\n")
    bindir = tmp_path / "bin"
    bindir.mkdir()
    fake = bindir / "claude"
    fake.write_text(FAKE)
    fake.chmod(fake.stat().st_mode | stat.S_IEXEC)
    capture = tmp_path / "capture.jsonl"
    monkeypatch.setattr(ra, "ROOT", root)
    monkeypatch.setattr(run, "REPO", root)
    monkeypatch.setattr(run, "RESULTS", root / "experiment" / "results")
    monkeypatch.setenv("PATH", f"{bindir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("FAKE_CAPTURE", str(capture))
    for v in ("KBA_MODEL", "FAKE_MODE", "ANTHROPIC_API_KEY", "RAG_PORT", "RAG_TOP_K"):
        monkeypatch.delenv(v, raising=False)
    return root, capture


@pytest.fixture
def rag():
    seen = []

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, obj):
            b = json.dumps(obj).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

        def do_GET(self):
            self._send({"status": "ok"})

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            seen.append((self.path, body))
            self._send({"question": body["question"], "fragments": FRAGS, "retrieved_tokens": 50,
                        "latency_ms": {"retrieval_ms": 12, "generation_ms": 0, "total_ms": 12}})

    srv = HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_port}", seen
    srv.shutdown()


def calls(capture):
    return [json.loads(x) for x in capture.read_text().splitlines()]


def opt(args, name):
    return args[args.index(name) + 1]


def ctx(model="claude-sonnet-5-5", rag_url="http://x", reset=None, **kw):
    return {"model": model, "k": 5, "rag_url": rag_url, "reset": reset or (lambda: {"baseline": "abc", "accion": "x"}),
            "orden": "intercalado", "semilla": None, **kw}


def claves():
    return json.loads((EXP / "claves.json").read_text(encoding="utf-8"))


# ------------------------------------------------------------------ preguntas y claves

def test_preguntas_sin_claves():
    qs = json.loads((EXP / "preguntas.json").read_text(encoding="utf-8"))
    assert [q["id"] for q in qs] == [f"P{i:02d}" for i in range(1, 16)]
    assert all(set(q) == {"id", "tipo", "texto"} for q in qs)
    tipos = [q["tipo"] for q in qs]
    assert [tipos.count(t) for t in dict.fromkeys(tipos)] == [5, 4, 4, 2]
    blob = json.dumps(qs, ensure_ascii=False)
    for c in claves():
        assert c["respuesta_referencia"] not in blob and c["fuente_verificable"] not in blob
    assert [c["id"] for c in claves()] == [q["id"] for q in qs]


def test_run_py_no_lee_claves():
    src = (EXP / "run.py").read_text(encoding="utf-8")
    assert "claves.json" not in src and "respuesta_referencia" not in src


# ------------------------------------------------------------------ brazo B

def test_prompt_b_tiene_fragmentos_y_nunca_claves(env, rag):
    root, capture = env
    url, seen = rag
    q = run.load_questions(["P03"])[0]
    row = run.run_item(q, {"brazo": "B", "rep": 1, "orden_idx": 1}, ctx(rag_url=url))
    assert not row["is_error"], row
    assert seen[0][0] == "/query" and seen[0][1] == {"question": q["texto"], "k": 5, "question_id": "P03", "use_llm": False}
    c = calls(capture)[0]["args"]
    prompt = c[c.index("-p") + 1]
    assert "FRAGMENTO-UNO" in prompt and "FRAGMENTO-DOS" in prompt and q["texto"] in prompt
    assert "raw/1-2-definiciones-1.md" in prompt and "Diapositiva 41" in prompt
    sysp = opt(c, "--system-prompt")
    for clave in claves():
        assert clave["respuesta_referencia"] not in prompt + sysp
        assert clave["fuente_verificable"] not in prompt + sysp
    assert row["retrieval_ms"] == 12 and row["retrieval_wall_ms"] is not None and row["retrieved_tokens"] == 50
    assert row["fragmentos"] == [{"source": f["source"], "heading": f["heading"], "score": f["score"]} for f in FRAGS]
    assert row["latencia_total_ms"] == row["retrieval_wall_ms"] + row["wall_ms"]
    assert row["total_input_tokens"] == 5 + 100 + 1000


def test_b_aislamiento_sin_herramientas(env, rag):
    root, capture = env
    q = run.load_questions(["P01"])[0]
    run.run_item(q, {"brazo": "B", "rep": 1}, ctx(rag_url=rag[0]))
    c = calls(capture)[0]
    a = c["args"]
    assert opt(a, "--tools") == "" and opt(a, "--setting-sources") == ""
    assert opt(a, "--mcp-config") == '{"mcpServers":{}}'
    for flag in ("--strict-mcp-config", "--disable-slash-commands", "--no-session-persistence"):
        assert flag in a
    assert "--allowedTools" not in a and opt(a, "--output-format") == "json"
    assert c["listing"] == []  # cwd temporal vacío


# ------------------------------------------------------------------ equidad: mismo modelo

def test_mismo_modelo_en_a_y_b(env, rag):
    root, capture = env
    q = run.load_questions(["P01"])[0]
    c = ctx(model="modelo-x", rag_url=rag[0])
    ra_row = run.run_item(q, {"brazo": "A", "rep": 1}, c)
    rb_row = run.run_item(q, {"brazo": "B", "rep": 1}, c)
    cs = calls(capture)
    assert [opt(x["args"], "--model") for x in cs] == ["modelo-x", "modelo-x"]
    assert ra_row["model"] == rb_row["model"] == "modelo-x"
    # mismas banderas de aislamiento en ambos (A además lleva MCP propio)
    for flag in ("--strict-mcp-config", "--disable-slash-commands", "--no-session-persistence"):
        assert all(flag in x["args"] for x in cs)
    assert all(opt(x["args"], "--tools") == "" and opt(x["args"], "--setting-sources") == "" for x in cs)


def test_modelo_por_defecto_y_kba_model(env, monkeypatch):
    assert run.resolve_model(None, {}) == "claude-sonnet-5-5"
    assert run.resolve_model(None, {"KBA_MODEL": "m-env"}) == "m-env"
    assert run.resolve_model("m-cli", {"KBA_MODEL": "m-env"}) == "m-cli"


# ------------------------------------------------------------------ brazo A: reset y línea base

def test_reset_antes_de_cada_pregunta_de_a(env, rag):
    root, capture = env
    n = []
    c = ctx(rag_url=rag[0], reset=lambda: n.append(1) or {"baseline": "abc", "accion": "worktree_reset"})
    plan = run.build_plan(["P01", "P02"], ["A", "B"], 2)
    qs = {q["id"]: q for q in run.load_questions()}
    rows = run.ejecutar(plan, qs, c, log=lambda *_: None)
    assert len(n) == sum(1 for p in plan if p["brazo"] == "A") == 4
    assert all(r["baseline_ok"] is True for r in rows if r["brazo"] == "A")
    assert all(r["baseline_ok"] is None for r in rows if r["brazo"] == "B")
    out = [json.loads(x) for x in (run.RESULTS / "experimento.jsonl").read_text().splitlines()]
    assert len(out) == 8


class Runner:
    def __init__(self, main="aaa", base="aaa", worktree=True):
        self.cmds, self.main, self.base, self.worktree = [], main, base, worktree

    def __call__(self, cmd, timeout=0):
        self.cmds.append(cmd)
        j = " ".join(cmd)
        if "rev-parse main" in j:
            return 0, self.main + "\n", ""
        if "kb-a-baseline^{commit}" in j:
            return 0, self.base + "\n", ""
        if " test -d " in j:
            return (0 if self.worktree else 1), "", ""
        return 0, "", ""


def test_reset_ok_resetea_worktree_consultor():
    r = Runner()
    info = run.reset_kba(r)
    j = [" ".join(c) for c in r.cmds]
    assert any("/worktrees/consultor reset --hard kb-a-baseline" in x for x in j)
    assert any("/worktrees/consultor clean -fd" in x for x in j)
    assert all(c[:6] == ["docker", "compose", "exec", "-T", "mcp-gateway", "git"] or "test" in c for c in r.cmds)
    assert info["accion"] == "worktree_reset"


def test_aborta_si_main_difiere_de_baseline(env, rag):
    r = Runner(main="bbb", base="aaa")
    with pytest.raises(run.BaselineError, match="fusionó cambios"):
        run.reset_kba(r)
    assert not any("reset" in c and "--hard" in c for c in r.cmds)  # no toca nada
    # y la corrida entera aborta con código 3 sin ejecutar claude
    root, capture = env
    qs = {q["id"]: q for q in run.load_questions()}
    with pytest.raises(run.BaselineError):
        run.ejecutar(run.build_plan(["P01"], ["A"], 1), qs, ctx(reset=lambda: run.reset_kba(Runner(main="b", base="a"))),
                     log=lambda *_: None)
    assert not capture.exists()


def test_main_aborta_con_codigo_3(env, rag, monkeypatch, capsys):
    monkeypatch.setattr(run, "reset_kba", lambda *a, **k: (_ for _ in ()).throw(run.BaselineError("difiere")))
    rc = run.main(["--brazo", "A", "--ids", "P01", "--reps", "1"])
    assert rc == 3 and "ABORTADO" in capsys.readouterr().err


# ------------------------------------------------------------------ ids únicos y escritura exclusiva

def test_run_ids_unicos_y_escritura_exclusiva(env, rag):
    root, capture = env
    qs = {q["id"]: q for q in run.load_questions()}
    plan = run.build_plan(["P01", "P02"], ["A", "B"], 3)
    rows = run.ejecutar(plan, qs, ctx(rag_url=rag[0]), log=lambda *_: None)
    ids = [r["run_id"] for r in rows]
    assert len(ids) == len(set(ids)) == 12
    files = sorted((run.RESULTS / "respuestas").iterdir())
    assert len(files) == 12
    r = rows[0]
    assert Path(root / r["respuesta_path"]).name == f"{r['question_id']}-{r['brazo']}-r{r['rep']}-{r['run_id']}.md"
    with pytest.raises(FileExistsError):
        run._guardar_respuesta(files[0], "otra")
    assert files[0].read_text().startswith("Respuesta falsa")


def test_error_se_registra_y_continua(env, rag, monkeypatch):
    root, capture = env
    monkeypatch.setenv("FAKE_MODE", "iserror")
    qs = {q["id"]: q for q in run.load_questions()}
    rows = run.ejecutar(run.build_plan(["P01", "P02"], ["B"], 1), qs, ctx(rag_url=rag[0]), log=lambda *_: None)
    assert len(rows) == 2 and all(r["is_error"] for r in rows)
    # RAG caído: error registrado, no excepción
    rows = run.ejecutar(run.build_plan(["P01"], ["B"], 1), qs, ctx(rag_url="http://127.0.0.1:1"), log=lambda *_: None)
    assert rows[0]["is_error"] and "URLError" in rows[0]["error"]


# ------------------------------------------------------------------ orden

def test_orden_intercalado_y_aleatorio_reproducible():
    p = run.build_plan(["P01", "P02"], ["A", "B"], 1)
    assert [x["question_id"] for x in p] == ["P01", "P01", "P02", "P02"]
    assert sorted(x["brazo"] for x in p[:2]) == ["A", "B"] and p[0]["brazo"] != p[2]["brazo"]
    ids = [f"P{i:02d}" for i in range(1, 16)]
    a = run.build_plan(ids, ["A", "B"], 3, "aleatorio", 7)
    b = run.build_plan(ids, ["A", "B"], 3, "aleatorio", 7)
    c = run.build_plan(ids, ["A", "B"], 3, "aleatorio", 8)
    key = lambda pl: [(x["question_id"], x["brazo"], x["rep"]) for x in pl]  # noqa: E731
    assert key(a) == key(b) and key(a) != key(c) and len(a) == 90
    assert sorted(key(a)) == sorted(key(run.build_plan(ids, ["A", "B"], 3)))
    with pytest.raises(run.ExperimentError):
        run.build_plan(ids, ["A"], 1, "aleatorio", None)


def test_dry_run_no_ejecuta(env, capsys):
    root, capture = env
    rc = run.main(["--brazo", "ambos", "--ids", "P01", "--dry-run"])
    out = capsys.readouterr().out
    assert rc == 0 and "DRY-RUN" in out and "***" in out and "tok-consultor-SECRETO" not in out
    assert not capture.exists() and not (run.RESULTS / "experimento.jsonl").exists()


def test_overhead(env):
    root, capture = env
    rows = run.run_overhead(2, "m", ra.load_env(root / ".env"), log=lambda *_: None)
    assert len(rows) == 4 and {r["config"] for r in rows} == {"B-sin-herramientas", "A-mcp-sin-pregunta"}
    cs = calls(capture)
    assert all("Responde solo: ok" in x["args"] for x in cs)
    assert (run.RESULTS / "overhead.jsonl").read_text().count("\n") == 4
    assert "tok-consultor-SECRETO" not in (run.RESULTS / "overhead.jsonl").read_text()


# ------------------------------------------------------------------ calificación ciega

def _sembrar_experimento(root, rag_url):
    qs = {q["id"]: q for q in run.load_questions()}
    return run.ejecutar(run.build_plan(["P01", "P14"], ["A", "B"], 1), qs, ctx(rag_url=rag_url), log=lambda *_: None)


def test_csv_ciego_y_mapa(env, rag, monkeypatch):
    root, _ = env
    rows = _sembrar_experimento(root, rag[0])
    monkeypatch.setattr(cal, "RESULTS", run.RESULTS)
    monkeypatch.setattr(cal, "REPO", root)
    cal.preparar(11, log=lambda *_: None)
    with open(run.RESULTS / "calificacion.csv", encoding="utf-8", newline="") as f:
        lec = list(csv.DictReader(f))
    assert list(lec[0].keys()) == cal.COLUMNAS
    assert not any(k.lower() in ("brazo", "run_id", "sistema") for k in lec[0])
    assert len(lec) == 4 and len({r["etiqueta"] for r in lec}) == 4
    cabecera = (run.RESULTS / "calificacion.csv").read_text().splitlines()[0]
    assert "brazo" not in cabecera
    mapa = json.loads((run.RESULTS / "calificacion_mapa.json").read_text())["mapa"]
    por_run = {r["run_id"]: r for r in rows}
    for r in lec:
        m = mapa[r["etiqueta"]]
        assert m["question_id"] == r["question_id"] and por_run[m["run_id"]]["brazo"] == m["brazo"]
        assert r["respuesta"].startswith("Respuesta falsa")
    assert {m["brazo"] for m in mapa.values()} == {"A", "B"}
    # reproducible y no pisa notas existentes
    with pytest.raises(cal.CalificacionError):
        cal.preparar(11, log=lambda *_: None)
    # destapar: sin calificar falla
    with pytest.raises(cal.CalificacionError, match="sin calificar"):
        cal.destapar(log=lambda *_: None)
    # calificar con un valor fuera de rango falla
    for i, r in enumerate(lec):
        r.update({"exactitud(0-4)": "4", "trazabilidad(0-3)": "3", "cobertura(0-2)": "2", "prudencia(0-1)": "1",
                  "calificador": "A"})
    lec[0]["exactitud(0-4)"] = "5"
    csv_path = run.RESULTS / "calificacion.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cal.COLUMNAS)
        w.writeheader()
        w.writerows(lec)
    with pytest.raises(cal.CalificacionError, match="fuera de rango"):
        cal.destapar(log=lambda *_: None)
    lec[0]["exactitud(0-4)"] = "4"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cal.COLUMNAS)
        w.writeheader()
        w.writerows(lec)
    out = cal.destapar(log=lambda *_: None)
    assert len(out) == 4 and {r["total"] for r in out} == {10}
    res = list(csv.DictReader(open(run.RESULTS / "calificacion_resultados.csv", encoding="utf-8")))
    assert {r["brazo"] for r in res} == {"A", "B"}


# ------------------------------------------------------------------ reporte

def test_reporte_con_datos_sinteticos(tmp_path):
    d = tmp_path / "res"
    d.mkdir()
    def j(name, rows):
        (d / name).write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    j("kba_runs.jsonl", [{"op": "ingesta", "total_input_tokens": 1000, "input_tokens": 10, "cache_creation_input_tokens": 90,
                          "output_tokens": 50, "wall_ms": 2000, "is_error": False},
                         {"op": "consulta", "total_input_tokens": 9999999, "output_tokens": 1}])
    j("rag_builds.jsonl", [{"mode": "full", "ts": "t", "files_changed": 6, "chunks_written": 189, "embedded_tokens": 14388,
                            "llm_tokens": 0, "elapsed_ms": 3000}, {"mode": "incremental", "embedded_tokens": 77777}])
    exp = []
    for b, base in (("A", 5000), ("B", 800)):
        for i in range(3):
            exp.append({"brazo": b, "tipo": "Puntual", "question_id": f"P0{i+1}", "rep": 1, "is_error": False,
                        "total_input_tokens": base + i, "input_tokens": 5, "cache_creation_input_tokens": 100,
                        "output_tokens": 100 + i, "num_turns": 6 if b == "A" else 1, "latencia_total_ms": 10000 + i,
                        "wall_ms": 9000, "retrieval_ms": 12, "retrieval_wall_ms": 20, "retrieved_tokens": 400})
    exp.append({"brazo": "A", "tipo": "Puntual", "question_id": "P09", "rep": 1, "is_error": True})
    j("experimento.jsonl", exp)
    j("overhead.jsonl", [{"config": "B-sin-herramientas", "total_input_tokens": 924, "output_tokens": 4, "wall_ms": 3000,
                          "is_error": False}])
    j("actualizacion.jsonl", [{"ts": "t", "brazo": "B", "archivo": "raw/x.md", "elapsed_ms": 500, "embedded_tokens": 300,
                               "chunks_written": 3, "llm_total_input_tokens": 0, "llm_output_tokens": 0}])
    with open(d / "calificacion_resultados.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["etiqueta", "brazo", "run_id", "question_id", "tipo", "rep", *rep.CRIT,
                                          "total", "calificador", "notas"])
        w.writeheader()
        for i, (b, ex) in enumerate((("A", 4), ("A", 2), ("B", 4), ("B", 4))):
            qid = "P14" if i % 2 else "P01"
            w.writerow({"etiqueta": f"R-{i}", "brazo": b, "run_id": str(i), "question_id": qid,
                        "tipo": "Abstención ante falta de evidencia" if qid == "P14" else "Puntual", "rep": 1,
                        "exactitud": ex, "trazabilidad": 3, "cobertura": 2, "prudencia": 1, "total": ex + 6,
                        "calificador": "A", "notas": ""})
    texto = rep.generar(d)
    assert "Tokens de embeddings" in texto and "14 388" in texto
    assert "77 777" not in texto and "9 999 999" not in texto  # no mezcla incremental ni consultas de KB-A
    assert "con error (excluidas): A=1" in texto
    assert "Overhead fijo" in texto and "924" in texto and "(e) Costo de actualización" in texto
    assert "Aciertos en P14-P15" in texto and "Nota >= 8" in texto
    rep.main(["--results", str(d)])
    assert (d / "tabla.md").read_text() == texto
    # sin datos no falla
    vacio = tmp_path / "vacio"
    vacio.mkdir()
    assert "Sin experimento.jsonl" in rep.generar(vacio)


# ------------------------------------------------------------------ costo de actualización

def test_costo_actualizacion(tmp_path):
    act = _load("costo_actualizacion")
    assert act.validar_archivo("raw/x.md") == "raw/x.md"
    for malo in ("../raw/x.md", "raw/../x.md", "wiki/x.md", "raw/x.txt"):
        with pytest.raises(act.ActualizacionError):
            act.validar_archivo(malo)
    vault = tmp_path / "vault"
    (vault / "raw").mkdir(parents=True)
    (vault / "raw" / "x.md").write_text("# X\n\n## Diapositiva 1\nhola\n\n## Diapositiva 2\nchao\n")
    cmds = []
    commit = act.modificar_vault("raw/x.md", "ACT-1", runner=lambda c: cmds.append(c) or (0, "deadbeef\n", ""), vault=vault)
    texto = (vault / "raw" / "x.md").read_text()
    assert "## Diapositiva 3" in texto and "ACT-1" in texto and commit == "deadbeef"
    assert any("commit" in c for c in cmds) and all("mcp-gateway" in c for c in cmds)
    posts = []

    def post(url, body):
        posts.append((url, body))
        if url.endswith("/index"):
            return {"mode": "incremental", "files_changed": 1, "chunks_written": 3, "embedded_tokens": 90, "elapsed_ms": 40}
        return {"fragments": [{"text": "... ACT-1 ..."}]}

    r = act.actualizar_b("raw/x.md", "ACT-1", "http://r", 5, post=post)
    assert posts[0] == ("http://r/index", {"path": "raw/x.md"}) and posts[1][1]["use_llm"] is False
    assert r["refleja"] and r["llm_total_input_tokens"] == 0 and r["embedded_tokens"] == 90
    agent = lambda *a, **k: {"run_id": "r1", "total_input_tokens": 500, "output_tokens": 20, "num_turns": 4, "wall_ms": 9}  # noqa: E731
    ra_ = act.actualizar_a("raw/x.md", "ACT-1", runner=lambda c: (0, "main:wiki/conceptos/a.md\n", ""), agent=agent)
    assert ra_["refleja"] and ra_["llm_total_input_tokens"] == 500 and ra_["embedded_tokens"] == 0
    assert any("reset --hard kb-a-baseline" in " ".join(c) for c in act.restaurar("http://r", dry=True))
