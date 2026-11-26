# Bitácora de construcción (bloque C: LLM Wiki, agentes y experimento)

Registro de cómo se construyó KB-A, qué se decidió, qué falló y cuánto costó en tokens cada paso. Las entradas son cronológicas; los números salen de `experiment/results/*.jsonl`.

## 2026-11-25 · Preparación y línea base

- Se clonó el repositorio y se trabajó en la rama `feat/kb-wiki`. `.env` se generó con secretos aleatorios (`openssl rand`) y nunca se versiona.
- `docker compose up --build -d`: los cuatro servicios quedan `healthy`. `scripts/seed-demo.sh` indexó las 4 fuentes de muestra en KB-B: 16 fragmentos y 1034 tokens de embeddings, 0 tokens de LLM, en 299 ms. `scripts/smoke.sh` y `scripts/mcp_check.py` dieron **TODO OK**.

## 2026-11-25 · Decisión: sin API keys de pago

La API de Anthropic se cobra por uso, así que toda la generación del experimento se hace con los CLI de suscripción. KB-B usa el RAG de B con `use_llm:false` (solo recuperación) y la respuesta la genera el mismo CLI y el mismo modelo que en KB-A. El costo es cero y el contador de tokens es el mismo en los dos brazos.

## 2026-11-25 · Spike: Claude Code sin interfaz como agente de la wiki

Invocación validada (Claude Code 2.1.303), ejecutada desde un directorio temporal vacío:

```
claude -p "<prompt>" --output-format json --model claude-sonnet-5-5 \
  --mcp-config <json con Bearer del rol> --strict-mcp-config --tools "" \
  --allowedTools "mcp__arquiwiki__..." --setting-sources "" \
  --disable-slash-commands --no-session-persistence --system-prompt "<rol>"
```

| Configuración | Tokens de entrada (cache creation + read) | Observación |
|---|---|---|
| Por defecto (`--allowedTools` solamente) | 37 456 + 72 349 | Carga el prompt de sistema completo de Claude Code, plugins y hooks del usuario. **Además el agente pudo usar Bash** (`ls`) aunque no estaba en `--allowedTools`. |
| Aislada (comando de arriba) | 2 749 + 2 441 | Solo ve las herramientas MCP. Al pedirle que liste el directorio, respondió que no podía. |
| Sobrecarga fija sin herramientas ("Responde solo: ok") | 924 | Línea base del CLI que se reporta aparte en el experimento. |

Conclusión: `--tools ""` es obligatorio para aislar al agente, porque `--allowedTools` solo aprueba permisos y no restringe el conjunto de herramientas. `--setting-sources ""` evita que entren los hooks y plugins personales. `--bare` no sirve, porque exige `ANTHROPIC_API_KEY`. La salida JSON trae `usage` (input, cache_creation, cache_read y output), `num_turns`, `duration_ms` y `total_cost_usd`. Con suscripción, este último es solo un costo equivalente a precio de lista.

## 2026-11-25 · Spike: Antigravity CLI (`agy` 1.5.17) como auditor

- El servidor se registró con `agy mcp add --header 'Authorization: Bearer ${GATEWAY_TOKEN_AUDITOR}' arquiwiki http://127.0.0.1:8002/mcp` y quedó en `~/.gemini/config/mcp_config.json`. `--settings` no acepta `mcpServers`, así que no existe configuración por sesión.
- **Falla:** en modo `agy -p` el agente no recibe las herramientas MCP y el gateway no registra ninguna petición. El log (`--log-file`) muestra `Not reloading plugin MCP servers: cannot get the signed-in user`: en modo print los servidores se intentan cargar antes de que termine la autenticación silenciosa.
- **Riesgo encontrado:** en modo Auto, `agy` lee archivos fuera del workspace sin pedir permiso (lo dice su changelog). En el spike leyó archivos del directorio padre. Mitigación: lanzarlo siempre desde un directorio vacío fuera del repositorio (nunca donde esté `.env`) y con `--sandbox`.
- `agy -p --output-format json` sí reporta `usage` (`input_tokens`, `output_tokens`, `thinking_tokens`, `cache_read_tokens`).
- Decisión: el auditor con Gemini se ejecuta en modo **interactivo** (pendiente de verificar con `/mcp`). Para las corridas automáticas, el auditor usa Claude con el esquema `GEMINI.md`, y la bitácora indica qué motor hizo cada lint.

