# ArquiWiki

Trabajo de investigación y caso práctico del curso de Arquitectura de Software. Tema: **Obsidian como LLM Wiki y su conexión con diferentes agentes de IA**.

El caso práctico construye dos bases de conocimiento sobre el mismo material del curso y las compara:

- **KB-A, LLM Wiki:** un vault de markdown (`raw/` fuentes, `wiki/` páginas) que mantienen agentes de IA conectados por MCP, visible en Obsidian.
- **KB-B, RAG:** fragmentación, embeddings locales y búsqueda vectorial en pgvector, con respuesta de Claude.

El experimento dispone de una corrida exploratoria de 30 respuestas para comparar consumo de tokens y calidad; incorpora un agente "Ingeniero de Sistemas" (modelado, criterios de aceptación y evaluación con normas ISO).

> [Video de presentación y demostración publicado](https://www.youtube.com/watch?v=dM8YIQNSeJo).

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
scripts/             Utilidades de despliegue y demo
```

## Documentos de muestra

Las cuatro muestras sintéticas están en [`kb-wiki/muestras/`](kb-wiki/muestras/), **fuera del corpus de evaluación**. `kb-wiki/vault/raw/` contiene exclusivamente los seis Markdown derivados de las presentaciones del profesor (183 diapositivas). MANI no forma parte del corpus académico de esta versión.

## Entregables

| Entregable | Acceso |
|---|---|
| Documento de investigación | [PDF de 44 páginas](docs/investigacion.pdf) · [Google Docs original](https://docs.google.com/document/d/1uFmCr0120qSVLiMvn05fTBuXrhV1pCGu08XgdMnWA38/edit) |
| Presentación | [PDF de diez diapositivas](presentacion/presentacion.pdf) · [Diseño original de Canva](https://www.canva.com/design/DAHb9ZDCH9o/pnZFvTz0BX4SO7rZ1X5MRw/edit) |
| Repositorio | [Código, documentación y evidencias de ArquiWiki](https://github.com/DresssOrtiz/arquiwiki) |
| Video | [Presentación y demostración del equipo](https://www.youtube.com/watch?v=dM8YIQNSeJo) |

El documento consolida investigación, cinco matrices, nueve diagramas, resultados y limitaciones del estudio exploratorio. La presentación conserva diez diapositivas y el video está publicado. Las fuentes editables originales se conservan en Google Docs y Canva. Las [matrices editables](docs/matrices/README.md) y la [checklist de cobertura](checklist.md) complementan la entrega.

Versión propuesta para la entrega: **v1.0.0**. El tag está pendiente de aprobación y creación; no se presenta como una versión ya publicada.

## Estado del proyecto y alcance de los resultados

Ya están publicados los **nueve diagramas**: HLD, cinco vistas C4 (contexto, contenedores, componentes del Gateway, dinámica y despliegue) y tres UML de paquetes. Los PR [#7](https://github.com/DresssOrtiz/arquiwiki/pull/7), [#8](https://github.com/DresssOrtiz/arquiwiki/pull/8) y [#9](https://github.com/DresssOrtiz/arquiwiki/pull/9) están fusionados. Hay [pruebas documentadas de B](docs/evidencia-B.md), [bitácora de C](docs/bitacora.md) y [30 respuestas históricas](experiment/results/respuestas/), una repetición de las quince preguntas por brazo. Las claves de evaluación nunca se entregan a los agentes ni se indexan.

El [análisis exploratorio](experiment/results/analisis-provisional.md), las [30 calificaciones asistidas provisionales](experiment/results/calificacion-asistida-provisional.csv) y las [métricas del experimento](experiment/results/metricas-experimento-provisional.json) documentan los resultados disponibles. Las notas están pendientes de validación humana y no constituyen una evaluación ciega ni definitiva. La corrida precede la corrección del corpus 1.2/31 y el arreglo de truncamiento del RAG (PR #9). No hay mediciones controladas de actualización ni overhead del CLI.

## Arquitectura de alto nivel

[HLD de ArquiWiki](docs/diagramas/HLD.png).

[C4 de contexto](docs/diagramas/C4-Contexto.png).

[UML de paquetes de la API](docs/diagramas/UML-Paquetes-API.png).

[UML de paquetes del gateway](docs/diagramas/UML-Paquetes-Gateway.png).

[UML de paquetes del RAG](docs/diagramas/UML-Paquetes-RAG.png).

## Corpus original del curso

Los seis PDF originales están en [`docs/corpus-original/`](docs/corpus-original/). Deben convertirse a **Markdown revisado** para alimentar KB-A y KB-B. Sus seis Markdown en [`kb-wiki/vault/raw/`](kb-wiki/vault/raw/) conservan 183/183 marcadores. La revisión de fidelidad comprende control estructural/léxico de las 183 páginas y revisión visual seleccionada de 50; quedan 133 sin revisión visual completa. La corrección de 1.2/31 ya existe, pero imágenes y relaciones de otras láminas siguen incompletas en texto. Una nueva evaluación requiere una versión congelada común del corpus, con archivos/hashes idénticos en ambos brazos y reconstrucción/reindexado de las bases. Las muestras siguen separadas fuera del corpus.

## Material del experimento (fuera de la indexación)

- [Quince preguntas — solo enunciados](experiment/preguntas.md), sin claves ni fuentes indicadas a los sistemas.
- [Rúbrica de evaluación 0–10](experiment/rubrica.md) para los evaluadores, nunca para los agentes.
- [Plantilla vacía de calificación](experiment/plantilla-evaluacion.csv), sin métricas ficticias.

No incluir `experiment/`, `docs/investigacion.pdf`, preguntas, rúbrica ni respuestas de referencia en `raw/`, `wiki/`, el índice vectorial o el contexto de los agentes evaluados. Separar las preguntas del material de aprendizaje no impide enviarlas individualmente durante la prueba.

[C4 de contenedores](docs/diagramas/C4-Contenedores.png).

[C4 de componentes del Gateway MCP](docs/diagramas/C4-Componentes-Gateway.png).

[C4 dinámico: consulta KB-B](docs/diagramas/C4-Dinamico.png). Representa el flujo del runner de experimento implementado en el [PR #7](https://github.com/DresssOrtiz/arquiwiki/pull/7).

[C4 de despliegue](docs/diagramas/C4-Despliegue.png).
