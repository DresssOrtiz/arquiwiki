# Agente Ingeniero de Sistemas

Agente para Claude Code que, a partir de un requisito, produce modelos de arquitectura, criterios de aceptación y una evaluación con normas ISO. Se apoya en la base de conocimiento del curso (LLM Wiki) a través del servidor MCP `arquiwiki`.

| Skill | Qué hace | Salida |
|---|---|---|
| `modelar` | Modelos C4 (Structurizr DSL) y UML (PlantUML), más nota de decisiones | `modelo.dsl`, `paquetes.puml`, `secuencia.puml`, `decisiones.md` |
| `criterios-aceptacion` | Gherkin en español, con escenario de calidad de seis componentes | `criterios.feature` |
| `evaluar-iso` | Evalúa contra ISO/IEC 25010, ISO/IEC/IEEE 29148 e ISO/IEC/IEEE 42010 | `evaluacion-iso.md` |

El rol, los principios y los límites están en [`PERFIL.md`](PERFIL.md).

## Instalación

```bash
cd agente-ing-sistemas
./install.sh                     # global: enlaza en ~/.claude
./install.sh /ruta/al/proyecto   # solo para un proyecto: enlaza en <proyecto>/.claude
./install.sh --uninstall         # quita los enlaces (acepta también un destino)
```

El script crea enlaces simbólicos al agente (`agents/ingeniero-sistemas.md`) y a las tres skills. Es idempotente, no pisa archivos que no sean sus propios enlaces y, con `--uninstall`, solo elimina enlaces que apuntan a este paquete. Como son enlaces, actualizar el repositorio actualiza el agente.

## Conexión con la wiki

El agente usa tres herramientas del MCP `arquiwiki`: `list_notes`, `read_note` y `search_notes`. Se conecta con el token del rol **consultor**, que lee todo el vault pero solo puede escribir en `wiki/consultas/`; el agente no escribe.

```bash
claude mcp add --transport http arquiwiki http://localhost:8002/mcp \
  --header "Authorization: Bearer $GATEWAY_TOKEN_CONSULTOR"
```

Verifica con `/mcp` dentro de Claude Code. Para levantar el gateway, ver `mcp-gateway/README.md`. Si el MCP no está disponible, el agente continúa con conocimiento general y lo declara en el entregable; las citas a la wiki (`wiki/conceptos/<pagina>.md`) solo aparecen cuando realmente consultó la página.

## Uso

Desde Claude Code, con el agente instalado:

```text
Usa el agente ingeniero-sistemas para modelar este requisito y definir sus criterios de aceptación:
RF-03: Cuando un usuario autenticado busque un producto, el sistema debe ...
```

```text
/modelar ejemplos/RF-ejemplo-1/requisito.md
/criterios-aceptacion ejemplos/RF-ejemplo-1/requisito.md
/evaluar-iso ejemplos/RF-ejemplo-1/
```

Flujo completo: modelar, luego criterios de aceptación, luego evaluar. La evaluación necesita los artefactos de los dos pasos anteriores; si faltan, los registra como brecha.

## Ejemplos

| Carpeta | Requisito | Atributo de calidad |
|---|---|---|
| `ejemplos/RF-ejemplo-1/` | Registro e inicio de sesión | Seguridad |
| `ejemplos/RF-ejemplo-2/` | Búsqueda de existencias | Rendimiento (p95 < 2 s, 60 usuarios concurrentes) |

Cada carpeta contiene `requisito.md`, `modelo.dsl`, `paquetes.puml`, `secuencia.puml`, `decisiones.md`, `criterios.feature` y `evaluacion-iso.md`. Los requisitos son **de ejemplo**: reemplazar por el RF real del SRS de MANI. Las citas a la wiki de los ejemplos son ilustrativas hasta que la wiki tenga páginas en `wiki/conceptos/`.

## Validación de los artefactos

```bash
# Structurizr DSL (structurizr/cli está descontinuada y ya no valida)
docker run --rm -v "$PWD":/usr/local/structurizr structurizr/structurizr validate -workspace modelo.dsl
# PlantUML: imprime SEQUENCE o DESCRIPTION si es válido, nada si hay error
docker run --rm -i plantuml/plantuml -syntax -pipe < paquetes.puml
docker run --rm -i plantuml/plantuml -syntax -pipe < secuencia.puml
```

## Estructura

```
agente-ing-sistemas/
├── PERFIL.md
├── install.sh
├── .claude/
│   ├── agents/ingeniero-sistemas.md
│   └── skills/{modelar,criterios-aceptacion,evaluar-iso}/   (SKILL.md + references/)
└── ejemplos/
```

## Advertencia sobre las normas

Las references de `evaluar-iso` resumen ISO/IEC 25010, 29148 y 42010 con palabras propias para orientar la evaluación. Las normas tienen derechos de autor: cotejar siempre con el texto oficial antes de usar un dictamen como entrega formal.
