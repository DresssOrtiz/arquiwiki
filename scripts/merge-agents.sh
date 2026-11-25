#!/usr/bin/env bash
# Fusiona en main las ramas de los agentes del vault de ejecución.
# Uso: scripts/merge-agents.sh [ruta-del-vault]   (por defecto .runtime/vault)
set -euo pipefail

VAULT="${1:-.runtime/vault}"
GIT=(git -c safe.directory='*' -c user.name="${GIT_USER_NAME:-arquiwiki}" -c user.email="${GIT_USER_EMAIL:-arquiwiki@local}")

cd "$VAULT"
[ "$("${GIT[@]}" rev-parse --abbrev-ref HEAD)" = "main" ] || { echo "El vault debe estar en la rama main" >&2; exit 1; }

for branch in agent/ingestor agent/consultor agent/auditor; do
  if ! "${GIT[@]}" rev-parse --verify -q "$branch" >/dev/null; then
    echo "- $branch: no existe, se omite"
    continue
  fi
  if "${GIT[@]}" merge-base --is-ancestor "$branch" HEAD; then
    echo "- $branch: sin cambios nuevos"
    continue
  fi
  if "${GIT[@]}" merge --no-ff -m "merge: $branch" "$branch" >/dev/null; then
    echo "- $branch: fusionada"
  else
    "${GIT[@]}" merge --abort
    echo "- $branch: CONFLICTO, se canceló. Resolver a mano en $VAULT" >&2
    exit 1
  fi
done
