---
titulo: Acuerdos (trade-offs) y tensión entre atributos
tipo: concepto
fuentes:
  - raw/3-2-atributos-de-calidad-3.md#Diapositiva 4
  - raw/3-2-atributos-de-calidad-3.md#Diapositiva 5
  - raw/3-2-atributos-de-calidad-3.md#Diapositiva 6
  - raw/3-2-atributos-de-calidad-3.md#Diapositiva 7
enlaces:
  - Atributos de calidad
  - Escenarios de calidad
  - ATAM
  - Función de encaje (fitness)
estado_salud: ok
actualizado: 2026-11-25
---

# Acuerdos (trade-offs) y tensión entre atributos

## Resumen
Los atributos de calidad no son independientes: satisfacer uno puede afectar positiva o negativamente a otros, por lo que el arquitecto debe decidir cuáles priorizar. A ese fenómeno se le llama "trade-off" o acuerdo (raw/3-2-atributos-de-calidad-3.md, diap. 4 y 7).

## Desarrollo
- Todos los atributos de calidad son buenos, pero su valor depende del proyecto y del stakeholder; "mejor calidad" exige preguntar para qué y para quién (raw/3-2-atributos-de-calidad-3.md, diap. 4).
- Algunos atributos pueden entrar en conflicto y hay que decidir cuál es el más importante; ejemplo: un sistema muy seguro puede ser menos usable. "Siempre hay un precio" (raw/3-2-atributos-de-calidad-3.md, diap. 4).
- Durante el diseño no puede lograrse la satisfacción de todos los atributos al 100 % (raw/3-2-atributos-de-calidad-3.md, diap. 7). Un arquitecto de software, idealmente, debería conocer sobre trade-offs (raw/3-2-atributos-de-calidad-3.md, diap. 7).
- Los atributos por sí mismos no son suficientes: no son operacionales, y decir que un sistema debe ser modificable o tener alta disponibilidad aporta poco; además el vocabulario para describirlos es muy variado y es necesario describir cada atributo por separado (raw/3-2-atributos-de-calidad-3.md, diap. 4). Los escenarios de calidad son la forma común de especificar requisitos de atributos (raw/3-2-atributos-de-calidad-3.md, diap. 4).
- Los acuerdos son decisiones significativas desde el punto de vista de la arquitectura; normalmente afectan a atributos de calidad, estructura, dependencias, interfaces y técnicas de construcción (raw/3-2-atributos-de-calidad-3.md, diap. 5).
- La diapositiva 6 presenta una "matriz de puntos de acuerdo por AC" solo como imagen; su contenido no está en el texto convertido (raw/3-2-atributos-de-calidad-3.md, diap. 6).
- Para gestionarlos se mencionan ATAM y, en arquitecturas evolutivas, la función de encaje (raw/3-2-atributos-de-calidad-3.md, diap. 7).

## Relaciones
- [[wiki/conceptos/atributos-de-calidad|Atributos de calidad]]: los atributos que entran en tensión.
- [[wiki/conceptos/escenarios-de-calidad|Escenarios de calidad]]: forma de especificar cada atributo por separado.
- [[wiki/conceptos/atam|ATAM]]: método citado para gestionar trade-offs.
- [[wiki/conceptos/funcion-de-encaje|Función de encaje (fitness)]]: mecanismo de valoración en arquitecturas evolutivas.

## Fuentes
- raw/3-2-atributos-de-calidad-3.md, diap. 4: tensión entre atributos.
- raw/3-2-atributos-de-calidad-3.md, diap. 5-6: acuerdos.
- raw/3-2-atributos-de-calidad-3.md, diap. 7: gestión de atributos de calidad.
