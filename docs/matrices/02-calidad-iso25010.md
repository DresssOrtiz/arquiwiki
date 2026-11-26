# 3.2 Matriz de atributos de calidad — ISO/IEC 25010:2023

> **Fuente principal y versión editable maestra:** [Investigación ArquiWiki, capítulo 3.2 (Google Drive)](https://docs.google.com/document/d/1uFmCr0120qSVLiMvn05fTBuXrhV1pCGu08XgdMnWA38/edit). Exportación fiel de la tabla nativa; ante diferencias prevalece el original de Drive.

| Atributo | LLM Wiki | Obsidian | Agentes IA | MCP | RAG |
| --- | --- | --- | --- | --- | --- |
| Adecuación funcional | M · síntesis verificable | M · navegación notas | A · ejecuta tareas | M · expone funciones | A · recuperar fuentes |
| Eficiencia rendimiento | M · costo de ingesta | A · lectura local | M · tokens/latencia | M · latencia de llamadas externas | M · búsqueda e índice |
| Compatibilidad | A · Markdown abierto | A · archivos estándar | M · clientes variados | A · estándares de interacción y contratos MCP | A · API/almacenes |
| Capacidad interacción | M · depende visor | A · grafo/navegación | M · interfaz agente | M · cliente abstraído | M · interfaz externa |
| Fiabilidad | M · necesita lint | M · depende de archivos | M · validar salidas y reintentos | M · validar herramientas | M · depende de retrieve |
| Seguridad | M · fuentes inmutables | M · archivos locales | B · permisos críticos | M · autorizar tools | M · control corpus |
| Mantenibilidad | A · páginas y Git | A · notas legibles | M · skills versionadas | A · contratos aislados | A · módulos separados |
| Flexibilidad | A · páginas extensibles | A · formato Markdown y ampliación con plugins | A · nuevos roles | A · sumar servidores | A · varios retrievers |
| Seguridad operacional | B · caso académico | B · uso principalmente informativo | M · límites de acciones | M · restringir efectos | B · lectura informativa |

**Lectura:** A = relación directa; M = contextual; B = indirecta; N/A = no aplicable; NE = evidencia insuficiente. **No son medidas experimentales ni certificaciones de calidad.**
