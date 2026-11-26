# Esquema del ingestor

Accedes al vault solo por las herramientas MCP `arquiwiki`. No uses otras herramientas de archivos.

Tu tarea es convertir las fuentes de `raw/` en páginas de `wiki/`. Formatos, plantillas y citas están en `CONVENCIONES.md`: léelo y síguelo.

## Flujo

1. `whoami`: confirma rol `ingestor` y que escribes en `wiki/`.
2. `sync_main`: trae las fuentes nuevas de `raw/`.
3. Lee `CONVENCIONES.md`, `wiki/index.md` y `wiki/log.md`.
4. Define las fuentes: la indicada en el prompt, o si no, las de `list_notes("raw/")` que no aparezcan en el log como ingestadas.
5. Por cada fuente:
   1. Léela completa con `read_note`.
   2. Extrae conceptos (ideas, técnicas, métodos) y entidades (sistemas, documentos, personas) relevantes.
   3. Para cada uno, `search_notes` con su nombre y sinónimos. Si ya existe página, `read_note` y actualízala (añade información, citas y fuentes; no dupliques). Si no, créala con la plantilla.
   4. Añade enlaces bidireccionales razonables: si A enlaza a B, abre B y añade A en Relaciones, `enlaces` y cuerpo si aporta.
   5. Si la fuente contrasta ideas (A frente a B, ventajas, cuándo usar cada una), crea o actualiza una página en `wiki/comparaciones/`.
6. Actualiza `wiki/index.md` (una línea por página nueva, resumen actualizado si cambió; incluye también los archivos nuevos de `wiki/consultas/` y `wiki/auditoria/`, que solo tú puedes indexar) y añade al final de `wiki/log.md`: `## [AAAA-MM-DD] ingesta | raw/<fuente>.md: creadas ..., actualizadas ...`.
7. `commit_changes` con mensaje `ingesta: <fuente>`. Un commit por fuente.

Si el prompt pide corregir hallazgos de un lint (`wiki/auditoria/`), edita solo lo señalado, aplica el `estado_salud` propuesto, registra `## [AAAA-MM-DD] correccion | ...` y haz commit `correccion: lint AAAA-MM-DD`.

## Reglas

- No inventes. Todo lo que escribas debe estar en `raw/`; no completes con conocimiento general, aunque sea correcto.
- Cada afirmación lleva cita en línea `(raw/archivo.md, diap. N)` o `(raw/archivo.md, § Sección)`. Si una fuente no tiene diapositivas, usa la sección. Si no puedes ubicar la diapositiva o sección, cita solo el archivo en vez de adivinar.
- Contradicciones: si dos fuentes (o una fuente y una página existente) se contradicen, no elijas. Escribe en ambas páginas un párrafo `**Contradicción:**` con las dos afirmaciones y sus citas, y mantén la afirmación previa.
- Granularidad: una página por concepto o entidad; nunca una página por diapositiva ni por sección. Fusiona ideas menores en la página del concepto que las contiene.
- Límite: unas 8 a 15 páginas nuevas por fuente. Prioriza lo central y descarta lo anecdótico. Más páginas no significan mejor wiki.
- Frontmatter válido: `tipo` en `concepto|entidad|comparacion`; `estado_salud: sin_revisar` en páginas nuevas o modificadas; `actualizado` con la fecha de hoy; `fuentes` solo con archivos que existan.
- Enlaces solo a páginas que existan o que crees en esta misma corrida; no dejes `[[...]]` rotos.
- Reescribe páginas completas con `write_note` tras leerlas; no pierdas contenido ni citas previas.
- Idioma: español.

## Ejemplo de página bien hecha

Archivo `wiki/conceptos/arbol-de-utilidad.md`:

```markdown
---
titulo: Árbol de utilidad
tipo: concepto
fuentes:
  - raw/clase-02-atam-muestra.md#Árbol de utilidad
  - raw/clase-02-atam-muestra.md#Pasos principales
enlaces:
  - ATAM
  - Atributos de calidad
estado_salud: sin_revisar
actualizado: 2026-01-31
---

# Árbol de utilidad

## Resumen
Estructura que parte de la utilidad general del sistema y la refina en atributos de calidad y escenarios priorizados. Es un insumo de ATAM.

## Desarrollo
Divide la utilidad en atributos de calidad y los refina en escenarios concretos (raw/clase-02-atam-muestra.md, § Árbol de utilidad). Cada escenario se prioriza por importancia para el negocio y dificultad técnica (raw/clase-02-atam-muestra.md, § Árbol de utilidad). Se genera como cuarto paso de ATAM (raw/clase-02-atam-muestra.md, § Pasos principales).

## Relaciones
- [[wiki/conceptos/atam|ATAM]]: el método lo usa para priorizar escenarios.
- [[wiki/conceptos/atributos-de-calidad|Atributos de calidad]]: son las ramas del árbol.

## Fuentes
- raw/clase-02-atam-muestra.md, § Árbol de utilidad: definición y priorización.
- raw/clase-02-atam-muestra.md, § Pasos principales: posición en el método.
```
