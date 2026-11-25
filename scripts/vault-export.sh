#!/usr/bin/env bash
# Copia wiki/ del vault de ejecución a kb-wiki/vault/ para poder versionarlo en el repositorio.
# Uso: scripts/vault-export.sh
set -euo pipefail

SRC=".runtime/vault/wiki/"
DST="kb-wiki/vault/wiki/"
[ -d "$SRC" ] || { echo "No existe $SRC. ¿Se levantó el compose?" >&2; exit 1; }

rsync -a --exclude '.obsidian' "$SRC" "$DST"
echo "wiki/ exportada a $DST. Revisa con: git status kb-wiki"
