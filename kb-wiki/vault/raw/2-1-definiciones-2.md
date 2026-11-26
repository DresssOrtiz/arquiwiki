# 2.1 Definiciones 2

> Fuente: `2.1 Definiciones 2.pdf` · 17 diapositivas · convertido con pdftotext el 2026-11-25. Texto extraído automáticamente: verificar contra el PDF.
> Se eliminó el pie repetido: "Andrés Armando Sánchez Martín"

## Diapositiva 1

(1306)
ARQUITECTURA DE SOFTWARE

2.1 Definiciones 2

asanchez-m@javeriana.edu.co - 3057642728  Andrés Armando Sánchez Martín – febrero de 2022

## Diapositiva 2

Agenda

 Patrón de Software

 Patrones Arquitectónicos
 Estilos Arquitectónicos
 Estilos y patrones Arquitecturales
 Proceso de Arquitectura
 Atributos de Calidad

2

## Diapositiva 3

PATRONES SOFTWARE

Los patrones de diseño son modelos muestra, que sirven como guía para la búsqueda de soluciones a
problemas comunes en el desarrollo de software y otros ámbitos del diseño de interacción o interfaces.

Patrones de
Patrones de
arquitectura

diseño
(Dominios)

De  Control de
Creacionales  Estructurales  Concurrencia  Distribución  Persistencia
comportamiento  acceso

GoF (Gang Of Four)

Un patrón de diseño es una manera de resolver un problema dentro de un contexto. En otras palabras,
los patrones son plantillas para soluciones a problemas comunes en el desarrollo de software que se
3  pueden usar en diferentes contextos.

## Diapositiva 4

PATRONES ARQUITECTURALES

AUNQUE UN PATRÓN ARQUITECTÓNICO TRANSMITE UNA
IMAGEN DE UN SISTEMA, NO ES UNA ARQUITECTURA
COMO TAL. UN PATRÓN ARQUITECTÓNICO ES MÁS BIEN UN
CONCEPTO QUE RESUELVE Y DELINEA ALGUNOS ELEMENTOS

COHESIVOS ESENCIALES DE UNA ARQUITECTURA DE SOFTWARE.
INNUMERABLES  ARQUITECTURAS  DIFERENTES  PUEDEN
IMPLEMENTAR EL MISMO PATRÓN Y, POR LO TANTO, COMPARTIR
LAS CARACTERÍSTICAS RELACIONADAS. ADEMÁS, LOS PATRONES
A MENUDO SE DEFINEN COMO ALGO "ESTRICTAMENTE
DESCRITO Y COMÚNMENTE DISPONIBLE".
4
Architectural Patterns: Definition (INFOTECH, 2012)

## Diapositiva 5

PATRONES ARQUITECTURALES: CLASIFICACIÓN

Broker  Model View
Pattern  Controller

Presentation-

Microkernel
Abstraction-
pattern
Control

Reflection  Layers pattern

MONOLÍTICOS  DISTRIBUIDOS
5
Pipes and  Blackboard
Filters  pattern

## Diapositiva 6

ESTILOS ARQUITECTURALES

UN ESTILO DE ARQUITECTURA ES UNA
COLECCIÓN DE DECISIONES DE DISEÑO,
APLICABLES EN UN CONTEXTO DETERMINADO,

QUE  RESTRINGEN  LAS  DECISIONES
ARQUITECTÓNICAS ESPECÍFICAS EN ESE
CONTEXTO Y OBTIENEN BENEFICIOS EN
CADA SISTEMA RESULTANTE.
Software Architecture: Foundations, Theory and Practice (Taylor, 2010)

6

## Diapositiva 7

ESTILOS ARQUITECTURALES: CLASIFICACIÓN

Estilos distribuidos
Estilos monolíticos Influenciados
Lenguajes de
por los  Capas
- Máquinas Virtuales
Programación  • Cliente Servidor  Peer-to-Peer
Modularidad  Disponibilidad

Curva de  • Programación estructurada  • n-Tier

