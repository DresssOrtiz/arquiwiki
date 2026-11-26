# 3.2 Atributos de Calidad 3

> Fuente: `3.2 Atributos de Calidad 3.pdf` · 32 diapositivas · convertido con pdftotext el 2026-11-25. Texto extraído automáticamente: verificar contra el PDF.
> Se eliminó el pie repetido: "Andrés Armando Sánchez Martín"

## Diapositiva 1

(1306)
ARQUITECTURA DE SOFTWARE

3.2 Atributos de Calidad 3

asanchez-m@javeriana.edu.co - 3057642728  Andrés Armando Sánchez Martín – febrero de 2023

## Diapositiva 2

Agenda

 Atributos de Calidad

 Tensión entre Atributos
 Acuerdos
 Gestión de Atributos de Calidad
 Evolución de Arquitectura
 Caso de Estudio Atributos de Calidad

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

TENSIÓN ENTRE ATRIBUTOS

Todos los ACs son buenos ...pero el valor depende del Proyecto y Stakeholder
- "Mejor calidad"...para qué?, para quién?

Los ACs no son independientes

- Algunos ACs pueden entrar en conflicto
- Qué es lo más importante?
- Ejemplo: Sistema muy seguro puede ser menos usable
Siempre hay un precio

2 consideraciones:
- Los ACs por sí mismos no son suficientes
- No son operacionales  ¡No hay sistema o
- Ejemplo: No aporta mucho decir que un Sistema debe ser modificable, o tener alta disponibilidad  arquitectura perfecta!
- El vocabulario para describer ACs es muy variado
- Es necesario describir cada atributo por separado
4
Escenarios Calidad: Forma común de especificar requisitos de AC

## Diapositiva 5

ACUERDOS (TRADE-OFFS)

 Decisiones significativas desde el
punto de vista de la arquitectura
del software

 Normalmente, decisiones que
afectan a:
 Atributos de calidad
 Estructura
 Dependencias
 Interfaces
5   Técnicas de construcción

## Diapositiva 6

ACUERDOS (TRADE-OFFS):
MATRIZ DE PUNTOS DE ACUERDO POR AC

6

## Diapositiva 7

GESTIÓN DE ATRIBUTOS DE CALIDAD

Es importante tener en cuenta que durante el
diseño de un sistema no puede lograrse la
satisfacción todos los atributos de calidad al
100%. Satisfacer cierto atributo de calidad puede
tener efectos positivos o negativos sobre otros

atributos que, de alguna manera, también se
desean satisfacer. En el contexto de diseño de
sistemas a este fenómeno se le conoce como
“trade-off”. Un arquitecto de software,
idealmente, debería conocer sobre “trade-offs”.
 En arquitecturas evolutivas:
  Función de encaje (fitness): mecanismo que
proporciona una valoración de la integridad
objetiva alguna combinación de atributos de
calidad
7  Architecture Trade-Off Analysis Method (ATAM)
  Medir valores de AC y evolucionar la
arquitectura

## Diapositiva 8

EVOLUCIÓN DE ARQUITECTURA

8  EVALUACIÓN DE MÉTRICAS  ARQUITECTURA EN EVOLUCIÓN

## Diapositiva 9

ESCENARIO DE CALIDAD: EJEMPLO

9

## Diapositiva 10

ESCENARIO DE CALIDAD: EJEMPLO DISPONIBILIDAD

10

## Diapositiva 11

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
11

## Diapositiva 12

DISEÑO CENTRADO EN ATRIBUTOS DE CALIDAD (ADD):
ESCENARIOS (FRAMEWORKS) Y TÁCTICAS

Escenario: Atributo de Calidad X

Tácticas para controlar
Estímulo  Respuesta
la respuesta

12
Algunos patrones y estilos ya implementan técnicas para el manejo de atributos

## Diapositiva 13

ESCENARIOS Y TÁCTICAS: CLASIFICACIÓN

Escenario

Eficiencia de  Capacidad de
Disponibilidad  Mantenibilidad  Seguridad  Usabilidad
ejecución  Prueba

Se clasifican según el atributo de calidad. Aunque no hay definición para todos los
13
atributos de calidad definidos en la ISO/IEC 25000

## Diapositiva 14

ESCENARIOS Y TÁCTICAS: DISPONIBILIDAD

Escenario: Disponibilidad

Tácticas para controlar  Falla ocultada o
Falla
la disponibilidad  sistema reparado

14

## Diapositiva 15

ESCENARIOS Y TÁCTICAS: DISPONIBILIDAD
Recuperación:
Recuperación:
Detección  Preparar /  Prevención
Reintroducción
Reparar

Quitar de
Ping / Eco  Votación  Modo Sombra
Servicio

