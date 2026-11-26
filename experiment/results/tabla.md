# Tablas del experimento KB-A vs KB-B

Generado por `experiment/reporte.py`. Mismo modelo y mismo CLI en ambos brazos.

## (a) Construcción

### KB-A: tokens de LLM (kba_runs.jsonl; ingesta, lint y corrección)

_Sin registros de construcción de KB-A._

### KB-B: indexación (rag_builds.jsonl, modo full)

| ts | Archivos | Fragmentos | Tokens de embeddings (modelo local) | Tokens de LLM | Tiempo (ms) |
|---|---|---|---|---|---|
| 2026-11-26T00:52:31+00:00 | 6 | 189 | 14 388 | 0 | 3 243 |
| 2026-11-26T01:32:06+00:00 | 6 | 189 | 14 388 | 0 | 2 985 |

Las columnas de tokens de LLM (KB-A) y de tokens de embeddings (KB-B) son magnitudes distintas y no se suman ni se restan: se comparan por separado. "Entrada total" incluye lecturas de caché (cada turno reenvía el contexto acumulado); "entrada nueva" es input + cache_creation.

## (b) Costo por consulta, por brazo

| Métrica (media / mediana / desv. est.) | KB-A (wiki) | KB-B (RAG) |
|---|---|---|
| Entrada total (tokens) | 41 417 / 41 795 / 16 641 | 2 962 / 2 931 / 242 |
| Entrada nueva (input + cache_creation) | 15 202 / 13 425 / 6 226 | 2 962 / 2 931 / 242 |
| Salida (tokens) | 1 509 / 1 458 / 660 | 684 / 518 / 404 |
| Turnos | 7.9 / 8 / 2.0 | 1 / 1 / 0.0 |
| Latencia total (ms) | 19 907 / 16 523 / 15 087 | 7 930 / 7 326 / 2 649 |
| Tiempo de claude, wall (ms) | 19 907 / 16 523 / 15 087 | 7 866 / 7 277 / 2 647 |

n (sin error): A=15, B=15; con error (excluidas): A=0, B=0.

| Solo KB-B (media / mediana / desv. est.) | Valor |
|---|---|
| Recuperación, servicio (ms) | 52 / 48 / 16 |
| Recuperación, reloj (ms) | 64 / 61 / 18 |
| Tokens recuperados | 502 / 523 / 83 |

- Entrada total: tokens de entrada que el CLI reporta (input + cache_creation + cache_read). En KB-A crece con cada turno porque el agente reenvía su contexto; en KB-B es un solo turno con los fragmentos.
- Entrada nueva: input + cache_creation, sin lecturas de caché; es menos sensible al orden de las corridas.
- Latencia total: en KB-A es el tiempo de `claude -p`; en KB-B suma recuperación (reloj) + `claude -p`. No incluye el reset de KB-A ni la espera entre corridas.
- Todos los tokens salen del campo `usage` del CLI, con el mismo modelo en ambos brazos; con suscripción no hay costo monetario real.

## (c) Por tipo de pregunta

| Tipo | Brazo | n | Entrada total (media) | Entrada nueva (media) | Salida (media) | Turnos (media) | Latencia total (mediana, ms) |
|---|---|---|---|---|---|---|---|
| Puntual | KB-A (wiki) | 5 | 36 802 | 12 959 | 1 137 | 7 | 15 344 |
| Puntual | KB-B (RAG) | 5 | 2 888 | 2 888 | 423 | 1 | 6 218 |
| Síntesis entre fuentes | KB-A (wiki) | 4 | 57 949 | 20 402 | 1 868 | 9.2 | 18 291 |
| Síntesis entre fuentes | KB-B (RAG) | 4 | 3 001 | 3 001 | 639 | 1 | 7 604 |
| Aplicación a caso | KB-A (wiki) | 4 | 39 860 | 15 896 | 2 039 | 8.5 | 16 896 |
| Aplicación a caso | KB-B (RAG) | 4 | 3 030 | 3 030 | 1 215 | 1 | 12 026 |
| Abstención ante falta de evidencia | KB-A (wiki) | 2 | 23 003 | 9 019 | 660 | 6 | 9 286 |
| Abstención ante falta de evidencia | KB-B (RAG) | 2 | 2 932 | 2 932 | 362 | 1 | 6 056 |

Cada fila agrupa las ejecuciones sin error del tipo indicado; n cuenta pregunta × repetición.

## (d) Calidad de las respuestas (rúbrica 0-10, calificación ciega)

_Sin calificacion_resultados.csv todavía._

## (e) Costo de actualización (un archivo modificado)

_Sin actualizacion.jsonl (se ejecuta después del experimento principal)._

## (f) Overhead fijo del CLI (prompt trivial, reportado aparte)

_Sin overhead.jsonl (`python3 experiment/run.py --overhead N`)._
