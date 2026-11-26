# language: es
# Escenario de calidad (seis componentes), seguridad: resistencia a fuerza bruta
# | Componente | Valor |
# | Fuente del estímulo | Atacante externo que automatiza intentos de inicio de sesión |
# | Estímulo | 6 intentos con contraseña incorrecta sobre la misma cuenta en 15 minutos |
# | Artefacto | API de acceso (servicio de autenticación) |
# | Entorno | Operación normal |
# | Respuesta | La cuenta se bloquea y el intento se registra |
# | Medida de la respuesta | Bloqueo desde el 5.º intento fallido, duración 15 minutos, 100 % de los intentos registrados |
# SUPUESTO: umbrales de 5 intentos, 15 minutos y 30 minutos de sesión; confirmar con el cliente.
@RF-01
Característica: Registro e inicio de sesión de usuario
  Como persona que usa MANI
  Quiero registrarme e iniciar sesión con correo y contraseña
  Para acceder a las funciones que exigen autenticación

  Antecedentes:
    Dado que el sistema está en operación normal

  @RF-01 @feliz
  Escenario: Registro exitoso
    Dado que no existe una cuenta con el correo "ana@ejemplo.com"
    Cuando envío el registro con correo "ana@ejemplo.com" y contraseña "Clave-Segura-2026"
    Entonces el sistema responde con código 201
    Y se crea la cuenta con la contraseña almacenada como hash con sal
    Y se envía un correo de verificación a "ana@ejemplo.com"

  @RF-01 @feliz
  Escenario: Inicio de sesión exitoso
    Dado que existe una cuenta verificada con el correo "ana@ejemplo.com"
    Cuando inicio sesión con correo "ana@ejemplo.com" y la contraseña correcta
    Entonces el sistema responde con código 200 y un token de sesión
    Y el token expira a los 30 minutos de inactividad

  @RF-01 @borde
  Esquema del escenario: Registro con contraseña fuera de los límites
    Cuando envío el registro con correo "ana@ejemplo.com" y contraseña de <longitud> caracteres
    Entonces el sistema responde con código <codigo>

    Ejemplos:
      | longitud | codigo |
      | 7        | 400    |
      | 8        | 201    |
      | 128      | 201    |
      | 129      | 400    |

  @RF-01 @borde
  Escenario: Registro con un correo ya registrado
    Dado que existe una cuenta con el correo "ana@ejemplo.com"
    Cuando envío el registro con correo "ana@ejemplo.com" y contraseña "Otra-Clave-2026"
    Entonces el sistema responde con código 409 y el mensaje "El correo ya está registrado"
    Y no se crea una segunda cuenta

  @RF-01 @error
  Esquema del escenario: Registro con correo inválido
    Cuando envío el registro con correo "<correo>" y contraseña "Clave-Segura-2026"
    Entonces el sistema responde con código 400 y el mensaje "Correo inválido"

    Ejemplos:
      | correo          |
      |                 |
      | sin-arroba      |
      | ana@            |
      | ana @ejemplo.co |

  @RF-01 @error
  Escenario: Inicio de sesión con contraseña incorrecta
    Dado que existe una cuenta verificada con el correo "ana@ejemplo.com"
    Cuando inicio sesión con correo "ana@ejemplo.com" y una contraseña incorrecta
    Entonces el sistema responde con código 401 y el mensaje "Credenciales inválidas"
    Y el mensaje es idéntico al de un correo inexistente

  @RF-01 @error
  Escenario: Inicio de sesión de una cuenta bloqueada
    Dado que la cuenta "ana@ejemplo.com" está bloqueada por intentos fallidos
    Cuando inicio sesión con la contraseña correcta
    Entonces el sistema responde con código 423 y el mensaje "Cuenta bloqueada temporalmente"
    Y no se emite ningún token

  @RF-01 @calidad @RNF-01-S
  Escenario: Resistencia a fuerza bruta
    Dado que existe una cuenta verificada con el correo "ana@ejemplo.com"
    Y el sistema está en operación normal
    Cuando un atacante envía 6 intentos con contraseña incorrecta en 15 minutos
    Entonces la cuenta queda bloqueada desde el 5.º intento fallido durante 15 minutos
    Y el 100 % de los intentos fallidos queda registrado con fecha y origen
