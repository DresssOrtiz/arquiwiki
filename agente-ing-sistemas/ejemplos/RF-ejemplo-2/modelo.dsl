workspace "MANI: RF-02 Búsqueda de existencias" "Ejemplo generado con la skill modelar" {

    model {
        usuario = person "Usuario" "Persona autenticada que consulta existencias"
        idp = softwareSystem "Proveedor de identidad" "Valida la sesión del usuario" "Externo"

        mani = softwareSystem "MANI" "Plataforma académica del equipo" {
            web = container "Aplicación web" "Pantalla de búsqueda y resultados paginados" "SPA"
            api = container "API de consulta" "Búsqueda de productos y existencias" "REST/JSON" {
                controlador = component "Controlador de búsqueda" "Valida parámetros y pagina" "Capa de presentación"
                servicio = component "Servicio de búsqueda" "Orquesta caché y consulta" "Capa de dominio"
                cache = component "Adaptador de caché" "Lee y escribe resultados frecuentes" "Capa de infraestructura"
                repositorio = component "Repositorio de existencias" "Consultas indexadas" "Capa de infraestructura"
            }
            cacheStore = container "Caché" "Resultados de búsquedas frecuentes, expiran a los 60 s" "Almacén en memoria" "Base de datos"
            bd = container "Base de datos de inventario" "Productos y existencias por bodega, con índices" "Relacional" "Base de datos"
        }

        usuario -> web "Busca productos" "HTTPS"
        web -> api "Solicita búsqueda paginada" "HTTPS/JSON"
        api -> idp "Valida la sesión" "HTTPS"
        api -> cacheStore "Lee y escribe resultados" "TCP"
        api -> bd "Consulta productos y existencias" "SQL"

        controlador -> servicio "Delega"
        servicio -> cache "Consulta la caché primero"
        servicio -> repositorio "Consulta en caso de fallo de caché"
        cache -> cacheStore "Lee y escribe" "TCP"
        repositorio -> bd "Consulta indexada" "SQL"
    }

    views {
        systemContext mani "Contexto" "Actores y sistemas externos de MANI para RF-02" {
            include *
            autoLayout
        }

        container mani "Contenedores" "Contenedores que participan en RF-02" {
            include *
            autoLayout
        }

        component api "Componentes" "Componentes internos de la API de consulta" {
            include *
            autoLayout
        }

        dynamic mani "FlujoBusqueda" "Búsqueda con fallo de caché" {
            usuario -> web "1. Escribe el texto de búsqueda"
            web -> api "2. Solicita búsqueda paginada"
            api -> idp "3. Valida la sesión"
            api -> cacheStore "4. Busca en caché"
            api -> bd "5. Consulta por índice si no hay caché"
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
