# Contrato del bloque B (para A y C)

Qué expone la infraestructura y cómo usarla. Si algo de aquí cambia, B actualiza este archivo.

## 1. Contenedores y puertos

Todos los puertos se publican solo en `127.0.0.1`.

| Servicio | Puerto | Tecnología | Función |
|----------|--------|-----------|---------|
| `pgvector` | 5432 | PostgreSQL 17 + pgvector | Esquema `app` (Fuente, Página) y esquema `rag` (chunks, registros) |
| `api` | 8000 | FastAPI | CRUD de Fuente y Página, relación N:M. Docs en `/docs` |
| `rag-service` | 8001 | FastAPI + fastembed | KB-B: indexación y consulta con registro de tokens |
| `mcp-gateway` | 8002 | Python, SDK `mcp` (FastMCP) | KB-A: acceso al vault por MCP con permisos por rol. Endpoint `/mcp` |
| `vault-init` | n/a | alpine/git | Tarea de una sola ejecución que crea el vault desde `kb-wiki/vault/` |

Volúmenes y rutas: `pgdata` (datos de Postgres), `./.runtime/vault` (vault de ejecución, repositorio git, el que se abre en Obsidian) y `./.runtime/worktrees/<rol>` (una copia de trabajo por agente).

## 2. Componentes por contenedor (insumo para C4 y paquetes UML)

- **api:** `routers` (fuentes, paginas, health), `schemas` (Pydantic), `models` (SQLAlchemy), `db` (sesión y creación de tablas).
- **rag-service:** `chunker` (por encabezados markdown), `embedder` (fastembed), `store` (pgvector), `llm` (cliente Anthropic), `metrics` (registro JSONL y tabla), `main` (rutas).
- **mcp-gateway:** `server` (herramientas MCP), `roles` (token a rol y permisos), `vault` (acceso seguro a rutas y git), `audit` (registro JSONL).

## 3. Entidades (API)

- **Fuente:** `id`, `titulo`, `tipo` (`pdf`, `markdown`, `url`, `otro`), `archivo_o_url`, `estado_ingesta` (`pendiente`, `ingestada`, `error`).
- **Pagina:** `id`, `titulo`, `tipo` (`concepto`, `entidad`, `comparacion`), `contenido`, `enlaces` (lista de títulos), `estado_salud` (`sin_revisar`, `ok`, `con_problemas`).
- **Relación N:M:** `PUT /paginas/{id}/fuentes/{fuente_id}` y `DELETE` del mismo recurso.

## 4. Gateway MCP: roles y permisos

Cada agente se conecta con su token Bearer (ver `.env`). Cada rol trabaja en su propia rama git (`agent/<rol>`), con copia de trabajo propia.

| Rol | Agente sugerido | Lee | Escribe |
|-----|-----------------|-----|---------|
| `ingestor` | Claude Code | `raw/`, `wiki/` | `wiki/` (todo) |
| `consultor` | Codex | `raw/`, `wiki/` | solo `wiki/consultas/` |
| `auditor` | Gemini CLI | `raw/`, `wiki/` | solo `wiki/auditoria/` |

`raw/` es de solo lectura para todos. Solo se escriben archivos `.md`.

Herramientas: `list_notes`, `read_note`, `search_notes`, `write_note`, `commit_changes`, `sync_main`. Para llevar el trabajo de los agentes a Obsidian se ejecuta `scripts/merge-agents.sh`.

## 5. Formato de los registros del experimento

Se guardan en `experiment/results/` (una línea JSON por evento).

**`rag_queries.jsonl`:** `ts`, `question_id` (opcional, lo envía quien consulta), `question`, `k`, `llm` (`anthropic` o `disabled`), `model`, `input_tokens`, `output_tokens`, `retrieved_tokens`, `retrieval_ms`, `generation_ms`, `total_ms`, `sources` (rutas citadas).

**`rag_builds.jsonl`:** `ts`, `mode` (`full` o `incremental`), `files_total`, `files_changed`, `chunks_written`, `embedded_tokens`, `llm_tokens` (siempre 0, los embeddings son locales), `elapsed_ms`.

**`gateway.jsonl`:** `ts`, `role`, `tool`, `path`, `allowed`, `chars_returned`, `bytes_written`. Los caracteres devueltos sirven como estimación aproximada (cerca de 4 caracteres por token) de lo que cada agente leyó de la wiki. Los tokens reales de KB-A salen de los contadores de uso de cada herramienta (Claude Code, Codex, Gemini CLI).

## 6. Cómo levantar y probar

```bash
cp .env.example .env        # completar contraseñas y tokens
docker compose up --build -d
docker compose ps           # todos en healthy
```

Los pasos completos estarán en el `README.md`.
