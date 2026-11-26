# language: es
# Escenario de calidad (seis componentes), rendimiento: tiempo de respuesta de la búsqueda
# | Componente | Valor |
# | Fuente del estímulo | 60 usuarios autenticados concurrentes |
# | Estímulo | Envían búsquedas por nombre o código de producto |
# | Artefacto | API de consulta con su caché y base de datos de inventario |
# | Entorno | Operación normal con un catálogo de 10000 productos |
# | Respuesta | El sistema devuelve la primera página de resultados |
# | Medida de la respuesta | Percentil 95 del tiempo de respuesta menor a 2 segundos; 0 % de errores por sobrecarga |
# SUPUESTO: 60 usuarios concurrentes, página de 20 resultados, caché con expiración de 60 s; confirmar con el cliente.
@RF-02
Característica: Búsqueda de existencias
  Como usuario autenticado de MANI
  Quiero buscar productos por nombre o código
  Para consultar su existencia por bodega

  Antecedentes:
    Dado que el catálogo contiene 10000 productos
    Y que he iniciado sesión como usuario autenticado

  @RF-02 @feliz
  Escenario: Búsqueda por nombre con coincidencias
    Dado que existe el producto "Tornillo 5mm" con 40 unidades en la bodega "Norte"
    Cuando busco "Tornillo"
    Entonces veo el producto "Tornillo 5mm"
    Y veo la existencia de 40 unidades en la bodega "Norte"

  @RF-02 @feliz
  Escenario: Búsqueda por código exacto
    Dado que existe el producto con código "TOR-005"
    Cuando busco "TOR-005"
    Entonces veo exactamente 1 resultado con el código "TOR-005"

  @RF-02 @borde
  Esquema del escenario: Búsqueda con textos límite
    Cuando busco "<texto>"
    Entonces el sistema responde con código <codigo>
    Y veo <cantidad> resultados

    Ejemplos:
      | texto                 | codigo | cantidad |
      | zzzzz                 | 200    | 0        |
      | a                     | 400    | 0        |
      | ab                    | 200    | 20       |

  @RF-02 @borde
  Escenario: Resultados paginados
    Dado que 45 productos coinciden con la búsqueda "Tornillo"
    Cuando busco "Tornillo" y solicito la página 3
    Entonces veo 5 resultados
    Y se indica que no hay más páginas

  @RF-02 @error
  Escenario: Búsqueda sin sesión
    Dado que mi sesión ha expirado
    Cuando busco "Tornillo"
    Entonces el sistema responde con código 401 y el mensaje "Sesión no válida"
    Y no se devuelven productos

  @RF-02 @error
  Escenario: Búsqueda con la caché caída
    Dado que la caché no está disponible
    Cuando busco "Tornillo"
    Entonces el sistema responde con código 200 con los resultados desde la base de datos
    Y el tiempo de respuesta es menor a 2 segundos

  @RF-02 @calidad @RNF-02-R
  Escenario: Tiempo de respuesta bajo carga normal
    Dado el sistema en operación normal con un catálogo de 10000 productos
    Y 60 usuarios autenticados concurrentes
    Cuando los usuarios envían búsquedas por nombre o código durante 10 minutos
    Entonces el sistema devuelve la primera página de resultados en cada búsqueda
    Y el percentil 95 del tiempo de respuesta es menor a 2 segundos
    Y el porcentaje de errores por sobrecarga es 0
