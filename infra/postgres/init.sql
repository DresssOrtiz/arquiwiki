-- Se ejecuta una sola vez, al crear el volumen de datos.
CREATE EXTENSION IF NOT EXISTS vector;

-- Entidades del CRUD (api)
CREATE SCHEMA IF NOT EXISTS app;
-- Chunks, embeddings y registros de métricas (rag-service)
CREATE SCHEMA IF NOT EXISTS rag;
