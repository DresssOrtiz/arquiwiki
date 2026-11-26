workspace "MANI: RF-01 Registro e inicio de sesión" "Ejemplo generado con la skill modelar" {

    model {
        usuario = person "Usuario" "Persona que se registra e inicia sesión"
        correo = softwareSystem "Servicio de correo" "Envía el mensaje de verificación de cuenta" "Externo"

        mani = softwareSystem "MANI" "Plataforma académica del equipo" {
            web = container "Aplicación web" "Formularios de registro e inicio de sesión" "SPA"
            api = container "API de acceso" "Registro, autenticación y emisión de sesiones" "REST/JSON" {
                controlador = component "Controlador de autenticación" "Recibe y valida las peticiones" "Capa de presentación"
                servicio = component "Servicio de autenticación" "Reglas de registro, intentos fallidos y bloqueo" "Capa de dominio"
                hasher = component "Cifrador de contraseñas" "Calcula y compara hashes con sal" "Componente de seguridad"
                emisor = component "Emisor de sesiones" "Crea y valida tokens con expiración" "Componente de seguridad"
                repositorio = component "Repositorio de usuarios" "Acceso a datos de usuarios" "Capa de infraestructura"
            }
            bd = container "Base de datos de usuarios" "Usuarios, hashes, contador de intentos" "Relacional" "Base de datos"
        }

        usuario -> web "Se registra e inicia sesión" "HTTPS"
        web -> api "Envía credenciales" "HTTPS/JSON"
        api -> bd "Lee y escribe usuarios" "SQL"
        api -> correo "Solicita correo de verificación" "SMTP/HTTPS"

        controlador -> servicio "Delega"
        servicio -> hasher "Cifra y compara contraseñas"
        servicio -> emisor "Pide token de sesión"
        servicio -> repositorio "Consulta y guarda usuarios"
        repositorio -> bd "Lee y escribe" "SQL"
    }

    views {
        systemContext mani "Contexto" "Actores y sistemas externos de MANI para RF-01" {
            include *
            autoLayout
        }

        container mani "Contenedores" "Contenedores que participan en RF-01" {
            include *
            autoLayout
        }

        component api "Componentes" "Componentes internos de la API de acceso" {
            include *
            autoLayout
        }

        dynamic mani "FlujoInicioSesion" "Inicio de sesión exitoso" {
            usuario -> web "1. Envía correo y contraseña"
            web -> api "2. Envía credenciales"
            api -> bd "3. Lee usuario y registra intento"
            autoLayout
        }

        styles {
            element "Person" {
                shape Person
            }
            element "Base de datos" {
                shape Cylinder
            }
            element "Externo" {
                background #999999
            }
        }
    }
}
