# 2.2 Atributos de Calidad 1

> Fuente: `2.2 Atributos de Calidad 1.pdf` · 44 diapositivas · convertido con pdftotext el 2026-11-25. Texto extraído automáticamente: verificar contra el PDF.
> Se eliminó el pie repetido: "Andrés Armando Sánchez Martín"

## Diapositiva 1

(1306)
ARQUITECTURA DE SOFTWARE

2.2 Atributos de Calidad 1

asanchez-m@javeriana.edu.co - 3057642728  Andrés Armando Sánchez Martín – febrero de 2022

## Diapositiva 2

Agenda

 Requerimientos
 Modelos de Calidad de Software
 ISO 25000 vs FURPS+
 Atributos de Calidad

2

## Diapositiva 3

REQUERIMIENTOS: ENTENDER EL PROBLEMA

A la hora de definir requerimientos y analizarlos es muy importante entender el
problema que estamos resolviendo
Espacio del Problema:  Solución:

oDiseño: todo lo referente a la planificación del software, desde
diseño UI, UX hasta diseño de sistemas
oDesarrollo: escribir el código, configuraciones y contrataciones
oIdea: ¿Qué queremos resolver?  de servicios
oCriterios de éxito: ¿Cómo identificamos si estamos resolviendo  oEvaluación: medir la eficiencia y eficacia del software frente al
el problema?  problema
oHistorias de usuario: Supuestos de historias de lo que va a ganar  oCriterios de aceptación: medir el impacto del software, no
el usuario al utilizar la solución usando las características del  importa lo bueno que sea el problema si los usuarios no lo usan
problema a resolver.  o no le ven uso
oDespliegue (deploy): lanzar el software en ambientes
productivos (mercado) y empezar a mejorar las características
con un feedback loop (crear, medir, aprender)
3

## Diapositiva 4

REQUERIMIENTOS: CLASIFICACIÓN

Plan de  Acuerdos de
Recursos  Certificaciones  Infraestructura
Despliegue  Servicios
Requerimientos  De proyecto
Documentación
Capacitaciones  Licencias  Plan de Transición
de Usuario

4

## Diapositiva 5

REQUERIMIENTOS: CLASIFICACIÓN

Requerimientos

De producto

Dominio  Software

Requerimientos  Requerimientos no
funcionales  funcionales
5
De negocio  De usuario  De Función
(Funciones  (Atributos de
indispensables)  calidad):

## Diapositiva 6

REQUERIMIENTOS: CLASIFICACIÓN

6

## Diapositiva 7

REQUERIMIENTOS: CLASIFICACIÓN

7

## Diapositiva 8

RIESGOS

En la toma de requerimientos
- dificultad / complejidad

En los atributos de calidad
- incertidumbre, cuanto mas
incertidumbre hay, mas alto es el riesgo.

Conocimiento del dominio
- Riesgo prototípico, son aquellos que
8
podemos atacar de forma estándar.

## Diapositiva 9

RESTRICCIONES

Restricciones del sistema que vienen impuestas:
 Muy poco software tiene libertad total
 Pueden ser técnicas u organizativas

 Pueden surgir del cliente o también de la organización
de desarrollo
 Limitan las alternativas a considerar para decisiones de
diseño particulares
 Ejemplos:
  Marcos de aplicaciones (frameworks)
  Lenguajes de programación, ...
9
 Normalmente son tus “amigos”

## Diapositiva 10

RESTRICCIONES

Las restricciones en el contexto de un proceso de desarrollo
de software se refiere a las restricciones que limitan las
opciones de diseño o implementaciones disponibles al
desarrollar.
Los StakeHolders, nos pueden poner limitaciones

relacionadas con su contexto de negocio, ejemplo:
 Las limitaciones legales, la implementación de un producto
podría tener restricciones en algún país, y esto seria una
limitante a considerar para el desarrollo del producto.
 Limitaciones técnicas, relacionadas con integraciones con
