# Plantillas mínimas PlantUML

Valida con `docker run --rm -v "$PWD":/data plantuml/plantuml -checkonly /data/<archivo>.puml`.

## Diagrama de paquetes
```
@startuml
title Paquetes: <RF-xx>
package "Presentación" {
  [Controlador]
}
package "Dominio" {
  [Servicio]
  [Entidad]
}
package "Infraestructura" {
  [Repositorio]
}
[Controlador] --> [Servicio]
[Servicio] --> [Entidad]
[Servicio] --> [Repositorio]
@enduml
```
Las dependencias deben ir de presentación hacia infraestructura; una flecha en sentido contrario es una violación a señalar.

## Diagrama de secuencia
```
@startuml
title Secuencia: <RF-xx> flujo principal
actor Usuario
participant "Aplicación web" as Web
participant "API" as Api
database "Base de datos" as BD

Usuario -> Web : envía solicitud
Web -> Api : POST /recurso
Api -> BD : consulta
BD --> Api : resultado
alt éxito
  Api --> Web : 200 con datos
  Web --> Usuario : muestra resultado
else error
  Api --> Web : 4xx con mensaje
  Web --> Usuario : muestra error
end
@enduml
```

## Reglas
- Todo archivo inicia con `@startuml` y termina con `@enduml`.
- Alias sin espacios (`as Api`); texto visible entre comillas.
- `alt`/`else`/`end`, `loop`/`end`, `opt`/`end` deben cerrarse.
- Flecha sólida `->` para llamada, punteada `-->` para respuesta.
