# 3.1 Matriz de principios SOLID

> **Fuente principal y versión editable maestra:** [Investigación ArquiWiki, capítulo 3.1 (Google Drive)](https://docs.google.com/document/d/1uFmCr0120qSVLiMvn05fTBuXrhV1pCGu08XgdMnWA38/edit). Exportación fiel de la tabla nativa; ante diferencias prevalece el original de Drive.

| Principio | LLM Wiki | Obsidian | Agentes IA | MCP | RAG |
| --- | --- | --- | --- | --- | --- |
| S: una responsabilidad | M · tareas de ingesta y consulta separadas | NE · requiere examinar clases internas | A · ingestor, consultor y auditor | M · operación acotada; SRP por verificar | A · servicios de indexar y consultar |
| O: abierto/cerrado | M · el esquema permite ampliar notas | NE · extensibilidad interna no comprobada | M · extensión mediante skills; verificar diseño | M · extensibilidad mediante contratos | M · extensión si respeta interfaz |
| L: sustitución | N/A · no hay subtipos | N/A · no hay herencia | NE · no se han probado contratos subtipo/base | N/A · interoperar no prueba LSP | N/A · intercambio no prueba LSP |
| I: segregación interfaces | M · responsabilidades de operaciones, no ISP probado | NE · no se han evaluado interfaces internas | A · skills específicas | A · tools granulares | A · API de búsqueda mínima |
| D: inversión dependencias | M · esquema desacopla | NE · depende de las dependencias internas | M · agente usa contrato de tools | M · protocolo favorece separación; DIP requiere código | M · dependencia de interfaz de store |

**Lectura:** A = relación directa; M = contextual; B = indirecta; N/A = no aplicable; NE = evidencia insuficiente. **No son medidas experimentales ni certificaciones de calidad.**
