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

if [ "$(curl -sf "$API/fuentes" | json 'len(d)')" != "0" ]; then
  echo "Ya hay fuentes cargadas; no se vuelven a crear."
else
  first=""
  for f in kb-wiki/vault/raw/*.md; do
    name=$(basename "$f")
    title=$(head -n1 "$f" | sed 's/^# *//')
    id=$(post "$API/fuentes" "{\"titulo\":\"$title\",\"tipo\":\"markdown\",\"archivo_o_url\":\"raw/$name\",\"estado_ingesta\":\"pendiente\"}" | json 'd["id"]')
    echo "Fuente $id: raw/$name"
    case "$name" in clase-02*) atam=$id ;; clase-03*) calidad=$id ;; esac
  done
  p1=$(post "$API/paginas" '{"titulo":"ATAM","tipo":"concepto","contenido":"Método para evaluar arquitecturas frente a objetivos de negocio.","enlaces":["Atributos de calidad"]}' | json 'd["id"]')
  p2=$(post "$API/paginas" '{"titulo":"Atributos de calidad","tipo":"concepto","contenido":"Escenarios, tácticas y modelo ISO/IEC 25010.","enlaces":["ATAM"]}' | json 'd["id"]')
  [ -n "${atam:-}" ] && curl -sf -X PUT "$API/paginas/$p1/fuentes/$atam" >/dev/null
  [ -n "${calidad:-}" ] && { curl -sf -X PUT "$API/paginas/$p2/fuentes/$calidad" >/dev/null; curl -sf -X PUT "$API/paginas/$p1/fuentes/$calidad" >/dev/null; }
  echo "Páginas $p1 y $p2 creadas y relacionadas."
fi

echo "Indexando el corpus en el RAG..."
post "$RAG/index" '{}' | json '{k: d[k] for k in ("mode","files_changed","chunks_written","embedded_tokens","elapsed_ms")}'
