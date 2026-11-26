# Decisiones de arquitectura: RF-01

## Resumen
El registro y el inicio de sesión se concentran en una API de acceso con una base de datos propia de usuarios. La seguridad se resuelve con tácticas de detectar, resistir y reaccionar.

## Supuestos
- Hay verificación de correo mediante un servicio externo (no está en el enunciado).
- Tecnología REST/JSON, hash con sal y token con expiración de 30 min (a confirmar con el equipo).
- Umbral de bloqueo: 5 intentos fallidos en 15 minutos (a confirmar).
- Nota sobre fuentes: la wiki aún no tiene páginas en `wiki/conceptos/`; se usó la muestra `raw/clase-03-atributos-calidad-muestra.md`, que lista las tácticas de seguridad (autenticación, autorización, cifrado). Cuando existan páginas de tácticas, citarlas aquí.

## Decisiones
| # | Decisión (patrón/táctica) | Atributo | Justificación | Fuente wiki |
|---|---|---|---|---|
| D1 | Autenticar actores (táctica: resistir ataques) con correo y contraseña en una API única | Seguridad | Un único punto de autenticación facilita auditar y proteger | `raw/clase-03-atributos-calidad-muestra.md` |
| D2 | Almacenar solo hashes con sal; nunca la contraseña | Seguridad | Limita el daño si se filtra la base de datos | `raw/clase-03-atributos-calidad-muestra.md` (cifrado) |
| D3 | Bloqueo temporal tras intentos fallidos (táctica: reaccionar ante ataques) | Seguridad | Frena fuerza bruta | conocimiento general |
| D4 | Token de sesión con expiración | Seguridad | Reduce la ventana de uso de un token robado | conocimiento general |
| D5 | Capas presentación, dominio, seguridad e infraestructura | Mantenibilidad | Aísla los componentes de seguridad para cambiarlos sin tocar el dominio | conocimiento general |

## Riesgos y compromisos
- El bloqueo temporal puede usarse para denegar servicio a una cuenta ajena (compromiso entre seguridad y disponibilidad).
- El mensaje de error genérico protege contra enumeración de usuarios, pero reduce la ayuda al usuario legítimo.
