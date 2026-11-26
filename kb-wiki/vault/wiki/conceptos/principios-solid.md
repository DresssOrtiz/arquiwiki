---
titulo: Principios SOLID
tipo: concepto
fuentes:
  - raw/1-2-definiciones-1.md#Diapositiva 41
  - raw/1-2-definiciones-1.md#Diapositiva 42
enlaces:
  - Características de la POO
  - Cohesión y acoplamiento
estado_salud: ok
actualizado: 2026-11-25
---

# Principios SOLID

## Resumen
Cinco principios de diseño orientado a objetos: SRP, OCP, LSP, ISP y DIP.

## Desarrollo
- **S – Single Responsibility (SRP):** una clase debería tener una, y solo una, razón para cambiar; Robert C. Martin identifica esa "razón para cambiar" como "responsabilidad" (raw/1-2-definiciones-1.md, diap. 41).
- **O – Open/Closed (OCP):** extender el comportamiento de una clase sin modificarla; abiertas a extensión, cerradas a modificación (raw/1-2-definiciones-1.md, diap. 41).
- **L – Liskov Substitution (LSP):** las clases derivadas deben poder sustituirse por sus clases base sin alterar el funcionamiento del sistema (raw/1-2-definiciones-1.md, diap. 41).
- **I – Interface Segregation (ISP):** interfaces específicas para un tipo de cliente, con una finalidad concreta (raw/1-2-definiciones-1.md, diap. 42).
- **D – Dependency Inversion (DIP):** depender de abstracciones, no de clases concretas; los módulos de alto nivel no deben depender de los de bajo nivel, y los detalles deben depender de las abstracciones (raw/1-2-definiciones-1.md, diap. 42).

## Relaciones
- [[wiki/conceptos/caracteristicas-poo|Características de la POO]]: base conceptual.
- [[wiki/conceptos/cohesion-y-acoplamiento|Cohesión y acoplamiento]]: se presentan junto a SOLID y POO.

## Fuentes
- raw/1-2-definiciones-1.md, diap. 41-42.
