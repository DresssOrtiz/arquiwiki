# ARQUIWIKI

## Guion del video de sustentación · Arquitectura de Software

Pontificia Universidad Javeriana · Santiago Hernández Barbosa · Tomás Ramírez Roa · Andrés David Ortiz Forero · Noviembre de 2026

Duración objetivo: 17 minutos (admite ajustes entre 15 y 18). Guion de grabación preparado para los tres integrantes. Las intervenciones y demostraciones quedan asignadas; se incorporan evidencias guardadas por Tomás y Santiago, sin presentar este libreto como una grabación ya realizada. Las referencias visuales corresponden al material previsto para la grabación. La calificación es asistida y provisional, pendiente de Andrés. Este archivo es material de producción para el repositorio, no un cuarto entregable académico.

# 1. Orden de intervención y qué debe mostrarse

00:00–00:50 — Andrés: portada, problema y objetivo de la comparación.

00:50–03:10 — Andrés: conocimiento, RAG, LLM Wiki, Obsidian, agentes y MCP.

03:10–04:30 — Andrés: cinco matrices y decisiones arquitectónicas principales.

04:30–07:10 — Tomás: arquitectura implementada, Docker, CRUD completo de Fuente y Página y permisos MCP.

07:10–09:40 — Santiago: vault, ingesta, consulta y estado del archivado de respuesta y auditoría de KB-A.

09:40–11:20 — Tomás: consultas de KB-B mediante RAG y registro de fuentes.

11:20–12:50 — Santiago: agente Ingeniero de Sistemas y estado de las tres skills.

12:50–15:20 — Andrés: diseño del experimento, rúbrica, lectura de los resultados exploratorios disponibles.

15:20–17:00 — Los tres: conclusiones respaldadas por evidencia, límites y cierre.

# 2. Libreto de grabación (texto que puede leerse en voz alta)

## 00:00–00:50 · Andrés — Apertura

[EN PANTALLA: portada «ArquiWiki» con asignatura e integrantes]. «Hola. Somos Santiago Hernández Barbosa, Tomás Ramírez Roa y Andrés David Ortiz Forero, del curso de Arquitectura de Software de la Pontificia Universidad Javeriana. Nuestro proyecto se llama ArquiWiki. Vamos a comparar dos maneras de organizar y consultar documentación con ayuda de inteligencia artificial: una wiki de páginas persistentes mantenida por agentes, y un sistema RAG que recupera información antes de responder. El objetivo no es defender una tecnología desde el principio, sino estudiar su funcionamiento, su arquitectura y su desempeño con evidencia comparable».

## 00:50–03:10 · Andrés — Marco conceptual

[EN PANTALLA: diapositiva «Base de conocimiento»]. «Una base de conocimiento es información organizada de forma que pueda consultarse y verificarse. No es lo mismo que un modelo de lenguaje: el contenido puede estar en documentos, páginas Markdown o índices externos, y el modelo lo utiliza cuando necesita responder».

[EN PANTALLA: diapositiva «RAG»]. «RAG significa generación aumentada por recuperación. Primero se preparan e indexan documentos. Después, cuando llega una pregunta, se recuperan fragmentos relevantes y se le entregan al modelo para responder. Hay RAG básico, avanzado y modular; por ejemplo, un sistema puede mejorar la consulta, combinar búsquedas o reordenar fragmentos. Su riesgo principal no es únicamente que el modelo se equivoque: también puede ocurrir que no encuentre la evidencia correcta».

[EN PANTALLA: diapositiva «LLM Wiki»]. «La propuesta LLM Wiki, presentada por Andrej Karpathy en 2026, plantea que un agente mantenga páginas de conocimiento sintetizadas y enlazadas. Distinguimos tres operaciones: ingesta de fuentes, consulta de páginas y auditoría o lint. La diferencia con RAG es que aquí se intenta conservar y mantener una síntesis entre consultas. Esto también crea un riesgo: un error puede quedar guardado y volver a utilizarse».

[EN PANTALLA: diapositiva «Herramientas y roles»]. «Obsidian es la herramienta con la que podemos navegar los archivos Markdown y sus conexiones; por sí sola no es una inteligencia artificial. Los agentes reciben tareas: ingestor, consultor y auditor. MCP, por su parte, es un protocolo para conectar esos agentes con herramientas y recursos. La idea es permitir operaciones definidas y restringidas; el uso de MCP no reemplaza los controles de permisos».

