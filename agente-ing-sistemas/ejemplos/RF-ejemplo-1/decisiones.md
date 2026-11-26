# Decisiones de arquitectura: RF-01

## Resumen
El registro y el inicio de sesión se concentran en una API de acceso con una base de datos propia de usuarios. La seguridad se resuelve con tácticas de detectar, resistir y reaccionar.

## Supuestos
- Hay verificación de correo mediante un servicio externo (no está en el enunciado).
- Tecnología REST/JSON, hash con sal y token con expiración de 30 min (a confirmar con el equipo).
- Umbral de bloqueo: 5 intentos fallidos en 15 minutos (a confirmar).
- Nota sobre fuentes: la wiki aún no tiene páginas en `wiki/conceptos/`, así que no se cita ninguna. Se usó el corpus crudo: `raw/3-2-atributos-de-calidad-3.md`, diap. 21, que organiza las tácticas de seguridad en detectar ataques (detectores de intrusos), resistir ataques (autenticación, autorización, confidencialidad e integridad de datos, limitar exposición y acceso) y recuperarse (restauración, traza de auditoría). Cuando existan páginas de tácticas, citarlas aquí.

## Decisiones
| # | Decisión (patrón/táctica) | Atributo | Justificación | Fuente wiki |
|---|---|---|---|---|
| D1 | Autenticar actores (táctica: resistir ataques) con correo y contraseña en una API única | Seguridad | Un único punto de autenticación facilita auditar y proteger | `raw/3-2-atributos-de-calidad-3.md`, diap. 21 (autenticación) |
| D2 | Almacenar solo hashes con sal; nunca la contraseña | Seguridad | Limita el daño si se filtra la base de datos | `raw/3-2-atributos-de-calidad-3.md`, diap. 21 (confidencialidad de datos); el hash con sal en concreto es conocimiento general |
| D3 | Bloqueo temporal tras intentos fallidos (táctica: reaccionar ante ataques) | Seguridad | Frena fuerza bruta | conocimiento general |
| D4 | Token de sesión con expiración | Seguridad | Reduce la ventana de uso de un token robado | conocimiento general |
| D5 | Capas presentación, dominio, seguridad e infraestructura | Mantenibilidad | Aísla los componentes de seguridad para cambiarlos sin tocar el dominio | `raw/2-2-atributos-de-calidad-1.md`, diap. 12 (capas para modificabilidad); la partición concreta es conocimiento general |

## Riesgos y compromisos
- El bloqueo temporal puede usarse para denegar servicio a una cuenta ajena (compromiso entre seguridad y disponibilidad).
- El mensaje de error genérico protege contra enumeración de usuarios, pero reduce la ayuda al usuario legítimo.
