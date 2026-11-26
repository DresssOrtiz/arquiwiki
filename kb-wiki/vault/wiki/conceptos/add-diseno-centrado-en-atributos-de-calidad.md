---
titulo: ADD (Diseño Centrado en Atributos de Calidad)
tipo: concepto
fuentes:
  - raw/3-1-atributos-de-calidad-2.md#Diapositiva 16
  - raw/3-1-atributos-de-calidad-2.md#Diapositiva 17
  - raw/3-1-atributos-de-calidad-2.md#Diapositiva 19
  - raw/3-1-atributos-de-calidad-2.md#Diapositiva 22
  - raw/3-2-atributos-de-calidad-3.md#Diapositiva 11
  - raw/3-2-atributos-de-calidad-3.md#Diapositiva 12
enlaces:
  - Atributos de calidad
  - Escenarios de calidad
  - Restricciones
  - Proceso de arquitectura
  - Tácticas de arquitectura
estado_salud: ok
actualizado: 2026-11-25
---

# ADD (Diseño Centrado en Atributos de Calidad)

## Resumen
Enfoque para definir una arquitectura de software cuyo diseño se basa en los requisitos de atributos de calidad. Es un proceso recursivo que descompone el sistema aplicando tácticas y patrones que satisfacen los drivers (raw/3-1-atributos-de-calidad-2.md, diap. 16).

## Desarrollo
- Sigue el ciclo "Plan, Do, and Check" (raw/3-1-atributos-de-calidad-2.md, diap. 16):
  - Plan: se consideran atributos de calidad y restricciones de diseño para elegir los tipos de elementos de la arquitectura.
  - Do: los elementos se instancian para satisfacer los atributos y los requisitos funcionales.
  - Check: se analiza el resultado para determinar si se satisfacen los requisitos.
- En cada etapa se eligen patrones y tácticas para satisfacer un conjunto de atributos (raw/3-1-atributos-de-calidad-2.md, diap. 17).
- Entrada: requisitos de atributos de calidad, restricciones y requisitos funcionales significativos para la arquitectura (raw/3-1-atributos-de-calidad-2.md, diap. 17).
- Salida: primeros niveles de descomposición modular, varias vistas del sistema según convenga, y un conjunto de elementos con funcionalidad asignada e interacciones entre ellos (raw/3-1-atributos-de-calidad-2.md, diap. 17).
- Escenarios (frameworks) y tácticas: el framework prioriza en el diseño, la solución y la implementación los requerimientos, riesgos y atributos definidos; plantea una estructura en la que cada escenario relaciona un atributo con distintas técnicas de implementación para mejorar la calidad (raw/3-1-atributos-de-calidad-2.md, diap. 19). Sus elementos: estímulo (cualquier hecho que afecte la calidad), técnicas de respuesta (controlan la respuesta al estímulo) y respuesta (la esperada o caso de éxito al implementar la técnica) (raw/3-1-atributos-de-calidad-2.md, diap. 19; raw/3-2-atributos-de-calidad-3.md, diap. 11).
- La estructura se resume como un escenario del atributo X con tácticas que controlan la respuesta entre el estímulo y la respuesta; algunos patrones y estilos ya implementan técnicas para el manejo de atributos (raw/3-2-atributos-de-calidad-3.md, diap. 12). Ver [[wiki/conceptos/tacticas-de-arquitectura|Tácticas de arquitectura]].
- Preguntas para la próxima clase: la tensión entre atributos de calidad, cómo se validan las decisiones en ADD y qué son los acuerdos (trade-offs) (raw/3-1-atributos-de-calidad-2.md, diap. 22).

## Relaciones
- [[wiki/conceptos/atributos-de-calidad|Atributos de calidad]]: son el eje del diseño.
- [[wiki/conceptos/escenarios-de-calidad|Escenarios de calidad]]: forma de especificar los requisitos de entrada.
- [[wiki/conceptos/restricciones|Restricciones]]: entrada del proceso.
- [[wiki/conceptos/proceso-de-arquitectura|Proceso de arquitectura]]: ADD es un enfoque de diseño dentro de él.
- [[wiki/conceptos/tacticas-de-arquitectura|Tácticas de arquitectura]]: técnicas que ADD aplica en cada escenario.

## Fuentes
- raw/3-1-atributos-de-calidad-2.md, diap. 16-17: definición, ciclo, entradas y salidas.
- raw/3-1-atributos-de-calidad-2.md, diap. 19: escenarios y tácticas.
- raw/3-1-atributos-de-calidad-2.md, diap. 22: preguntas siguientes.
- raw/3-2-atributos-de-calidad-3.md, diap. 11-12: estructura de escenarios y tácticas.
