---
name: modelar
description: Produce modelos de arquitectura (C4 en Structurizr DSL, paquetes y secuencia en PlantUML) y una nota de decisiones a partir de un requisito. Úsala cuando el usuario pida modelar, diagramar o diseñar la arquitectura de un requisito funcional o no funcional.
---

# Skill: modelar

Convierte un requisito en artefactos de modelado sintácticamente válidos y justificados con la wiki del curso.

## Entrada
Un requisito (texto o ruta a archivo) con identificador (`RF-xx` o `RNF-xx`). Si falta el identificador, pídelo o asigna uno provisional y decláralo.

## Pasos
1. **Leer el requisito** y extraer: actores (personas), sistemas externos, datos principales y atributo de calidad si lo hay.
2. **Identificar elementos C4**: un sistema de software (el que se modela), sus contenedores (aplicaciones, APIs, bases de datos, colas) y, solo para el contenedor central del flujo, sus componentes relevantes. No inventes tecnología sin decirlo: marca como "supuesto" lo que no esté en el requisito.
3. **Consultar la wiki** (MCP `arquiwiki`): `search_notes` con el atributo de calidad y el dominio (p. ej. "tácticas rendimiento") y `read_note` sobre las 1 a 3 páginas más relevantes de `wiki/conceptos/`. Si el MCP no responde, continúa con conocimiento general y escribe en la nota de decisiones: "Wiki no disponible; decisiones basadas en conocimiento general, sin cita".
4. **Elegir tácticas y patrones** que respondan al atributo de calidad. Cada uno entra a la nota de decisiones con justificación y cita.
5. **Escribir los artefactos** (plantillas mínimas en `references/`):
   - `modelo.dsl` (Structurizr DSL; ver `references/c4-structurizr.md`): workspace con vistas `systemContext` y `container`; si el requisito es un flujo, añade una vista `dynamic`; añade `component` solo si aporta.
   - `paquetes.puml` (PlantUML, diagrama de paquetes; ver `references/plantuml.md`): paquetes por capa o módulo y sus dependencias.
   - `secuencia.puml` (PlantUML, secuencia del flujo principal, con al menos una alternativa de error mediante `alt`).
   - `decisiones.md` (nota breve, formato abajo).
6. **Autoverificar** con la checklist y, si hay Docker, validar.

## Convenciones
- Mismos nombres de elementos en DSL, paquetes y secuencia (coherencia entre vistas).
- Identificadores del DSL en minúsculas, sin espacios ni acentos; nombres visibles en español.
- Cada vista con `title` o descripción; `autoLayout` en todas.
- Un diagrama, un propósito: no mezclar niveles C4 en una vista.

## Formato de `decisiones.md`
```
# Decisiones de arquitectura: <RF-xx>
## Resumen (2-3 líneas)
## Supuestos
- ...
## Decisiones
| # | Decisión (patrón/táctica) | Atributo | Justificación | Fuente wiki |
|---|---|---|---|---|
| D1 | ... | ... | ... | `wiki/conceptos/<pagina>.md` o "conocimiento general" |
## Riesgos y compromisos (trade-offs)
```

## Validación (si Docker está disponible)
```
docker run --rm -v "$PWD":/usr/local/structurizr structurizr/structurizr validate -workspace modelo.dsl
docker run --rm -i plantuml/plantuml -syntax -pipe < paquetes.puml
docker run --rm -i plantuml/plantuml -syntax -pipe < secuencia.puml
```
- Structurizr: sin salida y código 0 significa válido; un error imprime la línea. La imagen `structurizr/cli` está descontinuada (solo muestra un aviso y no valida); usa `structurizr/structurizr`.
- PlantUML: `-syntax` imprime el tipo de diagrama (`SEQUENCE`, `DESCRIPTION`) si es válido y nada si hay error. `-checkonly` no detecta todos los errores.
Si Docker no está disponible, dilo en la respuesta y revisa a mano la sintaxis contra las plantillas. No dejes archivos generados.

## Checklist de autoverificación
- [ ] El DSL define actores, sistema, contenedores y sistemas externos del requisito.
- [ ] Existen las vistas `systemContext` y `container` (y `dynamic` si hay flujo).
- [ ] Todas las relaciones tienen descripción; las de contenedores, tecnología o protocolo.
- [ ] `paquetes.puml` y `secuencia.puml` usan los mismos nombres que el DSL.
- [ ] La secuencia cubre camino feliz y al menos un error.
- [ ] Cada decisión tiene justificación y fuente (o declara que no hubo wiki).
- [ ] Los supuestos están listados, no escondidos en los diagramas.
- [ ] Los archivos pasan la validación o se declaró que no se pudo validar.