## 03:10–04:30 · Andrés — Matrices

[EN PANTALLA: resumen de cinco matrices del documento, sin convertirlas en diagramas]. «Evaluamos cinco temas —LLM Wiki, Obsidian, agentes, MCP y RAG— desde cinco perspectivas: SOLID, atributos de calidad ISO/IEC 25010, tácticas, patrones arquitectónicos y mercado laboral. Es importante distinguir las valoraciones teóricas de los resultados medidos: por ejemplo, una buena separación de componentes puede favorecer la mantenibilidad, pero no demuestra que el sistema tenga un tiempo de respuesta determinado».

«Encontramos relaciones útiles: una wiki compartida tiene semejanzas con el patrón Blackboard; un RAG vectorial puede organizarse como etapas de procesamiento, semejantes a Pipes and Filters; y MCP ayuda a desacoplar clientes de herramientas mediante contratos. No aplicamos SOLID mecánicamente a programas completos como Obsidian: lo analizamos en los componentes y sus responsabilidades. Las ofertas laborales consultadas muestran interés en agentes, RAG y MCP, pero las tres ofertas verificadas no representan todo el mercado colombiano».

## 04:30–07:10 · Tomás — Arquitectura y API

[EN PANTALLA: repositorio ArquiWiki y HLD]. «Para implementar el proyecto separamos la API de gestión, el servicio RAG, el gateway MCP y el almacenamiento. Esta separación permite analizar responsabilidades y probar cada componente. Ahora muestro cómo se comunican en la implementación real».

[MOSTRAR EN VIVO: `docker compose ps` y servicios realmente activos]. «Este es el despliegue observado. Ahora ejecutaré el CRUD completo de Fuente y Página: crear (POST), consultar (GET), actualizar (PUT) y eliminar (DELETE). Para cada entidad mostraremos la solicitud, su código HTTP y la respuesta». [MOSTRAR: POST, GET, PUT y DELETE en Fuente y Página, usando datos de demostración; verificar las respuestas y eliminar solo esos registros].

[MOSTRAR: una operación permitida y otra rechazada por permisos en MCP, solo si ambas fueron probadas]. «El servidor MCP define herramientas y permisos por rol. Aquí verificamos qué operación se permite, cuál se bloquea y dónde queda registrada». «La verificación documentó creación de fuentes y páginas con 201, consulta y actualización de página con 200, asociación mediante PUT /paginas/{id}/fuentes/{fuente_id}, eliminación con 204 y casos de título repetido 409, tipo inválido 422 y recurso eliminado 404. El gateway devolvió 401 sin token, bloqueó escritura en raw y rutas con `..`, y permitió al consultor escribir solo en wiki/consultas/. Estos resultados están en docs/evidencia-B.md. La verificación posterior corrigió un contador que truncaba fragmentos largos del RAG».

«Con esto paso al sistema de wiki, que mostrará Santiago».

## 07:10–09:40 · Santiago — LLM Wiki en Obsidian

[MOSTRAR: carpeta real del vault abierta en Obsidian]. «Esta es la alternativa KB-A. Las fuentes originales están separadas de las páginas producidas para consulta. En la demostración utilizaremos documentos reales del curso y podremos distinguir cada fuente de su síntesis».

[MOSTRAR EN VIVO: proceso real de ingesta por el agente, o un registro de ejecución si el procesamiento tarda demasiado]. «El agente ingestor lee una fuente, extrae conceptos y crea o actualiza una página. No basta con generar texto: necesitamos rastrear qué documento respalda cada afirmación». [MOSTRAR: página generada y referencia verificable a una diapositiva].