## 2026-11-25 · Esquemas y estructura del vault (WP1, WP2)

- Las convenciones quedaron en una sola fuente, `CONVENCIONES.md` en la raíz del vault, porque el gateway solo deja leer `raw/`, `wiki/` y los `.md` de la raíz. Los tres esquemas solo describen el flujo de su rol.
- El frontmatter quedó alineado con la entidad `Pagina` de la API (`titulo`, `tipo`, `enlaces`, `estado_salud`). Las consultas archivadas y los reportes de lint usan `tipo: consulta` y `tipo: auditoria`, que no existen en el enum de la API; si se sincronizan con la API, esas carpetas se excluyen.
- `index.md` y `log.md` solo los puede escribir el ingestor. Por eso él también indexa las consultas y los reportes de lint en su siguiente corrida.
- El consultor tiene dos modos: **demo** (archiva y hace commit) y **experimento** (solo lectura: su `--allowedTools` excluye `write_note` y `commit_changes`).

## 2026-11-25 · Agente Ingeniero de Sistemas (WP6)

- Perfil, subagente de Claude Code y tres skills (`modelar`, `criterios-aceptacion`, `evaluar-iso`), con dos ejemplos completos.
- Validación: `structurizr/structurizr validate` (exit 0 en los dos modelos; un DSL roto de control da exit 1) y `plantuml -syntax` (los 4 `.puml` válidos). La imagen `structurizr/cli` está descontinuada y no valida nada.
- Pendiente: reemplazar los requisitos de ejemplo por RF reales del SRS de MANI, cotejar los resúmenes de las normas ISO con el texto oficial y confirmar con el docente la interpretación de las normas.

## 2026-11-25 · Primer ciclo completo con las muestras (WP5)

Corpus: las 4 muestras sintéticas de `raw/`, de unos 1 KB cada una. Motor: `claude-sonnet-5-5` sin interfaz. Datos tomados de `experiment/results/kba_runs.jsonl`.

| Operación | Rol | Entrada total (cache creation + read) | Salida | Turnos | Tiempo |
|---|---|---|---|---|---|
| Ingesta clase-01 | ingestor | 42 246 (10 483 + 31 753) | 3 608 | 15 | 23 s |
| Ingesta clase-02 | ingestor | 65 182 (14 569 + 50 601) | 4 577 | 18 | 27 s |
| Ingesta clase-03 | ingestor | 67 750 (21 204 + 46 536) | 10 354 | 25 | 110 s |
| Ingesta mani-srs | ingestor | 66 813 (20 393 + 46 410) | 9 419 | 24 | 51 s |
| Lint | auditor (Claude con `GEMINI.md`) | 99 797 | 4 961 | 31 | 34 s |
| Consulta en modo demo | consultor | 61 129 | 3 075 | 14 | 22 s |

- **Construcción de KB-A con las muestras:** unos 242 000 tokens de entrada y 27 958 de salida para 17 páginas (14 conceptos y 3 entidades). La de KB-B fue de 1 034 tokens de embeddings y 0 de LLM. La entrada está dominada por relecturas de caché: cada turno del agente vuelve a enviar el contexto acumulado.
- **Calidad:** el lint no encontró hallazgos altos ni medios, solo 3 bajos (una cita sin sección y un resumen sin cita). La revisión manual de `atam.md` contra su fuente confirmó que las citas son fieles. La consulta citó la wiki y `raw/` y declaró como vacío lo que las fuentes no dicen (qué tácticas usa MANI).
- **Flujo de ramas:** `agent/ingestor` → `merge-agents.sh` → `main`, y luego el auditor y el consultor en sus ramas → nueva fusión. Dentro de `.runtime/worktrees/<rol>` `git log` no funciona porque el `.git` apunta a la ruta del contenedor; hay que usar `git -C .runtime/vault log --all`.
- **Pendiente:** una pasada de corrección del ingestor para aplicar `estado_salud: ok` e indexar el lint y la consulta. Hay que repetir todo con el corpus real cuando lleguen los PDF.

