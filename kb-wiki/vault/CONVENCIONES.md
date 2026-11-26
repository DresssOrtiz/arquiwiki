# Convenciones de la wiki (fuente única)

Aplican a todos los agentes. Los esquemas por rol (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) solo añaden el flujo de cada uno.

## Estructura

| Ruta | Contenido |
|------|-----------|
| `raw/` | Fuentes inmutables (diapositivas convertidas a markdown). Nadie escribe aquí. |
| `wiki/conceptos/` | Una página por idea o técnica (p. ej. `atam.md`, `arbol-de-utilidad.md`). |
| `wiki/entidades/` | Una página por sistema, persona, organización o documento concreto (p. ej. `mani.md`). |
| `wiki/comparaciones/` | Contraste entre dos o más conceptos/entidades que una fuente confronta. |
| `wiki/consultas/` | Respuestas archivadas del consultor. |
| `wiki/auditoria/` | Reportes de lint del auditor. |
| `wiki/index.md` | Catálogo de páginas. |
| `wiki/log.md` | Bitácora append-only. |

Nombres de archivo: kebab-case, minúsculas, sin tildes ni `ñ` (`modificabilidad.md`, `atributos-de-calidad.md`). El título humano va en el frontmatter (`Modificabilidad`).

## Plantilla de página (conceptos, entidades, comparaciones)

```markdown
---
titulo: Título humano con tildes
tipo: concepto            # concepto | entidad | comparacion
fuentes:
  - raw/archivo.md#Diapositiva 12
  - raw/otro.md#Sección o encabezado
enlaces:                  # títulos de las páginas relacionadas
  - Otro título
estado_salud: sin_revisar # sin_revisar | ok | con_problemas
actualizado: 2026-01-31
---

# Título humano

## Resumen
Dos o tres líneas.

## Desarrollo
Contenido con citas en línea tras cada afirmación.

## Relaciones
- [[wiki/conceptos/otro|Otro título]]: por qué se relacionan.

## Fuentes
- raw/archivo.md, diap. 12: qué aporta.
```

El frontmatter se alinea con la API: `titulo`, `tipo`, `enlaces` (títulos), `estado_salud`. Todo valor de `fuentes` debe existir en `raw/`. `estado_salud` lo fija el ingestor en `sin_revisar`; solo cambia tras un lint (el ingestor aplica lo propuesto por el auditor).

## Citas

- Con diapositivas: `(raw/1-2-definiciones-1.md, diap. 7)`; varias: `(raw/x.md, diap. 7-9)`.
- Sin diapositivas: `(raw/archivo.md, § Nombre de la sección)`.
- Toda afirmación factual lleva cita. Una cita señala la fuente que la respalda, no una página de la wiki.
- Enlaces internos: `[[ruta-sin-extension|Título]]`, con ruta desde la raíz (`[[wiki/conceptos/atam|ATAM]]`).

## Consulta archivada (`wiki/consultas/AAAA-MM-DD-<slug>.md`)

```markdown
---
titulo: Pregunta resumida
tipo: consulta
fecha: 2026-01-31
paginas_consultadas:
  - wiki/conceptos/atam.md
fuentes:
  - raw/clase-02-atam-muestra.md#Pasos principales
---

# Pregunta
Texto literal de la pregunta.

## Respuesta
Respuesta con citas a la wiki (`[[wiki/...|Título]]`) y a raw (`(raw/archivo.md, diap. N)`).

## Fuentes
- Wiki: [[...]]
- Raw: raw/archivo.md, diap. N

## Vacíos
Qué no cubre la wiki (o "ninguno").
```

## Reporte de lint (`wiki/auditoria/AAAA-MM-DD-lint.md`)

```markdown
---
titulo: Lint AAAA-MM-DD
tipo: auditoria
fecha: 2026-01-31
---

# Lint AAAA-MM-DD

## Resumen
Páginas revisadas: N. Hallazgos: alta X, media Y, baja Z. Páginas ok: A, con problemas: B.

## Hallazgos
| Severidad | Página | Tipo | Evidencia | Corrección sugerida |
|-----------|--------|------|-----------|---------------------|

## Estado de salud propuesto
| Página | estado_salud | Motivo |
|--------|--------------|--------|
```

## index.md

Secciones `## Conceptos`, `## Entidades`, `## Comparaciones`, `## Consultas archivadas`, `## Auditoría`. Una línea por página, orden alfabético:
`- [[wiki/conceptos/atam|ATAM]]: método para evaluar una arquitectura frente a objetivos de negocio.`

## log.md

Append-only: se añade al final, nunca se reescribe lo anterior. Cada entrada:
`## [AAAA-MM-DD] operación | detalle` (operaciones: `ingesta`, `consulta`, `lint`, `correccion`). Para ingesta, el detalle empieza por la ruta de la fuente (`raw/archivo.md`) y lista páginas creadas/actualizadas; así se sabe qué fuentes ya están ingestadas.

## Reglas de escritura

- `write_note` reemplaza el archivo completo. Antes de editar una página existente, `read_note`, y reescríbela íntegra conservando lo que no cambia.
- Solo `.md`, máximo 200 KB, rutas relativas con `/`.
- Cada rol escribe solo en sus carpetas (`whoami` las indica). Los cambios quedan en tu rama hasta `commit_changes`; una persona fusiona.
- No inventes: si algo no está en `raw/`, no entra en la wiki.
