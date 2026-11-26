# 3.1 Atributos de Calidad 2

> Fuente: `3.1 Atributos de Calidad 2.pdf` · 22 diapositivas · convertido con pdftotext el 2026-11-25. Texto extraído automáticamente: verificar contra el PDF.
> Se eliminó el pie repetido: "Andrés Armando Sánchez Martín"

## Diapositiva 1

(1306)
ARQUITECTURA DE SOFTWARE

3.1 Atributos de Calidad 2

asanchez-m@javeriana.edu.co - 3057642728  Andrés Armando Sánchez Martín – marzo de 2022

## Diapositiva 2

Agenda

 Atributos de Calidad
 Escenarios de Calidad
 Métricas de Calidad
 Diseño Centrado en Atributos de Calidad

2

## Diapositiva 3

ATRIBUTOS DE CALIDAD

“Los atributos de calidad son las expectativas de usuario, en general implícitas, de cuán bien
funcionará un producto.” - Software Requirements: 3rd Edition (Wiegers, Betty, 2013)
Performance / Rendimiento  Idoneidad Funcional

Eficiencia de ejecución
Escalabilidad
Compatibilidad
Modificabilidad
Usabilidad
Interoperabilidad  ISO/IEC
Confiabilidad
25000:2014
Seguridad
Seguridad
Disponibilidad  Mantenibilidad
Integración  Portabilidad
3

## Diapositiva 4

ATRIBUTOS DE CALIDAD

 Los atributos de calidad cualifican la funcionalidad
 Si un requisito functional fuese "cuando el usuario pulse el botón verde, un diálogo con opciones
aparece“ entonces:
 Un AC de rendimiento describiría la velocidad a la que debe aparecer

 Un AC de disponibilidad describiría cuándo podría fallar esta opción o con qué frecuencia sería reparada
 Un AC de usabilidad describiría cómo de fácil es aprender esta función

 Los atributos de calidad sí influyen en la arquitectura
 La calidad es el grado en que un Sistema satisfice las necesidades declaradas o implícitas de
las personas interesadas proporcionando valor
 Grado (no Booleano)

4
 Calidad = Encaje en un propósito (necesidades de stakeholders)
 Satisfacer requisitos (declarados o implícitos) - Proporcionar valor

## Diapositiva 5

ESCENARIO DE CALIDAD

 Describe un estímulo de un Sistema y una respuesta medible a dicho estímulo
 Estímulo = evento iniciado por una persona o sistema
 El estímulo genera una respuesta

 Debe ser medible
 La respuesta debe ser visible externamente y medible

5

## Diapositiva 6

ESCENARIO DE CALIDAD: COMPONENTES

 Fuente: Persona o Sistema que inicia el estímulo  Medida de respuesta: Criterio de éxito para el
escenario
 Estímulo: Evento que requiere que responda el
sistema   Debe ser específico y medible

 Artefacto: Parte del sistema o el sistema   Entorno: Circunstancias operativas
completo   Siempre debe ser definido (incluso si es
 Respuesta: Acción visible externamente  "normal")

6

## Diapositiva 7

ESCENARIO DE CALIDAD: TIPOS

Escenarios de uso
- El Sistema es utilizado (cualquier caso de uso o función del Sistema que se ejecuta)

- Describe cómo se comporta el Sistema en dichos casos
- Tiempo de ejecución, velocidad de respuesta, consume de memoria, throughput,...
Escenarios de cambio (o modificación)
- Cambio en cualquier componente dentro del Sistema, en entorno o la infraestructura
operacional
Escenarios de fallo:
7
- Alguna parte del Sistema, infraestructura o entorno falla

## Diapositiva 8

ESCENARIO DE CALIDAD: EJEMPLO

8

## Diapositiva 9

ESCENARIO DE CALIDAD: EJEMPLO DISPONIBILIDAD

9

## Diapositiva 10

ESCENARIO DE CALIDAD: PRIORIZACIÓN

 2 valores (Low/Medium/High)   Cómo es de importante para el éxito (cliente)
Ejemplo:   Cómo de difícil es de alcanzar (arquitecto)

Ref AC  Escenario  Prioridad

1  Disponibilidad  Cuando la base de datos no responda, el Sistema debería registrar el fallo en el  High, High
log y responder con datos anteriores durante 3 seg.
2  Disponibilidad  Un usuario que busca elementos de tipo X recibe una lista de Xs el 99% del  High, Medium
tiempo como media a la largo del año
3  Escalabilidad  Nuevos servidores pueden ser añadidos durante la ventana de mantenimiento  Low, Low
(en menos de 7 horas)
4  Rendimiento  Un usuario puede ver los resultados de búsqueda en menos de 5 segundos  High, High
cuando el Sistema tiene una carga de 2 búsquedas por seg
10  5  Fiabilidad  Las actualizaciones a elementos externos de tipo X deberían reflejarse en la  Low, Medium
aplicación dentro de 24 horas del cambio

## Diapositiva 11

MÉTRICAS DE CALIDAD:
¿CÓMO SABER SI MEJORAMOS?

Si no se mide

No se controla

Si no se controla
11
No se mejora

## Diapositiva 12

MÉTRICAS DE CALIDAD

 Los escenarios de AC requieren   Definiciones muy diversas
medir respuestas   No hay definiciones aceptadas
universalmente
 Problemas habituales:
 Demasiado compuestos

 Muchos AC tienen significados vagos
 Normalmente, un AC está compuesto de
 Ejemplo: desplegabilidad, escalabilidad  varias características