otros sistemas.
 El ciclo de vida del producto, agregará limitaciones al
producto, por ejemplo a medida que avanza el proceso de
implementación el modelo de datos va a ser más difícil de
modificar.
10  Nota: El arquitecto debe balancear entre los requerimiento y
las restricciones

## Diapositiva 11

ATRIBUTOS DE CALIDAD

 Son características medibles de interés para
usuarios o desarrolladores
 También conocidos como requisitos no-
funcionales

 Rendimiento, disponibilidad, modificabilidad,
testabilidad,…
 También conocidos como –idades (-ities en
inglés)
 Pueden especificarse mediante escenarios
 Técnica estímulo-respuesta: “Si ocurre un fallo
interno durante la operación normal, el sistema
reanuda la operación en menos de 30 segundos
y no se pierden datos” Priorizados por: El
11  cliente de acuerdo al éxito del sistema El
arquitecto de acuerdo al riesgo técnico

## Diapositiva 12

ATRIBUTOS DE CALIDAD

 Los atributos de calidad determinan la mayoría de
las decisiones de diseño en arquitectura
 Si la única preocupación fuese la funcionalidad,

un sistema monolíticos sería suficiente Sin
embargo, es habitual ver:
 Estructuras redundantes para fiabilidad
 Estructuras concurrentes para rendimiento
 Capas para modificabilidad …

 Priorizados por:
 El cliente de acuerdo al éxito del sistema
12
 El arquitecto de acuerdo al riesgo técnico

## Diapositiva 13

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
13

## Diapositiva 14

MODELOS DE CALIDAD DE SOFTWARE
A nivel de proceso

- ITIL (1989)
- ISO/IEC 15504 (1993)
“los modelos de calidad son aquellos documentos  • Dromey (1995)
que integran la mayor parte de las mejores  • PSP (1995)
- Bootstrap (1996)
prácticas, proponen temas de administración en  • TSP (1996)

los que cada organización debe hacer énfasis,  • IEEE 12207 (1996)
- COBIT 4,0 (1996)
integran diferentes prácticas dirigidas a los  • ISO 90003 (1997)
procesos clave y permiten medir los avances en  • CMMI (2000)
- ISO/IEC 20000 (2005)
calidad.”
Estudio comparativo de los modelos y estándares  A nivel de producto

de calidad del software (Scalone, 2006)  • McCall (1977)
- GQM (1984)
- Boehm (1986)
- FURPS+ (1987)
- Gilb (1988)
- ISO 9126-1 (1991)
14  • SQAE (1997)
- WebQEM (1998)
- ISO 25000 (2005->2014)

## Diapositiva 15

MODELOS DE CALIDAD DE SOFTWARE

FURPS+  ISO/IEC 25000:2014

- Functionality (Funcionalidad).  • Adecuación Funcional

- Usability (Usabilidad).  • Eficiencia de Desempeño
- Reliability (Confiabilidad).  • Compatibilidad
- Perfomance (Prestación).  • Usabilidad
- Supportability (Soporte).  • Fiabilidad
- + (Plus)  • Seguridad
- Mantenibilidad
- Portabilidad
15

## Diapositiva 16

MODELOS DE CALIDAD DE SOFTWARE: FURPS+
Funcionalidad:  Rendimiento/Prestación
- Características  • Velocidad de procesamiento
- Eficiencia
- Capacidades del sistemas
- Consumo de recurso.
- Generalidades de las
- Rendimiento efectivo total.
funciones
- Tiempo de respuesta.
- Seguridad del sistema
- Disponibilidad

