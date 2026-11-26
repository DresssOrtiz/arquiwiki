# Experimento comparativo KB-A (LLM Wiki) vs KB-B (RAG)

Compara, sobre el mismo corpus (6 PDF del curso en `kb-wiki/vault/raw/*.md`, una sección `## Diapositiva N` por página), un agente que navega la wiki por MCP (KB-A) y un RAG con pgvector (KB-B). Protocolo: capítulo 4 de `docs/investigacion.pdf`. Restricción: sin API keys de pago; toda la generación usa `claude -p` (suscripción) con **el mismo modelo** en ambos brazos.

## Estado de la evaluación exploratoria

Los PR #7, #8 y #9 están fusionados. Hay treinta respuestas históricas (15 por brazo, una repetición), no noventa, y cero errores de proceso. La corrida precede la corrección de `raw/1-2-definiciones-1.md`, diap. 31, y la corrección del tokenizador del PR #9. Su alcance es exploratorio.

- [Análisis provisional](results/analisis-provisional.md): métricas recalculadas y juicio asistido, sin ganador definitivo.
- [CSV asistido separado](results/calificacion-asistida-provisional.csv): 30 filas justificadas; NO ciego ni aprobado por Andrés. No reemplaza `calificacion.csv` ni requiere publicar su mapa privado.
- [Métricas del experimento provisional](results/metricas-experimento-provisional.json): valores recalculados a partir de los registros históricos.

`tabla.md`, `calificacion.csv`, las respuestas y todos los JSONL históricos se conservan intactos. No hay `actualizacion.jsonl` ni `overhead.jsonl`; el spike de la bitácora no sustituye la medición protocolizada. Los comandos siguientes describen el protocolo implementado. Las mediciones de actualización modifican la línea base y se realizan después de la evaluación principal, conservando por separado los resultados de cada versión.

## Archivos

| Archivo | Para qué |
|---|---|
| `preguntas.json` | 15 preguntas `{id, tipo, texto}`; es lo único que leen los runners |
| `claves.json` | `{id, fuente_verificable, respuesta_referencia}`; solo la usa `calificacion.py preparar`. Nunca se envía a un agente |
| `rubrica.md` | Rúbrica 0-10 transcrita |
| `run.py` | Corre los brazos A y B y escribe `results/experimento.jsonl` |
| `calificacion.py` | `preparar` (CSV ciego) y `destapar` (une con el mapa) |
| `reporte.py` | Genera `results/tabla.md` |
| `costo_actualizacion.py` | Costo de actualizar un documento (paso 6 del protocolo) |
| `prompts/kbb.md`, `prompts/kbb_system.md` | Prompt y system prompt de KB-B |
| `tests/` | Pruebas con `claude` y RAG falsos |

## Protocolo

1. Requisitos: `docker compose up -d` con los 4 servicios `healthy`; KB-B indexado con el corpus real; `claude` con sesión iniciada; la etiqueta `kb-a-baseline` en el vault (`.runtime/vault`) apuntando al mismo commit que `main`; tokens del gateway en `.env`.
2. Pruebas del plan sin ejecutar: `python3 experiment/run.py --brazo ambos --ids todas --reps 3 --dry-run`.
3. Medir el overhead fijo del CLI: `python3 experiment/run.py --overhead 3` (-> `results/overhead.jsonl`).
4. Corrida principal (15 x 2 x 3 = 90 respuestas):
   `python3 experiment/run.py --brazo ambos --ids todas --reps 3 --orden aleatorio --semilla 42`.
   Una sola repetición (`--reps 1`) debe declararse **exploratoria**. Opciones: `--ids P01,P02`, `--brazo A|B`, `--model`, `--k`.
5. Antes de **cada** ejecución del brazo A, `run.py` comprueba que `main` del vault == `kb-a-baseline` y resetea la rama del consultor (`git reset --hard kb-a-baseline` y `clean -fd` en `/worktrees/consultor`, vía `docker compose exec mcp-gateway`, porque desde el host el `.git` de los worktrees apunta a rutas del contenedor). Si `main` difiere, la corrida **aborta** (código 3). El consultor corre en `modo=experimento`: no tiene `write_note` ni `commit_changes`, así que no puede archivar respuestas; el reset es una segunda barrera. KB-B no tiene estado entre consultas (solo recupera).
6. Calificación ciega: `python3 experiment/calificacion.py preparar --semilla 42`; cada calificador rellena su copia del CSV (columna `calificador`; para el consenso, una fila con `consenso`); luego `python3 experiment/calificacion.py destapar --csv a.csv --csv c.csv`.
7. `python3 experiment/reporte.py` -> `results/tabla.md`.
8. **Al final**, `python3 experiment/costo_actualizacion.py --archivo raw/<x>.md --dry-run` y luego con `--yes`. Cambia la línea base (añade una diapositiva marcada al raw del vault, ingesta y fusiona en main), por eso va después del experimento principal. Se restaura con `python3 experiment/costo_actualizacion.py --restaurar --yes` (equivale a `git reset --hard kb-a-baseline` en el vault, en las ramas de los agentes, y reindexado `force` de KB-B). El script escribe desde el host en `.runtime/vault/raw` (los agentes no pueden) y hace el commit en main dentro del contenedor.