[EN PANTALLA: consulta histórica con fuente. El archivado en `wiki/consultas/` corresponde a una demostración separada, pendiente de grabación.] «El consultor responde usando la wiki. El modo de demostración permite archivar en su carpeta autorizada; en el experimento se bloquea la escritura para evitar acumulación de respuestas entre preguntas». [EN PANTALLA: cita al documento de origen]. «El auditor revisa enlaces, estructura e inconsistencias; el mantenimiento de índices generales, cuando aplique, corresponde al ingestor u otro proceso expresamente autorizado, no al consultor». [MOSTRAR: salida real de auditoría]. «Con el corpus real quedaron registrados seis procesos de ingesta, un lint y una corrección. El lint informó cinco hallazgos bajos y la corrección declaró aplicarlos; las 54 páginas recibieron estado ok. Puede consultarse experiment/results/kba_runs.jsonl y los archivos de cada ejecución. Ese estado es resultado de la auditoría automatizada, no una garantía de fidelidad completa a las imágenes de los PDF».

## 09:40–11:20 · Tomás — RAG

[MOSTRAR: proceso real de indexación sobre las mismas fuentes, estado del almacén vectorial y consulta a KB-B]. «La alternativa KB-B mantiene los documentos recuperables mediante un servicio RAG. Al preguntar, el sistema encuentra fragmentos, aporta ese contexto y produce una respuesta. En pantalla se observan las fuentes recuperadas y los registros disponibles».

[MOSTRAR: una misma pregunta de las quince, sin suministrar la respuesta de referencia al sistema]. «Esta pregunta es idéntica a la utilizada para KB-A. Registramos los fragmentos citados, la respuesta, el tiempo y los tokens que la herramienta realmente reporte». «La verificación de Tomás para P03, con use_llm:false y k igual a cinco, recuperó las diapositivas 41 y 42 de 1.2, que definen SRP y DIP, en 22 milisegundos de recuperación. Esa petición no generó texto con un LLM. Para las treinta respuestas del experimento, Santiago usó el mismo modelo del CLI en ambos brazos; KB-B recibió los fragmentos y generó sin herramientas. Son dos verificaciones distintas».

«Este registro permite comparar resultados sin suponer que usar RAG garantiza exactitud».

## 11:20–12:50 · Santiago — Agente Ingeniero de Sistemas

[MOSTRAR: agente-ing-sistemas/.claude/agents/ingeniero-sistemas.md y sus tres directorios de skills; implementación presente.] «Además del comparativo, el proyecto contempla un agente enfocado en tareas de Ingeniería de Sistemas. Su utilidad está en integrar herramientas específicas dentro de un flujo de trabajo».

[EN PANTALLA: skills implementadas y ejemplos existentes; demostración completa del requisito definitivo pendiente.] «Primero, un skill de modelado arquitectónico para apoyar un modelo C4 o UML; segundo, criterios de aceptación en formato Dado/Cuando/Entonces; y tercero, una revisión orientativa apoyada en normas ISO. Esta revisión no debe confundirse con una certificación oficial». «Las tres skills implementadas son modelar, criterios-aceptacion y evaluar-iso. El README documenta una comprobación de precarga del subagente y la salida de criterios con seis componentes. Existen ejemplos de modelos y Gherkin, pero no los presentamos como evidencia de ejecución completa sobre el requisito final del profesor».

## 12:50–15:20 · Andrés — Método y resultados

[EN PANTALLA: metodología y tipos de preguntas]. «Diseñamos quince preguntas basadas en seis presentaciones del curso: cinco puntuales, cuatro de síntesis entre clases, cuatro de aplicación a escenarios hipotéticos del proyecto y dos que no pueden responderse con el material disponible. Así evaluamos tanto recuperación como razonamiento y prudencia. Las dos bases reciben el mismo texto; las claves y la rúbrica se mantienen fuera de las herramientas que contestan».

«La rúbrica tiene diez puntos: cuatro por exactitud factual, tres por trazabilidad de fuentes, dos por cobertura y uno por prudencia al afirmar. Cada cita debe conducir al documento y, cuando sea posible, a la diapositiva correspondiente. Los PDF se convierten a Markdown; el cotejo actual confirmó 183 marcadores y revisó visualmente 50 láminas, pero faltan 133 y varias imágenes pierden información. No podemos afirmar que la conversión esté completamente validada. Para evitar que la wiki aprenda de preguntas anteriores en la comparación principal, restauramos el estado inicial entre pruebas; el archivado se muestra como funcionalidad, pero se evalúa por separado como posible acumulación. Registramos tokens, tiempos y construcción sin mezclar unidades; el costo de actualización y el overhead controlado no se midieron».