Redundancia  Sincronización
Latido  Transacciones
Activa  de Estado

Punto de
Redundancia  Monitoreo de
Excepciones  Control /
Pasiva  Procesos
Retroceso

15
Repuesto

## Diapositiva 16

ESCENARIOS Y TÁCTICAS: MANTENIBILIDAD

Escenario: Mantenibilidad

Tácticas para controlar  Cambio hecho,
Pedido de cambio  probado y
la mantenibilidad
desplegado

16

## Diapositiva 17

ESCENARIOS Y TÁCTICAS: MANTENIBILIDAD
Coherencia
Limitar opciones
semántica
Abstraer servicios
comunes
Confinar
modificaciones
Generaliza  Anticipar cambios

Ocultar  Restringir
información  comunicación
Prevenir efectos
dominó
Mantener la
Intermediarios
interfaz

Registro en  Adherir a
Polimorfismo
ejecución  protocolos
Diferir enlace
17
Archivos de  Reemplazo de
configuración  componentes

## Diapositiva 18

ESCENARIOS Y TÁCTICAS: EFICIENCIA DE EJECUCIÓN

Escenario: Eficiencia de ejecución

Tácticas para controlar  Respuesta dentro
Eventos  del tiempo
la eficiencia
esperado

18

## Diapositiva 19

ESCENARIOS Y TÁCTICAS: EFICIENCIA DE EJECUCIÓN
Demanda  Gestión de  Arbitraje
de recursos  recursos  de recursos

Mejorar la  Políticas de
eficiencia  Concurrencia  planificación de

computacional  tareas

Reducir
Réplicas
sobrecarga

Manejar tasa  Aumentar
de eventos  recursos

19  Frecuencia de
muestreo

## Diapositiva 20

ESCENARIOS Y TÁCTICAS: SEGURIDAD
Escenario: Seguridad

Tácticas para controlar  Detección,
Ataque  resistencia o
la seguridad
recuperación

20

## Diapositiva 21

ESCENARIOS Y TÁCTICAS: SEGURIDAD
Detectores de
intrusos
Detectar ataques
Confidencialidad  Limitar
Autenticación
de datos  exposición

Recuperación de
ataques
Autorización  Integridad  Limitar acceso

Restauración  Disponibilidad
Resistencia al
ataque
Traza de
21
Identificación
auditoría

## Diapositiva 22

ESCENARIOS Y TÁCTICAS: CAPACIDAD DE PRUEBA

Escenario: Capacidad de prueba

Tácticas para controlar
Funcionalidad  Fallas detectadas
la capacidad de prueba

22

## Diapositiva 23

ESCENARIOS Y TÁCTICAS: CAPACIDAD DE PRUEBA
Entradas y  Monitoreo
salidas  interno

Captura y  Monitoreo
reproducción  incorporado

Separar interfaz
de
implementación

Acceso
23  exclusivo para
pruebas

## Diapositiva 24

ESCENARIOS Y TÁCTICAS: USABILIDAD

Escenario: Usabilidad

Pedido de un  Tácticas para controlar  Información y
usuario  la usabilidad  asistencia
adecuada al usuario

24

## Diapositiva 25

ESCENARIOS Y TÁCTICAS: USABILIDAD
Separar la
Iniciativas del  Iniciativas del
interfaz de
usuario  sistema
usuario

Mantenibilidad:
Modelo del
Coherencia  Cancelar
usuario

semántica

Modelo del
Deshacer
sistema

Modelo de la
Agregación
tarea

25
Múltiples vistas

## Diapositiva 26

CASO DE ESTUDIO ATRIBUTOS DE CALIDAD:
ALMACÉN Y FACTURA

 Diseñar una herramienta de gestión comercial para Windows. Factura en pesos, USD o Euro. Permite trabajar
con lector de códigos de barras (EAN).
 Su arquitectura de 32 bits, mejora su rendimiento. Podrá trabajar de un modo más fácil y rápido, haciendo su
empresa más operativa.

 Permite gestionar varios almacenes, un número indefinido de artículos a los cuales se les puede añadir en su
ficha una foto del mismo, posibilidad de trabajar con proveedores, agentes, zonas, perfecto control de los
vendedores, comisiones, descuentos, y depósitos.Y todo con un sencillo diseño.
 Incorpora mejoras en el tratamiento de inventarios, tarifas, cambios automáticos de precios, listados, informes,
varios tipos de facturación, retenciones de I.R.P.F. remesa de recibos en soporte magnético, gestión de cobros,
etc.
 El diseño de documentos es configurable por el usuario, incorporación de modelos estándar de documentos,
