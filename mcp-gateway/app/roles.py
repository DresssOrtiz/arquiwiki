"""Roles, permisos y autenticación por token Bearer."""

import hmac
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    name: str
    write_prefixes: tuple[str, ...]  # carpetas del vault donde puede escribir


ROLES: dict[str, Role] = {
    "ingestor": Role("ingestor", ("wiki/",)),
    "consultor": Role("consultor", ("wiki/consultas/",)),
    "auditor": Role("auditor", ("wiki/auditoria/",)),
}

# Todos los roles leen raw/, wiki/ y los archivos .md de la raíz (esquemas CLAUDE.md, etc.).
# raw/ no aparece en ningún write_prefixes: es de solo lectura para todos.
READ_DIRS = ("raw", "wiki")


class TokenTable:
    def __init__(self, tokens: dict[str, Role]):
        self._tokens = tokens

    @classmethod
    def from_env(cls, env: dict[str, str] | None = None) -> "TokenTable":
        env = dict(os.environ) if env is None else env
        tokens: dict[str, Role] = {}
        for name, role in ROLES.items():
            token = env.get(f"GATEWAY_TOKEN_{name.upper()}", "").strip()
            if not token:
                raise RuntimeError(f"Falta GATEWAY_TOKEN_{name.upper()}")
            if token in tokens:
                raise RuntimeError("Dos roles no pueden compartir el mismo token")
            tokens[token] = role
        return cls(tokens)

    def authenticate(self, authorization: str | None) -> Role | None:
        """Devuelve el rol del encabezado 'Authorization: Bearer <token>' o None."""
        if not authorization:
            return None
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not token:
            return None
        found = None
        for known, role in self._tokens.items():  # recorre todos: tiempo constante por token
            if hmac.compare_digest(known.encode(), token.strip().encode()):
                found = role
        return found
