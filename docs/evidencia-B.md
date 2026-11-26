# Evidencia del bloque B (Tomás): ejecución real sobre `main`

Ejecutada el 25 de noviembre de 2026 sobre `main` en el commit `d4052ef`, con el corpus real de seis Markdown, desde cero (`docker compose down -v`, borrado de `.runtime/` y `docker compose up --build -d`). Es evidencia de ejecución local, no una corrida del experimento. Los registros de esta verificación se descartaron para no mezclarlos con `experiment/results/`.

## 1. Contenedores activos

| Servicio | Estado | Puerto |
|----------|--------|--------|
| `pgvector` | healthy | 5432 |
| `api` | healthy | 8000 |
| `rag-service` | healthy | 8001 |
| `mcp-gateway` | healthy | 8002 |
| `vault-init` | terminó con código 0 (siembra única) | n/a |

Pruebas unitarias: `api` 8 correctas, `kb-rag` 16 correctas y 1 de integración (se salta sin pgvector), `mcp-gateway` 25 correctas. `scripts/seed-demo.sh` y `scripts/smoke.sh` terminaron en OK.

## 2. Los mismos seis Markdown en KB-A y KB-B

KB-B indexa `/vault/raw`, que se siembra desde `kb-wiki/vault/raw/`, la misma carpeta que usa KB-A. Resultado de `GET /stats`: 6 documentos, 189 fragmentos. SHA-256 de cada archivo frente al hash guardado en `rag.documents`:

| Archivo | SHA-256 (12 primeros) | Fragmentos | Índice |
|---------|----------------------|-----------|--------|
| `1-2-definiciones-1.md` | `a8a2a0976426` | 49 | igual |
| `2-1-definiciones-2.md` | `daf41bbea821` | 18 | igual |
| `2-2-atributos-de-calidad-1.md` | `bf874be0dd38` | 45 | igual |
| `3-1-atributos-de-calidad-2.md` | `6d42183503fa` | 23 | igual |
| `3-2-atributos-de-calidad-3.md` | `e34c847265a9` | 33 | igual |
| `5-1-estilos-y-patrones-arquitecturales-3.md` | `088b1a4a8c23` | 21 | igual |

**Diferencia con la corrida preliminar de Santiago.** Comparando con el commit `6b4dbb6` (corpus real de Santiago, antes de la corrección de A), cinco archivos son idénticos y solo cambió `1-2-definiciones-1.md` (commit `52e24c7`, corrección de la diapositiva 31). Su indexado registró 14 388 tokens de embeddings y este 14 412. La corrida preliminar de KB-B se hizo, por lo tanto, sobre una versión anterior de ese archivo.

## 3. CRUD de Fuente y Página con relación N:M

Salida real de la API (cuerpos recortados):

```text
POST   /fuentes                 -> 201  {"titulo":"Evidencia B: Estilos","tipo":"markdown","estado_ingesta":"pendiente","id":10}
POST   /paginas                 -> 201  {"titulo":"Pagina de evidencia","tipo":"comparacion","estado_salud":"sin_revisar","id":7,"fuentes":[]}
PUT    /paginas/7/fuentes/10    -> 200  (la página ahora lista la fuente)
GET    /fuentes/10              -> 200  {"id":10,...,"paginas":[{"id":7,"titulo":"Pagina de evidencia"}]}
PUT    /paginas/7               -> 200  {"estado_salud":"ok",...}
POST   /paginas (título repetido) -> 409 {"detail":"Ya existe una página con ese título"}
POST   /fuentes (tipo inválido)   -> 422 {"detail":[{"msg":"Input should be 'pdf', 'markdown', 'url' or 'otro'"}]}
DELETE /paginas/7/fuentes/10    -> 200  {"fuentes":[]}
DELETE /paginas/7               -> 204
DELETE /fuentes/10              -> 204
GET    /fuentes/10              -> 404  {"detail":"Fuente no encontrada"}
```

`scripts/seed-demo.sh` crea las seis fuentes reales y dos páginas (`ATAM` desde `3-2-atributos-de-calidad-3.md` y `Atributos de calidad` desde `2-2-atributos-de-calidad-1.md`), y verifica cada relación.

## 4. Permisos del gateway MCP (`scripts/mcp_check.py`)

