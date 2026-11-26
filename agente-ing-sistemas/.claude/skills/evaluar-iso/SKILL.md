---
name: evaluar-iso
description: Evalúa un requisito y sus artefactos (modelos y criterios de aceptación) contra ISO/IEC 25010, ISO/IEC/IEEE 29148 e ISO/IEC/IEEE 42010 y genera evaluacion-iso.md con tablas, brechas y acciones priorizadas. Úsala cuando el usuario pida evaluar, auditar o revisar la calidad de un requisito o su descripción de arquitectura con normas ISO.
---

# Skill: evaluar-iso

Produce `evaluacion-iso.md`: un dictamen con evidencia, no una opinión. Cada veredicto cita el artefacto o la línea que lo sustenta.

## Entrada
- Requisito (`requisito.md` o texto).
- Artefactos disponibles: `modelo.dsl`, `paquetes.puml`, `secuencia.puml`, `decisiones.md`, `criterios.feature`. Si falta alguno, evalúa lo que haya y registra la ausencia como brecha.

## Pasos
1. **Leer todos los artefactos** antes de juzgar. Anota para cada uno qué afirma y qué calla.
2. **Consultar la wiki** (MCP `arquiwiki`): `search_notes` por "ISO 25010", "atributos de calidad" y el atributo del requisito; `read_note` de las páginas útiles. Cita las usadas. Si el MCP no está disponible, usa las references de esta skill y declara "wiki no disponible".
3. **Tabla ISO/IEC 25010** (versión 2023; detalle en `references/iso-25010.md`): una fila por cada una de las nueve características. Columnas: característica, ¿la toca el requisito? (Sí/No/Indirecta), evidencia en criterios de aceptación (escenario o "ninguna"), ¿verificable? (Sí/Parcial/No), brecha.
4. **Tabla ISO/IEC/IEEE 29148** (ver `references/iso-29148.md`): una fila por cada característica del requisito individual (necesario, apropiado, inequívoco, completo, singular, factible, verificable, correcto, conforme). Columnas: característica, veredicto (Cumple/Parcial/No cumple), evidencia (cita textual breve del requisito), reescritura sugerida. Añade 4 filas para el conjunto si se evalúan varios requisitos; con uno solo, indica "no evaluable".
5. **Tabla ISO/IEC/IEEE 42010** (ver `references/iso-42010.md`): filas para stakeholders, preocupaciones, puntos de vista, vistas, correspondencias, justificación de decisiones, identificación de la entidad (sistema de interés). Columnas: elemento, ¿presente en los artefactos?, evidencia, brecha.
6. **Resumen y acciones**: veredicto global en 3 líneas y lista de acciones priorizadas (Alta/Media/Baja) con responsable sugerido (analista, arquitecto, QA) y el artefacto a corregir.
7. **Autoverificar** con la checklist.

## Formato de salida exacto
```
# Evaluación ISO: <RF-xx>
> Evaluación asistida; cotejar con el texto oficial de cada norma.
## Fuentes consultadas
## 1. ISO/IEC 25010:2023 (calidad del producto)
| Característica | ¿La toca? | Evidencia en criterios | ¿Verificable? | Brecha |
## 2. ISO/IEC/IEEE 29148 (requisitos)
| Característica | Veredicto | Evidencia | Reescritura sugerida |
## 3. ISO/IEC/IEEE 42010 (descripción de arquitectura)
| Elemento | ¿Presente? | Evidencia | Brecha |
## 4. Resumen
## 5. Acciones priorizadas
| # | Prioridad | Acción | Artefacto | Responsable |
```

## Reglas de juicio
- "Cumple" exige evidencia citada. Sin evidencia, el veredicto máximo es "Parcial".
- Un atributo de calidad sin número en los criterios es "No verificable".
- No inventes la existencia de un artefacto. Si no lo recibiste, es brecha.
- Las normas son de pago: no copies su texto; usa las references, que son resúmenes propios.

## Checklist de autoverificación
- [ ] Las tres tablas están completas, sin celdas vacías (usa "n/a" con motivo).
- [ ] Cada "Cumple" tiene evidencia concreta.
- [ ] Cada "No cumple"/"Parcial" de 29148 trae reescritura sugerida.
- [ ] Las nueve características de 25010 aparecen.
- [ ] Hay advertencia de cotejo con la norma oficial.
- [ ] Las acciones están priorizadas y apuntan a un artefacto.
- [ ] Se citan las páginas de la wiki usadas, o se declara que no hubo wiki.
