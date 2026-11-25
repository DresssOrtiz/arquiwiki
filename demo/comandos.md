# Comandos de la demo (bloque B)

Apoyo para grabar los segmentos de B del video: arquitectura y despliegue (4:00 a 8:00) y RAG en vivo (11:00 a 12:30). Todo se ejecuta desde la raíz del repositorio. Mantén el archivo `.env` fuera de pantalla.

## Antes de grabar (una sola vez)

```bash
docker compose down -v && rm -rf .runtime       # estado limpio
docker compose up --build -d
docker compose ps                                # todo en healthy
scripts/seed-demo.sh                             # fuentes, páginas e índice RAG
scripts/smoke.sh                                 # debe terminar en TODO OK
docker compose down -v && rm -rf .runtime && docker compose up -d && scripts/seed-demo.sh   # limpia lo que dejó la prueba de humo
```

Ensayo completo antes de grabar. Si cambias el corpus, vuelve a correr `scripts/seed-demo.sh`.

## Segmento 4:00 a 6:00: arquitectura

Mostrar `docker-compose.yml` y los diagramas C4 de `docs/diagramas/` (los hace A).

```bash
docker compose ps
```

## Segmento 6:00 a 8:00: despliegue y CRUD

```bash
docker compose up -d
curl -s localhost:8000/fuentes | python3 -m json.tool
```

Abrir http://localhost:8000/docs y hacer en vivo: crear una Fuente, crear una Página, relacionarlas, actualizar, listar y borrar.

## Segmento 11:00 a 12:30: RAG en vivo

La misma pregunta que se le hace a la LLM Wiki:

```bash
curl -s -X POST localhost:8001/query -H 'content-type: application/json' \
  -d '{"question":"¿Qué pasos tiene ATAM?","question_id":"DEMO"}' | python3 -m json.tool
```

Señalar: los fragmentos recuperados con su fuente y puntaje, `usage` (tokens de entrada y salida), `retrieved_tokens` y `latency_ms`. Luego el registro acumulado:

```bash
tail -n 3 experiment/results/rag_queries.jsonl
```

Costo de actualizar un documento (agregar una línea a un archivo de `.runtime/vault/raw/` y reindexar):

```bash
curl -s -X POST localhost:8001/index -H 'content-type: application/json' -d '{}'
```

Se verá `mode: incremental` y `files_changed: 1`, con `embedded_tokens` solo de ese archivo.

## Si algo falla durante la demo

- `docker compose logs --tail 50 <servicio>` (`api`, `rag-service`, `mcp-gateway`).
- Sin `ANTHROPIC_API_KEY` la consulta devuelve fragmentos y `llm: disabled`; usa `"use_llm": false` para mostrarlo a propósito.
- Reinicio completo: `docker compose down -v && rm -rf .runtime && docker compose up -d && scripts/seed-demo.sh`.
