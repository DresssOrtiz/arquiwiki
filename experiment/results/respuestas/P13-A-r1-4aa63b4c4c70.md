**Principio SOLID: DIP (inversión de dependencias), con apoyo de OCP.**
- DIP dice que hay que depender de abstracciones y no de clases concretas. Los módulos de alto nivel no deben depender de los de bajo nivel, y los detalles deben depender de las abstracciones (raw/1-2-definiciones-1.md, diap. 42).
- Aplicado al caso: la lógica de ArquiWiki dependería de una interfaz de "modelo de lenguaje". Cada proveedor sería un detalle que implementa esa interfaz.
- OCP encaja con esto. Un proveedor nuevo se añadiría como una extensión, sin modificar las clases existentes, porque deben estar abiertas a extensión y cerradas a modificación (raw/1-2-definiciones-1.md, diap. 41).
- ISP sirve de complemento. La interfaz debe ser específica para su cliente y con una finalidad concreta (raw/1-2-definiciones-1.md, diap. 42).
- LSP exige que cualquier proveedor pueda sustituir a otro sin alterar el sistema (raw/1-2-definiciones-1.md, diap. 41).
- Esta aplicación a ArquiWiki es mi interpretación. La wiki no describe la arquitectura de ArquiWiki ni su uso de un LLM.

**Tácticas de mantenibilidad relevantes.** El escenario de mantenibilidad va del pedido de cambio al cambio hecho, probado y desplegado (raw/3-2-atributos-de-calidad-3.md, diap. 16). El catálogo nombra estas tácticas (raw/3-2-atributos-de-calidad-3.md, diap. 17):
- **Ocultar información, mantener la interfaz y restringir comunicación:** el resto de la app solo ve la interfaz estable.
- **Intermediarios:** una capa o adaptador entre la app y el proveedor.
- **Polimorfismo y diferir enlace:** el proveedor concreto se elige en ejecución o en configuración.
- **Archivos de configuración:** el proveedor, el modelo y las credenciales salen del código.
- **Reemplazo de componentes y adherir a protocolos:** se cambia el adaptador y se usa un protocolo común.
- **Confinar modificaciones, anticipar cambios y abstraer servicios comunes:** el cambio queda en un solo módulo.
- La wiki advierte que la conversión no permite asignar con certeza cada táctica a su grupo, por ejemplo "prevenir efectos dominó". Hay que verificarlo contra el PDF (raw/3-2-atributos-de-calidad-3.md, diap. 17).

**Cómo comprobar la decisión**
1. **Escenario de calidad:** redactarlo con estímulo "cambio de proveedor", respuesta "cambio hecho, probado y desplegado" y una medida, como los archivos modificados o el esfuerzo (raw/3-2-atributos-de-calidad-3.md, diap. 16). Esto sigue el esquema estímulo-respuesta de los escenarios.
2. **Métricas de mantenibilidad:** la cobertura de código en tests y el análisis estático (raw/2-2-atributos-de-calidad-1.md, diap. 38). Una prueba objetiva sería que el cambio solo toque el adaptador y la configuración.
3. **Tácticas de capacidad de prueba:** separar interfaz de implementación, captura y reproducción, y entradas y salidas (raw/3-2-atributos-de-calidad-3.md, diap. 23). Con un proveedor simulado se comprueba que la app funciona con cualquier implementación de la interfaz (LSP).
4. **Trade-offs:** evaluar el costo de la abstracción con el análisis de acuerdos, o con ATAM como método para gestionar atributos de calidad (raw/3-2-atributos-de-calidad-3.md, diap. 7).

## Fuentes
- Wiki: [[wiki/conceptos/principios-solid|Principios SOLID]], [[wiki/conceptos/tacticas-de-mantenibilidad|Tácticas de mantenibilidad]], [[wiki/conceptos/mantenibilidad|Mantenibilidad]], [[wiki/conceptos/tacticas-de-capacidad-de-prueba|Tácticas de capacidad de prueba]]
- Raw: raw/1-2-definiciones-1.md, diap. 41-42; raw/3-2-atributos-de-calidad-3.md, diap. 7, 16, 17, 23; raw/2-2-atributos-de-calidad-1.md, diap. 38

Vacíos: La wiki no contiene información sobre la arquitectura de ArquiWiki ni sobre su proveedor de LLM. Tampoco da procedimientos concretos para probar un cambio de proveedor ni asigna con certeza las tácticas a sus grupos. Esas partes son mi inferencia a partir de los conceptos. Solo verifiqué en raw/ el archivo 3-2 (diap. 7, 16, 17, 23). Las citas a raw/1-2 (diap. 41-42) y raw/2-2 (diap. 38) las copié de las páginas de la wiki y no las comprobé en las fuentes.