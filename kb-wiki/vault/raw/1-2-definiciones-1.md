# 1.2 Definiciones 1

> Fuente: `1.2 Definiciones 1.pdf` · 48 diapositivas · convertido con pdftotext el 2026-11-25. Texto extraído automáticamente: verificar contra el PDF.
> Se eliminó el pie repetido: "Andrés Armando Sánchez Martín"

## Diapositiva 1

(1306)
ARQUITECTURA DE SOFTWARE

1.2 Definiciones 1

asanchez-m@javeriana.edu.co - 3057642728  Andrés Armando Sánchez Martín – febrero de 2022

## Diapositiva 2

Agenda

 Ingeniería de Software
 Proceso de Desarrollo de Software
 Fundamentos de arquitectura
 Arquitectura de Software
 Principios SOLID y Características POO

2

## Diapositiva 3

INGENIERÍA DE SOFTWARE

El concepto “ingeniería de software” se propuso
originalmente en 1968, en una conferencia realizada
para discutir lo que entonces se llamaba la “crisis del
software” (Naur y Randell, 1969). Se volvió claro que los

enfoques individuales al desarrollo de programas no
escalaban hacia los grandes y complejos sistemas de
software. Éstos no eran confiables, costaban más de lo
esperado y se distribuían con demora.
A lo largo de las décadas de 1970 y 1980 se desarrolló
una variedad de nuevas técnicas y métodos de
ingeniería de software, tales como la programación
estructurada, el encubrimiento de información y el
desarrollo orientado a objetos. Se perfeccionaron
herramientas y notaciones estándar y ahora se usan de
3
manera extensa.

## Diapositiva 4

INGENIERÍA DE SOFTWARE: : DESARROLLO DE SOFTWARE

Es el proceso metodológico para la construcción
de soluciones de software.  Análisis de
Mantenimiento  Requerimientos
Existen varios enfoques (paradigmas) para  y Evolución

desarrollar software:
 Modelo de cascada
Diseño de la
 Modelo de espiral  Despliegue
Solución
 Desarrollo iterativo e incremental
 Desarrollo ágil  Desarrollo y
4
Evaluación

## Diapositiva 5

DESARROLLO DE SOFTWARE: DIFICULTADES

ESENCIALES  ACCIDENTALES

Especificación,
Detalles de la
diseño y

implementación y
comprobación del
producción actual
concepto
“Consideró a la especificación, diseño y comprobación del concepto la parte difícil de hacer
software. (…)

5
Si esto es cierto, hacer software siempre será difícil. No existe la bala de plata.”
(Frederick P. Brooks Jr., 1986)

## Diapositiva 6

DESARROLLO DE SOFTWARE: DIFICULTADES/RESTOS

ESENCIALES  ACCIDENTALES

Lenguajes de  Multi-

Complejidad  Conformidad
alto nivel  procesamiento

Tolerancia al  Entornos de  Nuevas
Invisibilidad
cambio  programación  tecnologías
6

## Diapositiva 7

DESARROLLO DE SOFTWARE: SOLUCIONES

Complejidad:
Conformidad:
No desarrollar: Comprar
Prototipado rápido
- OSS

Dificultades
Esenciales

Tolerancia al cambio;  Invisibilidad:
7  Desarrollo evolutivo  Grandes Diseñadores
¡Arquitectos!

## Diapositiva 8

PROCESO DE DESARROLLO DE SOFTWARE: FASES Y
ARTEFACTOS

Mejora del sistema  Descubrimiento  Abstracción

Disparador  Análisis de  Comprensión  Diseño de
Requerimientos  del problema  la Solución

Necesidad del Usuario  Análisis y  Modelado
documentación

8

## Diapositiva 9

PROCESO DE DESARROLLO DE SOFTWARE: FASES Y
ARTEFACTOS

Programación e
integración  Infraestructura

Diseño de  Solución  Desarrollo y  Artefacto de
Despliegue
la Solución  detallada  Evaluación  Software

Automatización de
pruebas  Operaciones

9

## Diapositiva 10

PROCESO DE DESARROLLO DE SOFTWARE: FASES Y
ARTEFACTOS

Arreglo de errores

Software  Mantenimiento y  Sistema
Despliegue
disponible  Evolución  deprecado

Nuevas funcionalidades

10

## Diapositiva 11

PROCESO DE DESARROLLO DE SOFTWARE:
METODOLOGÍAS TRADICIONALES VS AGILES

11

## Diapositiva 12

PROCESO DE DESARROLLO DE SOFTWARE:
METODOLOGÍAS TRADICIONALES VS AGILES

12

## Diapositiva 13