| Comprobación | ingestor | consultor | auditor |
|--------------|----------|-----------|---------|
| Sin token | 401 | 401 | 401 |
| `whoami` devuelve el rol del token | sí | sí | sí |
| Lee `raw/` (6 notas) | sí | sí | sí |
| Escribe en `raw/` | denegado | denegado | denegado |
| Ruta con `..` | denegada | denegada | denegada |
| Escribe en su carpeta | `wiki/` permitido | `wiki/consultas/` permitido | `wiki/auditoria/` permitido |
| `commit_changes` | rama `agent/ingestor` | rama `agent/consultor` | rama `agent/auditor` |
| Escribe en `wiki/otra.md` | n/a | denegado | n/a |

Cada llamada queda registrada en `experiment/results/gateway.jsonl` (rol, herramienta, ruta, permitido, caracteres devueltos, bytes escritos).

## 5. Consulta RAG real (sin LLM)

Pregunta P03, `use_llm:false`, `k=5`:

| Fuente | Encabezado | Puntaje |
|--------|-----------|---------|
| `raw/1-2-definiciones-1.md` | Diapositiva 41 | 0,4793 |
| `raw/3-1-atributos-de-calidad-2.md` | Diapositiva 17 | 0,4542 |
| `raw/1-2-definiciones-1.md` | Diapositiva 42 | 0,4498 |
| `raw/3-1-atributos-de-calidad-2.md` | Diapositiva 16 | 0,3941 |
| `raw/1-2-definiciones-1.md` | Diapositiva 43 | 0,3902 |

Recuperación en 22 ms. Las diapositivas 41 y 42 de la clase 1.2 son la fuente de referencia de P03. Con `use_llm:false` no hay consumo de tokens de LLM. La ruta de generación nativa (`AnthropicLLM`) no se ejecutó aquí por falta de clave; los tokens de la corrida preliminar vienen del CLI `claude -p` de Santiago.

## 6. Hallazgo técnico: el contador de tokens de KB-B se saturaba en 128

**Qué ocurría.** El tokenizador de `paraphrase-multilingual-MiniLM-L12-v2` trunca y rellena a 128 tokens, y `FastEmbedder.count_tokens` lo usaba tal cual. Como el contador nunca superaba 128, el fragmentador (límite configurado de 200) no partía los fragmentos largos, y el modelo de embeddings solo veía los primeros 128 tokens de cada uno.

**Medición sobre el índice de `main` (189 fragmentos).** Se reprodujo el índice exacto (189 fragmentos y 14 412 tokens) y se recontó con un tokenizador sin truncar ni rellenar:

| Medida | Valor |
|--------|-------|
| Fragmentos cuyo texto real supera 128 tokens | 40 (21 %) |
| Fragmentos que superan el límite configurado de 200 | 19; el máximo real es 375 |
| Tokens reales del corpus indexado | 17 613 |
| Tokens registrados (`embedded_tokens`) | 14 412, un 18,2 % menos |
| Tokens de texto que el embedding no veía | 3 201 (18,2 % del corpus) |

Una primera medición de este mismo hallazgo dio 30 % y un máximo de 384 tokens. Estaba inflada, porque los trozos desbordados por el tokenizador vienen rellenados hasta 128. Las cifras de la tabla son las correctas.

**Consecuencias.**
- La recuperación era ciega al final de los fragmentos largos. Es una causa plausible, **no demostrada**, de los fallos de KB-B en P02 y P09 de la corrida preliminar. No se comprobó con las 15 preguntas a propósito, para no ajustar el recuperador mirando el conjunto de evaluación; lo mostrará la repetición oficial.
- `embedded_tokens` y `retrieved_tokens` eran cotas inferiores. Los tokens de entrada que usa el experimento salen del CLI y no se afectan.

**Corrección (rama `fix/rag-conteo-tokens`).** El contador usa una copia del tokenizador sin truncamiento ni relleno; el tamaño de fragmento por defecto baja a 120 tokens y se recorta a la ventana del modelo si se configura un valor mayor. Resultado sobre el mismo corpus de `main`, con pgvector real:

| Medida | Antes | Después |
|--------|-------|---------|
| Fragmentos | 189 | 280 |
| Tokens embebidos (`embedded_tokens`) | 14 412 (registrado) | 20 234 |
| Máximo de tokens por fragmento | 375 | 118 |
| Fragmentos sobre la ventana de 128 | 40 | 0 |
| Tokens registrados igual a los reales | no | sí |

Pruebas de `kb-rag`: 21 correctas, con la de integración contra pgvector y el modelo reales. El índice cambia, así que hay que reindexar con `{"force": true}` antes de repetir KB-B con el corpus congelado.
