# ArquiWiki

Trabajo de investigación y caso práctico del curso de Arquitectura de Software. Tema: **Obsidian como LLM Wiki y su conexión con diferentes agentes de IA**.

El caso práctico construye dos bases de conocimiento sobre el mismo material del curso y las compara:

- **KB-A, LLM Wiki:** un vault de markdown (`raw/` fuentes, `wiki/` páginas) que mantienen agentes de IA conectados por MCP, visible en Obsidian.
- **KB-B, RAG:** fragmentación, embeddings locales y búsqueda vectorial en pgvector, con respuesta de Claude.

El experimento comparará consumo de tokens y calidad de respuesta; incorpora un agente "Ingeniero de Sistemas" (modelado, criterios de aceptación y evaluación con normas ISO).

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
  -d '{"titulo":"Atributos de calidad 3","tipo":"markdown","archivo_o_url":"raw/3-2-atributos-de-calidad-3.md"}'
curl -s localhost:8000/fuentes
```

También se puede usar la interfaz interactiva en http://localhost:8000/docs.

## Probar el RAG

```bash
curl -s -X POST localhost:8001/index -H 'content-type: application/json' -d '{}'
curl -s -X POST localhost:8001/query -H 'content-type: application/json' \
  -d '{"question":"¿Cómo define el curso la arquitectura de software y qué elementos la componen?","question_id":"P01","use_llm":false}'
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

Las cuatro muestras sintéticas están en [`kb-wiki/muestras/`](kb-wiki/muestras/), **fuera del corpus de evaluación**. `kb-wiki/vault/raw/` contiene exclusivamente los seis Markdown derivados de las presentaciones del profesor (183 diapositivas). MANI no forma parte del corpus académico de esta versión.

## Avances de documentación — persona A

Versiones preliminares revisadas al 25 de noviembre de 2026:

- [Documento de investigación](docs/investigacion.pdf) — fuente editable en [Drive](https://docs.google.com/document/d/1uFmCr0120qSVLiMvn05fTBuXrhV1pCGu08XgdMnWA38/edit); hay cambios editoriales recientes que requieren reexportar el PDF.
- [Guion del video](video/guion.md).
- [Checklist de cobertura y pendientes](checklist.md).
- [Cinco matrices comparativas exportadas a Markdown editable](docs/matrices/README.md), con fuente maestra en Google Drive.
- [Presentación preliminar en Canva](https://www.canva.com/d/kGASGIjBrTgCsAa).
- [Presentación exportada en PDF](presentacion/presentacion.pdf) — **reexportación pendiente**, porque el archivo se publicó antes de la última edición del Canva de diez diapositivas.

Ya están publicados **cinco diagramas** (HLD, C4 de contexto y tres UML de paquetes). Faltan cuatro modelos C4 y los resultados del experimento. La [bitácora](docs/bitacora.md) registra pruebas locales de Docker, API, MCP y RAG, pero aún no existe un conjunto final y comparable de respuestas y métricas. Las claves de evaluación nunca se entregan a los agentes ni se indexan.

## Arquitectura de alto nivel

[HLD de ArquiWiki](docs/diagramas/HLD.png).

[C4 de contexto](docs/diagramas/C4-Contexto.png).

[UML de paquetes de la API](docs/diagramas/UML-Paquetes-API.png).

[UML de paquetes del gateway](docs/diagramas/UML-Paquetes-Gateway.png).

[UML de paquetes del RAG](docs/diagramas/UML-Paquetes-RAG.png).

## Corpus original del curso

Los seis PDF originales están en [`docs/corpus-original/`](docs/corpus-original/); sus seis Markdown en [`kb-wiki/vault/raw/`](kb-wiki/vault/raw/) conservan **183 de 183 marcadores de diapositiva**. La revisión detectó y corrigió el orden mezclado de tres columnas de la diapositiva 31 de `1.2 Definiciones 1.pdf`; la inspección visual de **28 diapositivas** detectó gráficos cuyas relaciones no están completamente expresadas en el texto (p. ej., 1.2 diap. 11/21 y 3.1 diap. 8/9). Se debe cotejar y preservar la información visual antes de congelar el corpus. **No editar raw/ mientras B/C ejecutan las pruebas:** acordar cualquier corrección y volver a construir ambas bases con exactamente la misma versión. KB-A y KB-B deben usar exactamente las mismas versiones y hashes, sin materiales de muestra.

## Material del experimento (fuera de la indexación)

- [Quince preguntas — solo enunciados](experiment/preguntas.md), sin claves ni fuentes indicadas a los sistemas.
- [Rúbrica de evaluación 0–10](experiment/rubrica.md) para los evaluadores, nunca para los agentes.
- [Plantilla vacía de calificación](experiment/plantilla-evaluacion.csv), sin métricas ficticias.

No incluir `experiment/`, `docs/investigacion.pdf`, preguntas, rúbrica ni respuestas de referencia en `raw/`, `wiki/`, el índice vectorial o el contexto de los agentes evaluados. Separar las preguntas del material de aprendizaje no impide enviarlas individualmente durante la prueba.
