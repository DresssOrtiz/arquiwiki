---
titulo: Arquitectura de software
tipo: concepto
fuentes:
  - raw/1-2-definiciones-1.md#Diapositiva 18
  - raw/1-2-definiciones-1.md#Diapositiva 20
  - raw/1-2-definiciones-1.md#Diapositiva 24
  - raw/1-2-definiciones-1.md#Diapositiva 25
  - raw/1-2-definiciones-1.md#Diapositiva 26
  - raw/2-1-definiciones-2.md#Diapositiva 4
  - raw/2-1-definiciones-2.md#Diapositiva 6
enlaces:
  - ISO/IEC/IEEE 42010
  - Arquitectura vs diseño
  - Arquitecto de software
  - Ley de Conway
  - Arquitectura ágil
  - Patrones arquitectónicos
  - Estilos arquitectónicos
  - Proceso de arquitectura
  - Atributos de calidad
estado_salud: ok
actualizado: 2026-11-25
---

# Arquitectura de software

## Resumen
Estructura de alto nivel de un sistema: elementos de software, sus relaciones y las propiedades de ambos, junto con las decisiones principales de diseño.

## Desarrollo
- En sentido general, "architecture" es el proceso y producto de planificar, diseñar y construir edificios u otras estructuras, con tres cualidades: utilitas (utilidad), firmitas (durabilidad) y venustas (elegancia) (raw/1-2-definiciones-1.md, diap. 18).
- Definición ISO/IEC/IEEE 42010:2011: conceptos fundamentales o propiedades de un sistema en su entorno, representados por sus elementos, relaciones y los principios de su diseño y evolución. La descripción de arquitectura es el producto de trabajo explícito (modelos, texto o gráficos); "architecting" es el proceso de crear una arquitectura (raw/1-2-definiciones-1.md, diap. 24).
- La arquitectura comprende elementos de software, relaciones entre ellos y propiedades de ambos (raw/1-2-definiciones-1.md, diap. 24).
- Otras definiciones (raw/1-2-definiciones-1.md, diap. 25):
  - Bass, Clements & Kazman (2003): estructura del sistema compuesta por elementos de software, sus propiedades visibles y sus relaciones.
  - Taylor (2010): conjunto de decisiones principales de diseño tomadas para el sistema.
  - Fowler (2002): la arquitectura se reduce a las cosas importantes, cualesquiera que sean.
  - Definición de la clase: diseño conceptual de una solución que muestra componentes, funciones y estructura general, y cómo se comunican y relacionan.
- Características: múltiples cambios de contexto, servicio/producto virtual, sin límites físicos habituales, disciplina relativamente nueva de la que se puede aprender de otras (raw/1-2-definiciones-1.md, diap. 26).
- Niveles: la diapositiva distingue arquitectura empresarial, de sistemas y de software, y roles de arquitecto empresarial, de solución y técnico (raw/1-2-definiciones-1.md, diap. 20).
- Un patrón arquitectónico no es una arquitectura como tal: delinea elementos cohesivos esenciales, y muchas arquitecturas pueden implementar el mismo patrón (raw/2-1-definiciones-2.md, diap. 4). Un estilo restringe las decisiones arquitectónicas específicas de un contexto (raw/2-1-definiciones-2.md, diap. 6).

## Relaciones
- [[wiki/entidades/iso-iec-ieee-42010|ISO/IEC/IEEE 42010]]: fuente de la definición normativa.
- [[wiki/comparaciones/arquitectura-vs-diseno|Arquitectura vs diseño]]: qué decisiones son arquitectónicas.
- [[wiki/conceptos/arquitecto-de-software|Arquitecto de software]]: quien la define y la mantiene.
- [[wiki/conceptos/ley-de-conway|Ley de Conway]]: relación con la estructura de comunicación.
- [[wiki/conceptos/arquitectura-agil|Arquitectura ágil]]: arquitectura en contextos ágiles.
- [[wiki/conceptos/patrones-arquitectonicos|Patrones arquitectónicos]]: conceptos que delinean parte de ella.
- [[wiki/conceptos/estilos-arquitectonicos|Estilos arquitectónicos]]: restringen sus decisiones.
- [[wiki/conceptos/proceso-de-arquitectura|Proceso de arquitectura]]: cómo se produce.
- [[wiki/conceptos/atributos-de-calidad|Atributos de calidad]]: entrada del diseño arquitectónico.

## Fuentes
- raw/1-2-definiciones-1.md, diap. 18: arquitectura general.
- raw/1-2-definiciones-1.md, diap. 20: niveles.
- raw/1-2-definiciones-1.md, diap. 24-25: definiciones.
- raw/1-2-definiciones-1.md, diap. 26: características.
- raw/2-1-definiciones-2.md, diap. 4 y 6: patrón y estilo frente a arquitectura.
