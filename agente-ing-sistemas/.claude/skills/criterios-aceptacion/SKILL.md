---
name: criterios-aceptacion
description: Redacta criterios de aceptación en Gherkin en español (Dado/Cuando/Entonces) con trazabilidad al requisito y, si hay atributo de calidad, un escenario de calidad de seis componentes. Úsala cuando el usuario pida criterios de aceptación, escenarios de prueba o historias verificables para un requisito.
---

# Skill: criterios-aceptacion

Convierte un requisito en un archivo `criterios.feature` verificable, medible y trazable.

## Entrada
Requisito con identificador (`RF-xx`/`RNF-xx`). Opcional: modelos de la skill `modelar` para reutilizar nombres de actores y componentes.

## Pasos
1. **Descomponer el requisito** en comportamientos observables: un comportamiento, un escenario. Lista actores, precondiciones, datos y reglas de negocio.
2. **Cubrir tres familias** (mínimo un escenario de cada una):
   - Camino feliz.
   - Bordes: límites de datos (vacío, máximo, mínimo, caracteres especiales), estados límite, concurrencia.
   - Errores: entrada inválida, falta de permisos, dependencia caída.
3. **Hacer cada criterio medible**: sustituye adjetivos ("rápido", "seguro", "muchos") por cifras, códigos o mensajes exactos. Si el requisito no da el número, propón uno marcado como `# SUPUESTO:` para que el cliente lo confirme.
4. **Si hay atributo de calidad**, consulta la wiki (MCP `arquiwiki`: `search_notes` "escenarios de calidad" y el atributo) y añade el escenario de calidad: tabla de seis componentes más su traducción a Gherkin (ver `references/gherkin.md`). Si el MCP no está disponible, usa conocimiento general y decláralo en un comentario del archivo.
5. **Usar `Esquema del escenario` con `Ejemplos`** cuando varios casos comparten estructura y cambian solo los datos.
6. **Etiquetar**: cada escenario con `@RF-xx` (o `@RNF-xx`) y un tipo: `@feliz`, `@borde`, `@error`, `@calidad`.
7. **Autoverificar** con la checklist.

## Formato de salida exacto
Archivo `criterios.feature`:
```
# language: es
@RF-xx
Característica: <título del requisito>
  <Como/Quiero/Para, una línea cada uno>

  Antecedentes:
    Dado ...

  @RF-xx @feliz
  Escenario: ...
    Dado ...
    Cuando ...
    Entonces ...
    Y ...
```
Antes de la característica, un comentario con la tabla del escenario de calidad si aplica:
```
# Escenario de calidad (seis componentes)
# | Componente | Valor |
# | Fuente del estímulo | ... |
# | Estímulo | ... |
# | Artefacto | ... |
# | Entorno | ... |
# | Respuesta | ... |
# | Medida de la respuesta | ... |
```

## Reglas de redacción
- `Dado` describe estado, `Cuando` una única acción, `Entonces` un resultado observable. `Y`/`Pero` continúan el paso anterior.
- Un `Cuando` por escenario. Sin detalles de UI innecesarios (ni "hace clic en el botón azul").
- Datos concretos entre comillas; mensajes de error literales.
- No dependas del orden de ejecución entre escenarios.

## Checklist de autoverificación
- [ ] Empieza con `# language: es` y usa palabras clave en español.
- [ ] Hay escenarios feliz, borde y error.
- [ ] Ningún `Entonces` contiene adjetivos sin número ("rápido", "adecuado").
- [ ] Todo escenario lleva `@RF-xx` y un tipo.
- [ ] Hay `Esquema del escenario` con `Ejemplos` donde se repite estructura.
- [ ] El escenario de calidad (si aplica) tiene los seis componentes y medida numérica.
- [ ] Los supuestos de cifras están marcados `# SUPUESTO:`.
- [ ] El archivo se puede cargar con un analizador Gherkin (sintaxis y sangría correctas).
