#!/usr/bin/env python3
"""Genera experiment/results/tabla.md a partir de los registros del experimento.

  python3 experiment/reporte.py [--results experiment/results]

Lee (los que existan): kba_runs.jsonl, rag_builds.jsonl, experimento.jsonl, calificacion_resultados.csv,
actualizacion.jsonl y overhead.jsonl. No suma magnitudes de unidades distintas.
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

EXP = Path(__file__).resolve().parent
RESULTS = EXP / "results"
BRAZOS = ("A", "B")
NOMBRE = {"A": "KB-A (wiki)", "B": "KB-B (RAG)"}
CRIT = ["exactitud", "trazabilidad", "cobertura", "prudencia"]


def leer_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def fmt(v, dec: int = 0) -> str:
    if v is None:
        return "-"
    if isinstance(v, float):
        return f"{v:.{dec}f}" if dec else f"{v:,.0f}".replace(",", " ")
    if isinstance(v, int):
        return f"{v:,}".replace(",", " ")
    return str(v)


def tabla(cab: list[str], filas: list[list]) -> str:
    out = ["| " + " | ".join(cab) + " |", "|" + "|".join("---" for _ in cab) + "|"]
    out += ["| " + " | ".join(str(c) for c in f) + " |" for f in filas]
    return "\n".join(out)


def estad(vals: list[float]) -> tuple:
    vals = [v for v in vals if v is not None]
    if not vals:
        return (None, None, None)
    return (st.mean(vals), st.median(vals), st.stdev(vals) if len(vals) > 1 else None)


def triple(vals: list[float], dec: int = 0) -> str:
    m, md, sd = estad(vals)
    return f"{fmt(m, dec)} / {fmt(md, dec)} / {fmt(sd, dec)}" if m is not None else "-"


def entrada_nueva(r: dict) -> int:
    return (r.get("input_tokens") or 0) + (r.get("cache_creation_input_tokens") or 0)


# ------------------------------------------------------------------ (a) construcción

def seccion_construccion(kba: list[dict], builds: list[dict]) -> str:
    ops = ("ingesta", "lint", "correccion")
    filas_a = []
    for op in ops:
        rs = [r for r in kba if r.get("op") == op]
        if not rs:
            continue
        filas_a.append([op, len(rs), sum(1 for r in rs if r.get("is_error")),
                        fmt(sum(r.get("total_input_tokens") or 0 for r in rs)),
                        fmt(sum(entrada_nueva(r) for r in rs)),
                        fmt(sum(r.get("output_tokens") or 0 for r in rs)),
                        fmt(round(sum(r.get("wall_ms") or 0 for r in rs) / 1000, 1), 1)])
    out = ["## (a) Construcción", "", "### KB-A: tokens de LLM (kba_runs.jsonl; ingesta, lint y corrección)", ""]
    out.append(tabla(["Operación", "Ejecuciones", "Con error", "Entrada total (tokens LLM)",
                      "Entrada nueva (input + cache_creation)", "Salida (tokens LLM)", "Tiempo (s)"], filas_a)
               if filas_a else "_Sin registros de construcción de KB-A._")
    full = [b for b in builds if b.get("mode") == "full"]
    out += ["", "### KB-B: indexación (rag_builds.jsonl, modo full)", ""]
    if full:
        filas_b = [[b.get("ts", "-"), b.get("files_changed"), b.get("chunks_written"), fmt(b.get("embedded_tokens")),
                    fmt(b.get("llm_tokens")), fmt(b.get("elapsed_ms"))] for b in full]
        out.append(tabla(["ts", "Archivos", "Fragmentos", "Tokens de embeddings (modelo local)",
                          "Tokens de LLM", "Tiempo (ms)"], filas_b))
    else:
        out.append("_Sin registros de indexación de KB-B._")
    out += ["", "Las columnas de tokens de LLM (KB-A) y de tokens de embeddings (KB-B) son magnitudes distintas y "
            "no se suman ni se restan: se comparan por separado. \"Entrada total\" incluye lecturas de caché "
            "(cada turno reenvía el contexto acumulado); \"entrada nueva\" es input + cache_creation."]
    return "\n".join(out)


# ------------------------------------------------------------------ (b), (c) consulta

def _ok(rows: list[dict]) -> list[dict]:
    return [r for r in rows if not r.get("is_error")]


def seccion_consulta(exp: list[dict]) -> str:
    out = ["## (b) Costo por consulta, por brazo", ""]
    if not exp:
        return "\n".join(out + ["_Sin experimento.jsonl._"])
    ok = _ok(exp)
    metricas = [("Entrada total (tokens)", lambda r: r.get("total_input_tokens")),
                ("Entrada nueva (input + cache_creation)", entrada_nueva),
                ("Salida (tokens)", lambda r: r.get("output_tokens")),
                ("Turnos", lambda r: r.get("num_turns")),
                ("Latencia total (ms)", lambda r: r.get("latencia_total_ms")),
                ("Tiempo de claude, wall (ms)", lambda r: r.get("wall_ms"))]
    filas = []
    for nombre, fn in metricas:
        fila = [nombre]
        for b in BRAZOS:
            fila.append(triple([fn(r) for r in ok if r["brazo"] == b], 1 if nombre == "Turnos" else 0))
        filas.append(fila)
    out.append(tabla(["Métrica (media / mediana / desv. est.)", *[NOMBRE[b] for b in BRAZOS]], filas))
    n = {b: sum(1 for r in ok if r["brazo"] == b) for b in BRAZOS}
    e = {b: sum(1 for r in exp if r["brazo"] == b and r.get("is_error")) for b in BRAZOS}
    out += ["", f"n (sin error): A={n['A']}, B={n['B']}; con error (excluidas): A={e['A']}, B={e['B']}.", ""]
    extra = [r for r in ok if r["brazo"] == "B"]
    if extra:
        out.append(tabla(["Solo KB-B (media / mediana / desv. est.)", "Valor"],
                         [["Recuperación, servicio (ms)", triple([r.get("retrieval_ms") for r in extra])],
                          ["Recuperación, reloj (ms)", triple([r.get("retrieval_wall_ms") for r in extra])],
                          ["Tokens recuperados", triple([r.get("retrieved_tokens") for r in extra])]]))
        out.append("")
    out += ["- Entrada total: tokens de entrada que el CLI reporta (input + cache_creation + cache_read). En KB-A "
            "crece con cada turno porque el agente reenvía su contexto; en KB-B es un solo turno con los "
            "fragmentos.",
            "- Entrada nueva: input + cache_creation, sin lecturas de caché; es menos sensible al orden de las "
            "corridas.",
            "- Latencia total: en KB-A es el tiempo de `claude -p`; en KB-B suma recuperación (reloj) + `claude -p`. "
            "No incluye el reset de KB-A ni la espera entre corridas.",
            "- Todos los tokens salen del campo `usage` del CLI, con el mismo modelo en ambos brazos; con "
            "suscripción no hay costo monetario real."]
    out += ["", "## (c) Por tipo de pregunta", ""]
    tipos = list(dict.fromkeys(r["tipo"] for r in ok))
    filas = []
    for t in tipos:
        for b in BRAZOS:
            rs = [r for r in ok if r["tipo"] == t and r["brazo"] == b]
            if rs:
                filas.append([t, NOMBRE[b], len(rs), fmt(estad([r.get("total_input_tokens") for r in rs])[0]),
                              fmt(estad([entrada_nueva(r) for r in rs])[0]),
                              fmt(estad([r.get("output_tokens") for r in rs])[0]),
                              fmt(estad([r.get("num_turns") for r in rs])[0], 1),
                              fmt(estad([r.get("latencia_total_ms") for r in rs])[1])])
    out.append(tabla(["Tipo", "Brazo", "n", "Entrada total (media)", "Entrada nueva (media)", "Salida (media)",
                      "Turnos (media)", "Latencia total (mediana, ms)"], filas))
    out += ["", "Cada fila agrupa las ejecuciones sin error del tipo indicado; n cuenta pregunta × repetición."]
    return "\n".join(out)


# ------------------------------------------------------------------ (d) calificación

def leer_calificacion(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with open(path, encoding="utf-8", newline="") as f:
        filas = list(csv.DictReader(f))
    for r in filas:
        for c in (*CRIT, "total", "rep"):
            try:
                r[c] = int(r[c])
            except (ValueError, KeyError, TypeError):
                r[c] = None
    return filas


def consolidar(filas: list[dict]) -> list[dict]:
    """Una nota por etiqueta: la fila 'consenso' si existe; si no, la media de los calificadores."""
    por: dict[str, list[dict]] = defaultdict(list)
    for r in filas:
        por[r["etiqueta"]].append(r)
    out = []
    for et, rs in por.items():
        cons = [r for r in rs if (r.get("calificador") or "").strip().lower() == "consenso"]
        if cons:
            out.append(cons[-1])
            continue
        base = dict(rs[0])
        for c in (*CRIT, "total"):
            base[c] = st.mean([r[c] for r in rs])
        out.append(base)
    return out


def seccion_calificacion(filas: list[dict]) -> str:
    out = ["## (d) Calidad de las respuestas (rúbrica 0-10, calificación ciega)", ""]
    if not filas:
        return "\n".join(out + ["_Sin calificacion_resultados.csv todavía._"])
    notas = consolidar(filas)

    def linea(rs: list[dict]) -> list:
        return [len(rs), *[fmt(st.mean([r[c] for r in rs]), 2) for c in CRIT], fmt(st.mean([r["total"] for r in rs]), 2),
                f"{sum(1 for r in rs if r['total'] >= 8) / len(rs):.0%}"]

    cab = ["n", "Exactitud (0-4)", "Trazabilidad (0-3)", "Cobertura (0-2)", "Prudencia (0-1)", "Total (0-10)", "Nota >= 8"]
    out.append(tabla(["Brazo", *cab], [[NOMBRE[b], *linea([r for r in notas if r["brazo"] == b])]
                                       for b in BRAZOS if any(r["brazo"] == b for r in notas)]))
    out += ["", "### Por tipo de pregunta", ""]
    tipos = list(dict.fromkeys(r["tipo"] for r in notas))
    filas_t = [[t, NOMBRE[b], *linea(rs)] for t in tipos for b in BRAZOS
               if (rs := [r for r in notas if r["tipo"] == t and r["brazo"] == b])]
    out.append(tabla(["Tipo", "Brazo", *cab], filas_t))
    ctrl = [r for r in notas if r["question_id"] in ("P14", "P15")]
    if ctrl:
        out += ["", "### Aciertos en P14-P15 (exactitud = 4, abstención correcta)", ""]
        out.append(tabla(["Brazo", "Aciertos", "Respuestas"],
                         [[NOMBRE[b], sum(1 for r in ctrl if r["brazo"] == b and r["exactitud"] >= 4),
                           sum(1 for r in ctrl if r["brazo"] == b)] for b in BRAZOS if any(r["brazo"] == b for r in ctrl)]))
    out += ["", "Cada criterio se promedia sobre las respuestas calificadas; si hay una fila `consenso` esa es la nota, "
            "si no, la media de los calificadores. \"Nota >= 8\" es la proporción de respuestas con total >= 8/10. "
            "Con muestras de 15 a 90 respuestas no se infieren diferencias estadísticamente significativas."]
    return "\n".join(out)


# ------------------------------------------------------------------ (e) actualización, (f) overhead

def seccion_actualizacion(rows: list[dict]) -> str:
    out = ["## (e) Costo de actualización (un archivo modificado)", ""]
    if not rows:
        return "\n".join(out + ["_Sin actualizacion.jsonl (se ejecuta después del experimento principal)._"])
    filas = [[r.get("ts", "-"), r.get("brazo"), r.get("archivo"), fmt(r.get("elapsed_ms")),
              fmt(r.get("llm_total_input_tokens")), fmt(r.get("llm_output_tokens")),
              fmt(r.get("embedded_tokens")), fmt(r.get("chunks_written")), r.get("is_error", False)] for r in rows]
    out.append(tabla(["ts", "Brazo", "Archivo", "Tiempo (ms)", "LLM entrada total", "LLM salida",
                      "Tokens de embeddings", "Fragmentos", "Error"], filas))
    out += ["", "KB-B reindexa solo el archivo cambiado (tokens de embeddings, 0 de LLM); KB-A reingesta con el "
            "agente (tokens de LLM, 0 de embeddings). Columnas en unidades distintas: no se suman."]
    return "\n".join(out)


def seccion_overhead(rows: list[dict]) -> str:
    out = ["## (f) Overhead fijo del CLI (prompt trivial, reportado aparte)", ""]
    ok = _ok(rows)
    if not ok:
        return "\n".join(out + ["_Sin overhead.jsonl (`python3 experiment/run.py --overhead N`)._"])
    filas = []
    for c in dict.fromkeys(r["config"] for r in ok):
        rs = [r for r in ok if r["config"] == c]
        filas.append([c, len(rs), triple([r.get("total_input_tokens") for r in rs]),
                      triple([r.get("output_tokens") for r in rs]), triple([r.get("wall_ms") for r in rs])])
    out.append(tabla(["Configuración", "n", "Entrada total (media / mediana / desv.)", "Salida", "wall (ms)"], filas))
    out += ["", "Es el costo fijo de invocar `claude -p` con cada configuración (sistema + definiciones de "
            "herramientas) sin leer nada. No se resta de las consultas; sirve para interpretarlas."]
    return "\n".join(out)


def generar(results: Path) -> str:
    partes = ["# Tablas del experimento KB-A vs KB-B", "",
              "Generado por `experiment/reporte.py`. Mismo modelo y mismo CLI en ambos brazos.", "",
              seccion_construccion(leer_jsonl(results / "kba_runs.jsonl"), leer_jsonl(results / "rag_builds.jsonl")), "",
              seccion_consulta(leer_jsonl(results / "experimento.jsonl")), "",
              seccion_calificacion(leer_calificacion(results / "calificacion_resultados.csv")), "",
              seccion_actualizacion(leer_jsonl(results / "actualizacion.jsonl")), "",
              seccion_overhead(leer_jsonl(results / "overhead.jsonl")), ""]
    return "\n".join(partes)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Genera tabla.md")
    ap.add_argument("--results", type=Path, default=RESULTS)
    a = ap.parse_args(argv)
    texto = generar(a.results)
    (a.results / "tabla.md").write_text(texto, encoding="utf-8")
    print(f"Escrito {a.results / 'tabla.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
