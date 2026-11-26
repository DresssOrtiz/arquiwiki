---
titulo: Estilos arquitectónicos
tipo: concepto
fuentes:
  - raw/2-1-definiciones-2.md#Diapositiva 6
  - raw/2-1-definiciones-2.md#Diapositiva 7
  - raw/5-1-estilos-y-patrones-arquitecturales-3.md#Diapositiva 3
enlaces:
  - Patrones arquitectónicos
  - Estilos vs patrones arquitecturales
  - Arquitectura de software
  - Estilos de llamado y retorno
  - Estilos de flujo de datos
  - Estilos centrados en datos
  - Estilos de componentes independientes
estado_salud: ok
actualizado: 2026-11-25
---

# Estilos arquitectónicos

## Resumen
Colección de decisiones de diseño, aplicables en un contexto, que restringen las decisiones arquitectónicas específicas y generan beneficios en cada sistema resultante.

## Desarrollo
- Definición: colección de decisiones de diseño aplicables en un contexto determinado, que restringen las decisiones arquitectónicas específicas en ese contexto y obtienen beneficios en cada sistema resultante (raw/2-1-definiciones-2.md, diap. 6, citando a Taylor, 2010).
- Clasificación en dos grandes grupos (raw/2-1-definiciones-2.md, diap. 7):
  - Monolíticos: un solo equipo, una sola pieza de software. Incluyen lenguajes de programación/máquinas virtuales (programación estructurada, orientado a objetos), flujo de datos (batch, pipes and filters), invocación implícita (event-based, publisher-subscriber), intérprete (rule based) y memoria compartida (blackboard).
  - Distribuidos: múltiples equipos independientes, múltiples sistemas intercomunicados. Incluyen capas, cliente-servidor, peer-to-peer, n-tier y microservicios.
- La diapositiva menciona factores que influyen en la elección: curva de aprendizaje, modularidad, eficiencia, capacidad de prueba, capacidad de modificación, disponibilidad, adaptabilidad y uso de recursos (raw/2-1-definiciones-2.md, diap. 7). La asignación exacta de cada ítem a su grupo no es clara en el texto convertido.
- Otra clasificación (clase 5.1) agrupa los estilos en cuatro familias: llamado y retorno, flujo de datos, centrados en datos y componentes independientes (raw/5-1-estilos-y-patrones-arquitecturales-3.md, diap. 3).
  - Llamado y retorno: programa principal y subrutinas, orientado a objetos, multi-nivel, cliente-servidor.
  - Flujo de datos: lote secuencial, tubos y filtros.
  - Centrados en datos: pizarrón, centrado en base de datos, sistema experto basado en reglas.
  - Componentes independientes: invocación implícita (basado en eventos, publicar/suscribir, orientado a servicios 2.0) e invocación explícita (orientado a servicios 1.0).
- Ambas clasificaciones coinciden en varios estilos (p. ej. tubos y filtros, pizarrón) pero los agrupan con criterios distintos; en la clase 2.1 cliente-servidor figura entre los distribuidos (raw/2-1-definiciones-2.md, diap. 7) y en la 5.1 dentro de llamado y retorno (raw/5-1-estilos-y-patrones-arquitecturales-3.md, diap. 4). Son agrupaciones diferentes, no una afirmación opuesta explícita.

## Relaciones
- [[wiki/conceptos/patrones-arquitectonicos|Patrones arquitectónicos]]: concepto afín.
- [[wiki/comparaciones/estilos-vs-patrones-arquitecturales|Estilos vs patrones arquitecturales]]: diferencias.
- [[wiki/conceptos/arquitectura-de-software|Arquitectura de software]]: los estilos restringen sus decisiones.
- [[wiki/conceptos/estilos-de-llamado-y-retorno|Estilos de llamado y retorno]]: familia de la clase 5.1.
- [[wiki/conceptos/estilos-de-flujo-de-datos|Estilos de flujo de datos]]: familia de la clase 5.1.
- [[wiki/conceptos/estilos-centrados-en-datos|Estilos centrados en datos]]: familia de la clase 5.1.
- [[wiki/conceptos/estilos-de-componentes-independientes|Estilos de componentes independientes]]: familia de la clase 5.1.

## Fuentes
- raw/2-1-definiciones-2.md, diap. 6: definición.
- raw/2-1-definiciones-2.md, diap. 7: clasificación monolíticos/distribuidos.
- raw/5-1-estilos-y-patrones-arquitecturales-3.md, diap. 3-4: clasificación en cuatro familias.