## 2026-11-25 · Corpus real (WP3 aplicado)

- Andrés subió los 6 PDF del profesor a `docs/corpus-original/` (183 diapositivas). Se convirtieron con `scripts/pdf2md.py` a `kb-wiki/vault/raw/`: 66 KB de markdown, ninguna diapositiva vacía. El pie repetido "Andrés Armando Sánchez Martín" se eliminó automáticamente.
- Se retiraron las 4 muestras sintéticas. Sus corridas se descartaron del registro del experimento porque eran pruebas del pipeline.
- Limitación: en las diapositivas que son diagramas (por ejemplo 1.2, diap. 31) `pdftotext -layout` mezcla columnas. El texto se puede leer, pero pierde estructura. Andrés debe cotejar la conversión contra los PDF, según el protocolo del capítulo 4.
- KB-B reindexado con el corpus real: 189 fragmentos y 14 388 tokens de embeddings en 3,2 s, con 0 tokens de LLM. Comprobación: la pregunta de P03 (SRP y DIP) recupera 1.2, diap. 41 y 42, que es justo la fuente de referencia de A.

## 2026-11-25 · Cambios por revisión del PR #4

- **Muestras separadas del corpus:** las 4 muestras sintéticas se restauraron (desde `e064388^`) en `kb-wiki/muestras/`, fuera de `kb-wiki/vault/`, con un README que aclara que no son parte del corpus evaluado ni se cargan en KB-A/KB-B. `kb-wiki/vault/raw/` queda solo con los 6 archivos reales.
- **`scripts/seed-demo.sh`:** ahora mapea ATAM a `3-2-atributos-de-calidad-3.md` y "Atributos de calidad" a `2-2-atributos-de-calidad-1.md` (verificado con grep; ATAM solo figura en el temario de 3.2, así que el texto de la página se limitó a lo que dice la fuente). Tras la precarga comprueba con `GET /paginas/{id}` que cada página tenga su fuente, también en la rama idempotente (por título); si falta algo imprime error y sale con código 1. Probado desde cero, segunda corrida y fallo provocado.
- **`run_agent.py`:** `run_id` único (`uuid4().hex[:12]`) en el nombre del archivo de respuesta, en cada línea de `kba_runs.jsonl` (incluidos errores) y en el dict devuelto; la respuesta se escribe con `open(..., "x")`. Prueba nueva con reloj fijo y dos corridas de P01.

## 2026-11-25 · Construcción de KB-A con el corpus real (WP5)

Corpus: los 6 PDF del curso (183 diapositivas, 66 KB de markdown). Motor: `claude-sonnet-5-5` sin interfaz. Datos tomados de `experiment/results/kba_runs.jsonl`.

| Operación | Entrada total | Salida | Turnos | Tiempo |
|---|---|---|---|---|
| Ingesta 1.2 Definiciones 1 | 136 091 | 16 929 | 26 | 89 s |
| Ingesta 2.1 Definiciones 2 | 150 797 | 14 599 | 28 | 75 s |
| Ingesta 2.2 Atributos de calidad 1 | 185 271 | 21 349 | 30 | 106 s |
| Ingesta 3.1 Atributos de calidad 2 | 142 956 | 14 545 | 24 | 110 s |
| Ingesta 3.2 Atributos de calidad 3 | 305 256 | 31 706 | 42 | 158 s |
| Ingesta 5.1 Estilos y patrones 3 | 117 009 | 13 959 | 19 | 70 s |
| **Subtotal ingesta** | **1 037 380** | **113 087** | 169 | 10 min |
| Lint (auditor, Claude con `GEMINI.md`) | 603 745 | 24 622 | 70 | 230 s |
| Corrección (ingestor) | 945 846 | 72 026 | 121 | 327 s |
| **Total de construcción** | **2 586 971** | **209 735** | 360 | 19 min |

