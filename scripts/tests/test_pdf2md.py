import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pdf2md  # noqa: E402


def test_slugify():
    assert pdf2md.slugify("1.2 Definiciones 1.pdf") == "1-2-definiciones-1"
    assert pdf2md.slugify("5.1 Estilos y Patrones Arquitecturales 3.pdf") == "5-1-estilos-y-patrones-arquitecturales-3"
    assert pdf2md.slugify("Introducción – Atributos (Calidad).pdf") == "introduccion-atributos-calidad"


def test_bullets_and_spaces():
    out = pdf2md.clean_slide("   • Uno   \n  ▪ Dos\n– Tres\n Cuatro\nA      B   \n\n\n\n\nFin\f")
    assert out == "- Uno\n- Dos\n- Tres\n- Cuatro\nA  B\n\nFin"


def test_escape_hash():
    assert pdf2md.clean_slide("# no es titulo\ntexto # ok") == "\\# no es titulo\ntexto # ok"


def test_repeated_footer():
    slides = [f"Tema {i}\nArquitectura de Software" for i in range(5)]
    assert pdf2md.detect_repeated_lines(slides) == {"Arquitectura de Software"}
    assert pdf2md.detect_repeated_lines(slides[:2]) == set()  # muy pocas diapositivas
    md, st = pdf2md.render_markdown("t", "t.pdf", slides, today="2026-01-01")
    assert 'Se eliminó el pie repetido: "Arquitectura de Software"' in md
    assert md.count("Arquitectura de Software") == 1  # solo en el encabezado


def test_empty_slide():
    md, st = pdf2md.render_markdown("t", "t.pdf", ["Hola", "  \n\f"], today="2026-01-01")
    assert st["empty"] == 1
    assert "## Diapositiva 2\n\n" + pdf2md.EMPTY_MARK in md
    assert "2 diapositivas" in md


def make_pdf(path: Path, texts: list[str]) -> None:
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>"]
    kids = " ".join(f"{4 + 2 * i} 0 R" for i in range(len(texts)))
    objs.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(texts)} >>".encode())
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    for i, t in enumerate(texts):
        content = f"BT /F1 18 Tf 72 700 Td ({t}) Tj ET".encode()
        objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                    f"/Resources << /Font << /F1 3 0 R >> >> /Contents {5 + 2 * i} 0 R >>".encode())
        objs.append(b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream")
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for n, o in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{n} 0 obj\n".encode() + o + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    path.write_bytes(bytes(out))


@pytest.mark.skipif(not (shutil.which("pdftotext") and shutil.which("pdfinfo")), reason="poppler no instalado")
def test_integration(tmp_path, capsys):
    pdf = tmp_path / "1.2 Definiciones 1.pdf"
    make_pdf(pdf, ["Primera pagina", "Segunda pagina", "Tercera pagina"])
    out = tmp_path / "raw"
    assert pdf2md.main([str(tmp_path), "--out", str(out)]) == 0
    md = (out / "1-2-definiciones-1.md").read_text(encoding="utf-8")
    assert md.startswith("# 1.2 Definiciones 1\n")
    assert "3 diapositivas" in md
    for i, word in enumerate(["Primera", "Segunda", "Tercera"], 1):
        section = md.split(f"## Diapositiva {i}\n")[1].split("## Diapositiva")[0]
        assert f"{word} pagina" in section
    # no sobrescribe sin --force, y dry-run no escribe
    pdf2md.main([str(pdf), "--out", str(out)])
    assert "omitido" in capsys.readouterr().out
    pdf2md.main([str(pdf), "--out", str(tmp_path / "x"), "--dry-run"])
    assert not (tmp_path / "x").exists()
