import subprocess

import pytest

from app.vault import Vault


def git(cwd, *args):
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
        cwd=cwd, check=True, capture_output=True,
    )


@pytest.fixture()
def vault_dir(tmp_path):
    root = tmp_path / "vault"
    (root / "raw").mkdir(parents=True)
    (root / "wiki" / "consultas").mkdir(parents=True)
    (root / "wiki" / "auditoria").mkdir(parents=True)
    (root / "raw" / "atam.md").write_text("# ATAM\n\nMétodo de evaluación de arquitecturas.\n")
    (root / "wiki" / "consultas" / ".gitkeep").write_text("")
    (root / "wiki" / "auditoria" / ".gitkeep").write_text("")
    (root / "CLAUDE.md").write_text("# Esquema\n")
    git(root, "init", "-q", "-b", "main")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "semilla")
    return root


@pytest.fixture()
def vault(vault_dir, tmp_path):
    return Vault(vault_dir, tmp_path / "worktrees", max_bytes=1000)
