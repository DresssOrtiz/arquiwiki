# ARQUIWIKI

## Guion del video de sustentación · Arquitectura de Software

Pontificia Universidad Javeriana · Santiago Hernández Barbosa · Tomás Ramírez Roa · Andrés David Ortiz Forero · Noviembre de 2026

Duración objetivo: 17 minutos (admite ajustes entre 15 y 18). Guion de grabación preparado para los tres integrantes. Las intervenciones y demostraciones quedan asignadas; únicamente las afirmaciones sobre funcionamiento y cifras marcadas «COMPLETAR CON EVIDENCIA» se ajustarán después de las pruebas. Este archivo es material de producción para el repositorio, no un cuarto entregable académico.

# 1. Orden de intervención y qué debe mostrarse

00:00–00:50 — Andrés: portada, problema y objetivo de la comparación.

00:50–03:10 — Andrés: conocimiento, RAG, LLM Wiki, Obsidian, agentes y MCP.

03:10–04:30 — Andrés: cinco matrices y decisiones arquitectónicas principales.

04:30–07:10 — Tomás: arquitectura implementada, Docker, CRUD COMPLETO de Fuente y Página y permisos MCP.

07:10–09:40 — Santiago: vault, ingesta, consulta CON ARCHIVADO de respuesta y auditoría de KB-A.

09:40–11:20 — Tomás: consultas de KB-B mediante RAG y registro de fuentes.

11:20–12:50 — Santiago: agente Ingeniero de Sistemas y skills ejecutados.

12:50–15:20 — Andrés: diseño del experimento, rúbrica, lectura de resultados cuando existan.

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

«Encontramos relaciones útiles: una wiki compartida tiene semejanzas con el patrón Blackboard; un RAG vectorial puede organizarse como etapas de procesamiento, semejantes a Pipes and Filters; y MCP ayuda a desacoplar clientes de herramientas mediante contratos. No aplicamos SOLID mecánicamente a programas completos como Obsidian: lo analizamos en los componentes y sus responsabilidades. Las ofertas laborales consultadas muestran interés en agentes, RAG y MCP, pero tres ofertas verificadas no representan todo el mercado colombiano». 

## 04:30–07:10 · Tomás — Arquitectura y API

[EN PANTALLA: repositorio ArquiWiki y, cuando exista, diagrama arquitectónico aprobado]. «Para implementar el proyecto separamos la API de gestión, el servicio RAG, el gateway MCP y el almacenamiento. Esta separación permite analizar responsabilidades y probar cada componente. Ahora muestro cómo se comunican en la implementación real». 

[MOSTRAR EN VIVO: `docker compose ps` y servicios realmente activos]. «Este es el despliegue observado. Ahora ejecutaré el CRUD completo de Fuente y Página: crear (POST), consultar (GET), actualizar (PUT) y eliminar (DELETE). Para cada entidad mostraremos la solicitud, su código HTTP y la respuesta». [MOSTRAR: POST, GET, PUT y DELETE en Fuente y Página, usando datos de demostración; verificar las respuestas y eliminar solo esos registros].

[MOSTRAR: una operación permitida y otra rechazada por permisos en MCP, solo si ambas fueron probadas]. «El servidor MCP define herramientas y permisos por rol. Aquí verificamos qué operación se permite, cuál se bloquea y dónde queda registrada». [COMPLETAR CON EVIDENCIA: nombres exactos de endpoints, estados HTTP, controles ejecutados y un límite o fallo observado]. «Con esto paso al sistema de wiki, que mostrará Santiago». 

## 07:10–09:40 · Santiago — LLM Wiki en Obsidian

[MOSTRAR: carpeta real del vault abierta en Obsidian]. «Esta es la alternativa KB-A. Las fuentes originales están separadas de las páginas producidas para consulta. En la demostración utilizaremos documentos reales del curso y podremos distinguir cada fuente de su síntesis». 

