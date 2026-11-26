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
./install.sh --force             # además reemplaza enlaces ajenos (ver abajo)
```

El script crea enlaces simbólicos: el agente en `<destino>/.claude/agents/ingeniero-sistemas.md` y cada skill en `<destino>/.claude/skills/<nombre>` (`modelar`, `criterios-aceptacion`, `evaluar-iso`). Los nombres coinciden con el campo `name` de cada `SKILL.md` y con la lista `skills:` del frontmatter del agente.

Qué hace con lo que ya existe en el destino:

| Situación del destino | Comportamiento |
|---|---|
| No existe | Crea el enlace |
| Enlace que apunta a este paquete | Lo deja (o lo actualiza si apuntaba a otra ruta del paquete) |
| Enlace ajeno (otra instalación) | **No lo toca**: aviso `AVISO: omitido...` en stderr y lista de omitidos al final. Código de salida 0 |
| Archivo o directorio real | No lo toca nunca (ni con `--force`); aviso en stderr, código de salida 0 |
| Enlace ajeno con `--force` | Lo reemplaza por el de este paquete |

`--uninstall` solo elimina enlaces cuyo destino resuelto está dentro de este paquete. Como son enlaces, actualizar el repositorio actualiza el agente.

Prueba del instalador (directorio temporal, sin dependencias): `./tests/test_install.sh`.

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

El agente declara `skills: [modelar, criterios-aceptacion, evaluar-iso]` en su frontmatter, de modo que Claude Code inyecta el `SKILL.md` completo de cada una en su contexto al arrancar (los subagentes no heredan las skills del padre). Por eso el agente no necesita invocar `/modelar`; los comandos `/modelar` etc. de arriba son para la sesión principal. Los archivos de `references/` no se precargan: el agente los lee bajo demanda.

**Cómo comprobar el flujo.** En un proyecto con el paquete instalado (`./install.sh /ruta/al/proyecto`), abre Claude Code en ese proyecto y pide:

```text
Usa el agente ingeniero-sistemas para modelar este requisito: RF-03: Cuando un usuario autenticado busque un producto, el sistema debe ...
```

Debe delegar en el subagente, que produce `modelo.dsl`, `paquetes.puml`, `secuencia.puml` y `decisiones.md` siguiendo la skill `modelar` sin que la invoques. Señales de que la precarga funciona: los entregables respetan los nombres fijos y la plantilla de `decisiones.md`, y el agente no dice que le falte la skill. Para ver las skills y el agente reconocidos: `/agents` y `/skills`.

Verificado el 2026-11-25 con Claude Code 2.1.303. En un proyecto con el paquete instalado, `claude -p "Usa el agente ingeniero-sistemas para redactar los criterios de aceptación de RF-90 ..."` delegó en el subagente. Este confirmó que tenía precargadas `modelar`, `criterios-aceptacion` y `evaluar-iso`, y su `criterios.feature` incluyó el escenario de calidad de seis componentes. **Advertencia:** con `--disable-slash-commands` no se carga ninguna skill. En esa misma prueba con ese flag, el subagente respondió que no tenía skills y omitió el escenario de calidad. No lo uses al invocar este agente.

Flujo completo: modelar, luego criterios de aceptación, luego evaluar. La evaluación necesita los artefactos de los dos pasos anteriores; si faltan, los registra como brecha.

## Ejemplos

| Carpeta | Requisito | Atributo de calidad |
|---|---|---|
| `ejemplos/RF-ejemplo-1/` | Registro e inicio de sesión | Seguridad |
| `ejemplos/RF-ejemplo-2/` | Búsqueda de existencias | Rendimiento (p95 < 2 s, 60 usuarios concurrentes) |

Cada carpeta contiene `requisito.md`, `modelo.dsl`, `paquetes.puml`, `secuencia.puml`, `decisiones.md`, `criterios.feature` y `evaluacion-iso.md`. Los requisitos son **de ejemplo**: reemplazar por el RF real del SRS de MANI. Cuando se prepararon los ejemplos aún no había páginas en `wiki/conceptos/`; actualmente sí existen páginas exportadas. Los ejemplos históricos no se reescribieron y no citan páginas de wiki: citan el corpus crudo con número de diapositiva (`raw/<archivo>.md, diap. N`) cuando la diapositiva respalda la afirmación, y "conocimiento general" cuando no. Lo que proviene del SRS de MANI de muestra se cita a `kb-wiki/muestras/mani-srs-muestra.md`, un extracto sintético que no forma parte del corpus evaluado.

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
├── tests/test_install.sh
├── .claude/
│   ├── agents/ingeniero-sistemas.md
│   └── skills/{modelar,criterios-aceptacion,evaluar-iso}/   (SKILL.md + references/)
└── ejemplos/
```

## Advertencia sobre las normas

Las references de `evaluar-iso` resumen ISO/IEC 25010, 29148 y 42010 con palabras propias para orientar la evaluación. Las normas tienen derechos de autor: cotejar siempre con el texto oficial antes de usar un dictamen como entrega formal.
