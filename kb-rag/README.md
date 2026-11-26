# kb-rag (KB-B)

Servicio RAG: fragmenta el corpus de `raw/`, calcula embeddings locales, los guarda en pgvector y responde con Claude citando fuentes. Registra tokens y latencia de cada operación para el experimento.

## Cómo funciona

1. **Fragmentación** (`app/chunker.py`): por encabezados markdown. Cada fragmento lleva su ruta de encabezados como prefijo. Máximo 120 tokens por fragmento (`RAG_CHUNK_TOKENS`): el modelo de embeddings solo procesa 128 tokens por texto y descarta el resto, así que un fragmento más largo quedaría parcialmente invisible a la búsqueda. Si se configura un valor mayor que la ventana del modelo, el servicio lo recorta y lo avisa en el log. Los tokens se cuentan con una copia del tokenizador sin truncamiento ni relleno; contar con el tokenizador original satura el conteo en 128 y subestima el texto. Los párrafos más largos se parten con solapamiento de 20 palabras.
2. **Embeddings** (`app/embedder.py`): `paraphrase-multilingual-MiniLM-L12-v2` (384 dimensiones) con fastembed/ONNX. Corre en el contenedor y el modelo se descarga al construir la imagen. No consume tokens de ningún LLM.
3. **Almacén** (`app/store.py`): tablas `rag.documents` y `rag.chunks` con índice HNSW de similitud coseno.
4. **Consulta** (`app/service.py`): embebe la pregunta, recupera los `k` fragmentos más cercanos y, si hay `ANTHROPIC_API_KEY`, pide la respuesta a Claude con esos fragmentos como único contexto (`app/llm.py`).

## API (puerto 8001, docs en `/docs`)

| Ruta | Descripción |
|------|-------------|
| `POST /index` | `{}` indexa todo; `{"path": "raw/x.md"}` un archivo; `{"force": true}` reprocesa aunque no haya cambios |
| `POST /query` | `{"question": "...", "k": 5, "question_id": "P01", "use_llm": true}` |
| `GET /stats` | Documentos, fragmentos y tokens indexados |
| `GET /health` | Salud |

Respuesta de `/query`: `answer`, `fragments` (fuente, encabezado, puntaje, texto), `usage` (tokens de entrada y salida del LLM), `retrieved_tokens`, `latency_ms` y `sources`.

Sin `ANTHROPIC_API_KEY` o con `use_llm: false` solo se recupera (`llm: "disabled"`).

## Qué se mide

- **Construcción:** `rag_builds.jsonl`. `embedded_tokens` cuenta los tokens que pasaron por el modelo de embeddings. `llm_tokens` es siempre 0, porque el RAG no usa un LLM para construirse. Esto es lo que debe compararse con los tokens que gasta un agente al ingestar la wiki.
- **Actualización:** reindexar tras cambiar un documento reprocesa solo ese archivo (hash SHA-256). El registro `mode: "incremental"` da el costo.
- **Consulta:** `rag_queries.jsonl` guarda tokens de entrada y salida reales del LLM (campo `usage` de la API de Anthropic), tokens recuperados, latencias y fuentes citadas.

Los mismos registros se guardan en las tablas `rag.build_log` y `rag.query_log`.

## Pruebas

```bash
cd kb-rag && uv run pytest
```

La prueba de integración usa pgvector y el modelo reales, y se salta sin `TEST_DATABASE_URL`:

```bash
TEST_DATABASE_URL=postgresql://usuario:clave@localhost:5432/base uv run pytest -m integration
```

## Cambiar de modelo de embeddings

Cambiar `EMBEDDING_MODEL` cambia la dimensión de los vectores. El servicio lo detecta y se niega a arrancar con el esquema anterior: elimina el esquema `rag` (`DROP SCHEMA rag CASCADE`) y reindexa.
