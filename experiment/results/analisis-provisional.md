# Análisis exploratorio y calificación asistida provisional

Análisis descriptivo del 25 de noviembre de 2026 sobre la versión `7bdce5b`. Se conservan `tabla.md`, las respuestas y el CSV humano originales. Las notas asistidas son provisionales y están pendientes de validación humana.

## (a) Construcción

### KB-A: tokens de LLM (kba_runs.jsonl; ingesta, lint y corrección)

| Operación | Ejecuciones | Con error | Entrada total (tokens LLM) | Entrada nueva (input + cache_creation) | Salida (tokens LLM) | Tiempo (s) |
|---|---|---|---|---|---|---|
| ingesta | 6 | 0 | 1 037 380 | 233 557 | 113 087 | 608.5 |
| lint | 1 | 0 | 603 745 | 128 957 | 24 622 | 229.8 |
| correccion | 1 | 0 | 945 846 | 156 879 | 72 026 | 326.7 |

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
- Todos los tokens salen del campo `usage` del CLI, con el mismo modelo en ambos brazos; el costo equivalente del CLI no demuestra un pago marginal ni el costo total de la suscripción.

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

## (d) Calidad de las respuestas (rúbrica 0-10, calificación asistida provisional, NO ciega)

| Brazo | n | Exactitud (0-4) | Trazabilidad (0-3) | Cobertura (0-2) | Prudencia (0-1) | Total (0-10) | Nota >= 8 |
|---|---|---|---|---|---|---|---|
| KB-A (wiki) | 15 | 3.60 | 2.93 | 1.80 | 0.93 | 9.27 | 87% |
| KB-B (RAG) | 15 | 2.60 | 2.93 | 1.13 | 1 | 7.67 | 53% |

### Por tipo de pregunta

| Tipo | Brazo | n | Exactitud (0-4) | Trazabilidad (0-3) | Cobertura (0-2) | Prudencia (0-1) | Total (0-10) | Nota >= 8 |
|---|---|---|---|---|---|---|---|---|
| Puntual | KB-A (wiki) | 5 | 4 | 3 | 2 | 1 | 10 | 100% |
| Puntual | KB-B (RAG) | 5 | 2.80 | 3 | 1.20 | 1 | 8 | 60% |
| Síntesis entre fuentes | KB-A (wiki) | 4 | 3.25 | 3 | 1.50 | 1 | 8.75 | 75% |
| Síntesis entre fuentes | KB-B (RAG) | 4 | 2 | 2.75 | 0.75 | 1 | 6.50 | 25% |
| Aplicación a caso | KB-A (wiki) | 4 | 3.25 | 2.75 | 1.75 | 0.75 | 8.50 | 75% |
| Aplicación a caso | KB-B (RAG) | 4 | 2.25 | 3 | 1 | 1 | 7.25 | 50% |
| Abstención ante falta de evidencia | KB-A (wiki) | 2 | 4 | 3 | 2 | 1 | 10 | 100% |
| Abstención ante falta de evidencia | KB-B (RAG) | 2 | 4 | 3 | 2 | 1 | 10 | 100% |

### Aciertos en P14-P15 (exactitud = 4, abstención correcta)

| Brazo | Aciertos | Respuestas |
|---|---|---|
| KB-A (wiki) | 2 | 2 |
| KB-B (RAG) | 2 | 2 |

Cada criterio se promedia sobre 15 respuestas por brazo, calificadas una sola vez por IA. No hay consenso humano ni segundo evaluador. "Nota >= 8" es la proporción de respuestas con total >= 8/10. Con muestras de 15 a 90 respuestas no se infieren diferencias estadísticamente significativas.

En exactitud máxima (4/4) hay 10/15 respuestas de A y 6/15 de B; no es una tasa universal de exactitud, sino el recuento de esta rúbrica asistida. En trazabilidad máxima (3/3) hay 14/15 en cada brazo. Una referencia puede ser verificable aunque periférica y no contestar la pregunta. Se registran confusión de componentes en P07-B, omisiones de síntesis en P08/P09, agrupaciones imprecisas en P11, una cita de archivo errónea en P12-A y una generalización de pruebas en P13-A. El CSV conserva las observaciones por respuesta; no se calcula una tasa de alucinación sin un protocolo por afirmación.

## Notas por pregunta

| Pregunta | A /10 | B /10 |
|---|---|---|
| P01 | 10 | 10 |
| P02 | 10 | 5 |
| P03 | 10 | 10 |
| P04 | 10 | 10 |
| P05 | 10 | 5 |
| P06 | 10 | 10 |
| P07 | 10 | 6 |
| P08 | 8 | 5 |
| P09 | 7 | 5 |
| P10 | 10 | 7 |
| P11 | 9 | 9 |
| P12 | 7 | 8 |
| P13 | 8 | 5 |
| P14 | 10 | 10 |
| P15 | 10 | 10 |

