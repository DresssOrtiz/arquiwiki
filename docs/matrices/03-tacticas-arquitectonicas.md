# 3.3 Matriz de tácticas arquitectónicas

> **Fuente principal y versión editable maestra:** [Investigación ArquiWiki, capítulo 3.3 (Google Drive)](https://docs.google.com/document/d/1uFmCr0120qSVLiMvn05fTBuXrhV1pCGu08XgdMnWA38/edit). Exportación fiel de la tabla nativa; ante diferencias prevalece el original de Drive.

| Táctica | LLM Wiki | Obsidian | Agentes IA | MCP | RAG |
| --- | --- | --- | --- | --- | --- |
| Disponibilidad | M · versionar wiki | M · notas disponibles sin red | M · reintentos | M · fallback servidor | M · réplicas como opción de diseño |
| Rendimiento | M · índices de páginas navegables | M · acceso local | M · limitar contexto | M · paginar recursos | M · caché acelera; rerank cuesta |
| Seguridad | A · permisos separan raw/wiki | M · acceso local | A · mínimos privilegios | A · autorización por herramienta | M · control de fuentes y permisos |
| Modificabilidad | A · páginas pequeñas | A · Markdown editable y extensiones configurables | A · skills aisladas | A · contrato estable | M · secciones de pipeline separadas |
| Testabilidad | M · revisiones y pruebas de lint | M · inspección visual | M · casos y regresiones de agentes | A · probar llamadas | A · pruebas de recuperación/citas |
| Usabilidad | A · índice navegable | A · grafo y búsqueda | M · respuestas guiadas | B · el protocolo no es interfaz | M · citas en respuesta |
| Observabilidad | M · bitácora y comparación Git | B · grafo sin trazas operativas | A · trazas de acciones | A · bitácora de llamadas MCP | A · logs de consulta y métricas |

**Lectura:** A = relación directa; M = contextual; B = indirecta; N/A = no aplicable; NE = evidencia insuficiente. **No son medidas experimentales ni certificaciones de calidad.**
