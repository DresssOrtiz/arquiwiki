# Changelog

## [Sin publicar]

Versión propuesta: `v1.0.0`. El tag no ha sido creado.

### Documentación de entrega
- Documento de investigación consolidado, exportado desde Google Docs: 44 páginas, cinco matrices y nueve diagramas.
- Presentación de diez diapositivas con resultados exploratorios y limitaciones metodológicas.
- Video de presentación publicado y enlaces de los cuatro entregables reunidos en el README.
- Retirados los materiales de preparación de la grabación y los marcadores de carpetas ya pobladas.
- Conservados sin cambios el código, agentes, skills, corpus, diagramas y evidencias experimentales, incluidas las treinta calificaciones asistidas provisionales.

### Agregado
- Estructura del repositorio, `docker-compose.yml`, `.env.example` y contrato de contenedores (`docs/contrato-B.md`).
- `api/`: CRUD de Fuente y Página con relación N:M (FastAPI, SQLAlchemy 2) y pruebas.
- `kb-rag/`: RAG con fragmentación por encabezados, embeddings locales (fastembed), pgvector, respuesta con Claude y registro de tokens y latencia en `experiment/results/`.
- `mcp-gateway/`: servidor MCP (streamable HTTP) con permisos por rol, una rama y copia de trabajo de git por agente, y auditoría JSONL.
- Scripts: `smoke.sh`, `seed-demo.sh`, `merge-agents.sh`, `vault-export.sh`, `mcp_check.py`.
- Seis Markdown del corpus académico en `kb-wiki/vault/raw/`; cuatro documentos sintéticos separados en `kb-wiki/muestras/`, fuera de la evaluación.
- `README.md` con los pasos de despliegue.

### Corregido
- `kb-rag`: el conteo de tokens se saturaba en 128 (ventana del modelo de embeddings), por lo que el fragmentador no partía los fragmentos largos y el embedding descartaba el final de 40 de 189 fragmentos. Ahora se cuenta sin truncar, el tamaño por defecto es 120 tokens y se recorta a la ventana del modelo. El índice del corpus real pasa de 189 a 280 fragmentos y los tokens registrados coinciden con los reales. Requiere reindexar con `{"force": true}`.

### Decisiones
- `mcp-gateway` fija `mcp<2`: la serie 2.x renombró `FastMCP` a `MCPServer`.
- Fragmentos de 120 tokens: el modelo de embeddings multilingüe elegido solo procesa 128 tokens por texto. La primera versión usaba 200, pero el contador saturado impedía ver que superaban la ventana (ver "Corregido").
