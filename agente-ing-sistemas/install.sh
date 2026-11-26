#!/usr/bin/env bash
# Instala el agente "ingeniero-sistemas" y sus skills mediante enlaces simbólicos.
# Uso:
#   ./install.sh                      instala en ~/.claude (global)
#   ./install.sh /ruta/a/proyecto     instala en /ruta/a/proyecto/.claude
#   ./install.sh --uninstall [destino]  elimina solo los enlaces creados por este script
set -euo pipefail

ORIGEN="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.claude"
AGENTE="ingeniero-sistemas.md"
SKILLS=(modelar criterios-aceptacion evaluar-iso)

DESINSTALAR=0
DESTINO_ARG=""
for arg in "$@"; do
  case "$arg" in
    --uninstall) DESINSTALAR=1 ;;
    -h|--help) sed -n '2,6p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) DESTINO_ARG="$arg" ;;
  esac
done

if [ -n "$DESTINO_ARG" ]; then
  [ -d "$DESTINO_ARG" ] || { echo "Error: no existe el directorio $DESTINO_ARG" >&2; exit 1; }
  DESTINO="$(cd "$DESTINO_ARG" && pwd)/.claude"
else
  DESTINO="$HOME/.claude"
fi

# Crea un enlace de $1 (origen) en $2 (destino) sin pisar archivos ajenos.
enlazar() {
  local origen="$1" destino="$2"
  if [ -L "$destino" ]; then
    if [ "$(readlink "$destino")" = "$origen" ]; then
      echo "ya instalado: $destino"; return
    fi
    ln -sfn "$origen" "$destino"; echo "actualizado:  $destino"; return
  fi
  if [ -e "$destino" ]; then
    echo "omitido (existe y no es un enlace): $destino" >&2; return
  fi
  ln -s "$origen" "$destino"; echo "instalado:    $destino"
}

# Elimina $1 solo si es un enlace que apunta dentro de este paquete.
quitar() {
  local destino="$1"
  if [ -L "$destino" ] && [[ "$(readlink "$destino")" == "$ORIGEN"/* ]]; then
    rm "$destino"; echo "eliminado:    $destino"
  elif [ -e "$destino" ] || [ -L "$destino" ]; then
    echo "omitido (no es un enlace de este paquete): $destino" >&2
  fi
}

if [ "$DESINSTALAR" -eq 1 ]; then
  quitar "$DESTINO/agents/$AGENTE"
  for s in "${SKILLS[@]}"; do quitar "$DESTINO/skills/$s"; done
  echo "Desinstalación terminada en $DESTINO"
  exit 0
fi

mkdir -p "$DESTINO/agents" "$DESTINO/skills"
enlazar "$ORIGEN/agents/$AGENTE" "$DESTINO/agents/$AGENTE"
for s in "${SKILLS[@]}"; do enlazar "$ORIGEN/skills/$s" "$DESTINO/skills/$s"; done

echo
echo "Instalación terminada en $DESTINO"
echo "Falta conectar el MCP de la wiki (ver README.md), por ejemplo:"
echo '  claude mcp add --transport http arquiwiki http://localhost:8002/mcp \'
echo '    --header "Authorization: Bearer $GATEWAY_TOKEN_CONSULTOR"'
