# kb-wiki (KB-A: LLM Wiki)

KB-A es una base de conocimiento al estilo "LLM Wiki": un vault markdown con dos zonas.

- `raw/`: fuentes originales (solo lectura para todos los agentes).
- `wiki/`: páginas que los agentes escriben y mantienen (conceptos, entidades, comparaciones, consultas, auditoría).

Las reglas viven en el vault, no en el código: `CONVENCIONES.md` (formatos y citas) y un esquema por rol, `CLAUDE.md` (ingestor), `AGENTS.md` (consultor) y `GEMINI.md` (auditor). Los agentes acceden al vault **solo** por el gateway MCP (`mcp-gateway/`, `http://127.0.0.1:8002/mcp`, token Bearer por rol). Ver `mcp-gateway/README.md` y `docs/contrato-B.md`.

```
kb-wiki/
├── vault/      semilla del vault (raw/, wiki/, esquemas)
├── agents/     run_agent.py, prompts/ y tests/ (ejecución sin interfaz)
└── README.md
```

## Ciclo de vida del vault

`vault-init` siembra `.runtime/vault` desde `kb-wiki/vault` **solo la primera vez**. Cambios posteriores en la semilla no se propagan solos. Para resembrar desde cero (borra el trabajo de los agentes):

```bash
docker compose down -v && rm -rf .runtime && docker compose up -d && scripts/seed-demo.sh
```

## Flujo de ramas

1. Cada rol escribe en su propia rama `agent/<rol>`, con copia de trabajo en `.runtime/worktrees/<rol>`.
2. Nada llega a `main` hasta que una persona ejecuta `scripts/merge-agents.sh`.
3. `main` de `.runtime/vault` es lo que se ve en Obsidian.

Para ver el trabajo de un rol en vivo, abrir `.runtime/worktrees/<rol>` como vault en Obsidian. Para ver el resultado fusionado, abrir `.runtime/vault`.

## Operaciones con `run_agent.py`

Requisitos: gateway arriba (`docker compose ps`), `claude` en el PATH con sesión iniciada y tokens en `.env` (`GATEWAY_TOKEN_INGESTOR|CONSULTOR|AUDITOR`). El runner no tiene dependencias (Python 3.11+). Cada ejecución lanza `claude -p` en un directorio temporal vacío, sin herramientas propias, sin CLAUDE.md del repo, sin hooks ni plugins (`--tools "" --setting-sources "" --strict-mcp-config ...`), y con las herramientas MCP permitidas según rol. Eso baja la sobrecarga fija a unos 2,7k tokens. El token va en un archivo temporal (permisos 600) que se borra siempre; nunca se imprime ni se registra.

| Operación | Rol | Ejemplo |
|-----------|-----|---------|
| `ingesta` | ingestor | `python3 kb-wiki/agents/run_agent.py ingestor --op ingesta --fuente raw/<archivo>.md` |
| `consulta` | consultor | `python3 kb-wiki/agents/run_agent.py consultor --op consulta --modo experimento --pregunta "¿Qué es un estilo arquitectónico?" --question-id P01` |
| `lint` | auditor | `python3 kb-wiki/agents/run_agent.py auditor --op lint` |
| `correccion` | ingestor | `python3 kb-wiki/agents/run_agent.py ingestor --op correccion` |

Notas:

- `--modo experimento` (por defecto) quita `write_note` y `commit_changes` al consultor para que solo responda; `--modo demo` le permite guardar la respuesta en `wiki/consultas/`.
- `--fuente` es opcional en `ingesta`: sin ella el ingestor toma las fuentes aún no registradas en el log.
- `--dry-run` imprime el comando (token como `***`) y el prompt sin ejecutar nada.
- `--model` (o `KBA_MODEL`) cambia el modelo; por defecto `claude-sonnet-5-5`. `--timeout` por defecto: 1800 s en ingesta, 600 s en las demás.
- Tras ingerir, correr la auditoría o fusionar: `scripts/merge-agents.sh`.
- Exit code distinto de 0 si `claude` falla o devuelve `is_error`.
- Desde Python (WP7): `from run_agent import run_agent; rec = run_agent("consultor", "consulta", "experimento", pregunta="...", question_id="P01")` devuelve el registro, con el texto en `rec["respuesta"]`.
- Si `experiment/results/` lo creó root (p. ej. un contenedor), el runner falla con un mensaje claro: `sudo chown -R $(id -un) experiment/results`.

## Cómo se miden los tokens

- `experiment/results/kba_runs.jsonl`: una línea por ejecución con `run_id` (identificador único de 12 hex por ejecución; también en errores), `input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, `total_input_tokens` (suma de los tres), `output_tokens`, `num_turns`, `duration_ms`, `duration_api_ms`, `wall_ms` (medido por el runner) y `cost_usd_equiv`. La respuesta completa queda en `experiment/results/kba_runs/<ts>-<rol>-<op>[-<qid>]-<run_id>.md` (se crea en modo exclusivo: nunca sobrescribe).
- `cost_usd_equiv` es el costo a precio de lista de la API; con suscripción no es lo que se paga, solo sirve para comparar.
- `experiment/results/gateway.jsonl`: cada llamada MCP con rol, herramienta, ruta y caracteres devueltos. Sirve como estimación de lectura (cerca de 4 caracteres por token), útil para separar "lo que leyó de la wiki" de la sobrecarga del agente.

## Conexión interactiva para la demo

**Claude Code:**

```bash
claude mcp add --transport http arquiwiki http://localhost:8002/mcp \
  --header "Authorization: Bearer $GATEWAY_TOKEN_CONSULTOR"
```

Con el alcance local por defecto, esto queda en la configuración del usuario (con el token en claro). Al terminar: `claude mcp remove arquiwiki`. Verificar con `/mcp`.

**Antigravity (`agy`, auditor con Gemini):** el registro ya hecho es `agy mcp add --header 'Authorization: Bearer ${GATEWAY_TOKEN_AUDITOR}' arquiwiki http://127.0.0.1:8002/mcp`. Pendiente de verificar en modo interactivo si `agy` expande la variable; si no lo hace, registrar con el token literal. Pasos:

1. Exportar `GATEWAY_TOKEN_AUDITOR` en la terminal.
2. Lanzar `agy` desde un directorio vacío (por ejemplo `mkdir -p /tmp/agy-demo && cd /tmp/agy-demo`).
3. Ejecutar `/mcp` y comprobar que `arquiwiki` aparece conectado.

Advertencia: el modo Auto de `agy` puede leer archivos fuera del workspace. No lanzarlo desde el repo, para no exponer `.env` con los tokens.

## Limitación conocida

`agy -p` (sin interfaz) **no carga servidores MCP** (verificado con `agy` 1.5.17); solo lo hace el modo interactivo. Por eso el auditor sin interfaz de `run_agent.py` usa Claude con el esquema `GEMINI.md` (`motor` = `claude` en el registro), y la auditoría con Gemini se hace de forma interactiva en la demo.
