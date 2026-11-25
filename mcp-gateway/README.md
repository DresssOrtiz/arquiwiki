# mcp-gateway

Servidor MCP (Python, SDK `mcp` 1.x, transporte streamable HTTP) que expone el vault de KB-A a los agentes con permisos por rol. Endpoint: `http://localhost:8002/mcp`. Salud: `GET /health`.

## Roles

El rol se deduce del token Bearer. Los tokens se definen en `.env` (`GATEWAY_TOKEN_INGESTOR`, `GATEWAY_TOKEN_CONSULTOR`, `GATEWAY_TOKEN_AUDITOR`).

| Rol | Lee | Escribe |
|-----|-----|---------|
| `ingestor` | `raw/`, `wiki/`, `.md` de la raíz | `wiki/` |
| `consultor` | igual | `wiki/consultas/` |
| `auditor` | igual | `wiki/auditoria/` |

`raw/` es de solo lectura para todos. Solo se escriben `.md` de hasta 200 KB. Se rechazan rutas absolutas, `..`, archivos ocultos y enlaces simbólicos.

## Herramientas

| Herramienta | Qué hace |
|-------------|----------|
| `whoami` | Muestra el rol, la rama y las carpetas escribibles |
| `list_notes(prefix)` | Lista notas `.md` legibles |
| `read_note(path)` | Lee una nota |
| `search_notes(query, limit)` | Busca texto en todas las notas |
| `write_note(path, content)` | Crea o reemplaza una nota en una carpeta permitida |
| `commit_changes(message)` | Confirma lo escrito en la rama del rol |
| `sync_main()` | Trae a la rama del rol lo ya fusionado en `main` |

## Ramas por agente

Cada rol trabaja en un `git worktree` propio (`.runtime/worktrees/<rol>`, rama `agent/<rol>`). Nada llega a `main` ni a Obsidian hasta que una persona ejecuta `scripts/merge-agents.sh`. Para ver el trabajo de un agente en vivo, abrir su carpeta de worktree como vault en Obsidian.

## Conectar los agentes

Las rutas de los comandos se verificaron contra la documentación de cada herramienta en noviembre de 2026. Si una versión nueva cambia algo, `/mcp` (Claude Code y Gemini CLI) o `codex mcp list` muestran el estado de la conexión.

**Claude Code (ingestor):**

```bash
claude mcp add --transport http arquiwiki http://localhost:8002/mcp \
  --header "Authorization: Bearer $GATEWAY_TOKEN_INGESTOR"
```

**Codex (consultor):** agregar a `~/.codex/config.toml` y exportar la variable en la terminal que lanza Codex.

```toml
[mcp_servers.arquiwiki]
url = "http://localhost:8002/mcp"
bearer_token_env_var = "GATEWAY_TOKEN_CONSULTOR"
```

**Gemini CLI (auditor):** agregar a `~/.gemini/settings.json`. Gemini CLI usa `httpUrl`, no `url`, para streamable HTTP.

```json
{
  "mcpServers": {
    "arquiwiki": {
      "httpUrl": "http://localhost:8002/mcp",
      "headers": { "Authorization": "Bearer ${GATEWAY_TOKEN_AUDITOR}" }
    }
  }
}
```

## Auditoría

Cada llamada se registra en `experiment/results/gateway.jsonl` con rol, herramienta, ruta, si fue permitida, caracteres devueltos y bytes escritos. Los caracteres devueltos sirven como estimación aproximada de lo que cada agente leyó (cerca de 4 caracteres por token).

## Decisiones

- Se fija `mcp<2`: la serie 2.x renombró `FastMCP` a `MCPServer` y cambió otras APIs.
- Modo sin estado (`stateless_http`): el rol se lee del token en cada petición, sin sesiones que reutilizar.
- La verificación de `Host` del SDK está desactivada porque otros contenedores acceden como `mcp-gateway:8002`. La protección es el token y la publicación solo en `127.0.0.1`.

## Pruebas

```bash
cd mcp-gateway && uv run pytest
```