PROCESO DE DESARROLLO DE SOFTWARE:
METODOLOGÍAS TRADICIONALES VS AGILES

13

## Diapositiva 14

PROCESO DE DESARROLLO DE SOFTWARE:
METODOLOGÍAS TRADICIONALES VS AGILES

14

## Diapositiva 15

PROCESO DE DESARROLLO DE SOFTWARE:
METODOLOGÍAS TRADICIONALES VS AGILES

15

## Diapositiva 16

PROCESO DE DESARROLLO DE SOFTWARE:
METODOLOGÍAS TRADICIONALES VS AGILES

 Arquitectos en la torre de marfil   Arquitectura que puede reaccionar a cambios en
  Falta de comunicación
entorno

  Adaptación a cambios continuos
 Centralización de todas las decisiones
  También conocidas como arquitecturas evolutivas
  Arquitecto = cuello de botella
  Buena arquitectura permite agilidad
 Tomar demasiadas decisiones
  Mejor comprensión de decisiones y soluciones de
  Retrasar ciertas decisiones puede ser mejor que  compromiso
deshacerlas
 Anti-patrón común: adopción de técnicas de
 Big Design Up-Front  desarrollo de software ágil que crean arquitecturas
  Demasiados diagramas y documentos innecesarios  que no son ágiles

16
  Retardos debidos al proceso de arquitectura    Causado por demasiado enfoque en funcionalidad

## Diapositiva 17

PROCESO DE DESARROLLO DE SOFTWARE: ROLES

Tradicional  Ágil

Experto del dominio  Partes interesadas (stakeholders)

Analista  Cliente / Dueño del producto

Administrador de sistemas (SysAdmin)  DevOps / SRE (site reliability engineer)

Arquitecto, Desarrollador, QA – Tester  Equipo de Desarrollo (Team)

17
Gestor del proyecto  Facilitador

## Diapositiva 18

FUNDAMENTOS DE ARQUITECTURA

Architecture = Proceso y producto de planificar, diseñar y
construir edificios u otras estructuras

Utilitas (utilidad):
- Ser útil y funcionar bien para las personas que lo van a usar

Firmitas (durabilidad):
- Mantenerse de forma robusta y en buena condición

Venustas (elegancia):
18  • Ser agradable a las personas

## Diapositiva 19

FUNDAMENTOS DE ARQUITECTURA:
ARQUITECTURA VS DISEÑO

Arquitectura se enfoca en estructura
de alto nivel de un sistema de software

Decisiones de diseño principales del
sistema
Si hay que cambiarlas ⇒ Coste elevado

"Toda arquitectura conlleva diseño pero no todo el diseño es
19
arquitectura" G. Booch

## Diapositiva 20

FUNDAMENTOS DE ARQUITECTURA

Arquitectura

Arquitecto Empresarial
Empresarial

Arquitecto de Solución

Arquitecto Técnico
Arquitectura de
Sistemas

Arquitectura de
Software
20

Niveles del Rol

## Diapositiva 21

FUNDAMENTOS DE ARQUITECTURA
Arquitectura
Empresarial

21

## Diapositiva 22

FUNDAMENTOS DE ARQUITECTURA: LA IMPORTANCIA DE LA
COMUNICACIÓN - LEY DE CONWAY

“LAS ORGANIZACIONES QUE DISEÑAN
SISTEMAS ESTÁN LIMITADAS A PRODUCIR

DISEÑOS QUE SON COPIAS DE LAS
ESTRUCTURAS DE COMUNICACIÓN
DE ESTAS ORGANIZACIONES”
Ley de Conway (Melvin Conway, 1967)

22

## Diapositiva 23

LA IMPORTANCIA DE LA COMUNICACIÓN
LEY DE CONWAY

23

## Diapositiva 24

ARQUITECTURA DE SOFTWARE

- Arquitectura [ISO/IEC/IEEE 42010:2011, 3.2]: Conceptos fundamentales o propiedades de un
Sistema en su entorno representados por sus elementos, relaciones y los principios de su diseño y
evolución
- Descripción de arquitectura: Producto de trabajo explícito que expresa una arquitectura de un

sistema, normalmente a través de modelos, texto o gráficos
- Diseñar una arquitectura (architecting): Proceso de crear una arquitectura

La arquitectura
comprende

Elementos de  Relaciones  Propiedades de
24
software  entre ellos  ambos

## Diapositiva 25

ARQUITECTURA DE SOFTWARE

- “La estructura del sistema, compuesta por elementos de software, sus propiedades visibles y sus relaciones” –
Software Architecture in Practice (Bass, Clements & Kazman, 2003)
- “El conjunto de decisiones principales de diseño tomadas para el sistema” – Software Architecture:
Foundations, Theory and Practice (Taylor, 2010)

