FUENTE = {
    "titulo": "Clase 2: ATAM",
    "tipo": "markdown",
    "archivo_o_url": "raw/clase-02-atam.md",
}
PAGINA = {"titulo": "ATAM", "tipo": "concepto", "contenido": "Método de evaluación.", "enlaces": ["QAW"]}


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_crud_fuente(client):
    r = client.post("/fuentes", json=FUENTE)
    assert r.status_code == 201
    creada = r.json()
    assert creada["estado_ingesta"] == "pendiente"
    fid = creada["id"]

    assert client.get(f"/fuentes/{fid}").json()["titulo"] == FUENTE["titulo"]
    assert len(client.get("/fuentes").json()) == 1

    r = client.put(f"/fuentes/{fid}", json={"estado_ingesta": "ingestada"})
    assert r.status_code == 200
    assert r.json()["estado_ingesta"] == "ingestada"
    assert r.json()["titulo"] == FUENTE["titulo"]  # no se pisan los campos omitidos

    assert client.delete(f"/fuentes/{fid}").status_code == 204
    assert client.get(f"/fuentes/{fid}").status_code == 404


def test_crud_pagina(client):
    r = client.post("/paginas", json=PAGINA)
    assert r.status_code == 201
    pid = r.json()["id"]
    assert r.json()["estado_salud"] == "sin_revisar"
    assert r.json()["enlaces"] == ["QAW"]

    r = client.put(f"/paginas/{pid}", json={"estado_salud": "ok", "enlaces": ["QAW", "ADD"]})
    assert r.json()["estado_salud"] == "ok"
    assert r.json()["enlaces"] == ["QAW", "ADD"]

    assert client.delete(f"/paginas/{pid}").status_code == 204
    assert client.get(f"/paginas/{pid}").status_code == 404


def test_validacion(client):
    assert client.post("/fuentes", json={**FUENTE, "tipo": "inventado"}).status_code == 422
    assert client.post("/paginas", json={**PAGINA, "titulo": ""}).status_code == 422


def test_no_encontrado(client):
    assert client.get("/fuentes/999").status_code == 404
    assert client.put("/paginas/999", json={"contenido": "x"}).status_code == 404
    assert client.delete("/paginas/999").status_code == 404


def test_titulo_de_pagina_duplicado(client):
    assert client.post("/paginas", json=PAGINA).status_code == 201
    assert client.post("/paginas", json=PAGINA).status_code == 409


def test_relacion_n_a_m(client):
    f1 = client.post("/fuentes", json=FUENTE).json()["id"]
    f2 = client.post("/fuentes", json={**FUENTE, "titulo": "MANI SRS"}).json()["id"]
    p1 = client.post("/paginas", json=PAGINA).json()["id"]
    p2 = client.post("/paginas", json={**PAGINA, "titulo": "Tácticas"}).json()["id"]

    # una página cita varias fuentes y una fuente alimenta varias páginas
    client.put(f"/paginas/{p1}/fuentes/{f1}")
    client.put(f"/paginas/{p1}/fuentes/{f2}")
    client.put(f"/paginas/{p2}/fuentes/{f1}")
    client.put(f"/paginas/{p1}/fuentes/{f1}")  # idempotente

    assert {f["id"] for f in client.get(f"/paginas/{p1}").json()["fuentes"]} == {f1, f2}
    assert {p["id"] for p in client.get(f"/fuentes/{f1}").json()["paginas"]} == {p1, p2}

    r = client.delete(f"/paginas/{p1}/fuentes/{f2}")
    assert [f["id"] for f in r.json()["fuentes"]] == [f1]
    assert client.delete(f"/paginas/{p1}/fuentes/{f2}").status_code == 404
    assert client.put(f"/paginas/{p1}/fuentes/999").status_code == 404


def test_borrar_fuente_quita_el_vinculo(client):
    f = client.post("/fuentes", json=FUENTE).json()["id"]
    p = client.post("/paginas", json=PAGINA).json()["id"]
    client.put(f"/paginas/{p}/fuentes/{f}")
    client.delete(f"/fuentes/{f}")
    assert client.get(f"/paginas/{p}").json()["fuentes"] == []
