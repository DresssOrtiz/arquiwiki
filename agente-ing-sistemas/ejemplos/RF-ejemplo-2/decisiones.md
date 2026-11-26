# Decisiones de arquitectura: RF-02 y RNF-02-R

## Resumen
La búsqueda se atiende desde una API de consulta que lee primero de una caché y, si falla, consulta una base de datos con índices. La respuesta se pagina para acotar el trabajo por petición.

## Supuestos
- 60 usuarios concurrentes y 10.000 productos (cifras del requisito; la concurrencia es supuesto del ejemplo).
- La autenticación se valida contra un proveedor de identidad externo.
- Caché en memoria con expiración de 60 s; se acepta que la existencia mostrada pueda tener hasta 60 s de antigüedad (a confirmar con el cliente).
- Nota sobre fuentes: la wiki aún no tiene páginas en `wiki/conceptos/`, así que no se cita ninguna. Se usó el corpus crudo: `raw/3-2-atributos-de-calidad-3.md`, diap. 19, que clasifica las tácticas de eficiencia de ejecución en demanda de recursos (mejorar la eficiencia computacional, reducir sobrecarga, manejar la tasa de eventos), gestión de recursos (concurrencia, réplicas, aumentar recursos) y arbitraje de recursos (políticas de planificación). La caché y la paginación no aparecen nombradas en la diapositiva; se ubican en esas categorías por interpretación. Cuando existan páginas de tácticas, citarlas aquí.

## Decisiones
| # | Decisión (patrón/táctica) | Atributo | Justificación | Fuente wiki |
|---|---|---|---|---|
| D1 | Caché de resultados frecuentes (táctica: gestionar recursos) | Rendimiento | Evita consultar la base de datos en búsquedas repetidas | `raw/3-2-atributos-de-calidad-3.md`, diap. 19 (gestión de recursos, réplicas); la caché en sí es conocimiento general |
| D2 | Índices en nombre y código de producto | Rendimiento | La consulta por índice mantiene el tiempo estable con 10.000 filas | conocimiento general |
| D3 | Paginación de resultados (táctica: controlar la demanda de recursos) | Rendimiento | Limita datos por petición y tamaño de respuesta | `raw/3-2-atributos-de-calidad-3.md`, diap. 19 (demanda de recursos, reducir sobrecarga); la paginación en sí es conocimiento general |
| D4 | Validar la sesión con un proveedor externo antes de buscar | Seguridad | Solo usuarios autenticados consultan (RNF-03 del extracto de SRS) | `kb-wiki/muestras/mani-srs-muestra.md` (extracto sintético de SRS, no es del corpus del curso) |
| D5 | Patrón repositorio entre dominio e infraestructura | Mantenibilidad | Permite cambiar el almacén sin tocar el servicio de búsqueda | conocimiento general |

## Riesgos y compromisos
- La caché mejora el tiempo pero introduce datos de hasta 60 s de antigüedad (consistencia frente a rendimiento).
- Un fallo de la caché degrada al camino con base de datos; el tiempo en ese camino debe cumplir también la medida (se prueba en el escenario de calidad).
- El proveedor de identidad externo agrega latencia y una dependencia; conviene medir su aporte al p95.
