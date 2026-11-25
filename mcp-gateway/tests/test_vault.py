import subprocess

import pytest

from app.roles import ROLES
from app.vault import VaultError

ING, CON, AUD = ROLES["ingestor"], ROLES["consultor"], ROLES["auditor"]


def branch_files(vault_dir, branch):
    out = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", branch],
        cwd=vault_dir, capture_output=True, text=True, check=True,
    ).stdout
    return out.split()


# ---------------------------------------------------------------- lectura


def test_lista_y_lee_notas(vault):
    notas = vault.list_notes(ING)
    assert "raw/atam.md" in notas and "CLAUDE.md" in notas
    assert all(not n.endswith(".gitkeep") for n in notas)
    assert "ATAM" in vault.read_note(ING, "raw/atam.md")
    assert vault.list_notes(ING, "raw/") == ["raw/atam.md"]


def test_busqueda_sin_distinguir_mayusculas(vault):
    hits = vault.search_notes(CON, "EVALUACIÓN")
    assert hits and hits[0]["path"] == "raw/atam.md" and hits[0]["line"] == 3
    with pytest.raises(VaultError):
        vault.search_notes(CON, "  ")


@pytest.mark.parametrize(
    "ruta",
    ["../secreto.md", "raw/../../x.md", "/etc/passwd", "raw\\atam.md", ".git/config", "wiki/.oculto.md", "", "raw/\x00.md"],
)
def test_rutas_peligrosas_se_rechazan(vault, ruta):
    with pytest.raises(VaultError):
        vault.read_note(ING, ruta)
    with pytest.raises(VaultError):
        vault.write_note(ING, ruta, "x")


def test_solo_se_lee_raw_wiki_y_raiz(vault):
    with pytest.raises(VaultError, match="Solo se puede leer"):
        vault.read_note(ING, "otra/cosa.md")


def test_un_enlace_simbolico_no_saca_del_vault(vault, tmp_path):
    secreto = tmp_path / "secreto.md"
    secreto.write_text("clave")
    ws = vault.workspace(ING)
    (ws / "wiki" / "enlace.md").symlink_to(secreto)
    with pytest.raises(VaultError):
        vault.read_note(ING, "wiki/enlace.md")
    with pytest.raises(VaultError):
        vault.write_note(ING, "wiki/enlace.md", "x")
    assert "wiki/enlace.md" not in vault.list_notes(ING)


# ---------------------------------------------------------------- permisos de escritura


def test_raw_es_de_solo_lectura_para_todos(vault):
    for role in (ING, CON, AUD):
        with pytest.raises(VaultError, match="solo lectura"):
            vault.write_note(role, "raw/atam.md", "pisado")
        with pytest.raises(VaultError, match="solo lectura"):
            vault.write_note(role, "raw/nuevo.md", "nuevo")
    assert "ATAM" in vault.read_note(ING, "raw/atam.md")


def test_cada_rol_escribe_solo_en_su_carpeta(vault):
    vault.write_note(ING, "wiki/atam.md", "# ATAM")
    vault.write_note(CON, "wiki/consultas/p01.md", "# P01")
    vault.write_note(AUD, "wiki/auditoria/lint.md", "# Lint")

    with pytest.raises(VaultError):
        vault.write_note(CON, "wiki/atam.md", "x")
    with pytest.raises(VaultError):
        vault.write_note(CON, "wiki/auditoria/lint.md", "x")
    with pytest.raises(VaultError):
        vault.write_note(AUD, "wiki/consultas/p01.md", "x")
    with pytest.raises(VaultError):
        vault.write_note(ING, "CLAUDE.md", "x")  # la raíz no se escribe


def test_solo_markdown_y_con_limite_de_tamano(vault):
    with pytest.raises(VaultError, match=".md"):
        vault.write_note(ING, "wiki/script.sh", "x")
    with pytest.raises(VaultError, match="máximo"):
        vault.write_note(ING, "wiki/grande.md", "x" * 2000)


# ---------------------------------------------------------------- git por rol


def test_cada_rol_trabaja_en_su_rama_y_main_no_cambia(vault, vault_dir):
    vault.write_note(ING, "wiki/atam.md", "# ATAM")
    vault.write_note(CON, "wiki/consultas/p01.md", "# P01")
    assert "Commit" in vault.commit_changes(ING, "ingesta: atam")
    assert "Commit" in vault.commit_changes(CON, "consulta: p01")

    assert "wiki/atam.md" in branch_files(vault_dir, "agent/ingestor")
    assert "wiki/consultas/p01.md" not in branch_files(vault_dir, "agent/ingestor")
    assert "wiki/consultas/p01.md" in branch_files(vault_dir, "agent/consultor")
    assert "wiki/atam.md" not in branch_files(vault_dir, "main")  # main solo cambia al fusionar


def test_commit_sin_cambios_y_mensaje_vacio(vault):
    assert vault.commit_changes(ING, "nada") == "No hay cambios que confirmar"
    with pytest.raises(VaultError):
        vault.commit_changes(ING, "  ")


def test_el_rol_no_ve_lo_de_otro_hasta_fusionar(vault, vault_dir):
    vault.write_note(ING, "wiki/atam.md", "# ATAM")
    vault.commit_changes(ING, "ingesta")
    assert "wiki/atam.md" not in vault.list_notes(CON)

    subprocess.run(
        ["git", "-c", "user.name=h", "-c", "user.email=h@h", "merge", "--no-edit", "agent/ingestor"],
        cwd=vault_dir, check=True, capture_output=True,
    )
    vault.sync_main(CON)
    assert "wiki/atam.md" in vault.list_notes(CON)


def test_sync_main_trae_documentos_nuevos_de_raw(vault, vault_dir):
    vault.workspace(AUD)  # crea la copia de trabajo antes del cambio
    (vault_dir / "raw" / "nuevo.md").write_text("# Nuevo\n")
    subprocess.run(["git", "add", "-A"], cwd=vault_dir, check=True)
    subprocess.run(
        ["git", "-c", "user.name=h", "-c", "user.email=h@h", "commit", "-q", "-m", "nuevo doc"],
        cwd=vault_dir, check=True,
    )
    assert "raw/nuevo.md" not in vault.list_notes(AUD)
    vault.sync_main(AUD)
    assert "raw/nuevo.md" in vault.list_notes(AUD)


def test_sync_main_exige_arbol_limpio(vault):
    vault.write_note(ING, "wiki/a.md", "x")
    with pytest.raises(VaultError, match="commit_changes"):
        vault.sync_main(ING)
