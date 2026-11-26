# MANI: extracto de SRS (MUESTRA)

> Documento sintético de muestra para probar los pipelines. No corresponde al SRS real de MANI.

## Alcance

MANI es un sistema ficticio de gestión de inventario. Permite registrar productos, movimientos de entrada y salida y consultar existencias por bodega.

## Requisitos funcionales

- RF-01: el sistema debe permitir crear, consultar, actualizar y eliminar productos.
- RF-02: el sistema debe registrar cada movimiento de inventario con fecha, cantidad y responsable.
- RF-03: el sistema debe emitir una alerta cuando la existencia baje del mínimo definido.

## Requisitos no funcionales

- RNF-01 (rendimiento): la consulta de existencias debe responder en menos de 2 segundos con 10.000 productos.
- RNF-02 (disponibilidad): disponibilidad mensual mínima de 99,5 %.
- RNF-03 (seguridad): toda operación de escritura requiere un usuario autenticado con rol autorizado.