Usabilidad  Capacidad de Soporte:
- Factores humanos.  • Adaptabilidad.
- Factores estéticos.  • Extensibilidad.
- Consistencia de la interfaz.  • Mantenibilidad.
- Documentación.  • Compatibilidad.
- Ayuda  • Configurabilidad.
- Requisitos de instalación.
Confiabilidad  • Internacionalización
- Exactitud de las salidas  +
- Tiempo medio de fallos  • Restricciones de Implementación
- Frecuencia de fallas  • Restricciones de Interfaz
- Recuperabilidad frente a  • Empaquetamiento: para
fallos.  distribución
16  • Grado de prevención.  • Restricciones Legales
- Capacidad de predicción  • Restricciones físicas

## Diapositiva 17

MODELOS DE CALIDAD DE SOFTWARE:
ISO/IEC 25000:2014

Efectividad  Libre de Riesgos

Eficacia  • Economic risk mitigation

- Health and safety risk
mitigation
Satisfacción  • Environmental risk
mitigation
- Usefulness  Cobertura de
- Trust  Contexto
- Pleasure  Calidad en Uso
- Context completeness
17
- Comfort  • Flexibility

## Diapositiva 18

MODELOS DE CALIDAD DE SOFTWARE:
ISO/IEC 25000:2014
Adecuación Funcional  Fiabilidad
- Madurez
- Completitud funcional.  • Disponibilidad
- Corrección funcional.  • Tolerancia a fallos.
- Pertinencia funcional.  • Capacidad de recuperación
Eficiencia de desempeño  Seguridad

- Comportamiento temporal.  • Confidencialidad
- Utilización de recursos  • Integridad
- Capacidad  • No repudio
- Responsabilidad
Compatibilidad  • Autenticidad
- Coexistencia  Mantenibilidad
- Interoperabilidad  • Modularidad
- Reusabilidad
Usabilidad
- Analizabilidad
- Capacidad para reconocer su adecuación  • Capacidad para ser modificado
- Capacidad de aprendizaje
- Capacidad para ser usado  Calidad en Producto  • Capacidad para ser probado
Portabilidad
- Protección contra errores de usuario
- Adaptabilidad
18  • Estética de la interfaz de usuario
- Capacidad para ser instalado
- Accesibilidad
- Capacidad para ser reemplazado

## Diapositiva 19

IDONEIDAD FUNCIONAL

Comparación:
Requerimientos Funcionales y Funcionalidades implementadas

Completitud  Exactitud  Pertinencia
Funcional  Funcional  Funcional

19

## Diapositiva 20

IDONEIDAD FUNCIONAL

Comparación: resultado esperado y resultado obtenido

Completitud  Exactitud  Pertinencia
Funcional  Funcional  Funcional

20

## Diapositiva 21

IDONEIDAD FUNCIONAL

Comparación: objetivos cumplidos y objetivos esperados

Completitud  Exactitud  Pertinencia
Funcional  Funcional  Funcional

21

## Diapositiva 22

EFICIENCIA DE EJECUCIÓN

Comparación: Tiempo transcurrido entre pedido y respuesta y
tiempo esperado o tiempo máximo tolerado

Tiempo a  Uso de
Capacidad
Comportamiento  Recursos

22

## Diapositiva 23

EFICIENCIA DE EJECUCIÓN

Comparación: Consumo de recursos y
consumo esperado o tolerado de recursos

Tiempo a  Uso de
Capacidad
Comportamiento  Recursos

23

## Diapositiva 24

EFICIENCIA DE EJECUCIÓN

Comparación: Límite de tolerancia detectado y
límite de tolerancia esperado

Tiempo a  Uso de
Capacidad
Comportamiento  Recursos

24

## Diapositiva 25

COMPATIBILIDAD

Implementación de estándares y disponibilidad de esquemas: HATEOAS,
JSON Schema, SOAP, Open API

Andrés Armando Sánchez Martín  Interoperabilidad  Coexistencia

25

## Diapositiva 26

COMPATIBILIDAD

Cantidad de fallos por razones externas en un tiempo dado

Andrés Armando Sánchez Martín  Interoperabilidad  Coexistencia

26

## Diapositiva 27

USABILIDAD

Reconocimiento  Curva de
Operabilidad
de idoneidad  aprendizaje

