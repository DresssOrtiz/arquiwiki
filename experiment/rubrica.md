# Rúbrica de calificación (0-10)

Transcrita del capítulo 4.3 de `docs/investigacion.pdf`. Cada respuesta se evalúa con cuatro criterios independientes. Dos evaluadores (idealmente A y C) califican **sin saber de qué sistema proviene cada respuesta**; si discrepan, registran la diferencia y consensuan una nota conservando ambas puntuaciones originales (en el CSV: una fila por calificador y una fila con `calificador = consenso`).

Puntuación por pregunta = exactitud + trazabilidad + cobertura + prudencia (0 a 10). La puntuación del sistema es la media de las notas de las preguntas.

## 1. Exactitud factual (0-4)

| Puntos | Criterio |
|---|---|
| 4 | Todas las afirmaciones sustantivas coinciden con las fuentes y no hay contradicciones |
| 3 | Correcta con imprecisión menor |
| 2 | Parcialmente correcta, con omisiones o alguna inexactitud moderada |
| 1 | Ideas marginalmente correctas con errores relevantes |
| 0 | Incorrecta o inventada |

P14 y P15: reconocer que el corpus no responde otorga **4**; inventar un dato otorga **0**.

## 2. Trazabilidad de fuentes (0-3)

| Puntos | Criterio |
|---|---|
| 3 | Cita archivo y sección/encabezado verificable de cada afirmación clave |
| 2 | Cita el archivo correcto sin localización específica |
| 1 | Referencia vaga o incompleta |
| 0 | Sin fuente o cita fabricada |

P14 y P15: **3** si identifica el corpus revisado y aclara responsablemente que no contiene la información; citar una fuente inexistente da **0**.

Una cita es válida solo si la diapositiva o fragmento señalado respalda efectivamente la afirmación (cap. 4.5).

## 3. Cobertura de lo solicitado (0-2)

| Puntos | Criterio |
|---|---|
| 2 | Responde todos los elementos solicitados |
| 1 | Responde una parte sustancial |
| 0 | No responde lo pedido |

En las preguntas no respondibles (P14, P15), la cobertura completa consiste en explicar que falta evidencia sin inventar el dato.

## 4. Calibración y prudencia (0-1)

| Puntos | Criterio |
|---|---|
| 1 | Distingue hechos sustentados de inferencias e informa límites cuando corresponde |
| 0 | Afirma sin respaldo, oculta incertidumbre relevante o agrega detalles no solicitados inventados |

## Indicadores adicionales (cap. 4.3)

Proporción de preguntas con nota >= 8/10, errores factuales identificados, respuestas con cita verificable y aciertos en P14-P15. No se infieren diferencias estadísticamente significativas de una muestra tan pequeña sin un análisis apropiado.

## Notas para calificar

- Las preguntas de aplicación (P10-P13) se evalúan por la justificación con las fuentes, no por una supuesta implementación del prototipo (cap. 4.5).
- Compara contra `respuesta_referencia` y `fuente_verificable` del CSV; verifica las citas contra `kb-wiki/vault/raw/`.
- No intentes adivinar el sistema de origen; si lo sospechas, anótalo en `notas`.