restricción de accesos a la aplicación configurables por el administrador, enlace opcional con la contabilidad
26  CONTAGEWIN, terminal punto de venta TPVWIN compartiendo la misma información, represente todo tipo
de estadísticas de clientes, proveedores, agentes, zonas, etc

## Diapositiva 27

CASO DE ESTUDIO ATRIBUTOS DE CALIDAD:
ALMACÉN Y FACTURA

 Características:

  Multi-almacén, amplio fichero de artículos, clientes, proveedores, comisiones, descuentos, depósitos.
  Su diseño permite el enlace desde presupuestos/pedidos, pedidos/albaranes, albaranes/facturas, facturas/recibos.
  Facturación en pesos, USD, Euro
  Incorpora mejoras en tratamiento de inventarios, tarifas, cambios automáticos de precios, listados, informes, varios tipos
de facturación, retenciones de IR.P.F., remesa de recibos en soporte magnéticos.
  Gestión de cobros, envío de documentos vía fax desde la aplicación.

27

## Diapositiva 28

CASO DE ESTUDIO ATRIBUTOS DE CALIDAD:
DEIMOS

DEIMOS Space tiene como objetivo liderar el campo del desarrollo de software empotrado en tiempo real, que
cubre el ciclo de vida completo de desarrollo y producción desde la fase de análisis de requisitos a través del
diseño detallado y de arquitectura, codificación, testeo, integración, validación y aceptación. Estos desarrollos de
software usan típicamente HOORA/UML para el análisis y modelado de requisitos, HRT-HOOD y Ada/C/C++
para el diseño e implementación.

El alcance de los desarrollos incluye software de aplicación de alto nivel así como servicios básicos de software
empotrado para el tratamiento de telemetría y tele-comandos, programación de tareas, detección de fallos,
aislamiento y recuperación y controladores de dispositivos.
Además de desarrollos para misiones específicas, DEIMOS Space realiza y participa en estudios tecnológicos
dirigidos a mejorar el estado del arte del software empotrado en tiempo real.
 1. Software de control de vuelo: DEIMOS Space tiene capacidad para desarrollar software embarcado de
control de vuelo critico en seguridad para: Sistemas de Control de órbita y Altitud (AOCS); Sistemas de
Medida y Control de Altitud (ACMS); sistemas de Guiado, Navegación y Control (GNC). Se aplican técnicas de
aseguramiento de productos software tales como análisis de Fiabilidad, Disponibilidad, Mantenibilidad y
28  Seguridad (RAMS); Análisis del árbol de Fallos (FTA); Análisis de Criticidad y Efectos de Modo Fallo (FMECA);
Análisis de Efectos de Errores Software (SEEA).

## Diapositiva 29

CASO DE ESTUDIO ATRIBUTOS DE CALIDAD:
DEIMOS

 2. Software de tratamiento de Datos a Bordo: DEIMOS Space puede desarrollar software para subsistemas de
Gestión de Datos a bordo (OBDH) que utiliza memoria de almacenamiento masivo, recogida y envío de
telemetría, recepción y distribución de tele-comandos, gestión del interface de la plataforma de vuelo, y tareas
de mantenimiento autónomo del sistema.

 3. Software de control de Instrumentos: DEIMOS Space tiene capacidad para desarrollar software empotrado
de tiempo real para ordenadores encargados de controlar instrumentos científicos a bordo de satélites y
sondas espaciales. Típicamente el software realiza funciones especificas de comando y control de instrumentos,
procesamiento de datos científicos y mantenimiento, control y monitorización del interface del instrumento y
gestión de modos.
 4. Validación de software de Segmento Espacio: DEIMOS Space puede realizar validación de software usando
técnicas en línea con el estado del arte y entornos de testeo, e incluyendo métodos de análisis estático y
dinámico.
 5. Simulación de Sistemas Embarcados: DEIMOS Space complementa sus actividades en el rea de software
embarcado con experiencia en simulación como medio para apoyar el desarrollo, validación y análisis de
29  productos software. Para mas información acerca de las actividades de DEIMOS Space en el campo de Sistemas
en Tiempo Real, por favor contacte con D. Mike Rennie.

## Diapositiva 30

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

30
Complementaria:
1. Tutorial de JavaEE 8 https://javaee.github.io/tutorial/

## Diapositiva 31

¿Preguntas?

Andrés Armando Sánchez Martín – febrero de 2023

## Diapositiva 32

PARA LA PRÓXIMA CLASE

 ¿Qué compone una arquitectura?
 ¿Cuáles son los tipos de ambientes del software?

 ¿Cuáles son los patrones y estilos de arquitectura
mas usados en la actualidad?
Taller:
 Entregar Documento con la identificación de los
Atributos de Calidad, Escenarios de Calidad y Los
Acuerdos para cada Caso de Estudio.
32
 Entrega clase 4.2
