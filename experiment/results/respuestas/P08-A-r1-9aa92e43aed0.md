La wiki no relaciona DIP con las tácticas de mantenibilidad, ni las fuentes revisadas. Solo puedo darte las dos piezas por separado.

**Qué dice la wiki sobre cada una**
- **DIP:** consiste en depender de abstracciones y no de clases concretas. Los módulos de alto nivel no deben depender de los de bajo nivel, y los detalles deben depender de las abstracciones (raw/1-2-definiciones-1.md, diap. 42). Está en [[wiki/conceptos/principios-solid|Principios SOLID]].
- **Tácticas de mantenibilidad:** el escenario va de un pedido de cambio a un cambio hecho, probado y desplegado (raw/3-2-atributos-de-calidad-3.md, diap. 16). Las tácticas nombradas incluyen ocultar información, mantener la interfaz, intermediarios, adherir a protocolos, polimorfismo, diferir enlace, archivos de configuración y reemplazo de componentes (raw/3-2-atributos-de-calidad-3.md, diap. 17). Están en [[wiki/conceptos/tacticas-de-mantenibilidad|Tácticas de mantenibilidad]].

**Qué no dice**
- Ninguna fuente menciona el cambio de una dependencia en relación con DIP.
- Ninguna fuente asigna DIP a una táctica concreta, como intermediarios o mantener la interfaz.
- La conversión de la diap. 17 tampoco permite asignar con certeza cada táctica a su grupo, por ejemplo "prevenir efectos dominó". Hay que verificarlo contra el PDF (raw/3-2-atributos-de-calidad-3.md, diap. 17).

Cualquier vínculo que yo propusiera, como "DIP implementa la táctica de intermediarios", sería inferencia mía y no aparece en el vault. Por eso no lo afirmo.

## Fuentes
- Wiki: [[wiki/conceptos/principios-solid|Principios SOLID]], [[wiki/conceptos/tacticas-de-mantenibilidad|Tácticas de mantenibilidad]]
- Raw: raw/1-2-definiciones-1.md, diap. 42; raw/3-2-atributos-de-calidad-3.md, diap. 16-17

Vacíos: la wiki no contiene información sobre la relación entre DIP y las tácticas de mantenibilidad, ni sobre el cambio de una dependencia, y las fuentes revisadas tampoco.