# Muestras sintéticas

Cuatro documentos cortos y ficticios (`clase-01-fundamentos-muestra.md`, `clase-02-atam-muestra.md`, `clase-03-atributos-calidad-muestra.md`, `mani-srs-muestra.md`) que se usaron para probar el pipeline antes de tener el corpus real.

- **No forman parte del corpus evaluado** y no se cargan ni en KB-A ni en KB-B: viven fuera de `kb-wiki/vault/`, así que ni el vault de ejecución, ni el RAG (que indexa `vault/raw`), ni los agentes los ven.
- **Para qué sirven:** pruebas del pipeline y ejemplos. Los ejemplos del agente Ingeniero de Sistemas los citan como `kb-wiki/muestras/<archivo>`.
- El corpus evaluado está en `kb-wiki/vault/raw/` (los 6 documentos del curso).