Andrés Armando Sánchez Martín  Protección a  Estética de
Relación entre conceptos de  Accesibilidad
dominio y acciones de sistema
errores  interfaz

27

## Diapositiva 28

USABILIDAD

Reconocimiento  Curva de
Operabilidad
de idoneidad  aprendizaje

Andrés Armando Sánchez Martín  Protección a  Estética de
de consultas a soporte Accesibilidad
errores Cantidad y tipo interfaz

28

## Diapositiva 29

USABILIDAD

Reconocimiento  Curva de
Operabilidad
de idoneidad  aprendizaje

Andrés Armando Sánchez Martín  Protección aCantidad de pasos
Estética
hastadelograr objetivos.Accesibilidad
errores  Métricasinterfaz
de conversión.

29

## Diapositiva 30

USABILIDAD

Comparación: Cantidad
Reconocimiento  Curva de
de intentos fallidos e
intentos totales de interacción.  Operabilidad
de idoneidad  aprendizaje

Andrés Armando Sánchez Martín  Protección a  Estética de
Accesibilidad
errores  interfaz

30

## Diapositiva 31

USABILIDAD

Curva de de estética
Reconocimiento Encuestas de apreciación
Operabilidad
de idoneidad  aprendizaje

Andrés Armando Sánchez Martín  Protección a  Estética de
Accesibilidad
errores  interfaz

31

## Diapositiva 32

USABILIDAD

Reconocimiento  Curva
Adhesión  de
a estándares  Operabilidad
de idoneidad  aprendizaje

Andrés Armando Sánchez Martín  Protección a  Estética de
Accesibilidad
errores  interfaz

32

## Diapositiva 33

CONFIABILIDAD

Madurez  Disponibilidad

Tolerancia a  Capacidad de
fallos Tiempo medio entre averías
recuperación

33

## Diapositiva 34

CONFIABILIDAD

Madurez  Disponibilidad

Tolerancia a  Capacidad de
Cantidad de tiempo fuera de recuperación
fallos  servicio

34

## Diapositiva 35

CONFIABILIDAD

Madurez  Chaos testing Disponibilidad

Tolerancia a  Capacidad de
fallos  recuperación

35

## Diapositiva 36

CONFIABILIDAD

Tiempo medio hasta la recuperación
Madurez  Disponibilidad

Tolerancia a  Capacidad de
fallos  recuperación

36

## Diapositiva 37

SEGURIDAD

Penetration testing

Comprobación
Confidencialidad
de Hechos

Integridad

Traza de
Autenticidad
responsabilidad

37

## Diapositiva 38

MANTENIBILIDAD

Cobertura de código en tests y análisis estático de código
Capacidad de
Modularidad
Análisis

Reusabilidad

Capacidad de  Capacidad de
Modificación  Prueba

38

## Diapositiva 39

PORTABILIDAD

Cantidad de dependencias a entornos específicos.

Capacidad de  Capacidad de
Adaptabilidad
Instalación  Reemplazo

39

## Diapositiva 40

PORTABILIDAD

Requerimientos del entorno de despliegue

Capacidad de  Capacidad de
Adaptabilidad
Instalación  Reemplazo

40

## Diapositiva 41

PORTABILIDAD

Estándares o herramientas de carga o conversión de datos.
Implementación de interfaces comunes.

Capacidad de  Capacidad de
Adaptabilidad
Instalación  Reemplazo

41

## Diapositiva 42

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

42
Complementaria:
1. Tutorial de JavaEE 8 https://javaee.github.io/tutorial/

## Diapositiva 43

¿Preguntas?

Andrés Armando Sánchez Martín – febrero de 2022

## Diapositiva 44

PARA LA PRÓXIMA CLASE

 ¿Qué son los escenarios de calidad?
 ¿Cómo se miden los atributos de calidad?
 ¿Qué es ADD (Diseño Centrado en Atributos de
Calidad)?

44
