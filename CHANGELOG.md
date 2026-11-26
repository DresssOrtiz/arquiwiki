# Changelog

## [Sin publicar]

### Agregado
- Estructura del repositorio, `docker-compose.yml`, `.env.example` y contrato de contenedores (`docs/contrato-B.md`).
- `api/`: CRUD de Fuente y Página con relación N:M (FastAPI, SQLAlchemy 2) y pruebas.
- `kb-rag/`: RAG con fragmentación por encabezados, embeddings locales (fastembed), pgvector, respuesta con Claude y registro de tokens y latencia en `experiment/results/`.
- `mcp-gateway/`: servidor MCP (streamable HTTP) con permisos por rol, una rama y copia de trabajo de git por agente, y auditoría JSONL.
- Scripts: `smoke.sh`, `seed-demo.sh`, `merge-agents.sh`, `vault-export.sh`, `mcp_check.py`.
- Documentos de muestra sintéticos en `kb-wiki/vault/raw/` y guía de demo en `demo/comandos.md`.
- `README.md` con los pasos de despliegue.

### Corregido
- `kb-rag`: el conteo de tokens se saturaba en 128 (ventana del modelo de embeddings), por lo que el fragmentador no partía los fragmentos largos y el embedding descartaba el final de 40 de 189 fragmentos. Ahora se cuenta sin truncar, el tamaño por defecto es 120 tokens y se recorta a la ventana del modelo. El índice del corpus real pasa de 189 a 280 fragmentos y los tokens registrados coinciden con los reales. Requiere reindexar con `{"force": true}`.

### Decisiones
- `mcp-gateway` fija `mcp<2`: la serie 2.x renombró `FastMCP` a `MCPServer`.
- Fragmentos de 200 tokens (no 400) porque el modelo de embeddings multilingüe elegido rinde mejor con textos cortos.
