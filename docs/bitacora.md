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