- **Resultado:** 54 páginas (conceptos, entidades y 5 comparaciones), todas con `estado_salud: ok` tras el lint y la corrección. Los 6 commits de ingesta, el lint y la corrección quedaron fusionados en `main` del vault de ejecución, con la etiqueta **`kb-a-baseline`**: es el estado al que vuelve el experimento antes de cada pregunta. La wiki se exportó a `kb-wiki/vault/wiki/` con `scripts/vault-export.sh` para versionarla.
- **Comparación con KB-B:** la construcción de KB-B costó 14 388 tokens de embeddings y 0 de LLM, en 3,2 s. La de KB-A costó unos 2,6 millones de tokens de entrada del LLM (más del 99 % son relecturas de caché) y 210 mil de salida. Son unidades distintas y no se suman.
- **Calidad (revisión manual):** `principios-solid` coincide palabra por palabra con 1.2, diap. 41-42 (respuesta de P03). `escenarios-de-calidad` reconstruye bien los seis componentes de 3.1, diap. 6, aunque `pdftotext` había mezclado las columnas. El agente declara qué diapositivas son solo imagen en vez de inventar su contenido.
- **Lint:** 0 hallazgos altos o medios y 5 bajos (un sinónimo distinto entre páginas, una frase sin cita, `fuentes` y `enlaces` incompletos en el frontmatter y el índice sin el reporte). Los corrigió el ingestor.
- **Hallazgo de costo:** la corrección costó casi lo mismo que la ingesta completa (946 mil tokens de entrada) para cambiar sobre todo un campo del frontmatter en 54 páginas. La causa es que `write_note` reemplaza el archivo entero, así que cada cambio obliga a leer y reescribir la página completa. Para la discusión del experimento: el mantenimiento de una LLM Wiki es caro con herramientas de escritura de grano grueso. Una herramienta de parche (por ejemplo, actualizar solo el frontmatter) en el gateway lo abarataría; queda como recomendación para B.

## 2026-11-25 · Experimento comparativo (WP7)

- **Qué se construyó** (`experiment/`): `preguntas.json` y `claves.json` (15 preguntas transcritas del cap. 4.2 con un script de extracción, revisadas contra el PDF), `rubrica.md`, `run.py` (brazos A y B, overhead, dry-run), `calificacion.py` (CSV ciego y destape), `reporte.py` (tablas), `costo_actualizacion.py` y pruebas. Detalle y amenazas en `experiment/README.md`.
- **Equidad:** mismo modelo y misma invocación aislada de `claude -p` en ambos brazos (solo cambia que A lleva el MCP del consultor y B ninguna herramienta). B recibe los fragmentos de `/query` con `use_llm:false` y reglas de respuesta equivalentes a `AGENTS.md`. Antes de cada pregunta de A se verifica que `main` == `kb-a-baseline` y se resetea la rama del consultor vía `docker compose exec`; si difiere, la corrida aborta.
- **Decisiones:** `run.py` ignora `ANTHROPIC_API_KEY` para no cobrar la API; `latencia_total_ms` de B suma recuperación y generación; el parseo de la salida JSON de `claude` se replicó en `run.py` porque `run_agent` no lo expone como función (convendría extraerlo).
- **Verificado:** pruebas con `claude` y RAG falsos (38 en verde junto con las de `run_agent`). No se ejecutó ninguna corrida real ni se consultó el RAG; los números llegarán con la corrida principal.
- **Pendiente:** corrida de 90 respuestas, calificación ciega por dos personas, y el costo de actualización (después de la corrida principal; cambia la línea base).

## 2026-11-25 · Piloto del experimento (P01, una repetición)

| Brazo | Entrada total | Salida | Latencia total | Fuentes citadas |
|---|---|---|---|---|
| A (LLM Wiki) | 40 036 | 1 929 | 15,3 s | 1.2 diap. 18, 19, 24, 25; 2.1 diap. 4 y 6, además de 3 páginas de la wiki |
| B (RAG, k=5) | 2 956 | 772 | 7,5 s (recuperación + generación) | 1.2 diap. 24 y 25 |

