La wiki solo cubre en parte la pregunta. Cubre la clasificación de ambos estilos, pero no cómo se comparan ni cómo influyen en la calidad.

**Lo que sí hay en la wiki**
- Los estilos de flujo de datos y los centrados en datos son dos familias distintas dentro de la clasificación en cuatro familias de la clase 5.1.
  - Flujo de datos incluye lote secuencial y tubos y filtros (raw/5-1-estilos-y-patrones-arquitecturales-3.md, diap. 8 y 10). Ver [[wiki/conceptos/estilos-de-flujo-de-datos|Estilos de flujo de datos]].
  - Centrados en datos incluye pizarrón, centrado en base de datos y sistema experto basado en reglas (raw/5-1-estilos-y-patrones-arquitecturales-3.md, diap. 11-14). Ver [[wiki/conceptos/estilos-centrados-en-datos|Estilos centrados en datos]].
- La clase 2.1 nombra ambos tipos entre los estilos monolíticos, es decir, un solo equipo y una sola pieza de software.
  - Flujo de datos aparece como "batch" y "pipes and filters".
  - Los centrados en datos aparecen como "blackboard", descrito como memoria compartida, e "intérprete (rule based)" (raw/2-1-definiciones-2.md, diap. 7). Ver [[wiki/conceptos/estilos-arquitectonicos|Estilos arquitectónicos]].
- Esa misma diapositiva lista factores que influyen en la elección del estilo: curva de aprendizaje, modularidad, eficiencia, capacidad de prueba, capacidad de modificación, disponibilidad, adaptabilidad y uso de recursos (raw/2-1-definiciones-2.md, diap. 7). La wiki indica que el texto convertido no deja claro a qué grupo corresponde cada ítem.
- Sobre el contraste entre los dos estilos, lo único que dice la wiki es el nombre de cada uno según su familia: el flujo de datos se nombra por los datos que se mueven entre pasos, y los centrados en datos por los datos que se almacenan. Esto sale de los nombres de las familias, no de una explicación de las fuentes.

**Lo que la wiki no contiene**
- No hay una descripción de cómo funciona cada estilo. Las diapositivas convertidas solo traen los títulos y los diagramas no se extrajeron (raw/5-1-estilos-y-patrones-arquitecturales-3.md, diap. 10 y 12-14).
- La wiki no contiene información sobre cómo elegir entre flujo de datos y centrado en datos afecta a atributos de calidad concretos, como modificabilidad, desempeño o disponibilidad. Las fuentes revisadas tampoco la traen.
- Lo único que sí dicen las fuentes es general: el estilo restringe las decisiones arquitectónicas y se elige según esos factores de calidad (raw/2-1-definiciones-2.md, diap. 6-7). Los atributos están en tensión entre sí, así que hay que tomar decisiones de compromiso. Ver [[wiki/conceptos/acuerdos-trade-offs|Acuerdos (trade-offs)]].

## Fuentes
- Wiki: [[wiki/conceptos/estilos-de-flujo-de-datos|Estilos de flujo de datos]], [[wiki/conceptos/estilos-centrados-en-datos|Estilos centrados en datos]], [[wiki/conceptos/estilos-arquitectonicos|Estilos arquitectónicos]], [[wiki/conceptos/acuerdos-trade-offs|Acuerdos (trade-offs)]]
- Raw: raw/5-1-estilos-y-patrones-arquitecturales-3.md, diap. 3, 8-14; raw/2-1-definiciones-2.md, diap. 6-7

Vacíos: no hay descripción del funcionamiento de tubos y filtros ni de los estilos centrados en datos, ni una comparación entre ellos, ni su impacto en atributos de calidad concretos. Haría falta ingerir el contenido de los diagramas o fuentes adicionales.