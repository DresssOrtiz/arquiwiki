---
titulo: Atributos de calidad
tipo: concepto
fuentes:
  - raw/2-2-atributos-de-calidad-1.md#Diapositiva 5
  - raw/2-2-atributos-de-calidad-1.md#Diapositiva 11
  - raw/2-2-atributos-de-calidad-1.md#Diapositiva 12
  - raw/2-2-atributos-de-calidad-1.md#Diapositiva 13
  - raw/2-2-atributos-de-calidad-1.md#Diapositiva 44
  - raw/2-1-definiciones-2.md#Diapositiva 14
  - raw/2-1-definiciones-2.md#Diapositiva 17
  - raw/3-1-atributos-de-calidad-2.md#Diapositiva 2
  - raw/3-1-atributos-de-calidad-2.md#Diapositiva 3
  - raw/3-1-atributos-de-calidad-2.md#Diapositiva 4
  - raw/3-2-atributos-de-calidad-3.md#Diapositiva 3
  - raw/3-2-atributos-de-calidad-3.md#Diapositiva 4
  - raw/3-2-atributos-de-calidad-3.md#Diapositiva 13
  - raw/3-2-atributos-de-calidad-3.md#Diapositiva 32
enlaces:
  - Proceso de arquitectura
  - Arquitectura de software
  - Requerimientos
  - Modelos de calidad de software
  - ISO/IEC 25000
  - FURPS+
  - Idoneidad funcional
  - Eficiencia de desempeño
  - Compatibilidad
  - Usabilidad
  - Confiabilidad
  - Seguridad
  - Mantenibilidad
  - Portabilidad
  - Escenarios de calidad
  - Métricas de calidad
  - ADD (Diseño Centrado en Atributos de Calidad)
  - Acuerdos (trade-offs) y tensión entre atributos
  - Tácticas de arquitectura
  - Caso de estudio Almacén y Factura
  - Caso de estudio DEIMOS Space
estado_salud: ok
actualizado: 2026-11-25
---

# Atributos de calidad

## Resumen
Expectativas de usuario, en general implícitas, sobre cuán bien funcionará un producto. Son características medibles, también llamadas requisitos no funcionales o "-idades" (raw/2-2-atributos-de-calidad-1.md, diap. 11).

## Desarrollo
- Definición: "los atributos de calidad son las expectativas de usuario, en general implícitas, de cuán bien funcionará un producto" (raw/2-1-definiciones-2.md, diap. 14; raw/2-2-atributos-de-calidad-1.md, diap. 13; raw/3-1-atributos-de-calidad-2.md, diap. 3; raw/3-2-atributos-de-calidad-3.md, diap. 3, citando Software Requirements, 3rd Edition, Wiegers y Betty, 2013).
- Son características medibles de interés para usuarios o desarrolladores; ejemplos: rendimiento, disponibilidad, modificabilidad, testabilidad (raw/2-2-atributos-de-calidad-1.md, diap. 11).
- Pueden especificarse mediante escenarios con la técnica estímulo-respuesta; ejemplo: "si ocurre un fallo interno durante la operación normal, el sistema reanuda la operación en menos de 30 segundos y no se pierden datos" (raw/2-2-atributos-de-calidad-1.md, diap. 11). Ver [[wiki/conceptos/escenarios-de-calidad|Escenarios de calidad]].
- Se priorizan por el cliente, de acuerdo al éxito del sistema, y por el arquitecto, de acuerdo al riesgo técnico (raw/2-2-atributos-de-calidad-1.md, diap. 11-12).
- Determinan la mayoría de las decisiones de diseño en arquitectura: si solo importara la funcionalidad bastaría un sistema monolítico, pero son habituales las estructuras redundantes para fiabilidad, las concurrentes para rendimiento y las capas para modificabilidad (raw/2-2-atributos-de-calidad-1.md, diap. 12).
- Cualifican la funcionalidad: si el requisito funcional fuera "cuando el usuario pulse el botón verde, aparece un diálogo con opciones", uno de rendimiento describiría la velocidad de aparición, uno de disponibilidad cuándo podría fallar o con qué frecuencia se repararía, y uno de usabilidad qué tan fácil es aprender la función (raw/3-1-atributos-de-calidad-2.md, diap. 4).
- Sí influyen en la arquitectura (raw/3-1-atributos-de-calidad-2.md, diap. 4).
- La calidad es el grado (no booleano) en que un sistema satisface las necesidades declaradas o implícitas de las personas interesadas proporcionando valor; equivale a encajar en un propósito (raw/3-1-atributos-de-calidad-2.md, diap. 4).
- Lista de la diapositiva: performance/rendimiento, escalabilidad, modificabilidad, usabilidad, interoperabilidad, seguridad, disponibilidad e integración; junto a las características de ISO/IEC 25000:2014 (idoneidad funcional, compatibilidad, seguridad, mantenibilidad, portabilidad, entre otras) (raw/2-1-definiciones-2.md, diap. 14; raw/2-2-atributos-de-calidad-1.md, diap. 13; raw/3-1-atributos-de-calidad-2.md, diap. 3; raw/3-2-atributos-de-calidad-3.md, diap. 3). La conversión no deja claro qué ítems pertenecen a cada columna.
- No son independientes: algunos entran en conflicto (por ejemplo, un sistema muy seguro puede ser menos usable) y su valor depende del proyecto y del stakeholder (raw/3-2-atributos-de-calidad-3.md, diap. 4). Ver [[wiki/conceptos/acuerdos-trade-offs|Acuerdos (trade-offs) y tensión entre atributos]].
- Las tácticas de arquitectura se clasifican según el atributo de calidad que controlan (raw/3-2-atributos-de-calidad-3.md, diap. 13). Ver [[wiki/conceptos/tacticas-de-arquitectura|Tácticas de arquitectura]].
- Casos de estudio de la clase para identificar atributos, escenarios y acuerdos: [[wiki/entidades/almacen-y-factura|Almacén y Factura]] y [[wiki/entidades/deimos-space|DEIMOS Space]] (raw/3-2-atributos-de-calidad-3.md, diap. 32).
- Medición: ver [[wiki/conceptos/metricas-de-calidad|Métricas de calidad]]; diseño guiado por ellos: [[wiki/conceptos/add-diseno-centrado-en-atributos-de-calidad|ADD]] (raw/3-1-atributos-de-calidad-2.md, diap. 2).
- Preguntas para la clase siguiente: atributos de FURPS+ y de ISO 25000 (raw/2-1-definiciones-2.md, diap. 17); qué son los escenarios de calidad, cómo se miden y qué es ADD (raw/2-2-atributos-de-calidad-1.md, diap. 44).

