"""Servidor MCP (streamable HTTP, sin estado). El rol sale del token Bearer de cada petición."""

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

from app.audit import Audit
from app.roles import Role, TokenTable
from app.vault import Vault, VaultError

INSTRUCTIONS = (
    "Acceso a la wiki ArquiWiki (vault de markdown). raw/ contiene las fuentes y es de solo "
    "lectura; wiki/ contiene las páginas. Cada rol escribe solo en sus carpetas. Los cambios "
    "quedan en tu propia rama: usa commit_changes al terminar."
)


class _AuthMiddleware:
    """Rechaza con 401 cualquier petición sin token válido (salvo /health)."""

    def __init__(self, app: ASGIApp, tokens: TokenTable):
        self.app, self.tokens = app, tokens

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http" and scope["path"] != "/health":
            request = Request(scope)
            if self.tokens.authenticate(request.headers.get("authorization")) is None:
                response: Response = JSONResponse(
                    {"error": "Token Bearer ausente o inválido"},
                    status_code=401,
                    headers={"WWW-Authenticate": "Bearer"},
                )
                await response(scope, receive, send)
                return
        await self.app(scope, receive, send)


def create_app(vault: Vault, tokens: TokenTable, audit: Audit):
    mcp = FastMCP(
        "arquiwiki-vault",
        instructions=INSTRUCTIONS,
        stateless_http=True,
        json_response=True,
        # Se publica solo en 127.0.0.1 y exige token; la verificación de Host impediría
        # el acceso desde otros contenedores de la red de compose.
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
    )

    def role_of(ctx: Context) -> Role:
        request = ctx.request_context.request
        role = tokens.authenticate(request.headers.get("authorization")) if request else None
        if role is None:
            raise ValueError("No autenticado")
        return role

    def run(ctx: Context, tool: str, path: str | None, fn: Callable[[Role], Any]) -> Any:
        role = role_of(ctx)
        try:
            result = fn(role)
        except VaultError as exc:
            audit.record(role.name, tool, path, allowed=False, detail=str(exc))
            raise ValueError(str(exc)) from None
        if isinstance(result, int):
            audit.record(role.name, tool, path, allowed=True, bytes_written=result)
        else:
            text = result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)
            audit.record(role.name, tool, path, allowed=True, chars_returned=len(text))
        return result

    @mcp.tool()
    def whoami(ctx: Context) -> dict:
        """Indica tu rol y en qué carpetas puedes escribir."""
        role = role_of(ctx)
        audit.record(role.name, "whoami", None, allowed=True)
        return {"role": role.name, "branch": f"agent/{role.name}", "can_write": list(role.write_prefixes)}

    @mcp.tool()
    def list_notes(ctx: Context, prefix: str = "") -> list[str]:
        """Lista las notas .md legibles (raw/, wiki/ y raíz), opcionalmente bajo un prefijo como 'wiki/'."""
        return run(ctx, "list_notes", prefix or None, lambda r: vault.list_notes(r, prefix))

    @mcp.tool()
    def read_note(ctx: Context, path: str) -> str:
        """Lee una nota por su ruta relativa, por ejemplo 'raw/clase-02-atam.md'."""
        return run(ctx, "read_note", path, lambda r: vault.read_note(r, path))

    @mcp.tool()
    def search_notes(ctx: Context, query: str, limit: int = 20) -> list[dict]:
        """Busca texto (sin distinguir mayúsculas) en todas las notas legibles."""
        return run(ctx, "search_notes", query, lambda r: vault.search_notes(r, query, min(max(limit, 1), 100)))

    @mcp.tool()
    def write_note(ctx: Context, path: str, content: str) -> str:
        """Crea o reemplaza una nota .md en una carpeta permitida para tu rol. raw/ nunca es escribible."""

        def action(r: Role) -> int:
            return vault.write_note(r, path, content)

        written = run(ctx, "write_note", path, action)
        return f"Escrito {path} ({written} bytes). Recuerda commit_changes."

    @mcp.tool()
    def commit_changes(ctx: Context, message: str) -> str:
        """Confirma en tu rama (agent/<rol>) todo lo escrito. Una persona fusiona las ramas después."""
        return run(ctx, "commit_changes", None, lambda r: vault.commit_changes(r, message))

    @mcp.tool()
    def sync_main(ctx: Context) -> str:
        """Trae a tu rama lo ya fusionado en main (por ejemplo, documentos nuevos en raw/)."""
        return run(ctx, "sync_main", None, lambda r: vault.sync_main(r))

    @mcp.custom_route("/health", methods=["GET"])
    async def health(_: Request) -> Response:
        return JSONResponse({"status": "ok"})

    app = mcp.streamable_http_app()
    app.add_middleware(_AuthMiddleware, tokens=tokens)
    return app


def build_from_env(env: dict[str, str] | None = None):
    import os

    env = dict(os.environ) if env is None else env
    audit_path = env.get("AUDIT_LOG")
    return create_app(
        Vault(Path(env.get("VAULT_DIR", "/vault")), Path(env.get("WORKTREES_DIR", "/worktrees"))),
        TokenTable.from_env(env),
        Audit(Path(audit_path) if audit_path else None),
    )
