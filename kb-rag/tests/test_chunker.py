from app.chunker import chunk_markdown

count = lambda t: len(t.split())  # noqa: E731

DOC = """# Clase 2: ATAM

Introducción breve.

## Pasos

1. Presentar ATAM.
2. Presentar la arquitectura.

## Árbol de utilidad

Divide la utilidad en atributos de calidad.
"""


def test_cada_seccion_lleva_su_ruta_de_encabezados():
    chunks = chunk_markdown(DOC, count, max_tokens=50)
    headings = [c.heading for c in chunks]
    assert headings == ["Clase 2: ATAM", "Clase 2: ATAM > Pasos", "Clase 2: ATAM > Árbol de utilidad"]
    assert chunks[1].text.startswith("Clase 2: ATAM > Pasos\n\n")
    assert [c.ord for c in chunks] == [0, 1, 2]


def test_los_tokens_del_fragmento_incluyen_el_prefijo():
    chunk = chunk_markdown(DOC, count, max_tokens=50)[0]
    assert chunk.tokens == count(chunk.text)


def test_agrupa_parrafos_hasta_el_limite():
    body = "\n\n".join(f"parrafo {i} con cuatro palabras" for i in range(10))
    chunks = chunk_markdown(f"# T\n\n{body}", count, max_tokens=20)
    assert len(chunks) > 1
    assert all(c.tokens <= 20 for c in chunks)


def test_parrafo_largo_se_parte_con_solapamiento():
    palabras = [f"w{i}" for i in range(100)]
    chunks = chunk_markdown("# T\n\n" + " ".join(palabras), count, max_tokens=30, overlap_words=5)
    assert len(chunks) > 3
    assert all(c.tokens <= 30 for c in chunks)
    primero, segundo = chunks[0].text.split()[1:], chunks[1].text.split()[1:]  # sin el título "T"
    assert primero[-5:] == segundo[:5]
    # no se pierde ninguna palabra
    todas = {w for c in chunks for w in c.text.split()}
    assert set(palabras) <= todas


def test_ignora_encabezados_dentro_de_bloques_de_codigo():
    doc = "# A\n\ntexto\n\n```\n# no es titulo\n```\n"
    assert {c.heading for c in chunk_markdown(doc, count)} == {"A"}


def test_documento_vacio():
    assert chunk_markdown("", count) == []
    assert chunk_markdown("# Solo titulo\n", count) == []
