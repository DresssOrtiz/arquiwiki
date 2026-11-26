El contexto recuperado no contiene información sobre ArquiWiki, sus agentes ni la separación `raw/` / `wiki/`. Solo hay material genérico sobre tácticas de seguridad y restricciones, que puede servir de base para la propuesta.

**Restricciones**
- Las restricciones vienen impuestas, pueden ser técnicas u organizativas, y limitan las alternativas de diseño (raw/2-2-atributos-de-calidad-1.md, diap. 9). Por tanto, "los agentes consultan `raw/` y solo algunos editan `wiki/`" encaja como restricción de diseño, no como una opción más.

**Tácticas de seguridad aplicables**

La diapositiva de seguridad agrupa las tácticas en cuatro familias: detectar ataques, resistir ataques, limitar la exposición o el acceso, y recuperarse de ataques (raw/3-2-atributos-de-calidad-3.md, diap. 21). El texto de la diapositiva está desordenado, así que la asignación exacta es aproximada. Esto es lo que propondría con ella:
- **Identificación y autenticación** de cada agente, para saber quién consulta o edita (raw/3-2-atributos-de-calidad-3.md, diap. 21).
- **Autorización** que distinga el permiso de lectura sobre `raw/` del de escritura sobre `wiki/`, concedido solo a los agentes designados (raw/3-2-atributos-de-calidad-3.md, diap. 21).
- **Limitar acceso y exposición**, es decir, el mínimo de agentes y de contenido accesible (raw/3-2-atributos-de-calidad-3.md, diap. 21).
- **Confidencialidad e integridad de los datos**, para proteger el contenido (raw/3-2-atributos-de-calidad-3.md, diap. 21).
- **Traza de auditoría** de lecturas y ediciones (raw/3-2-atributos-de-calidad-3.md, diap. 21).
- **Detectores de intrusos** para detectar ataques, y **restauración** para recuperarse (raw/3-2-atributos-de-calidad-3.md, diap. 21).

## Fuentes
- Raw: raw/2-2-atributos-de-calidad-1.md, diap. 9; raw/3-2-atributos-de-calidad-3.md, diap. 21

Vacíos: los fragmentos no describen cómo implementar estas tácticas, ni roles, permisos, control de versiones o mecanismos concretos para `raw/` y `wiki/`. Tampoco detallan qué hace cada táctica de la diapositiva 21, que solo las enumera.