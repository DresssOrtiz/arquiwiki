#!/usr/bin/env bash
# Prueba de humo del sistema levantado con `docker compose up`.
# Cubre: salud, CRUD de Fuente y Página con relación N:M, RAG (index y query) y gateway MCP.
# Deja notas de prueba en las ramas agent/* del vault; para limpiar:
#   docker compose down -v && rm -rf .runtime
set -euo pipefail
cd "$(dirname "$0")/.."

set -a; [ -f .env ] && . ./.env; set +a
API="http://127.0.0.1:${API_PORT:-8000}"
RAG="http://127.0.0.1:${RAG_PORT:-8001}"
GW="http://127.0.0.1:${GATEWAY_PORT:-8002}"
FAIL=0

ok()   { echo "  ok    $1"; }
fail() { echo "  FALLA $1"; FAIL=1; }
status() { curl -s -o /dev/null -w '%{http_code}' "$@"; }
expect() { # expect <código esperado> <descripción> <curl args...>
  local want="$1" label="$2"; shift 2
  local got; got=$(status "$@")
  [ "$got" = "$want" ] && ok "$label ($got)" || fail "$label (esperado $want, llegó $got)"
}
json() { python3 -c "import sys,json; d=json.load(sys.stdin); print($1)"; }

echo "== Salud"
expect 200 "api" "$API/health"
expect 200 "rag-service" "$RAG/health"
expect 200 "mcp-gateway" "$GW/health"

echo "== CRUD de Fuente y Página"
FID=$(curl -s -X POST "$API/fuentes" -H 'content-type: application/json' \
  -d '{"titulo":"Prueba de humo","tipo":"markdown","archivo_o_url":"raw/smoke.md"}' | json 'd["id"]')
PID=$(curl -s -X POST "$API/paginas" -H 'content-type: application/json' \
  -d "{\"titulo\":\"Pagina de humo $RANDOM\",\"tipo\":\"concepto\",\"contenido\":\"hola\"}" | json 'd["id"]')
expect 200 "relacionar página y fuente" -X PUT "$API/paginas/$PID/fuentes/$FID"
[ "$(curl -s "$API/paginas/$PID" | json 'len(d["fuentes"])')" = "1" ] && ok "la página cita 1 fuente" || fail "relación N:M"
expect 200 "actualizar fuente" -X PUT "$API/fuentes/$FID" -H 'content-type: application/json' -d '{"estado_ingesta":"ingestada"}'
expect 204 "borrar página" -X DELETE "$API/paginas/$PID"
expect 204 "borrar fuente" -X DELETE "$API/fuentes/$FID"
expect 404 "fuente borrada ya no existe" "$API/fuentes/$FID"

echo "== RAG"
INDEX=$(curl -s -X POST "$RAG/index" -H 'content-type: application/json' -d '{}' \
  | json '{k: d[k] for k in ("mode","files_changed","chunks_written","embedded_tokens","elapsed_ms")}')
ok "index: $INDEX"
FRAGS=$(curl -s -X POST "$RAG/query" -H 'content-type: application/json' \
  -d '{"question":"¿Qué es ATAM?","k":3,"use_llm":false,"question_id":"smoke"}' | json 'len(d["fragments"])')
[ "$FRAGS" -gt 0 ] && ok "query devuelve $FRAGS fragmentos" || fail "query sin fragmentos (¿hay documentos en raw/?)"

echo "== Gateway MCP"
if command -v uv >/dev/null; then
  uv run --quiet --with "mcp<2" --with httpx python scripts/mcp_check.py || FAIL=1
else
  echo "  (se omite: falta uv)"
fi

[ "$FAIL" = 0 ] && echo "TODO OK" || { echo "HAY FALLAS"; exit 1; }
