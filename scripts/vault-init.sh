#!/bin/sh
# Siembra el vault de ejecución desde la semilla versionada (kb-wiki/vault).
# Idempotente: si /vault ya es un repositorio git, no toca nada.
set -eu

SEED=/seed
VAULT=/vault

git config --global --add safe.directory '*'

if [ -d "$VAULT/.git" ]; then
  echo "vault-init: el vault ya existe, no se modifica."
  exit 0
fi

echo "vault-init: copiando semilla a $VAULT"
cp -a "$SEED"/. "$VAULT"/

cd "$VAULT"
git init -q -b main
git config user.name "arquiwiki-init"
git config user.email "init@arquiwiki.local"
git add -A
git commit -q -m "vault: semilla inicial"
echo "vault-init: listo."
