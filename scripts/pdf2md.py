#!/usr/bin/env python3
"""Convierte PDF de diapositivas a markdown, una seccion `## Diapositiva N` por pagina.

Uso:
    python3 scripts/pdf2md.py <pdf|directorio> [...] --out kb-wiki/vault/raw [--force] [--dry-run]

Decisiones:
- Extraccion: UNA sola llamada `pdftotext -layout` por PDF; poppler termina cada
  pagina con `\\f`, asi que se separa por ese caracter. Es mucho mas rapido que N
  llamadas y, como control de robustez, el numero de trozos se compara con
  `pdfinfo`; si no coincide se cae al modo lento (una llamada por pagina, `-f N -l N`).
- Espacios: se quita toda la sangria inicial (4+ espacios serian un bloque de
  codigo en markdown) y los huecos internos de >=3 espacios (columnas de tablas
  en -layout) se reducen a 2 espacios: se conserva la separacion visual entre
  columnas sin inflar los chunks del RAG.
- Pie repetido: linea presente en >60 % de las diapositivas (minimo 3 diapositivas).
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import Counter
from datetime import date
from pathlib import Path

EMPTY_MARK = "_(sin texto extraíble: probablemente imagen)_"
FOOTER_THRESHOLD = 0.60
MIN_SLIDES_FOR_FOOTER = 3
# Bullets: Unicode comunes + glifos Symbol/Wingdings que pdftotext deja en zona privada.
_BULLET_RE = re.compile(r"^[•▪●◦■□‣–]\s*")


def slugify(name: str) -> str:
    """'1.2 Definiciones 1.pdf' -> '1-2-definiciones-1' (sin extension .pdf)."""
    if name.lower().endswith(".pdf"):
        name = name[:-4]
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_ = "".join(c for c in nfkd if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", ascii_).strip("-") or "documento"


def clean_slide(text: str) -> str:
    """Limpia el texto crudo de una diapositiva (sin quitar pie repetido)."""
    text = text.replace("\f", "").replace("\r", "")
    lines = []
    for raw in text.split("\n"):
        line = raw.strip()  # quita sangria (evita bloques de codigo) y espacios finales
        line = re.sub(r"\s{3,}", "  ", line)
        if _BULLET_RE.match(line):
            line = "- " + _BULLET_RE.sub("", line, count=1)
        if line.startswith("#"):
            line = "\\" + line
        lines.append(line)
    out = "\n".join(lines)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip()


def detect_repeated_lines(slides: list[str], threshold: float = FOOTER_THRESHOLD,
                          min_slides: int = MIN_SLIDES_FOR_FOOTER) -> set[str]:
    """Lineas (ya limpias) que aparecen en mas de `threshold` de las diapositivas."""
    if len(slides) < min_slides:
        return set()
    counts: Counter[str] = Counter()
    for s in slides:
        counts.update({ln.strip() for ln in s.split("\n") if ln.strip()})
    return {ln for ln, c in counts.items() if c / len(slides) > threshold}


def remove_lines(slide: str, repeated: set[str]) -> str:
    kept = [ln for ln in slide.split("\n") if ln.strip() not in repeated]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(kept)).strip()


def render_markdown(title: str, source_name: str, raw_pages: list[str],
                    today: str | None = None) -> tuple[str, dict]:
    """Devuelve (markdown, stats). Funcion pura: no toca disco."""
    today = today or date.today().isoformat()
    cleaned = [clean_slide(p) for p in raw_pages]
    repeated = detect_repeated_lines(cleaned)
    cleaned = [remove_lines(s, repeated) for s in cleaned]
    n = len(cleaned)
    header = (f"> Fuente: `{source_name}` · {n} diapositivas · convertido con pdftotext el {today}. "
              "Texto extraído automáticamente: verificar contra el PDF.")
    if repeated:
        footers = " | ".join(sorted(repeated))
        header += f'\n> Se eliminó el pie repetido: "{footers}"'
    parts = [f"# {title}", "", header]
    empty = 0
    for i, s in enumerate(cleaned, 1):
        if not s:
            empty += 1
            s = EMPTY_MARK
        parts += ["", f"## Diapositiva {i}", "", s]
    md = "\n".join(parts) + "\n"
    return md, {"slides": n, "empty": empty, "chars": len(md), "footers": sorted(repeated)}


# ---------------------------------------------------------------- I/O

def _need_tools() -> None:
    missing = [t for t in ("pdftotext", "pdfinfo") if not shutil.which(t)]
    if missing:
        sys.exit(f"error: faltan {', '.join(missing)} (poppler). Instala con: brew install poppler")


def _run(cmd: list[str]) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd[:1])} fallo ({r.returncode}): {r.stderr.strip()}")
    return r.stdout


def page_count(pdf: Path) -> int:
    m = re.search(r"^Pages:\s+(\d+)", _run(["pdfinfo", str(pdf)]), re.M)
    if not m:
        raise RuntimeError(f"pdfinfo no informo el numero de paginas de {pdf}")
    return int(m.group(1))


def extract_pages(pdf: Path) -> list[str]:
    n = page_count(pdf)
    out = _run(["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"])
    pages = out.split("\f")
    if pages and pages[-1].strip() == "":
        pages = pages[:-1]
    if len(pages) == n:
        return pages
    # Fallback robusto: una llamada por pagina.
    return [_run(["pdftotext", "-f", str(i), "-l", str(i), "-layout", "-enc", "UTF-8", str(pdf), "-"])
            for i in range(1, n + 1)]


def collect_pdfs(inputs: list[str]) -> list[Path]:
    pdfs: list[Path] = []
    for item in inputs:
        p = Path(item)
        if p.is_dir():
            pdfs += sorted(p.glob("*.pdf"))
        elif p.is_file():
            pdfs.append(p)
        else:
            sys.exit(f"error: no existe {p}")
    return pdfs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="PDF de diapositivas -> markdown por diapositiva.")
    ap.add_argument("inputs", nargs="+", help="PDF o directorios con PDF")
    ap.add_argument("--out", required=True, help="directorio de salida")
    ap.add_argument("--force", action="store_true", help="sobrescribir salidas existentes")
    ap.add_argument("--dry-run", action="store_true", help="solo mostrar que se haria")
    args = ap.parse_args(argv)
    _need_tools()
    out_dir = Path(args.out)
    pdfs = collect_pdfs(args.inputs)
    if not pdfs:
        sys.exit("error: no se encontraron PDF")
    rc = 0
    for pdf in pdfs:
        target = out_dir / f"{slugify(pdf.name)}.md"
        if target.exists() and not args.force:
            print(f"[omitido] {pdf.name} -> {target} (existe; usa --force)")
            continue
        if args.dry_run:
            print(f"[dry-run] {pdf.name} -> {target}")
            continue
        try:
            md, st = render_markdown(pdf.stem, pdf.name, extract_pages(pdf))
        except RuntimeError as e:
            print(f"[error] {pdf.name}: {e}", file=sys.stderr)
            rc = 1
            continue
        out_dir.mkdir(parents=True, exist_ok=True)
        target.write_text(md, encoding="utf-8")
        extra = f", pie eliminado: {st['footers']}" if st["footers"] else ""
        print(f"[ok] {pdf.name} -> {target}: {st['slides']} diapositivas, "
              f"{st['empty']} vacías, {st['chars']} caracteres{extra}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
