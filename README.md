# ArquiWiki

Trabajo de investigación y caso práctico del curso de Arquitectura de Software. Tema: **Obsidian como LLM Wiki y su conexión con diferentes agentes de IA**.

El caso práctico construye dos bases de conocimiento sobre el mismo material del curso y las compara:

- **KB-A, LLM Wiki:** un vault de markdown (`raw/` fuentes, `wiki/` páginas) que mantienen agentes de IA conectados por MCP, visible en Obsidian.
- **KB-B, RAG:** fragmentación, embeddings locales y búsqueda vectorial en pgvector, con respuesta de Claude.

Mide el consumo de tokens de cada enfoque y añade un agente "Ingeniero de Sistemas" (modelado, criterios de aceptación y evaluación con normas ISO).

> Video de demostración: _pendiente de publicar_ (se enlazará aquí).

## Requisitos

- Docker con Compose v2 (o Podman con `podman compose`, ver más abajo).
- [uv](https://docs.astral.sh/uv/) solo para ejecutar las pruebas y `scripts/smoke.sh` desde la máquina anfitriona.
- Opcional: una `ANTHROPIC_API_KEY` para que el RAG genere respuestas. Sin ella, el RAG devuelve solo los fragmentos recuperados.
- Opcional: [Obsidian](https://obsidian.md/) para abrir el vault.

## Despliegue paso a paso

```bash
git clone https://github.com/DresssOrtiz/arquiwiki.git
cd arquiwiki
cp .env.example .env
```

Edita `.env`: cambia `POSTGRES_PASSWORD` y los tres `GATEWAY_TOKEN_*` (por ejemplo con `openssl rand -hex 24`) y, si quieres respuestas del RAG, pon `ANTHROPIC_API_KEY`. En Linux, ajusta también `HOST_UID` y `HOST_GID` con tu `id -u` y `id -g`.

```bash
docker compose up --build -d
docker compose ps
```

La primera construcción descarga el modelo de embeddings (unos 220 MB) y tarda varios minutos. Cuando `api`, `rag-service`, `mcp-gateway` y `pgvector` aparezcan como `healthy`, el sistema está listo.

Precarga los datos de demostración e indexa el corpus:

```bash
scripts/seed-demo.sh
```

Verifica todo con la prueba de humo:

```bash
scripts/smoke.sh
```

Para empezar de cero: `docker compose down -v && rm -rf .runtime`.

## Servicios

| Servicio | URL | Para qué |
|----------|-----|----------|
| `api` | http://localhost:8000/docs | CRUD de Fuente y Página |
| `rag-service` | http://localhost:8001/docs | Indexar y consultar KB-B |
| `mcp-gateway` | http://localhost:8002/mcp | Acceso de los agentes al vault (KB-A) |
| `pgvector` | localhost:5432 | PostgreSQL con pgvector |

Todos los puertos se publican solo en `127.0.0.1`. Detalle de cada componente en [`docs/contrato-B.md`](docs/contrato-B.md), [`kb-rag/README.md`](kb-rag/README.md) y [`mcp-gateway/README.md`](mcp-gateway/README.md).

## Probar el CRUD

```bash
curl -s -X POST localhost:8000/fuentes -H 'content-type: application/json' \
  -d '{"titulo":"Clase 2: ATAM","tipo":"markdown","archivo_o_url":"raw/clase-02-atam-muestra.md"}'
curl -s localhost:8000/fuentes
```

También se puede usar la interfaz interactiva en http://localhost:8000/docs.

## Probar el RAG

```bash
curl -s -X POST localhost:8001/index -H 'content-type: application/json' -d '{}'
curl -s -X POST localhost:8001/query -H 'content-type: application/json' \
  -d '{"question":"¿Qué es ATAM y qué pasos tiene?","question_id":"P01"}'
```

Cada consulta queda registrada en `experiment/results/rag_queries.jsonl` con tokens, latencia y fuentes citadas.

## Usar el vault con Obsidian y los agentes

1. Abre la carpeta `.runtime/vault` como vault en Obsidian.
2. Conecta cada agente al gateway con su token (comandos en [`mcp-gateway/README.md`](mcp-gateway/README.md)).
3. Cada agente trabaja en su propia rama de git. Para llevar su trabajo a `main` y verlo en Obsidian:

```bash
scripts/merge-agents.sh
```

4. Para versionar las páginas generadas en este repositorio: `scripts/vault-export.sh`.

## Pruebas

```bash
(cd api && uv run pytest)
(cd kb-rag && uv run pytest)
(cd mcp-gateway && uv run pytest)
```

## Con Podman

El `docker-compose.yml` es compatible con `podman compose`. Los puntos que pueden requerir ajuste son el mapeo de usuarios en los volúmenes (`HOST_UID` y `HOST_GID`) y el acceso a `./.runtime`; en Podman sin privilegios agrega `:Z` a los volúmenes si SELinux está activo. Esta ruta no se probó en el equipo de desarrollo (macOS con Docker).

## Estructura

```
api/                 CRUD de Fuente y Página (FastAPI)
kb-rag/              KB-B: RAG sobre pgvector
mcp-gateway/         Gateway MCP con permisos por rol
kb-wiki/vault/       KB-A: semilla del vault (raw/, wiki/, esquemas)
agente-ing-sistemas/ Agente Ingeniero de Sistemas
experiment/          Preguntas, rúbrica y resultados
docs/                Investigación, matrices, diagramas y bitácora
presentacion/        Presentación
video/               Guion y enlace del video
scripts/             Utilidades de despliegue y demo
```

## Documentos de muestra

Los archivos `*-muestra.md` de `kb-wiki/vault/raw/` son sintéticos y sirven para probar los pipelines. Se reemplazan por los apuntes reales de las clases 1 a 5 y los documentos del proyecto MANI.

## Avances de documentación — persona A

Versiones preliminares revisadas al 25 de noviembre de 2026:

- [Documento de investigación](docs/investigacion.pdf).
- [Guion del video](video/guion.md).
- [Checklist de cobertura y pendientes](checklist.md).
- [Presentación preliminar en Canva](https://www.canva.com/d/kGASGIjBrTgCsAa).

Los diagramas, resultados experimentales y evidencias de ejecución siguen pendientes. Las claves de evaluación incluidas en el informe deben permanecer fuera del corpus y del contexto de los agentes evaluados.

## Arquitectura de alto nivel

[HLD de ArquiWiki](docs/diagramas/HLD.png).

[C4 de contexto](docs/diagramas/C4-Contexto.png).

[UML de paquetes de la API](docs/diagramas/UML-Paquetes-API.png).

[UML de paquetes del gateway](docs/diagramas/UML-Paquetes-Gateway.png).
