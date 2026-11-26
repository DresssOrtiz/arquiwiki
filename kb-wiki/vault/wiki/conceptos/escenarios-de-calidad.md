---
titulo: Escenarios de calidad
tipo: concepto
fuentes:
  - raw/3-1-atributos-de-calidad-2.md#Diapositiva 5
  - raw/3-1-atributos-de-calidad-2.md#Diapositiva 6
  - raw/3-1-atributos-de-calidad-2.md#Diapositiva 7
  - raw/3-1-atributos-de-calidad-2.md#Diapositiva 8
  - raw/3-1-atributos-de-calidad-2.md#Diapositiva 9
  - raw/3-1-atributos-de-calidad-2.md#Diapositiva 10
  - raw/3-2-atributos-de-calidad-3.md#Diapositiva 4
  - raw/3-2-atributos-de-calidad-3.md#Diapositiva 9
  - raw/3-2-atributos-de-calidad-3.md#Diapositiva 10
  - raw/3-2-atributos-de-calidad-3.md#Diapositiva 12
enlaces:
  - Atributos de calidad
  - Métricas de calidad
  - ADD (Diseño Centrado en Atributos de Calidad)
  - Acuerdos (trade-offs) y tensión entre atributos
  - Tácticas de arquitectura
estado_salud: ok
actualizado: 2026-11-25
---

# Escenarios de calidad

## Resumen
Un escenario de calidad describe un estímulo sobre un sistema y una respuesta medible a ese estímulo (raw/3-1-atributos-de-calidad-2.md, diap. 5). Es la forma de expresar un atributo de calidad de modo verificable.

## Desarrollo
- El estímulo es un evento iniciado por una persona o un sistema y genera una respuesta; esta debe ser visible externamente y medible (raw/3-1-atributos-de-calidad-2.md, diap. 5).
- Componentes (raw/3-1-atributos-de-calidad-2.md, diap. 6):
  - Fuente: persona o sistema que inicia el estímulo.
  - Estímulo: evento que requiere que el sistema responda.
  - Artefacto: parte del sistema o el sistema completo.
  - Respuesta: acción visible externamente.
  - Medida de respuesta: criterio de éxito del escenario; debe ser específica y medible.
  - Entorno: circunstancias operativas; siempre debe definirse, incluso si es "normal".
- Tipos (raw/3-1-atributos-de-calidad-2.md, diap. 7):
  - Escenarios de uso: el sistema es utilizado y se describe cómo se comporta (tiempo de ejecución, velocidad de respuesta, consumo de memoria, throughput).
  - Escenarios de cambio (o modificación): cambio en un componente del sistema, en el entorno o en la infraestructura operacional.
  - Escenarios de fallo: falla alguna parte del sistema, la infraestructura o el entorno.
- Priorización: se asignan dos valores (Low/Medium/High): qué tan importante es para el éxito (cliente) y qué tan difícil es de alcanzar (arquitecto) (raw/3-1-atributos-de-calidad-2.md, diap. 10).
- Ejemplos de la tabla de priorización (raw/3-1-atributos-de-calidad-2.md, diap. 10):
  - Disponibilidad: cuando la base de datos no responda, el sistema registra el fallo en el log y responde con datos anteriores durante 3 seg. (High, High).
  - Rendimiento: un usuario ve los resultados de búsqueda en menos de 5 segundos con carga de 2 búsquedas por seg. (High, High).
  - Escalabilidad: nuevos servidores pueden añadirse durante la ventana de mantenimiento en menos de 7 horas (Low, Low).
- Las diapositivas 8 y 9 contienen ejemplos de escenario (general y de disponibilidad) solo como imagen; su contenido no está en el texto convertido (raw/3-1-atributos-de-calidad-2.md, diap. 8-9).
- Los escenarios de calidad son la forma común de especificar requisitos de atributos de calidad, porque los atributos por sí mismos no son operacionales (raw/3-2-atributos-de-calidad-3.md, diap. 4). En la clase 3.2 el ejemplo general y el de disponibilidad (diap. 9-10) también son solo imagen (raw/3-2-atributos-de-calidad-3.md, diap. 9-10).
- Cada escenario se asocia con tácticas que controlan la respuesta (raw/3-2-atributos-de-calidad-3.md, diap. 12). Ver [[wiki/conceptos/tacticas-de-arquitectura|Tácticas de arquitectura]].

## Relaciones
- [[wiki/conceptos/atributos-de-calidad|Atributos de calidad]]: los escenarios concretan y hacen medibles los atributos.
- [[wiki/conceptos/metricas-de-calidad|Métricas de calidad]]: la medida de respuesta requiere métricas.
- [[wiki/conceptos/add-diseno-centrado-en-atributos-de-calidad|ADD]]: el diseño parte de los requisitos de atributos de calidad.
- [[wiki/conceptos/acuerdos-trade-offs|Acuerdos (trade-offs) y tensión entre atributos]]: cada atributo se describe por separado con escenarios.
- [[wiki/conceptos/tacticas-de-arquitectura|Tácticas de arquitectura]]: controlan la respuesta del escenario.

## Fuentes
- raw/3-1-atributos-de-calidad-2.md, diap. 5-7: definición, componentes y tipos.
- raw/3-1-atributos-de-calidad-2.md, diap. 8-10: ejemplos y priorización.
- raw/3-2-atributos-de-calidad-3.md, diap. 4, 9-10 y 12: escenarios como forma de especificar atributos.