## Método y límites de esta calificación

Se leyeron las 30 respuestas completas, las preguntas, claves y rúbrica, y se contrastaron las afirmaciones relevantes con los PDF originales. Se otorga trazabilidad a una cita real y precisa incluso si solo respalda un fragmento periférico; esto no sustituye cobertura ni exactitud. Para una pregunta respondible, abstenerse honestamente conserva prudencia pero pierde cobertura y exactitud de la respuesta pedida. Para P14/P15 la abstención sí es la respuesta correcta. Las cuatro subnotas son juicios asistidos, no mediciones instrumentales.

El CSV conserva identificador, brazo explícito, pregunta, ruta y SHA-256 de respuesta, fuente original, subnotas, justificación, errores y campos vacíos para validación humana. No requiere el mapa privado ni modifica el CSV ciego. La evaluación fue realizada una sola vez con asistencia de IA; no hay un segundo evaluador. P08/P09, P10 y P12/P13 presentan aspectos sujetos a revisión humana: se distinguen omisiones, inferencias admisibles y citas erróneas.

## Datos medidos e interpretación

- Consultas: 30 registros, 30 identificadores únicos, 15 por brazo, una repetición y cero errores de proceso; esto no equivale a cero errores de contenido. Mismo alias `claude-sonnet-5-5`.
- Entrada LLM acumulada: A 621 251, B 44 425; entrada nueva: A 228 026, B 44 425; salida: A 22 634, B 10 256. La entrada total de A es 13,98 veces la de B en esta corrida; no es una razón de precios.
- Medianas de latencia: A 16 523 ms, B 7 326 ms. B incluye recuperación y CLI; A, CLI. No incluyen reset ni espera entre corridas. No equivalen a latencia interna pura del modelo.
- `cost_usd_equiv` suma USD 1,1775345 en A y USD 0,2802 en B: USD 1,4577345 total. Es el equivalente registrado por el CLI, no una factura ni una medición del costo total de la suscripción. No se consultaron tarifas actuales ni se estimó electricidad/hardware.
- Construcción A: 2 586 971 tokens de entrada total, 519 393 de entrada nueva, 2 067 578 de caché leída (79,92 %), 209 735 de salida y 1 165 007 ms (19,42 min). Los ocho pasos incluyen seis ingestas, lint y corrección. El estado `ok` lo asignó el flujo de agentes; no certifica la fidelidad de los PDF.
- Construcción B histórica: dos indexaciones completas de 189 fragmentos y 14 388 tokens registrados, 3 243 y 2 985 ms; son ejecuciones separadas, no un único costo de construcción acumulable. Los dos incrementales sin cambios (7 y 10 ms) NO miden actualización de contenido.
- El truncamiento histórico hace que `embedded_tokens` y `retrieved_tokens` sean cotas inferiores. Los contadores del CLI siguen siendo los registrados de LLM. La medición posterior de Tomás (280 fragmentos y 20 234 tokens) corresponde al recuperador corregido, no a estas respuestas.

## Amenazas que impiden un resultado definitivo

La corrida usó el corpus anterior a la corrección de 1.2/31 y el RAG anterior al PR #9. La revisión del corpus verificó 183 marcadores consecutivos y examinó visualmente 50 láminas; 133 aún carecen de revisión visual completa. Persisten pérdidas de información gráfica en 1.2/11 y /21, 3.1/8-9 y 5.1/10, /12-13. La corrección de 1.2/31 conserva las tres columnas del PDF, pero es posterior a la corrida. La presencia de encabezados no garantiza fidelidad semántica. El problema de truncamiento puede afectar recuperación, pero no se ha demostrado como causa de P02/P09. A consulta síntesis persistentes y B cinco fragmentos: son estrategias distintas, no contextos idénticos. Hay una repetición por pregunta, orden intercalado y cachés, sin control de temperatura. La evaluación actual es asistida, no ciega ni aprobada. No se declara ganador, significancia ni superioridad general.

## Mediciones ausentes

No existen `actualizacion.jsonl` ni `overhead.jsonl` del protocolo. No se dispone de estas mediciones. La bitácora contiene un spike de 924 tokens con prompt trivial, pero no sustituye la medición controlada por configuración. No se resta de las consultas. El costo de actualización permanece sin medición; una nueva evaluación requiere corpus congelado y reconstrucción/reindexación sobre la misma versión.

Fuentes: [registros](experimento.jsonl), [respuestas](respuestas/), [CSV provisional](calificacion-asistida-provisional.csv), [métricas del experimento](metricas-experimento-provisional.json), [rúbrica](../rubrica.md), [claves](../claves.json), [evidencia B](../../docs/evidencia-B.md). `calificacion.py` implementa el flujo de evaluación humana. Las tablas de construcción y consulta se calcularon con las funciones de `reporte.py`; `tabla.md` conserva su contenido histórico.