[MOSTRAR EN VIVO: proceso real de ingesta por el agente, o un registro de ejecución si el procesamiento tarda demasiado]. «El agente ingestor lee una fuente, extrae conceptos y crea o actualiza una página. No basta con generar texto: necesitamos rastrear qué documento respalda cada afirmación». [MOSTRAR: página generada y referencia verificable a una diapositiva].

[MOSTRAR: consulta al agente, respuesta con fuente y archivo de esa consulta en `wiki/consultas/`]. «El agente consultor responde usando la wiki y guarda un registro Markdown de la pregunta y la respuesta en su carpeta autorizada». [MOSTRAR: la página de consulta creada y su cita al documento de origen]. «El auditor revisa enlaces, estructura e inconsistencias; el mantenimiento de índices generales, cuando aplique, corresponde al ingestor u otro proceso expresamente autorizado, no al consultor». [MOSTRAR: salida real de auditoría]. [COMPLETAR CON EVIDENCIA: archivo, permisos efectivos y resultados observados].

## 09:40–11:20 · Tomás — RAG

[MOSTRAR: proceso real de indexación sobre las mismas fuentes, estado del almacén vectorial y consulta a KB-B]. «La alternativa KB-B mantiene los documentos recuperables mediante un servicio RAG. Al preguntar, el sistema encuentra fragmentos, aporta ese contexto y produce una respuesta. En pantalla se observan las fuentes recuperadas y los registros disponibles». 

[MOSTRAR: una misma pregunta de las quince, sin suministrar la respuesta de referencia al sistema]. «Esta pregunta es idéntica a la utilizada para KB-A. Registramos los fragmentos citados, la respuesta, el tiempo y los tokens que la herramienta realmente reporte». [COMPLETAR CON EVIDENCIA: fuente recuperada, respuesta verificable, latencia y tokens reales; si una métrica no está disponible, decirlo]. «Este registro permite comparar resultados sin suponer que usar RAG garantiza exactitud». 

## 11:20–12:50 · Santiago — Agente Ingeniero de Sistemas

[MOSTRAR: agente y archivo de instrucciones, solo si están implementados]. «Además del comparativo, el proyecto contempla un agente enfocado en tareas de Ingeniería de Sistemas. Su utilidad está en integrar herramientas específicas dentro de un flujo de trabajo». 

[MOSTRAR: tres skills ejecutados con salidas auténticas]. «Primero, un skill de modelado arquitectónico para apoyar un modelo C4 o UML; segundo, criterios de aceptación en formato Dado/Cuando/Entonces; y tercero, una revisión orientativa apoyada en normas ISO. Esta revisión no debe confundirse con una certificación oficial». [COMPLETAR CON EVIDENCIA: nombre de cada skill, ejemplo de entrada y salida real. Si alguno no está implementado, debe indicarse expresamente y no simular su ejecución].

## 12:50–15:20 · Andrés — Método y resultados

[EN PANTALLA: metodología y tipos de preguntas]. «Diseñamos quince preguntas basadas en seis presentaciones del curso: cinco puntuales, cuatro de síntesis entre clases, cuatro de aplicación a escenarios hipotéticos del proyecto y dos que no pueden responderse con el material disponible. Así evaluamos tanto recuperación como razonamiento y prudencia. Las dos bases reciben el mismo texto; las claves y la rúbrica se mantienen fuera de las herramientas que contestan». 

«La rúbrica tiene diez puntos: cuatro por exactitud factual, tres por trazabilidad de fuentes, dos por cobertura y uno por prudencia al afirmar. Cada cita debe conducir al documento y, cuando sea posible, a la diapositiva correspondiente. Los PDF de clase se convierten a Markdown y se cotejan antes de cargarlos por igual en ambos sistemas. Para evitar que la wiki aprenda de preguntas anteriores en la comparación principal, restauramos el estado inicial entre pruebas; el archivado se muestra como funcionalidad, pero se evalúa por separado como posible acumulación. También registramos tokens, tiempos, costos de construcción y actualización sin mezclar unidades distintas». 