Según el
contexto

Métricas de  Métricas de  Métricas de
12
Proceso  Proyecto  Producto

## Diapositiva 13

MÉTRICAS DE ATRIBUTOS DE CALIDAD: PROCESO

Proceso de
Ingeniería de  Recopilación  • Métricas
Software  de datos

Proyecto de
Software  Calculo de  • Métricas
métricas

Producto de
Software  Evaluación  • Indicadores
13
de métricas

## Diapositiva 14

MÉTRICAS DE ATRIBUTOS DE CALIDAD

Intentar medir de forma objetiva aspectos de la calidad
Numerosas métricas para diferentes aspectos  Valores Absolutos  Seguridad
Medidas
Operacionales
Valores y modelos

estadísticos

Análisis  Estructura
algorítmico  modulas
Medidas
Métricas
Estructurales
Complejidad

Testeabilidad  Agilidad  Usabilidad
Medidas de
14  Procesos
Desplegabilidad  Mantenibilidad

## Diapositiva 15

MÉTRICAS DE ATRIBUTOS DE CALIDAD: EJEMPLOS
Numero de  Grado de
errores  integridad
Medidas
Operacionales
Porcentaje de  Numero de
disponibilidad  usuarios activos

Reducción de  Puntos de
grafo  optimización
Medidas
Métricas
Estructurales
Tiempo de
función

Numero de  Aceptación de
líneas  usuario
Medidas de
Procesos
15
Tiempo de
despliegue

## Diapositiva 16

DISEÑO CENTRADO EN ATRIBUTOS DE CALIDAD (ADD)

El método ADD es un enfoque a la definición de una
arquitectura de software en el que se basa el proceso de diseño
de los requisitos del software de atributos de calidad. ADD es
un proceso de diseño recursivo que descompone un sistema o

elemento del sistema mediante la aplicación de tácticas
arquitectónicas y los patrones que satisfacen los drivers.
ADD sigue esencialmente el ciclo “Plan, Do, and Check”:
 Plan: Los atributos de calidad y las restricciones de diseño
son consideradas para seleccionar qué tipos de elementos
se utilizan en la arquitectura.
 Do: Los elementos son instanciados para satisfacer los
atributos de calidad, así como los requisitos funcionales.
16   Check: El resultado es analizado para determinar si los
requisitos son satisfechos.

## Diapositiva 17

DISEÑO CENTRADO EN ATRIBUTOS DE CALIDAD (ADD)

 Define una arquitectura del software basada en ACs
 Proceso de descomposición recursivo
 En cada etapa, se eligen patrones y tácticas para satisfacer un conjunto de ACs

 Entrada
 Requisitos AC
 Restricciones
 Req. funcionales significativos para la arquitectura
 Salida
 Primeros niveles de descomposición modular

17
 Varias vistas del Sistema según se consideren apropiadas
 Conjunto de elementos con funcionalidad asignada e interacciones entre los elementos

## Diapositiva 18

DISEÑO CENTRADO EN ATRIBUTOS DE CALIDAD (ADD)

18

## Diapositiva 19

DISEÑO CENTRADO EN ATRIBUTOS DE CALIDAD (ADD):
ESCENARIOS (FRAMEWORKS) Y TÁCTICAS

Framework de diseño orientado a  Estímulo: cualquier hecho que
atributos: Busca priorizar en el diseño, la  1
afecte la calidad

solución e implementación los
requerimientos, riesgos y atributos de  Técnicas de respuesta: buscará
calidad que fueron definidos para el  2
proyecto. Plantea una estructura de  controlar la respuesta al estímulo
escenarios y tácticas, en dónde cada  Respuesta: respuesta esperada o
escenario relaciona un atributos de calidad
con distintas técnicas de implementación  3 caso de éxito al implementar la
buscando mejorar la calidad.  técnica
19

## Diapositiva 20

BIBLIOGRAFÍA / REFERENCIAS

1. Software Architecture in Practice, Third Edition.2013. Len Bass, Paul Clements, Rick Kazman. disponible en Biblioteca
General.
2. Essential Software Architecture. Ian Gorton. Springer.2006. disponible en Biblioteca General.
3. The Art of Software Architecture. Stephen Albin.Wiley.2003.

4. Documenting software architectures views and beyond 2nd ed., Clements, Paul. Addison-Wesley. 2011. disponible en
Biblioteca General
5. The process of Software Architecting. Peter Eeles, Peter Cripps. Addison Wesley.2010. disponible en Biblioteca
General.
6. Software Systems Architecture: Working with Stakeholders Using Viewpoints and Perspectives. Nick Rozanski y Eoin
Woods. disponible en Biblioteca General.
7. Microsoft® Application Architecture Guide. 2nd Edition. David Hill. Patterns and practices. Disponible en:
http://www.microsoft.com/en-us/download/details.aspx?id=16236
8. Beginning Java™ EE 7 Platform with GlassFish™ 3. From Novice to Professional Second Edition. Antonio Goncalves,

20
Complementaria:
1. Tutorial de JavaEE 8 https://javaee.github.io/tutorial/

## Diapositiva 21

¿Preguntas?

Andrés Armando Sánchez Martín – marzo de 2022

## Diapositiva 22

PARA LA PRÓXIMA CLASE

 ¿Cuál es la tensión entre los Atributos de Calidad?
 ¿Cómo se validan las decisiones en ADD?
 ¿Qué son los Acuerdos (Trade-offs)?

22
