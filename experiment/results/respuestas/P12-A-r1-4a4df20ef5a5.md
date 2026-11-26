**Aviso:** la wiki y `raw/` no contienen información sobre "KB-B". Lo busqué y no aparece, así que no sé cómo está construido ese sistema ni su base de datos. Lo que sigue es el catálogo general de tácticas de disponibilidad del curso, que puedes aplicar a KB-B.

**Tácticas de disponibilidad aplicables**

El escenario de disponibilidad parte de una **falla** y debe acabar en **falla ocultada o sistema reparado** (raw/3-2-atributos-de-calidad-3.md, diap. 14). La diapositiva 15 las agrupa en detección, recuperación (preparar/reparar), recuperación (reintroducción) y prevención. Estas son las que encajan con una base de datos que no responde:

- **Detección:** ping/eco, latido (*heartbeat*) y excepciones (raw/3-2-atributos-de-calidad-3.md, diap. 15). Sirven para notar que la base de datos dejó de responder.
- **Recuperación (preparar/reparar):** redundancia activa, redundancia pasiva, repuesto, votación y punto de control/retroceso (diap. 15). La idea es tener una réplica de la base de datos que tome el relevo, o volver a un estado anterior consistente.
- **Recuperación (reintroducción):** modo sombra y sincronización de estado (diap. 15). Sirven para reincorporar la instancia reparada sin perder datos.
- **Prevención:** quitar de servicio, transacciones y monitoreo de procesos (diap. 15).

La diapositiva 15 no permite asignar con certeza cada táctica a su categoría. La wiki lo advierte y recomienda verificar contra el PDF. Por eso el reparto anterior es aproximado.

**Cómo comprobar la recuperación**

La wiki no define un procedimiento de verificación. Solo aporta medidas y una práctica relacionadas con la confiabilidad:

- **Tiempo medio hasta la recuperación** y **cantidad de tiempo fuera de servicio** (raw/2-2-atributos-de-calidad-1.md, diap. 34 y 36).
- **Chaos testing** (diap. 35).
- Las diapositivas no indican qué medida corresponde a cada subcaracterística (disponibilidad, tolerancia a fallos, capacidad de recuperación).

Con esto, la comprobación sería provocar el fallo de la base de datos con *chaos testing* y medir el tiempo de caída y el de recuperación. Es una inferencia mía a partir de esas medidas, no un procedimiento que dé la fuente.

Las diapositivas 9 y 10 (escenario de calidad de disponibilidad) son imágenes sin texto convertido, así que no pude consultar el ejemplo concreto.

## Fuentes
- Wiki: [[wiki/conceptos/tacticas-de-disponibilidad|Tácticas de disponibilidad]], [[wiki/conceptos/confiabilidad|Confiabilidad]]
- Raw: raw/3-2-atributos-de-calidad-3.md, diap. 14-15; raw/2-2-atributos-de-calidad-1.md, diap. 34-36 (citadas desde la wiki, sin verificarlas en `raw/`)

Vacíos: la wiki y las fuentes no mencionan KB-B. Tampoco describen qué hace cada táctica, ni un procedimiento de pruebas de recuperación, ni cómo asignar cada táctica a su categoría.