# Evaluación ISO: RF-02 y RNF-02-R

> Evaluación asistida; cotejar con el texto oficial de cada norma. Requisito de ejemplo; reemplazar por el RF real del SRS de MANI.

## Fuentes consultadas
- Wiki: sin páginas en `wiki/conceptos/` al momento de generar el ejemplo, por lo que no se cita ninguna. Se usaron las references de la skill y, como fuente del corpus, `raw/3-2-atributos-de-calidad-3.md`, diap. 19 (tácticas de eficiencia de ejecución). Wiki no disponible para citas definitivas.
- Extracto de SRS: `kb-wiki/muestras/mani-srs-muestra.md` (extracto sintético de SRS, no es del corpus del curso).
- Artefactos evaluados: `requisito.md`, `modelo.dsl`, `paquetes.puml`, `secuencia.puml`, `decisiones.md`, `criterios.feature`.

## 1. ISO/IEC 25010:2023 (calidad del producto)
| Característica | ¿La toca? | Evidencia en criterios | ¿Verificable? | Brecha |
|---|---|---|---|---|
| Idoneidad funcional | Sí | Búsqueda por nombre, por código, paginación y casos vacíos | Sí | No se define si la búsqueda es por prefijo, por subcadena o tolerante a tildes. |
| Eficiencia de desempeño | Sí | Escenario `@calidad`: p95 < 2 s con 60 usuarios y 10000 productos | Sí | Falta uso de recursos (CPU, memoria de la caché) y capacidad máxima (cuántos usuarios antes de degradar). |
| Compatibilidad | Indirecta | Ninguna | No | Dependencia del proveedor de identidad sin criterio de fallo ni de contrato. |
| Capacidad de interacción | Indirecta | Mensajes de error y paginación | Parcial | Sin criterio de usabilidad (p. ej., mensaje cuando no hay resultados). |
| Fiabilidad | Sí | Escenario con caché caída | Parcial | Sin criterio de disponibilidad ni de comportamiento si cae la base de datos. |
| Seguridad | Sí | Escenario de sesión expirada (401) | Parcial | No hay criterio de autorización por bodega (¿todo usuario ve todas las bodegas?). |
| Mantenibilidad | Indirecta | Ninguna (capas en `paquetes.puml`) | No | Sin criterios sobre pruebas ni cambio del almacén de datos. |
| Flexibilidad | Indirecta | Ninguna | No | Escalabilidad por encima de 60 usuarios no está definida. |
| Protección (safety) | No | n/a | n/a | Ninguna. |

## 2. ISO/IEC/IEEE 29148 (requisitos)
Se evalúa el RF-02 y el RNF-02-R. Conjunto: no evaluable con solo dos requisitos.

| Característica | Veredicto | Evidencia | Reescritura sugerida |
|---|---|---|---|
| Necesario | Cumple | RNF-01 de `kb-wiki/muestras/mani-srs-muestra.md` (extracto sintético) fija el mismo objetivo de rendimiento | n/a |
| Apropiado | Cumple | No impone caché ni base de datos | n/a |
| Inequívoco | Parcial | RF-02: "buscar por nombre o código" no define el tipo de coincidencia | "El sistema debe devolver los productos cuyo nombre contenga el texto buscado (sin distinguir mayúsculas) o cuyo código coincida exactamente." |
| Completo | Parcial | RNF-02-R no indica duración de la medición ni qué operación se mide | "Durante 10 minutos de carga sostenida, la búsqueda debe cumplir p95 < 2 s." |
| Singular | No cumple | RF-02 combina buscar por dos campos y consultar existencia por bodega | Separar: RF-02a (buscar por nombre o código) y RF-02b (consultar existencia por bodega). |
| Factible | Cumple | 10.000 filas con índices y caché es una carga modesta | n/a |
| Verificable | Cumple | RNF-02-R trae percentil, tiempo, concurrencia y volumen | n/a |
| Correcto | Parcial | La cifra de 60 usuarios no tiene fuente | Registrar interesado y validar la concurrencia pico real. |
| Conforme | Parcial | Tiene identificador; RF-02 omite la condición de activación | "Cuando un usuario autenticado envíe un texto de búsqueda, el sistema debe devolver los productos que coincidan, con su existencia por bodega." |

## 3. ISO/IEC/IEEE 42010 (descripción de arquitectura)
| Elemento | ¿Presente? | Evidencia | Brecha |
|---|---|---|---|
| Entidad de interés | Presente | Sistema "MANI" en `modelo.dsl` | Ninguna |
| Stakeholders | Parcial | Solo "Usuario" y el proveedor de identidad | Faltan operador de la plataforma y responsable del inventario. |
| Preocupaciones | Parcial | Rendimiento explícito; seguridad implícita | No hay lista por stakeholder. |
| Puntos de vista | Parcial | C4 y UML usados | No se declara qué preocupación cubre cada uno. |
| Vistas | Presente | Cuatro vistas en el DSL y dos diagramas UML | Ninguna |
| Correspondencias | Presente | Los componentes del DSL aparecen con el mismo nombre en `paquetes.puml` y `secuencia.puml` (salvo `Cliente de identidad`, solo en paquetes) | Falta tabla explícita; `Cliente de identidad` no existe en el DSL. |
| Justificación de decisiones | Parcial | `decisiones.md` con cinco decisiones y riesgos | Sin alternativas descartadas (p. ej., motor de búsqueda dedicado). |
| Conformidad | Parcial | Rendimiento cubierto por la vista dinámica y la secuencia | Ninguna vista muestra la carga ni el dimensionamiento. |

## 4. Resumen
El requisito de rendimiento es el más sólido del paquete: tiene medida, concurrencia y volumen, y el escenario de calidad lo hace verificable. El requisito funcional es ambiguo y no singular. La arquitectura atiende el atributo con caché, índices y paginación, justificados, pero la descripción carece de stakeholders completos y alternativas descartadas. La cifra de concurrencia sigue sin fuente.

## 5. Acciones priorizadas
| # | Prioridad | Acción | Artefacto | Responsable |
|---|---|---|---|---|
| 1 | Alta | Separar RF-02 en dos y precisar el tipo de coincidencia | `requisito.md` | Analista |
| 2 | Alta | Validar con el cliente la concurrencia (60) y la antigüedad aceptable de la caché (60 s) | `requisito.md`, `decisiones.md` | Analista |
| 3 | Media | Añadir criterios de autorización por bodega y de caída de la base de datos | `criterios.feature` | QA |
| 4 | Media | Declarar stakeholders, preocupaciones y tabla de correspondencias | `decisiones.md` | Arquitecto |
| 5 | Baja | Documentar alternativas (motor de búsqueda dedicado) y límites de capacidad | `decisiones.md` | Arquitecto |
