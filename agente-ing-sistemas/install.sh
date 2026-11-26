#!/usr/bin/env bash
# Instala el agente "ingeniero-sistemas" y sus skills mediante enlaces simbólicos.
# Uso:
#   ./install.sh                      instala en ~/.claude (global)
#   ./install.sh /ruta/a/proyecto     instala en /ruta/a/proyecto/.claude
#   ./install.sh --uninstall [destino]  elimina solo los enlaces que apuntan a este paquete
#   ./install.sh --force [destino]    reemplaza también enlaces ajenos (nunca archivos ni directorios reales)
# Sin --force, un destino ya ocupado por algo ajeno se omite con un AVISO en stderr y el
# script termina con código 0 listando lo omitido.
set -euo pipefail

ORIGEN="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)/.claude"
AGENTE="ingeniero-sistemas.md"
SKILLS=(modelar criterios-aceptacion evaluar-iso)

DESINSTALAR=0
FORZAR=0
DESTINO_ARG=""
for arg in "$@"; do
  case "$arg" in
    --uninstall) DESINSTALAR=1 ;;
    --force) FORZAR=1 ;;
    -h|--help) sed -n '2,12p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) DESTINO_ARG="$arg" ;;
  esac
done

if [ -n "$DESTINO_ARG" ]; then
  [ -d "$DESTINO_ARG" ] || { echo "Error: no existe el directorio $DESTINO_ARG" >&2; exit 1; }
  DESTINO="$(cd "$DESTINO_ARG" && pwd)/.claude"
else
  DESTINO="$HOME/.claude"
fi

# Devuelve la ruta absoluta (con los directorios resueltos) a la que apunta el enlace $1.
destino_resuelto() {
  local enlace="$1" t dir
  t="$(readlink "$enlace")"
  [[ "$t" == /* ]] || t="$(dirname "$enlace")/$t"
  dir="$(cd -P "$(dirname "$t")" 2>/dev/null && pwd -P)" || { printf '%s' "$t"; return; }
  printf '%s/%s' "$dir" "$(basename "$t")"
}

# ¿$1 es un enlace que apunta dentro de este paquete?
es_propio() {
  [ -L "$1" ] && [[ "$(destino_resuelto "$1")" == "$ORIGEN"/* ]]
}

OMITIDOS=()

# Crea un enlace de $1 (origen) en $2 (destino).
#  - no existe                       -> lo crea
#  - enlace de este paquete          -> lo deja o lo actualiza
#  - enlace ajeno                    -> NO lo toca (salvo --force) y avisa por stderr
#  - archivo o directorio real       -> NO lo toca nunca y avisa por stderr
enlazar() {
  local origen="$1" destino="$2"
  if [ -L "$destino" ]; then
    if es_propio "$destino"; then
      if [ "$(readlink "$destino")" = "$origen" ]; then
        echo "ya instalado: $destino"
      else
        ln -sfn "$origen" "$destino"; echo "actualizado:  $destino"
      fi
    elif [ "$FORZAR" -eq 1 ]; then
      echo "reemplazado (--force; apuntaba a $(readlink "$destino")): $destino"
      ln -sfn "$origen" "$destino"
    else
      echo "AVISO: omitido, es un enlace ajeno a este paquete (apunta a $(readlink "$destino")): $destino" >&2
      OMITIDOS+=("$destino")
    fi
    return
  fi
  if [ -e "$destino" ]; then
    echo "AVISO: omitido, existe y no es un enlace (no se toca): $destino" >&2
    OMITIDOS+=("$destino"); return
  fi
  ln -s "$origen" "$destino"; echo "instalado:    $destino"
}

# Elimina $1 solo si es un enlace que apunta dentro de este paquete.
quitar() {
  local destino="$1"
  if es_propio "$destino"; then
    rm "$destino"; echo "eliminado:    $destino"
  elif [ -e "$destino" ] || [ -L "$destino" ]; then
    echo "AVISO: omitido, no es un enlace de este paquete: $destino" >&2
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
if [ "${#OMITIDOS[@]}" -gt 0 ]; then
  echo "Instalación terminada en $DESTINO con ${#OMITIDOS[@]} elemento(s) omitido(s) por pertenecer a otra instalación:" >&2
  printf '  %s\n' "${OMITIDOS[@]}" >&2
  echo "Revisa esos destinos; para reemplazar los enlaces ajenos vuelve a ejecutar con --force." >&2
else
  echo "Instalación terminada en $DESTINO"
fi
echo "Falta conectar el MCP de la wiki (ver README.md), por ejemplo:"
echo '  claude mcp add --transport http arquiwiki http://localhost:8002/mcp \'
echo '    --header "Authorization: Bearer $GATEWAY_TOKEN_CONSULTOR"'
