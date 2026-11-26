# Evaluación ISO: RF-01 y RNF-01-S

> Evaluación asistida; cotejar con el texto oficial de cada norma. Requisito de ejemplo; reemplazar por el RF real del SRS de MANI.

## Fuentes consultadas
- Wiki: sin páginas en `wiki/conceptos/` al momento de generar el ejemplo. Se usaron `raw/clase-03-atributos-calidad-muestra.md` (muestra) y las references de la skill. Wiki no disponible para citas definitivas.
- Artefactos evaluados: `requisito.md`, `modelo.dsl`, `paquetes.puml`, `secuencia.puml`, `decisiones.md`, `criterios.feature`.

## 1. ISO/IEC 25010:2023 (calidad del producto)
| Característica | ¿La toca? | Evidencia en criterios | ¿Verificable? | Brecha |
|---|---|---|---|---|
| Idoneidad funcional | Sí | Escenarios de registro e inicio de sesión (feliz, borde, error) | Sí | No hay criterio para la verificación del correo (qué pasa si el enlace expira). |
| Eficiencia de desempeño | Indirecta | Ninguna | No | Falta un tiempo máximo de respuesta para autenticar. |
| Compatibilidad | Indirecta | Ninguna | No | Integración con el servicio de correo sin criterio de fallo (qué hace el registro si el correo no sale). |
| Capacidad de interacción | Sí | Mensajes de error literales en 400, 401, 409, 423 | Parcial | No se verifica protección ante errores del usuario más allá de mensajes; sin criterio de accesibilidad. |
| Fiabilidad | Indirecta | Ninguna | No | Sin criterio de disponibilidad del servicio de autenticación. |
| Seguridad | Sí | Escenario `@calidad` de fuerza bruta; hash con sal; expiración de token | Sí | Faltan: cifrado en tránsito (TLS), política de contraseñas más allá de longitud, cierre de sesión, auditoría de inicios exitosos. |
| Mantenibilidad | Indirecta | Ninguna (la separación en capas está en `paquetes.puml`) | No | Sin criterio de pruebas ni de cambio del algoritmo de hash. |
| Flexibilidad | No | n/a (sin requisito de escalabilidad o despliegue) | n/a | Ninguna por ahora. |
| Protección (safety) | No | n/a (sin riesgo físico o ambiental) | n/a | Ninguna. |

## 2. ISO/IEC/IEEE 29148 (requisitos)
Se evalúa el RF-01 y el RNF-01-S. Conjunto: no evaluable con solo dos requisitos.

| Característica | Veredicto | Evidencia | Reescritura sugerida |
|---|---|---|---|
| Necesario | Cumple | RNF-03 del extracto de SRS exige usuario autenticado en escrituras | n/a |
| Apropiado | Cumple | RF-01 no dicta tecnología | n/a |
| Inequívoco | No cumple | RNF-01-S: "proteger" y "accesos no autorizados" sin definir | "El sistema debe bloquear una cuenta durante 15 minutos tras 5 intentos fallidos de inicio de sesión en 15 minutos." |
| Completo | Parcial | RF-01 no define campos, reglas de contraseña ni verificación de correo | "El sistema debe aceptar contraseñas de 8 a 128 caracteres y rechazar correos con formato inválido." |
| Singular | No cumple | RF-01 combina registro e inicio de sesión | Separar: RF-01a (registro) y RF-01b (inicio de sesión). |
| Factible | Cumple | Práctica común con tecnología estándar | n/a |
| Verificable | Parcial | RF-01 verificable; RNF-01-S no tiene medida | Ver reescritura de inequívoco; añadir "las contraseñas se almacenan solo como hash con sal". |
| Correcto | Parcial | No hay fuente identificada para RNF-01-S | Registrar interesado y fuente (cliente, docente) y validar los umbrales. |
| Conforme | Parcial | Tiene identificador, pero RF-01 no usa "debe" con actor y condición completos | "Cuando una persona no registrada envíe un correo válido y una contraseña válida, el sistema debe crear su cuenta." |

## 3. ISO/IEC/IEEE 42010 (descripción de arquitectura)
| Elemento | ¿Presente? | Evidencia | Brecha |
|---|---|---|---|
| Entidad de interés | Presente | Sistema "MANI" en `modelo.dsl` | Ninguna |
| Stakeholders | Parcial | Solo "Usuario" y servicio de correo | Faltan administrador, equipo de seguridad, docente. |
| Preocupaciones | Parcial | Seguridad en `requisito.md` y `decisiones.md` | No hay lista explícita de preocupaciones por stakeholder. |
| Puntos de vista | Parcial | C4 (contexto, contenedores, componentes, dinámica) y UML (paquetes, secuencia) | No se declara qué preocupación cubre cada punto de vista. |
| Vistas | Presente | Cuatro vistas en `modelo.dsl`, `paquetes.puml`, `secuencia.puml` | Ninguna |
| Correspondencias | Parcial | Nombres coherentes entre DSL y UML | `Cliente de correo` aparece en paquetes pero no como componente en el DSL; no hay tabla de correspondencias. |
| Justificación de decisiones | Parcial | `decisiones.md` con cinco decisiones | Solo D1 y D2 tienen fuente; faltan alternativas descartadas. |
| Conformidad | Parcial | Seguridad cubierta por vistas y decisiones | Confidencialidad en tránsito (TLS) no aparece en ninguna vista. |

## 4. Resumen
El requisito funcional es verificable gracias a los criterios, pero el requisito de seguridad llega vago y solo se vuelve medible con los supuestos de los criterios. La arquitectura cubre la seguridad con vistas coherentes, pero la descripción es débil en stakeholders, correspondencias y alternativas. Los umbrales (5 intentos, 15 y 30 minutos) son supuestos sin validar.

## 5. Acciones priorizadas
| # | Prioridad | Acción | Artefacto | Responsable |
|---|---|---|---|---|
| 1 | Alta | Reescribir RNF-01-S con medidas (bloqueo, hash, expiración) y validar umbrales con el cliente | `requisito.md` | Analista |
| 2 | Alta | Separar RF-01 en registro e inicio de sesión | `requisito.md` | Analista |
| 3 | Media | Añadir criterios de TLS, cierre de sesión y fallo del servicio de correo | `criterios.feature` | QA |
| 4 | Media | Declarar stakeholders, preocupaciones y tabla de correspondencias | `decisiones.md` | Arquitecto |
| 5 | Baja | Registrar alternativas descartadas por decisión (p. ej., sesión en servidor frente a token) | `decisiones.md` | Arquitecto |
