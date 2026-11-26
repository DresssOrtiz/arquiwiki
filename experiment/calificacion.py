#!/usr/bin/env python3
"""Calificación ciega de las respuestas del experimento.

  python3 experiment/calificacion.py preparar --semilla 42 [--reps 1|todas|N]
  # los calificadores rellenan exactitud/trazabilidad/cobertura/prudencia/calificador en calificacion.csv
  python3 experiment/calificacion.py destapar [--csv calificacion.csv ...]

`preparar` mezcla las respuestas y les pone una etiqueta (R-xxxx). El CSV NO contiene el brazo; el
mapa etiqueta -> brazo queda en calificacion_mapa.json (no abrir hasta terminar de calificar).
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from pathlib import Path

EXP = Path(__file__).resolve().parent
REPO = EXP.parent
RESULTS = EXP / "results"

COLUMNAS = ["etiqueta", "question_id", "pregunta", "respuesta_referencia", "fuente_verificable", "respuesta",
            "exactitud(0-4)", "trazabilidad(0-3)", "cobertura(0-2)", "prudencia(0-1)", "total", "calificador",
            "notas"]
CRITERIOS = [("exactitud(0-4)", 4), ("trazabilidad(0-3)", 3), ("cobertura(0-2)", 2), ("prudencia(0-1)", 1)]
NOMBRES = ["exactitud", "trazabilidad", "cobertura", "prudencia"]


class CalificacionError(Exception):
    pass


def _leer_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        raise CalificacionError(f"No existe {path}")
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def _resolver(p: str) -> Path:
    path = Path(p)
    return path if path.is_absolute() else REPO / path


def seleccionar(rows: list[dict], reps: str) -> list[dict]:
    ok = [r for r in rows if not r.get("is_error") and r.get("respuesta_path")]
    if reps == "todas":
        return ok
    n = int(reps)
    return [r for r in ok if r.get("rep") == n]


def preparar(semilla: int, reps: str = "1", force: bool = False, log=print) -> list[dict]:
    csv_path, mapa_path = RESULTS / "calificacion.csv", RESULTS / "calificacion_mapa.json"
    if (csv_path.exists() or mapa_path.exists()) and not force:
        raise CalificacionError(f"{csv_path.name} o {mapa_path.name} ya existen (podrían tener notas); "
                                f"usa --force solo si quieres rehacerlos")
    preguntas = {q["id"]: q for q in json.loads((EXP / "preguntas.json").read_text(encoding="utf-8"))}
    claves = {c["id"]: c for c in json.loads((EXP / "claves.json").read_text(encoding="utf-8"))}
    rows = seleccionar(_leer_jsonl(RESULTS / "experimento.jsonl"), reps)
    if not rows:
        raise CalificacionError("No hay respuestas sin error para calificar")
    rng = random.Random(semilla)
    rng.shuffle(rows)
    usadas: set[str] = set()
    salida, mapa = [], {}
    for r in rows:
        while True:
            etiqueta = f"R-{rng.getrandbits(16):04x}"
            if etiqueta not in usadas:
                usadas.add(etiqueta)
                break
        qid = r["question_id"]
        texto = _resolver(r["respuesta_path"]).read_text(encoding="utf-8")
        salida.append({"etiqueta": etiqueta, "question_id": qid, "pregunta": preguntas[qid]["texto"],
                       "respuesta_referencia": claves[qid]["respuesta_referencia"],
                       "fuente_verificable": claves[qid]["fuente_verificable"], "respuesta": texto,
                       **{c: "" for c in COLUMNAS[6:]}})
        mapa[etiqueta] = {"brazo": r["brazo"], "run_id": r["run_id"], "question_id": qid,
                          "tipo": r.get("tipo") or preguntas[qid]["tipo"], "rep": r.get("rep")}
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS)
        w.writeheader()
        w.writerows(salida)
    mapa_path.write_text(json.dumps({"semilla": semilla, "reps": reps, "mapa": mapa}, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    # La cita a `wiki/` o enlaces [[...]] delatan a KB-A: se avisa, no se altera la respuesta.
    delatoras = sum(1 for s in salida if "wiki/" in s["respuesta"] or "[[" in s["respuesta"])
    log(f"{len(salida)} respuestas preparadas -> {csv_path}")
    log(f"AVISO ceguera: {delatoras} respuestas citan wiki/ o [[...]] (típico de KB-A); ver amenazas en README.")
    return salida


def _entero(valor: str, maximo: int, campo: str, etiqueta: str) -> int:
    try:
        v = int(str(valor).strip())
    except ValueError:
        raise CalificacionError(f"{etiqueta}: '{campo}' vacío o no numérico ({valor!r})")
    if not 0 <= v <= maximo:
        raise CalificacionError(f"{etiqueta}: '{campo}' fuera de rango 0-{maximo} ({v})")
    return v


def destapar(csvs: list[Path] | None = None, parcial: bool = False, log=print) -> list[dict]:
    csvs = csvs or [RESULTS / "calificacion.csv"]
    info = json.loads((RESULTS / "calificacion_mapa.json").read_text(encoding="utf-8"))
    mapa = info["mapa"]
    out, errores = [], []
    for path in csvs:
        with open(path, encoding="utf-8", newline="") as f:
            filas = list(csv.DictReader(f))
        vistas = set()
        for fila in filas:
            et = fila["etiqueta"]
            if et not in mapa:
                raise CalificacionError(f"{path.name}: etiqueta desconocida {et} (no está en el mapa)")
            vistas.add(et)
            if not any((fila[c] or "").strip() for c, _ in CRITERIOS):
                if parcial:
                    continue
                errores.append(f"{et}: sin calificar")
                continue
            try:
                notas = [_entero(fila[c], m, c, et) for c, m in CRITERIOS]
            except CalificacionError as e:
                errores.append(str(e))
                continue
            total = sum(notas)
            decl = (fila.get("total") or "").strip()
            if decl and int(float(decl)) != total:
                errores.append(f"{et}: total declarado {decl} != suma {total}")
                continue
            cal = (fila.get("calificador") or "").strip()
            if not cal:
                errores.append(f"{et}: falta calificador")
                continue
            m = mapa[et]
            out.append({"etiqueta": et, "brazo": m["brazo"], "run_id": m["run_id"], "question_id": m["question_id"],
                        "tipo": m["tipo"], "rep": m["rep"], **dict(zip(NOMBRES, notas)), "total": total,
                        "calificador": cal, "notas": fila.get("notas", "")})
        faltan = set(mapa) - vistas
        if faltan and not parcial:
            errores.append(f"{path.name}: faltan {len(faltan)} etiquetas del mapa")
    if errores:
        raise CalificacionError("Calificación inválida:\n  " + "\n  ".join(errores))
    dest = RESULTS / "calificacion_resultados.csv"
    campos = ["etiqueta", "brazo", "run_id", "question_id", "tipo", "rep", *NOMBRES, "total", "calificador", "notas"]
    with open(dest, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(out)
    log(f"{len(out)} calificaciones destapadas -> {dest}")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Calificación ciega")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("preparar")
    p.add_argument("--semilla", type=int, required=True)
    p.add_argument("--reps", default="1", help="1 (por defecto), otro número o 'todas'")
    p.add_argument("--force", action="store_true")
    d = sub.add_parser("destapar")
    d.add_argument("--csv", action="append", type=Path, help="CSV calificado (repetible: un calificador por archivo)")
    d.add_argument("--parcial", action="store_true", help="ignora filas sin calificar")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "preparar":
            preparar(a.semilla, a.reps, a.force)
        else:
            destapar(a.csv, a.parcial)
    except CalificacionError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