## Relaciones
- [[wiki/conceptos/proceso-de-arquitectura|Proceso de arquitectura]]: son entrada del proceso.
- [[wiki/conceptos/arquitectura-de-software|Arquitectura de software]]: la arquitectura debe satisfacerlos.
- [[wiki/conceptos/requerimientos|Requerimientos]]: son los requerimientos no funcionales.
- [[wiki/conceptos/modelos-de-calidad-de-software|Modelos de calidad de software]], [[wiki/entidades/iso-iec-25000|ISO/IEC 25000]], [[wiki/entidades/furps-plus|FURPS+]]: modelos que los organizan.
- [[wiki/conceptos/idoneidad-funcional|Idoneidad funcional]], [[wiki/conceptos/eficiencia-de-desempeno|Eficiencia de desempeño]], [[wiki/conceptos/compatibilidad|Compatibilidad]], [[wiki/conceptos/usabilidad|Usabilidad]], [[wiki/conceptos/confiabilidad|Confiabilidad]], [[wiki/conceptos/seguridad|Seguridad]], [[wiki/conceptos/mantenibilidad|Mantenibilidad]], [[wiki/conceptos/portabilidad|Portabilidad]]: detalle por característica.
- [[wiki/conceptos/escenarios-de-calidad|Escenarios de calidad]]: forma de especificarlos de modo medible.
- [[wiki/conceptos/metricas-de-calidad|Métricas de calidad]]: forma de medirlos.
- [[wiki/conceptos/add-diseno-centrado-en-atributos-de-calidad|ADD]]: diseño de arquitectura basado en ellos.
- [[wiki/conceptos/acuerdos-trade-offs|Acuerdos (trade-offs) y tensión entre atributos]]: conflictos entre atributos.
- [[wiki/conceptos/tacticas-de-arquitectura|Tácticas de arquitectura]]: técnicas para satisfacerlos.
- [[wiki/entidades/almacen-y-factura|Caso de estudio Almacén y Factura]], [[wiki/entidades/deimos-space|Caso de estudio DEIMOS Space]]: casos de aplicación.

## Fuentes
- raw/2-1-definiciones-2.md, diap. 14 y 17.
- raw/2-2-atributos-de-calidad-1.md, diap. 5, 11-13 y 44.
- raw/3-1-atributos-de-calidad-2.md, diap. 2-4: agenda, definición y relación con la funcionalidad.
- raw/3-2-atributos-de-calidad-3.md, diap. 3-4, 13 y 32: definición, tensión entre atributos, clasificación de tácticas y casos de estudio.
