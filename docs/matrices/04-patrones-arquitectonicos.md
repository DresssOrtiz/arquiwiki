# 3.4 Matriz de patrones arquitectónicos

> **Fuente principal y versión editable maestra:** [Investigación ArquiWiki, capítulo 3.4 (Google Drive)](https://docs.google.com/document/d/1uFmCr0120qSVLiMvn05fTBuXrhV1pCGu08XgdMnWA38/edit). Exportación fiel de la tabla nativa; ante diferencias prevalece el original de Drive.

| Patrón | LLM Wiki | Obsidian | Agentes IA | MCP | RAG |
| --- | --- | --- | --- | --- | --- |
| Blackboard | M · analogía de espacio común de conocimiento | M · grafo de notas | M · coordinación de escritores por comprobar | M · canal de acceso | B · no esencial |
| Adapter | B · esquema no es Adapter por sí solo | M · plugins | A · wrappers herramientas | M · adaptador requiere implementación | M · adaptador almacén vectorial |
| Repository | N/A · persistir archivos no prueba Repository | N/A · vault no es Repository por sí solo | N/A · Git no demuestra Repository | N/A · protocolo no define Repository | M · acceso mediante store; validar abstracción |
| Pipes and Filters | M · operaciones independientes | B · visor final | A · pasos secuenciales | M · canal herramientas | A · fragmentar/indexar/recuperar |
| Gateway | M · entrada wiki | B · no aporta | M · acceso herramientas | A · mcp-gateway | M · API del servicio RAG |
| Cliente-servidor | B · puede ser local | B · aplicación local | A · cliente de tools | A · cliente/servidor MCP | A · API de consulta y pgvector |

**Lectura:** A = relación directa; M = contextual; B = indirecta; N/A = no aplicable; NE = evidencia insuficiente. **No son medidas experimentales ni certificaciones de calidad.**
