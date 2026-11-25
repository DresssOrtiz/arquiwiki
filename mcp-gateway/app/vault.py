"""Acceso al vault: rutas seguras, permisos por rol y git (una rama y copia de trabajo por rol)."""

import os
import subprocess
import threading
from pathlib import Path, PurePosixPath

from app.roles import READ_DIRS, Role


class VaultError(Exception):
    """Error de uso (permiso, ruta inválida, git). El mensaje se muestra al agente."""


class Vault:
    def __init__(self, vault_dir: Path, worktrees_dir: Path, max_bytes: int = 200_000):
        self.vault_dir = Path(vault_dir)
        self.worktrees_dir = Path(worktrees_dir)
        self.max_bytes = max_bytes
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ git

    def _git(self, cwd: Path, *args: str, role: str = "gateway") -> str:
        cmd = [
            "git",
            "-c", "safe.directory=*",
            "-c", f"user.name=agent-{role}",
            "-c", f"user.email={role}@arquiwiki.local",
            *args,
        ]
        env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
        proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
        if proc.returncode != 0:
            raise VaultError(f"git {args[0]} falló: {(proc.stderr or proc.stdout).strip()}")
        return proc.stdout.strip()

    def workspace(self, role: Role) -> Path:
        """Copia de trabajo del rol (git worktree sobre la rama agent/<rol>); se crea al primer uso."""
        ws = self.worktrees_dir / role.name
        with self._lock:
            if (ws / ".git").exists():
                return ws
            self.worktrees_dir.mkdir(parents=True, exist_ok=True)
            self._git(self.vault_dir, "worktree", "prune")
            self._git(self.vault_dir, "worktree", "add", "-B", f"agent/{role.name}", str(ws), "main")
        return ws

    # ------------------------------------------------------------------ rutas

    @staticmethod
    def _normalize(path: str) -> str:
        if not isinstance(path, str) or not path.strip():
            raise VaultError("La ruta no puede estar vacía")
        if "\x00" in path or "\\" in path or path.startswith("/"):
            raise VaultError("Ruta inválida: use rutas relativas con '/' (por ejemplo wiki/atam.md)")
        parts = PurePosixPath(path).parts
        if any(p in (".", "..") or p.startswith(".") for p in parts):
            raise VaultError("Ruta inválida: no se permiten '..' ni archivos ocultos")
        return "/".join(parts)

    def _check_read(self, rel: str) -> None:
        parts = rel.split("/")
        if parts[0] in READ_DIRS or (len(parts) == 1 and rel.endswith(".md")):
            return
        raise VaultError("Solo se puede leer raw/, wiki/ y los archivos .md de la raíz")

    def _check_write(self, role: Role, rel: str) -> None:
        if rel.startswith("raw/") or rel == "raw":
            raise VaultError("raw/ es de solo lectura para todos los roles")
        if not any(rel.startswith(p) for p in role.write_prefixes):
            permitido = ", ".join(role.write_prefixes)
            raise VaultError(f"El rol '{role.name}' solo puede escribir en: {permitido}")
        if not rel.endswith(".md"):
            raise VaultError("Solo se pueden escribir archivos .md")

    def _resolve(self, ws: Path, rel: str) -> Path:
        target = ws / rel
        resolved = target.resolve()
        if not resolved.is_relative_to(ws.resolve()):
            raise VaultError("Ruta fuera del vault")
        if target.is_symlink():
            raise VaultError("No se permiten enlaces simbólicos")
        return resolved

    def _iter_notes(self, ws: Path):
        roots = [ws / d for d in READ_DIRS] + sorted(ws.glob("*.md"))
        for root in roots:
            files = root.rglob("*.md") if root.is_dir() else [root]
            for f in sorted(files):
                rel = f.relative_to(ws)
                if f.is_file() and not f.is_symlink() and not any(p.startswith(".") for p in rel.parts):
                    yield rel.as_posix(), f

    # ------------------------------------------------------------------ operaciones

    def list_notes(self, role: Role, prefix: str = "", limit: int = 1000) -> list[str]:
        ws = self.workspace(role)
        notes = [rel for rel, _ in self._iter_notes(ws) if rel.startswith(prefix)]
        return notes[:limit]

    def read_note(self, role: Role, path: str) -> str:
        rel = self._normalize(path)
        self._check_read(rel)
        target = self._resolve(self.workspace(role), rel)
        if not target.is_file():
            raise VaultError(f"No existe {rel}")
        return target.read_text(encoding="utf-8")

    def search_notes(self, role: Role, query: str, limit: int = 20) -> list[dict]:
        if not query.strip():
            raise VaultError("La búsqueda no puede estar vacía")
        needle = query.casefold()
        results: list[dict] = []
        for rel, f in self._iter_notes(self.workspace(role)):
            for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                if needle in line.casefold():
                    results.append({"path": rel, "line": n, "text": line.strip()[:200]})
                    if len(results) >= limit:
                        return results
        return results

    def write_note(self, role: Role, path: str, content: str) -> int:
        rel = self._normalize(path)
        self._check_write(role, rel)
        data = content.encode("utf-8")
        if len(data) > self.max_bytes:
            raise VaultError(f"La nota supera el máximo de {self.max_bytes} bytes")
        target = self._resolve(self.workspace(role), rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return len(data)

    def commit_changes(self, role: Role, message: str) -> str:
        if not message.strip():
            raise VaultError("El mensaje de commit no puede estar vacío")
        ws = self.workspace(role)
        self._git(ws, "add", "-A", role=role.name)
        if not self._git(ws, "status", "--porcelain", role=role.name):
            return "No hay cambios que confirmar"
        self._git(ws, "commit", "-m", message.strip(), role=role.name)
        sha = self._git(ws, "rev-parse", "--short", "HEAD", role=role.name)
        return f"Commit {sha} en agent/{role.name}"

    def sync_main(self, role: Role) -> str:
        """Trae a la rama del rol lo que ya se fusionó en main (por ejemplo, documentos nuevos en raw/)."""
        ws = self.workspace(role)
        if self._git(ws, "status", "--porcelain", role=role.name):
            raise VaultError("Hay cambios sin confirmar: use commit_changes antes de sync_main")
        try:
            return self._git(ws, "merge", "--no-edit", "main", role=role.name)
        except VaultError:
            self._git(ws, "merge", "--abort", role=role.name)
            raise VaultError("Conflicto al fusionar main; se canceló. Avise a una persona.")