- Las dos respuestas contienen la referencia de Andrés (42010 y elementos, relaciones y propiedades, 1.2 diap. 24-25). A sintetiza más: agrega diseño frente a arquitectura y patrón frente a estilo, porque sigue los enlaces de la wiki. B se limita a los 5 fragmentos y declara como vacío lo que no recuperó.
- El estado de A se verificó antes de la pregunta: `main` == `kb-a-baseline` (fe38dfd). La consulta no cambió el vault.
- A gastó unas 13,5 veces más tokens de entrada que B y tardó el doble. Es un solo dato, así que todavía no se generaliza.

## 2026-11-25 · Corrida principal del experimento (15 preguntas, 1 repetición)

Se hizo en 3 tandas (P01 del piloto, P02-P05, P06-P10 y P11-P15) para no agotar el cupo de la suscripción. Son 30 ejecuciones, sin errores. `main` del vault quedó igual a `kb-a-baseline` (fe38dfd) antes y después de cada pregunta de A. Las tablas completas están en `experiment/results/tabla.md`.

| Por consulta (media) | KB-A (wiki) | KB-B (RAG) |
|---|---|---|
| Entrada total | 41 417 | 2 962 |
| Entrada nueva (sin relecturas de caché) | 15 202 | 2 962 |
| Salida | 1 509 | 684 |
| Turnos | 7,9 | 1 |
| Latencia (mediana) | 16,5 s | 7,3 s |

- **Consumo de la corrida:** unos 0,67 millones de tokens de entrada (621 mil de A y 44 mil de B), con un costo equivalente de unos $1,30. Como se usa la suscripción, no hubo costo monetario.
- **Por tipo de pregunta:** las de síntesis son las más caras para A (58 mil de entrada en promedio y 9,2 turnos), porque el agente sigue enlaces entre páginas. Para B el costo casi no cambia con el tipo de pregunta (unos 3 mil por consulta).
- **Observaciones cualitativas** (preliminares; la calificación ciega está pendiente):
  - **P02:** B no recuperó 1.2, diap. 31 (diagrama cuyo texto quedó desordenado) y respondió que no tenía la información. A respondió bien, porque la ingesta había reconstruido el diagrama.
  - **P09:** B no recuperó ningún fragmento de la clase 5.1 sobre estilos. A encontró las dos familias con sus diapositivas y aclaró qué comparación no está en el corpus.
  - **P14 y P15 (abstención):** ambos brazos declararon que no tenían evidencia y no inventaron cifras.
- **Calificación:** `calificacion.csv` se generó con etiquetas ciegas (semilla 20261125). La deben llenar dos evaluadores humanos según la rúbrica de A. El mapa para destapar (`calificacion_mapa.json`) no se versiona hasta terminar la calificación. Hay una amenaza a la ceguera: 16 de las 30 respuestas citan `wiki/` o `[[...]]`, lo que delata a KB-A.
- **Pendientes:**
  - El costo de actualización (`costo_actualizacion.py`), después de la calificación, porque cambia la línea base.
  - La medición del overhead (`run.py --overhead`).
  - El cotejo PDF→Markdown de A.

## 2026-11-25 · Resultados marcados como preliminares (cotejo del corpus en curso)

- Después de la corrida principal, A corrigió `raw/1-2-definiciones-1.md`, diap. 31 (el diagrama de las funciones del arquitecto, que es la fuente de P02), como parte del cotejo PDF→Markdown (commit 52e24c7 en `main`).
- KB-A (`kb-a-baseline`) y el índice de KB-B se construyeron con la versión anterior. Todas las cifras y observaciones de la corrida principal quedan como **preliminares**, en especial la de P02.
- Decisión del equipo: no se repite P02 ni el experimento hasta que A confirme la versión definitiva del corpus, para ahorrar tokens. Entonces se decidirá qué reconstruir (reingesta y reindexado) y qué preguntas repetir. Mientras tanto no se modifica el corpus ni el vault de ejecución.
