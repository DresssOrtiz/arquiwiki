#!/usr/bin/env bash
# Prueba de install.sh en un directorio temporal. Bash puro, sin dependencias.
# Sale con código distinto de 0 si alguna comprobación falla.
set -uo pipefail

RAIZ="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
INSTALL="$RAIZ/install.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

FALLOS=0
ok()   { echo "  ok   - $1"; }
fallo(){ echo "  FALLO - $1"; FALLOS=$((FALLOS+1)); }
verificar() { # descripción, comando...
  local d="$1"; shift
  if "$@" >/dev/null 2>&1; then ok "$d"; else fallo "$d"; fi
}
apunta_a() { [ -L "$1" ] && [ "$(readlink "$1")" = "$2" ]; }

SKILLS=(modelar criterios-aceptacion evaluar-iso)
PROY="$TMP/proyecto"; mkdir -p "$PROY"
D="$PROY/.claude"

echo "(a) instalación en limpio"
"$INSTALL" "$PROY" >"$TMP/a.out" 2>"$TMP/a.err"; rc=$?
verificar "código de salida 0" [ "$rc" -eq 0 ]
verificar "enlace del agente" apunta_a "$D/agents/ingeniero-sistemas.md" "$RAIZ/.claude/agents/ingeniero-sistemas.md"
for s in "${SKILLS[@]}"; do
  verificar "enlace de la skill $s en skills/$s" apunta_a "$D/skills/$s" "$RAIZ/.claude/skills/$s"
  verificar "skills/$s resuelve a un SKILL.md" test -f "$D/skills/$s/SKILL.md"
  verificar "el nombre de la skill $s coincide con su carpeta" grep -q "^name: $s\$" "$D/skills/$s/SKILL.md"
  verificar "el agente declara la skill $s" grep -q "^  - $s\$" "$D/agents/ingeniero-sistemas.md"
done
verificar "sin avisos en stderr" test ! -s "$TMP/a.err"

echo "(b) reinstalación idempotente"
"$INSTALL" "$PROY" >"$TMP/b.out" 2>"$TMP/b.err"; rc=$?
verificar "código de salida 0" [ "$rc" -eq 0 ]
verificar "todo figura como ya instalado" test "$(grep -c '^ya instalado' "$TMP/b.out")" -eq 4
verificar "sin avisos en stderr" test ! -s "$TMP/b.err"
verificar "enlace de modelar intacto" apunta_a "$D/skills/modelar" "$RAIZ/.claude/skills/modelar"

echo "(c) enlace ajeno previo no se pisa"
AJENO="$TMP/otra-instalacion/modelar"; mkdir -p "$AJENO"; echo "ajeno" > "$AJENO/SKILL.md"
PROY2="$TMP/proyecto2"; mkdir -p "$PROY2/.claude/skills"
ln -s "$AJENO" "$PROY2/.claude/skills/modelar"
"$INSTALL" "$PROY2" >"$TMP/c.out" 2>"$TMP/c.err"; rc=$?
verificar "código de salida 0" [ "$rc" -eq 0 ]
verificar "modelar conserva su destino ajeno" apunta_a "$PROY2/.claude/skills/modelar" "$AJENO"
verificar "se imprimió aviso en stderr sobre modelar" grep -q "AVISO.*modelar" "$TMP/c.err"
verificar "el resumen lista lo omitido" grep -q "omitido(s)" "$TMP/c.err"
verificar "las demás skills sí se instalaron" apunta_a "$PROY2/.claude/skills/criterios-aceptacion" "$RAIZ/.claude/skills/criterios-aceptacion"
verificar "el agente sí se instaló" apunta_a "$PROY2/.claude/agents/ingeniero-sistemas.md" "$RAIZ/.claude/agents/ingeniero-sistemas.md"
# un directorio real tampoco se toca
PROY3="$TMP/proyecto3"; mkdir -p "$PROY3/.claude/skills/evaluar-iso"; echo x > "$PROY3/.claude/skills/evaluar-iso/propio.txt"
"$INSTALL" "$PROY3" >/dev/null 2>"$TMP/c3.err"
verificar "un directorio real existente no se toca" test -f "$PROY3/.claude/skills/evaluar-iso/propio.txt"
verificar "y avisa" grep -q "AVISO.*evaluar-iso" "$TMP/c3.err"
# --force sí reemplaza el enlace ajeno
"$INSTALL" --force "$PROY2" >/dev/null 2>&1
verificar "--force reemplaza el enlace ajeno" apunta_a "$PROY2/.claude/skills/modelar" "$RAIZ/.claude/skills/modelar"
verificar "--force no borra el contenido ajeno" test -f "$AJENO/SKILL.md"
# restaurar el ajeno para la prueba (d)
rm "$PROY2/.claude/skills/modelar"; ln -s "$AJENO" "$PROY2/.claude/skills/modelar"

echo "(d) --uninstall quita solo los propios"
"$INSTALL" --uninstall "$PROY2" >"$TMP/d.out" 2>"$TMP/d.err"; rc=$?
verificar "código de salida 0" [ "$rc" -eq 0 ]
verificar "el enlace ajeno sigue en su sitio" apunta_a "$PROY2/.claude/skills/modelar" "$AJENO"
verificar "el contenido ajeno sigue intacto" test -f "$AJENO/SKILL.md"
verificar "se quitó el agente propio" test ! -e "$PROY2/.claude/agents/ingeniero-sistemas.md"
for s in criterios-aceptacion evaluar-iso; do
  verificar "se quitó la skill propia $s" test ! -L "$PROY2/.claude/skills/$s"
done
"$INSTALL" --uninstall "$PROY" >/dev/null 2>&1
verificar "desinstalar el proyecto limpio quita todo" test ! -L "$D/skills/modelar" -a ! -L "$D/skills/evaluar-iso" -a ! -L "$D/agents/ingeniero-sistemas.md"
verificar "los archivos del paquete siguen existiendo" test -f "$RAIZ/.claude/skills/modelar/SKILL.md"

echo
if [ "$FALLOS" -eq 0 ]; then echo "TODO EN VERDE"; exit 0; fi
echo "$FALLOS comprobación(es) fallida(s)"; exit 1
