# Plantilla mínima: C4 con Structurizr DSL

Referencia de sintaxis: documentación oficial de Structurizr DSL. Valida con `structurizr/structurizr validate` (la imagen `structurizr/cli` está descontinuada).

## Esqueleto con contexto, contenedores, componentes y flujo dinámico
```
workspace "Nombre" "Descripción breve" {
    model {
        usuario = person "Usuario" "Rol que interactúa"
        externo = softwareSystem "Sistema externo" "Qué ofrece" "Externo"

        sistema = softwareSystem "Sistema" "Qué hace" {
            web = container "Aplicación web" "Interfaz" "SPA"
            api = container "API" "Lógica de negocio" "REST/JSON" {
                controlador = component "Controlador" "Recibe peticiones" "Capa de presentación"
                servicio = component "Servicio" "Reglas de negocio" "Capa de dominio"
            }
            bd = container "Base de datos" "Persistencia" "Relacional" "Base de datos"
        }

        usuario -> web "Usa" "HTTPS"
        web -> api "Invoca" "HTTPS/JSON"
        api -> bd "Lee y escribe" "SQL"
        api -> externo "Consulta" "HTTPS"
        controlador -> servicio "Delega"
    }

    views {
        systemContext sistema "Contexto" "Descripción de la vista" {
            include *
            autoLayout
        }
        container sistema "Contenedores" "Descripción de la vista" {
            include *
            autoLayout
        }
        component api "Componentes" "Descripción de la vista" {
            include *
            autoLayout
        }
        dynamic sistema "Flujo" "Flujo principal" {
            usuario -> web "1. Envía solicitud"
            web -> api "2. Invoca"
            api -> bd "3. Persiste"
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
```

## Reglas que evitan errores de validación
- Cada paso de `dynamic` debe corresponder a una relación declarada en el modelo con el mismo origen y destino.
- En una vista `dynamic` sobre un sistema, usa personas y contenedores (no mezcles componentes de contenedores distintos).
- Los identificadores no admiten espacios ni acentos; los nombres entre comillas sí.
- La etiqueta (último argumento de `container`/`softwareSystem`) se usa luego en `styles`.
- Evita declarar dos veces la misma relación origen-destino; combina el texto en una sola.