El orden por defecto intercala A y B por pregunta, alternando cuál va primero. Con `--orden aleatorio --semilla S` se baraja `(pregunta, brazo, rep)` de forma reproducible; la semilla queda en cada línea del registro.

## Equidad entre brazos

Idéntico: corpus, modelo (`--model`/`KBA_MODEL`/`claude-sonnet-5-5`), CLI y versión, directorio temporal vacío como cwd, `--tools ""`, `--setting-sources ""`, `--strict-mcp-config`, `--disable-slash-commands`, `--no-session-persistence`, `--output-format json`, ejecución secuencial, texto de la pregunta, instrucciones de respuesta (solo evidencia, citas `raw/archivo.md, diap. N`, decir si no hay evidencia, formato respuesta + `## Fuentes`, español, breve), fuente de los contadores de tokens (campo `usage` del CLI) y `ANTHROPIC_API_KEY` ignorada en ambos.

Distinto, por diseño (es lo que se compara): KB-A explora el vault con herramientas MCP de solo lectura en varios turnos y puede leer la wiki; KB-B recibe de un solo golpe los `k` fragmentos (k = `RAG_TOP_K`, 5) y no tiene herramientas. Las reglas de KB-A viven en `AGENTS.md`/`CONVENCIONES.md` del vault (el agente las lee por MCP); las de KB-B van en `prompts/kbb_system.md`. El prompt de KB-A añade "parte de `wiki/index.md`" y la línea de modo experimento (que en B no aplica); el de B añade los fragmentos.

## Qué se mide

Por respuesta (`results/experimento.jsonl`): `input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, `output_tokens`, `total_input_tokens`, `num_turns`, `wall_ms` (solo `claude -p`), `duration_api_ms`, `retrieval_ms` (servicio) y `retrieval_wall_ms` (reloj) en B, `latencia_total_ms` (A: `wall_ms`; B: recuperación + `claude -p`), `fragmentos` y `retrieved_tokens` (B), `baseline_ok` (A), `cost_usd_equiv` (precio de lista; no se paga con suscripción). Las respuestas se guardan sin editar en `results/respuestas/<qid>-<A|B>-r<rep>-<run_id>.md` (escritura exclusiva). Construcción, actualización y overhead se reportan por separado, sin sumar tokens de LLM con tokens de embeddings.

## Amenazas a la validez

- **Ceguera imperfecta.** Las respuestas de KB-A citan páginas de la wiki (`wiki/...`, `[[...]]`) y las de KB-B solo `raw/`; eso delata el sistema y es parte legítima de la trazabilidad, así que no se elimina. `preparar` avisa cuántas respuestas lo muestran. Mitigaciones: calificar por pregunta y no por sistema, anotar sospechas y reportar el límite.
- **Muestra pequeña.** 15 preguntas y 3 repeticiones no permiten inferir significancia; una sola repetición es exploratoria. Las repeticiones no son independientes (mismo modelo, misma pregunta).
- **Variabilidad del modelo y sin control de temperatura:** `claude -p` no expone temperatura ni top-p. El modelo puede cambiar de versión interna entre corridas; el registro guarda el alias, no un hash de modelo.
- **Cachés y orden:** `cache_read_input_tokens` depende de cachés del servicio y de la hora; por eso se reporta también la entrada nueva y se alterna/aleatoriza el orden.
- **Conversión del corpus:** `pdftotext` mezcla columnas en diapositivas de diagramas; ambos brazos usan el mismo markdown, pero la calidad del texto limita a los dos.
- **Preguntas que nombran el sistema:** P12, P14 y P15 mencionan KB-A/KB-B; los dos brazos ven la misma pregunta, pero puede inducir respuestas sobre el prototipo.
- **Calidad de la wiki:** la wiki de KB-A la construyó un agente y puede no haberse revisado por completo; su calidad es un factor de confusión (mide esa wiki, no solo la estrategia).
- **Aislamiento incompleto del reset:** solo se resetea la rama del consultor; si otro rol fusionó algo a `main`, el chequeo de línea base lo detecta y aborta. El índice de KB-B no se verifica contra el hash del corpus en cada pregunta: se asume el indexado congelado.
- **Latencia:** depende de la carga del servicio de Claude y de la red; la de KB-B excluye la espera entre corridas pero incluye la recuperación local.
- **Costo de actualización:** el ingestor es no determinista y la ingesta de un archivo no equivale a reindexar; se reporta cada unidad por separado.
- **Datos por errores:** las ejecuciones con `is_error` se registran pero se excluyen de medias y de la calificación; hay que reportar cuántas fueron.

## Pruebas

`uv run --with pytest pytest experiment/tests kb-wiki/agents/tests -q`