[EN PANTALLA: tabla de resultados SOLO cuando haya datos]. «Después de ejecutar las pruebas obtuvimos los siguientes registros: [COMPLETAR: total de preguntas probadas, repeticiones y errores]. En calidad, KB-A obtuvo [DATO REAL] y KB-B [DATO REAL]; la mediana de latencia fue [DATO REAL] frente a [DATO REAL]. El consumo de tokens medido fue [DATO REAL] frente a [DATO REAL], especificando qué contabilizó cada sistema». [SI NO HAY MEDICIONES: reemplazar esta última oración por «Todavía no hay registros suficientemente verificables para comparar cifras y, por eso, no declaramos un ganador»].

«La diferencia entre construir una base y consultarla es decisiva. Una wiki puede requerir más procesamiento al principio; un RAG puede consumir recursos durante la recuperación y generación. No mezclamos tokens de embeddings con los tokens de generación del modelo. Finalmente, nuestros resultados solo permiten describir este prototipo y estas preguntas; no demostrar que una tecnología sea universalmente superior». 

## 15:20–17:00 · Conclusiones y cierre compartidos

[ANDRÉS] «En términos conceptuales, encontramos dos compromisos de diseño: una wiki acumula síntesis que debe mantenerse, mientras RAG consulta fragmentos de las fuentes al responder. Ambos necesitan control de calidad, trazabilidad y manejo de cambios. Esta es una conclusión del diseño, independientemente de los números». 

[TOMÁS] «En la implementación verificamos [COMPLETAR CON EVIDENCIA: componentes ejecutados, comportamiento observable y principal dificultad]. El aprendizaje arquitectónico fue [COMPLETAR: decisión técnica justificada y su consecuencia]». 

[SANTIAGO] «En el flujo de agentes observamos [COMPLETAR CON EVIDENCIA: ingesta, consulta, auditoría y resultado observable]. La principal limitación que identificamos fue [COMPLETAR: límite real del sistema]». 

[ANDRÉS] «La comparación de las respuestas indica [COMPLETAR SOLO CON RESULTADOS: diferencia de exactitud, fuentes, costo y validez]. Por el tamaño limitado de la evaluación, nuestros hallazgos se interpretan como un ejercicio exploratorio. Gracias». 

# 3. Checklist concreta para la grabación

Andrés: portada, conceptos, matriz-resumen de cinco criterios, explicación de rúbrica y captura de tabla de resultados una vez medida. El discurso conceptual y metodológico está listo para ensayo.

Tomás: arquitectura verificada, contenedores activos y CRUD completo por POST, GET, PUT y DELETE en Fuente y Página; controles MCP y consulta RAG con métricas. No mostrar contraseñas, tokens ni secretos.

Santiago: Obsidian con fuentes de clase convertidas a Markdown, páginas generadas, una ingesta real, una consulta con cita y archivo dentro de `wiki/consultas/`, una auditoría y agente Ingeniero de Sistemas cuando sus skills estén probados. La edición y publicación del video corresponde a Santiago.

Producción: Santiago coordina montaje, edición y publicación de un solo video público; Andrés prepara guion y narración de sus bloques; Tomás y Santiago preparan y narran las demostraciones de sus componentes. Audio entendible, pantalla legible, créditos y enlace final en el repositorio. No sustituir demostraciones por capturas ficticias.

# 4. Pendientes finales que NO deben inventarse

COMPLETAR CON TOMÁS: rutas exactas de POST/GET/PUT/DELETE para Fuente y Página, respuestas HTTP de la demo, contenedores activos, controles MCP, recuperación RAG y métricas.

COMPLETAR CON SANTIAGO: Markdown de clases verificado, ingesta, consulta con archivo en `wiki/consultas/`, auditoría y ejecución real de los tres skills previstos.

COMPLETAR CON ANDRÉS: modelos de arquitectura cuando se elaboren, puntuaciones, conclusión empírica y narración de sus segmentos; la edición y publicación del video corresponde a Santiago.

La duración se ajusta con los tiempos de las demostraciones; el libreto no debe forzar a los integrantes a afirmar que una prueba pasó si no la ejecutaron.
