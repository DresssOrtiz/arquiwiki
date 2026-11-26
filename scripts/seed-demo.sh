#!/usr/bin/env bash
# Precarga datos de demo: una Fuente por cada documento de raw/ y dos Páginas de ejemplo,
# y deja indexado el RAG. Es idempotente: si ya hay fuentes, no vuelve a crearlas.
set -euo pipefail
cd "$(dirname "$0")/.."

set -a; [ -f .env ] && . ./.env; set +a
API="http://127.0.0.1:${API_PORT:-8000}"
RAG="http://127.0.0.1:${RAG_PORT:-8001}"
json() { python3 -c "import sys,json; d=json.load(sys.stdin); print($1)"; }
post() { curl -sf -X POST "$1" -H 'content-type: application/json' -d "$2"; }

# Fuentes del corpus real que respaldan cada página de ejemplo (verificadas con grep):
#   ATAM aparece en 3-2-atributos-de-calidad-3.md; atributos de calidad, en 2-2-atributos-de-calidad-1.md.
SRC_ATAM="3-2-atributos-de-calidad-3.md"
SRC_CALIDAD="2-2-atributos-de-calidad-1.md"
P_ATAM="ATAM"
P_CAL="Atributos de calidad"

fail() { echo "ERROR: $*" >&2; exit 1; }

if [ "$(curl -sf "$API/fuentes" | json 'len(d)')" != "0" ]; then
  echo "Ya hay fuentes cargadas; no se vuelven a crear."
else
  atam=""; calidad=""
  for f in kb-wiki/vault/raw/*.md; do
    name=$(basename "$f")
    title=$(head -n1 "$f" | sed 's/^# *//')
    id=$(post "$API/fuentes" "{\"titulo\":\"$title\",\"tipo\":\"markdown\",\"archivo_o_url\":\"raw/$name\",\"estado_ingesta\":\"pendiente\"}" | json 'd["id"]')
    echo "Fuente $id: raw/$name"
    case "$name" in "$SRC_ATAM") atam=$id ;; "$SRC_CALIDAD") calidad=$id ;; esac
  done
  [ -n "$atam" ] || fail "no existe la fuente esperada raw/$SRC_ATAM en kb-wiki/vault/raw/"
  [ -n "$calidad" ] || fail "no existe la fuente esperada raw/$SRC_CALIDAD en kb-wiki/vault/raw/"
  if [ "$(curl -sf "$API/paginas" | json 'len(d)')" = "0" ]; then
    p1=$(post "$API/paginas" '{"titulo":"ATAM","tipo":"concepto","contenido":"Architecture Trade-Off Analysis Method (ATAM): método de análisis de acuerdos (trade-offs) arquitecturales. En el curso aparece como técnica para gestionar los acuerdos entre atributos de calidad, que no pueden satisfacerse todos al 100%.","enlaces":["Atributos de calidad"]}' | json 'd["id"]')
    p2=$(post "$API/paginas" '{"titulo":"Atributos de calidad","tipo":"concepto","contenido":"Propiedades de un sistema que se especifican mediante escenarios de calidad; se revisan con modelos de calidad como ISO/IEC 25000 y FURPS+.","enlaces":["ATAM"]}' | json 'd["id"]')
    curl -sf -X PUT "$API/paginas/$p1/fuentes/$atam" >/dev/null
    curl -sf -X PUT "$API/paginas/$p2/fuentes/$calidad" >/dev/null
    echo "Páginas $p1 (ATAM) y $p2 (Atributos de calidad) creadas."
  else
    echo "Ya había páginas; se comprobarán las existentes."
  fi
fi

# Comprobación: cada página de ejemplo existe y está relacionada con su fuente real.
check_rel() { # titulo_pagina archivo_fuente
  python3 - "$API" "$1" "$2" <<'PY' || exit 1
import json, sys, urllib.request
api, titulo, archivo = sys.argv[1:4]
get = lambda u: json.load(urllib.request.urlopen(api + u))
pag = [p for p in get("/paginas") if p["titulo"] == titulo]
if not pag:
    sys.exit(f"ERROR: falta la página '{titulo}'")
p = get(f"/paginas/{pag[0]['id']}")
rutas = [f["archivo_o_url"] for f in p["fuentes"]]
if f"raw/{archivo}" not in rutas:
    sys.exit(f"ERROR: la página '{titulo}' no está relacionada con raw/{archivo} (fuentes: {rutas})")
print(f"OK: '{titulo}' <- raw/{archivo}")
PY
}
check_rel "$P_ATAM" "$SRC_ATAM"
check_rel "$P_CAL" "$SRC_CALIDAD"
echo "Páginas de ejemplo relacionadas con sus fuentes (verificado)."

echo "Indexando el corpus en el RAG..."
post "$RAG/index" '{}' | json '{k: d[k] for k in ("mode","files_changed","chunks_written","embedded_tokens","elapsed_ms")}'
