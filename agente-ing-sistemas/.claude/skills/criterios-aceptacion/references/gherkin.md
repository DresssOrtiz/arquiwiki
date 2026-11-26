# Referencia Gherkin en español

## Palabras clave (`# language: es`)
| Concepto | Palabra |
|---|---|
| Característica | `Característica` |
| Contexto común | `Antecedentes` |
| Caso | `Escenario` |
| Caso parametrizado | `Esquema del escenario` |
| Tabla de datos del esquema | `Ejemplos` |
| Pasos | `Dado`, `Cuando`, `Entonces`, `Y`, `Pero` |

Las variables del esquema van entre `<ángulos>` y deben coincidir con los encabezados de `Ejemplos`.

## Ejemplo mínimo
```
# language: es
@RF-00
Característica: Búsqueda de elementos
  Como usuario
  Quiero buscar por nombre
  Para encontrar rápidamente lo que necesito

  Antecedentes:
    Dado que existen 3 elementos registrados

  @RF-00 @feliz
  Escenario: Búsqueda con coincidencia
    Cuando busco "alfa"
    Entonces veo 1 resultado
    Y el resultado se muestra en menos de 2 segundos

  @RF-00 @borde
  Esquema del escenario: Búsqueda con textos límite
    Cuando busco "<texto>"
    Entonces veo <cantidad> resultados

    Ejemplos:
      | texto | cantidad |
      |       | 0        |
      | zzz   | 0        |
```

## Escenario de calidad: de la tabla a Gherkin
Los seis componentes del escenario de calidad se trasladan así:

| Componente | Paso Gherkin |
|---|---|
| Entorno | `Dado` (condiciones de operación) |
| Artefacto | `Dado` (el elemento bajo prueba) |
| Fuente del estímulo | sujeto del `Cuando` |
| Estímulo | verbo del `Cuando` |
| Respuesta | primer `Entonces` |
| Medida de la respuesta | `Y` con número y unidad (percentil, tiempo, porcentaje) |

Ejemplo (rendimiento):
```
@RNF-00 @calidad
Escenario: Consulta bajo carga normal
  Dado el sistema en operación normal con 60 usuarios concurrentes
  Y el catálogo con 10000 elementos
  Cuando los usuarios consultan el catálogo
  Entonces el sistema devuelve los resultados
  Y el percentil 95 del tiempo de respuesta es menor a 2 segundos
```

## Medibilidad: de vago a verificable
| Vago | Verificable |
|---|---|
| "responde rápido" | "p95 < 2 s con 60 usuarios concurrentes" |
| "es seguro" | "bloquea la cuenta tras 5 intentos fallidos en 10 minutos" |
| "maneja errores" | "devuelve 400 con el mensaje 'Correo inválido'" |