Eficiencia  • Orientado a Objetos  • Micro Services
aprendizaje
Flujo de Datos  Memoria
Uso de
Adaptabilidad
- Batch  Compartida
Capacidad de  Capacidad de  • Pipes and Filters  • Blackboard  Interprete  Recursos
Prueba  Modificación
- Rule Based

Invocación Implícita  múltiples equipos
un solo equipo, una sola  • Event-based  independientes, múltiples
- Publisher-suscriber
pieza de software.  sistemas intercomunicados.
7

## Diapositiva 8

ESTILOS Y PATRONES ARQUITECTURALES

 Un patrón es una solución prediseñada para un
problema que puede aplicarse en cualquier contexto

donde se presente el problema.
 Un estilo es un modelo conceptual que define un
vocabulario común. algunas decisiones de diseño
arquitectural pueden actuar al mismo tiempo como
estilos y patrones.
8

## Diapositiva 9

ESTILOS Y PATRONES ARQUITECTURALES: TAREA

Client /  Publish
Blackboard
Server  subscribe

Multi tier  MVC  Web Service

Micro
Interceptores  Hexagonal
9
servicios

## Diapositiva 10

PROCESO DE ARQUITECTURA

Dominio del problema  Dominio de la Solución
Objetivos de  Requerimientos  Diseño de la
Diseño  Funcionales  arquitectura

Arquitecto
Atributos de
Restricciones  Actividad de Diseño  Acuerdos
Calidad

Preocupaciones
Riesgos  Documentación
(Concerns)

10  Entradas  Salidas

## Diapositiva 11

PROCESO DE ARQUITECTURA: ARQUITECTO
Objetivos
Requerimientos  Experiencia
Atributos de calidad
Restricciones
Stakeholders  Preocupaciones
Riesgos

Arquitectura
Acuerdos
Documentación
Experiencia
de la
Principios  Arquitecto
Patrones
Comunidad  Estilos
Anti-patrones
Estándares
Metodologías  Tecnologías
11

## Diapositiva 12

PROCESO DE ARQUITECTURA
Objetivos de  Atributos de
Escenarios
negocio  calidad
Análisis
Arquitectura de  Estrategias de  Decisiones de
software  arquitectura  Arquitectura

Trade-offs

Impacta
Puntos sensibles

No-Riesgos

12  Destilado en
Tipos de riesgos  Riesgos

## Diapositiva 13

PROCESO DE ARQUITECTURA: DISEÑO
Entity-Control-Boundary
(ECB)

Diseño arquitectónico
(Alto nivel)

Diseño Lógico

Diseño Detallado

13

## Diapositiva 14

ATRIBUTOS DE CALIDAD

“Los atributos de calidad son las expectativas de usuario, en general implícitas, de cuán bien
funcionará un producto.” - Software Requirements: 3rd Edition (Wiegers, Betty, 2013)

Performance / Rendimiento  Idoneidad Funcional

Eficiencia de ejecución
Escalabilidad
Compatibilidad
Modificabilidad
Usabilidad  ISO/IEC
Interoperabilidad  25000:2014
Confiabilidad
Seguridad
Seguridad
Disponibilidad
Mantenibilidad
14
Integración  Portabilidad

## Diapositiva 15

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

15
Complementaria:
1. Tutorial de JavaEE 8 https://javaee.github.io/tutorial/

## Diapositiva 16

¿Preguntas?

Andrés Armando Sánchez Martín – febrero de 2022

## Diapositiva 17

PARA LA PRÓXIMA CLASE

 ¿Cuáles son los tipos de requerimientos?
 ¿Cuáles son los atributos de calidad de FURPS+?

 ¿Cuáles son los atributos de calidad de ISO 25000?
Presentación:
 Explicar el estilo u patrón asignado explicando:
 Definición, historia, componentes (elementos),
casos de estudio relevantes (casos de aplicación),
ventajas, desventajas,
17
 Entrega Clase 3,2