- "(…) la arquitectura se reduce a las cosas importantes, cualesquiera que sean" – Patterns of Enterprise
Application Architecture (Fowler, 2002)

Podemos decir que:  A  B
La arquitectura de software es el diseño
conceptual de una solución, donde se muestran
los componentes, funciones y estructura
general de usa solución. Además, de mostrar
25
como se comunican y relacionan  C  D  E

## Diapositiva 26

ARQUITECTURA DE SOFTWARE: CARACTERÍSTICAS

- Múltiples cambios en contexto
- Servicio/producto virtual

- No suele haber límites físicos
- Disciplina relativamente nueva
- Podemos aprender mucho de
otras disciplinas

26

## Diapositiva 27

ARQUITECTURA DE SOFTWARE: EJEMPLOS

27

## Diapositiva 28

ARQUITECTURA DE SOFTWARE: EJEMPLOS

28

## Diapositiva 29

ARQUITECTURA DE SOFTWARE: EJEMPLOS

29

## Diapositiva 30

ARQUITECTURA DE SOFTWARE: EJEMPLOS

Flujo de datos - Flux

30

## Diapositiva 31

### Arquitectura de software: funciones de un arquitecto de software

La diapositiva organiza su contenido en **tres columnas**, sin asociar por filas equivalentes los conceptos de cada una:

1. **Analiza el contexto:** requerimientos (funcionales y no funcionales), riesgos y restricciones.
2. **Posee herramientas de diseño:** atributos de calidad, estilos de arquitectura, patrones de arquitectura y tácticas.
3. **Diseña la solución:** modelo, razonamientos, documentación e implementación. La figura incluye flechas de retroalimentación entre esos elementos.

*Texto estructurado tras revisión visual de la diapositiva 31 del PDF original; no se añadieron requisitos ni resultados del prototipo.*

## Diapositiva 32

ARQUITECTURA DE SOFTWARE: FUNCIONES DE UN
ARQUITECTO DE SOFTWARE

Tomar decisiones arquitectónicas

Analizar continuamente la arquitectura

Estar al día de las tendencias actuales

Asegurar cumplimiento decisiones existentes

Experiencia diversa

Conocimiento del dominio de negocio

Poseer habilidades interpersonales

Comprender y navegar en política empresarial
32

## Diapositiva 33

FUNCIONES DE UN ARQUITECTO DE SOFTWARE:
IDENTIFICAR INVOLUCRADOS
Internos  Externo
Todos los individuos, roles u
organizaciones que:  • Analista  • Cliente
 Deberían conocer la arquitectura  • Diseñador  • Usuarios finales

 Tienen que ser convencidos de la  • Personas de  • Auditor
arquitectura  negocios  Autoridades
 Tienen que trabajar con la  • Desarrollador  públicas
arquitectura o el código  • Product owner  • Suministradores
 Necesitan la documentación de la  • Diseñador de  • Proveedores
arquitectura para realizar su trabajo  UX  servicios
 Tienen que tomar decisiones sobre el  • Jefe de proyecto  externos
33
sistema o su desarrollo  • Etc  • Etc

## Diapositiva 34

FUNCIONES DE UN ARQUITECTO DE SOFTWARE:
IDENTIFICAR INVOLUCRADOS
Cliente  Manager  Dev  Usuario  QA

34
Sistema

## Diapositiva 35

FUNCIONES DE UN ARQUITECTO DE SOFTWARE:
IDENTIFICAR INVOLUCRADOS
Cliente  Manager  Dev  Usuario  QA

Andrés Armando Sánchez Martín  Entrega a tiempo y
dentro del presupuesto

35
Sistema

## Diapositiva 36

FUNCIONES DE UN ARQUITECTO DE SOFTWARE:
IDENTIFICAR INVOLUCRADOS
Cliente  Manager  Dev  Usuario  QA

Permite equipos
independientes y
comunicación clara

36
Sistema

## Diapositiva 37

FUNCIONES DE UN ARQUITECTO DE SOFTWARE:
IDENTIFICAR INVOLUCRADOS
Cliente  Manager  Dev  Usuario  QA

Es fácil de implementar
y de mantener

37
Sistema

## Diapositiva 38

FUNCIONES DE UN ARQUITECTO DE SOFTWARE:
IDENTIFICAR INVOLUCRADOS
Cliente  Manager  Dev  Usuario  QA

Es confiable y estará
disponible cuando lo
necesite

38
Sistema

## Diapositiva 39

