Redactaría el escenario con los seis componentes de la wiki (raw/3-1-atributos-de-calidad-2.md, diap. 6). Es un escenario de uso: el sistema se usa y se describe su comportamiento en tiempo de ejecución, velocidad de respuesta y throughput (raw/3-1-atributos-de-calidad-2.md, diap. 7). Pertenece al atributo eficiencia de desempeño, que compara el tiempo entre pedido y respuesta con el esperado o el máximo tolerado (raw/2-2-atributos-de-calidad-1.md, diap. 22).

| Componente | Definición en la wiki | Aplicado a tu caso |
|---|---|---|
| Fuente | Persona o sistema que inicia el estímulo | Clientes o aplicaciones que consultan la API de ArquiWiki |
| Estímulo | Evento que requiere que el sistema responda | 60 solicitudes de consulta simultáneas |
| Artefacto | Parte del sistema o el sistema completo | La API de consultas |
| Entorno | Circunstancias operativas; siempre debe definirse, incluso si es "normal" | Operación normal, con 60 solicitudes concurrentes |
| Respuesta | Acción visible externamente | La API procesa cada consulta y devuelve su resultado |
| Medida de respuesta | Criterio de éxito, específico y medible | Ver abajo |

**Medida de éxito.** La wiki no trae el umbral de tu caso. El 5 y el 95 % que uso abajo son valores que propongo yo, no vienen de las fuentes. Una redacción posible sería: «el 95 % de las 60 consultas simultáneas responde en menos de 5 segundos». El ejemplo de la wiki sigue ese patrón: un usuario ve los resultados de búsqueda en menos de 5 segundos con carga de 2 búsquedas por segundo (raw/3-1-atributos-de-calidad-2.md, diap. 10). Ese ejemplo se prioriza como High/High: importancia para el cliente y dificultad para el arquitecto (raw/3-1-atributos-de-calidad-2.md, diap. 10).

**Escenario completo (propuesto).** «Cuando clientes envían 60 consultas simultáneas a la API en operación normal, la API las procesa y responde a cada una; el 95 % se responde en menos de 5 s.»

**Tácticas relacionadas.** Cada escenario se asocia con tácticas que controlan su respuesta (raw/3-2-atributos-de-calidad-3.md, diap. 12). Las de eficiencia de ejecución se agrupan en demanda, gestión y arbitraje de recursos. Entre ellas están concurrencia, réplicas, aumentar recursos y políticas de planificación de tareas (raw/3-2-atributos-de-calidad-3.md, diap. 19). La wiki advierte que la conversión no permite asignar con certeza cada táctica a su categoría.

## Fuentes
- Wiki: [[wiki/conceptos/escenarios-de-calidad|Escenarios de calidad]], [[wiki/conceptos/eficiencia-de-desempeno|Eficiencia de desempeño]], [[wiki/conceptos/tacticas-de-eficiencia-de-ejecucion|Tácticas de eficiencia de ejecución]]
- Raw: raw/3-1-atributos-de-calidad-2.md, diap. 6, 7 y 10 (la diap. 6 la verifiqué en el fuente); raw/2-2-atributos-de-calidad-1.md, diap. 22; raw/3-2-atributos-de-calidad-3.md, diap. 12 y 19

Vacíos: la wiki no contiene información sobre umbrales ni percentiles para una API de consultas. Los ejemplos de escenario general de las diap. 8-9 son solo imagen y no están en el texto convertido.