[EN PANTALLA: tablas de experiment/results/analisis-provisional.md, rótulo «exploratorio»]. «Tenemos treinta respuestas guardadas: quince por alternativa, una repetición y cero errores de proceso. La evaluación asistida provisional propone 9,27 sobre diez para KB-A y 7,67 para KB-B; las treinta notas siguen pendientes de validación humana. No es calificación humana ciega. La mediana de latencia fue 16,52 segundos frente a 7,33, y la entrada media registrada del LLM fue 41 417 frente a 2 962 tokens, incluyendo caché. La salida acumulada fue 22 634 frente a 10 256 tokens».

«Hay dos límites decisivos: después de esa corrida se corrigió la diapositiva 31 del corpus y el truncamiento de fragmentos del RAG. Por eso P02 y P09 no prueban que RAG sea inferior. Ambos sistemas evitaron inventar los datos experimentales que faltaban en P14 y P15. Estos son resultados exploratorios; no declaramos ganador ni significancia estadística».

«La diferencia entre construir una base y consultarla es decisiva. Una wiki puede requerir más procesamiento al principio; un RAG puede consumir recursos durante la recuperación y generación. No mezclamos tokens de embeddings con los tokens de generación del modelo. Finalmente, nuestros resultados solo permiten describir este prototipo y estas preguntas; no demostrar que una tecnología sea universalmente superior».

## 15:20–17:00 · Conclusiones y cierre compartidos

[ANDRÉS] «En términos conceptuales, encontramos dos compromisos de diseño: una wiki acumula síntesis que debe mantenerse, mientras RAG consulta fragmentos de las fuentes al responder. Ambos necesitan control de calidad, trazabilidad y manejo de cambios. Esta es una conclusión del diseño, independientemente de los números».

[TOMÁS] «En la implementación verificamos cuatro servicios saludables, CRUD y relaciones N:M, permisos por rol y recuperación RAG. Identificamos que el contador de tokens limitaba la fragmentación y dejaba texto fuera de la ventana del modelo. El aprendizaje arquitectónico fue corregir el contador y ajustar el tamaño de fragmento: la verificación documentada pasó de 189 a 280 fragmentos, sin exceder la ventana, aunque todavía no se repitió el experimento».

[SANTIAGO] «En el flujo de agentes observamos seis ingestas reales, lint, corrección y quince consultas de KB-A con registros individuales. La principal limitación que identificamos fue que una síntesis puede conservar omisiones de las imágenes y que reescribir páginas completas incrementa el procesamiento. El estado ok de la wiki no elimina la necesidad de cotejar el PDF».

[ANDRÉS] «La comparación de las respuestas indica diferencias descriptivas de cobertura, tokens y tiempos en la versión histórica. Las notas asistidas requieren validación y las correcciones posteriores impiden trasladar esas diferencias al sistema actual. Por el tamaño limitado de la evaluación, nuestros hallazgos se interpretan como un ejercicio exploratorio. Gracias».

# 3. Estado del material audiovisual

La grabación, el montaje y el enlace público están pendientes. El material previsto comprende arquitectura, CRUD de Fuente/Página y asociación N:M, permisos MCP, navegación de wiki, registros de ingesta/lint/corrección, recuperación RAG y resultados exploratorios.

La demostración de archivado es independiente del modo experimental de solo lectura. La demostración completa de las tres skills sobre el requisito definitivo aún no dispone de evidencia suficiente; los ejemplos sintéticos existentes no la sustituyen. La generación nativa de RAG no se ejecutó en la verificación documentada de Tomás por falta de clave API.

La evaluación asistida sigue pendiente de validación humana. El costo de actualización y el overhead controlado del CLI no se midieron. Las cifras históricas no describen el rendimiento del recuperador posterior al PR #9.

Referencias: [evidencia B](../docs/evidencia-B.md), [bitácora](../docs/bitacora.md), [análisis provisional](../experiment/results/analisis-provisional.md), [CSV asistido](../experiment/results/calificacion-asistida-provisional.csv) y [paquete de skills](../agente-ing-sistemas/README.md).