FUNCIONES DE UN ARQUITECTO DE SOFTWARE:
IDENTIFICAR INVOLUCRADOS
Cliente  Manager  Dev  Usuario  QA

Es fácil de comprobar

39
Sistema

## Diapositiva 40

FUNCIONES DE UN ARQUITECTO DE SOFTWARE:
IDENTIFICAR INVOLUCRADOS
Cliente  Manager  Dev  Usuario  QA

Es fácil de comprobar

40
Sistema

## Diapositiva 41

PRINCIPIOS SOLID

S – Single Responsibility Principle (SRP):
- Según este principio “una clase debería tener una, y solo una, razón para cambiar”. Es esto,
precisamente, “razón para cambiar”, lo que Robert C. Martin identifica como “responsabilidad”.
O – Open/Closed Principle (OCP):

- Deberías ser capaz de extender el comportamiento de una clase, sin modificarla”. En otras
palabras: las clases que usas deberían estar abiertas para poder extenderse y cerradas para
modificarse.
L – Liskov Substitution Principle (LSP):
- “las clases derivadas deben poder sustituirse por sus clases base”. Esto significa que los
objetos deben poder ser reemplazados por instancias de sus subtipos sin alterar el correcto
funcionamiento del sistema o lo que es lo mismo: si en un programa utilizamos cierta
clase, deberíamos poder usar cualquiera de sus subclases sin interferir en la funcionalidad
41
del programa.

## Diapositiva 42

PRINCIPIOS SOLID

I – Interface Segregation Principle (ISP):
- “Haz interfaces que sean específicas para un tipo de cliente”,
es decir, para una finalidad concreta.

D – Dependency Inversion Principle (DIP)
- “Depende de abstracciones, no de clases concretas”. 1. Los
módulos de alto nivel no deberían depender de módulos
de bajo nivel. Ambos deberían depender de abstracciones. 2.
Las abstracciones no deberían depender de los
42
detalles. Los detalles deberían depender de las abstracciones.

## Diapositiva 43

CARACTERÍSTICAS POO

Abstracción
Este proceso permite identificar características y comportamientos, relevantes y
comunes, permitiendo así definir las entidades y como se relacionan y
comunican entre ellas.

Encapsulamiento
Es una barrera protectora que evita que el código y los datos sean accedidos por
azar o error por otros fragmentos de código o fuera de la clase.
Modularidad
Se basa en el principio de “Divide y vencerás”, dividir una aplicación en
43  componentes llamados “módulos” los que son independientes al resto de la
aplicación (en lo posible) reduciendo la dependencia..

## Diapositiva 44

CARACTERÍSTICAS POO

Principio de Ocultación
Es el proceso de ocultar todos los detalles internos de un objeto al mundo exterior.

Polimorfismo

- Es la capacidad por la cual, podemos crear funciones o variables de referencia, que se
comporta de manera diferente en diferentes contexto programático
Herencia
Poder juntar las características y comportamientos comunes en entidades, y organizarlas de
manera jerárquica para que se relacionen con otras.
Recolector de basura
44  Optimizar el uso de los recursos de hardware de una manera transparente para el usuario y
programador.

## Diapositiva 45

SOLID Y POO: COHESIÓN Y ACOPLAMIENTO
Acoplamiento  Cohesión

- El acoplamiento se refiere  • La cohesión de software
al grado de  es el grado en que
interdependencia que  elementos diferentes
tienen dos unidades de  de un sistema

software entre sí,  permanecen unidos
entendiendo por unidades  para alcanzar un
de software: clases,  mejor resultado que si
subtipos, métodos,  trabajaran por separado.
módulos, funciones,  Se refiere a la forma en
bibliotecas, etc.  que podemos agrupar
- Si dos unidades de  diversas unidades de
software son  software para crear una
completamente  unidad mayor
independientes la una de
45  la otra, decimos que están
desacopladas.

## Diapositiva 46

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

46
Complementaria:
1. Tutorial de JavaEE 8 https://javaee.github.io/tutorial/

## Diapositiva 47

¿Preguntas?

Andrés Armando Sánchez Martín – febrero de 2022

## Diapositiva 48

PARA LA PRÓXIMA CLASE

 ¿Qué un Patrón de Software?
 ¿Cuáles son los Estilos Arquitectónicos?
 ¿Cuáles son los Patrones Arquitectónicos?

 ¿Qué son los Requerimientos?
 ¿Qué son los modelos de calidad de Software?
Tarea:
 Hacer un cuadro comparativo de los patrones de
diseño de software y los patrones de arquitectura de
software
 Definición, diagrama, ventajas, desventaja y
48
componentes
 Entrega clase 2.2
