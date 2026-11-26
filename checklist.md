# ARQUIWIKI — CONTROL DE COBERTURA Y PENDIENTES

Arquitectura de Software · Andrés David Ortiz Forero (persona A) · Control al 25 de noviembre de 2026

Esta checklist es un archivo auxiliar del repositorio; no crea un cuarto entregable. La entrega del equipo tiene tres piezas: (1) documento único de investigación; (2) presentación en Canva; (3) repositorio GitHub con código, archivos editables y evidencias. «☑» significa contenido o evidencia disponible; «☐» significa pendiente o sin prueba verificable. No se marca como completado un sistema solo porque exista código.

# 1. Estado de las ocho responsabilidades de A

☑ 1. Investigación de cinco temas: LLM Wiki, Obsidian, agentes, MCP y RAG incluidos en el capítulo 1 del documento.

☑ 2. Investigación adicional del profesor: tipos y comparación de RAG, funcionamiento de LLM Wiki, vínculo con agentes, evolución, casos de uso, mercado e ISO en el capítulo 2.

☑ 3. Cinco matrices terminadas y auditadas en el capítulo 3 del documento principal: SOLID, calidad ISO/IEC 25010:2023, tácticas, patrones y mercado laboral. Se verificaron las cinco tablas y se ajustaron celdas y paginación. La muestra laboral se limita a tres vacantes verificadas; Mercado Libre no se evalúa.

◐ 4. Diagramas arquitectónicos: HLD, C4 de Contexto y UML de paquetes de API, Gateway MCP y RAG ya incorporados al documento (cinco figuras). ☐ Quedan los C4 de Contenedores, Componentes del sistema, Dinámico y Despliegue, sujetos a validar la integración. Existe además una vista C4 de componentes del Gateway que no sustituye sus diagramas UML.

☑ 5a. Quince preguntas redactadas (5/4/4/2), referencias cotejadas y correcciones de P03/P04 incorporadas. ☑ 5b. Rúbrica de 0–10 definida. ☑ 5c. Preguntas sin respuestas, rúbrica y plantilla de evaluación separadas en `experiment/`, fuera del vault indexado. ☐ 5d. Ejecutar ambas bases, calificar y analizar resultados reales (requiere B/C).

☑ 6. Presentación conceptual lista en el Canva original: diez diapositivas, un solo HLD, metodología 5/4/4/2 y tres ofertas laborales verificadas. Los resultados experimentales se añadirán únicamente cuando B/C entreguen evidencia auténtica.

☑ 7. Checklist de cobertura realizada y revisada en Google Drive. Se mantendrá actualizada como documento de seguimiento mientras el equipo termina la implementación y entrega; esa actualización continua no deja incompleta la tarea personal de control.

☑ 8. Guion del video terminado por Andrés: estructura, libreto para los tres integrantes, pruebas previstas, metodología y cierre. El video es responsabilidad compartida; las demostraciones y cifras auténticas se incorporarán al grabar. Santiago coordina edición y publicación. Andrés debe grabar sus intervenciones, pero la redacción del guion está finalizada.

# 2. Documento único de investigación

☑ Portada académica con nombres, profesor y escudo de la universidad, adaptada del Laboratorio 2.

☑ Capítulos 1 y 2: investigación principal y nota extra.

☑ Capítulo 3: cinco matrices editables revisadas en contenido, consistencia de filas, valoración, términos ISO y presentación. Se corrigieron observabilidad, disponibilidad, seguridad operacional y paginación para evitar tablas partidas.

☑ Capítulo 4: diseño del experimento, 15 preguntas, claves, rúbrica y protocolo documentados. ☑ Material operativo de preguntas/rúbrica separado en `experiment/`. ☐ Ejecutar, verificar y analizar los resultados auténticos de KB-A y KB-B.

◐ Capítulo 5: cinco diagramas incorporados (HLD, C4 de Contexto, UML API, UML Gateway MCP y UML RAG). Faltan los otros cuatro modelos C4.

☐ Capítulo 6: resultados medidos y análisis; requiere logs y respuestas auténticas de KB-A y KB-B.

☑ Revisión general de bibliografía y coherencia del documento: enlace ISO/IEC 25010:2023, Gist LLM Wiki, encuesta Stack Overflow 2026 y documentación principal consultables; se corrigieron referencias desactualizadas a los diagramas y se retiró una referencia docente duplicada. ☑ Las cinco matrices se muestran completas en páginas separadas del PDF (39 páginas). ⚠ Las tablas están a 9 pt y pueden requerir ampliación si el profesor pide lectura en impresión.

# 3. Presentación en Canva

☑ Presentación original de Canva actualizada a diez diapositivas: portada, problema, conceptos, herramientas, matrices, un único HLD, método y cierre provisional.

☑ Nombres de los tres integrantes y del profesor incorporados en la portada de Canva.

☑ Hallazgos y límites de las matrices integrados en la presentación preliminar de Canva; la metodología 5/4/4/2 también fue incorporada.

☑ La presentación ya incluye el HLD requerido por el guion. Los modelos C4 y UML adicionales permanecen en el documento de investigación y no se duplican en Canva. ☐ Incorporar resultados finales solo tras recibir mediciones verificadas de KB-A y KB-B.

☐ Sustituir la lámina de estado por resultados medidos y conclusiones verificables cuando se reciban de B/C.

# 4. Archivos editables destinados a GitHub

☑ Investigación y cinco tablas maestras conservadas en el documento original de Drive. ☑ Las cinco matrices se exportaron sin reinterpretar sus celdas a Markdown editable en `docs/matrices/` de GitHub, con enlace de regreso al documento maestro.

☑ Preguntas y respuestas de referencia conservadas en el capítulo 4 del documento principal. ☑ En `experiment/preguntas.md` se publicó SOLO el enunciado de las 15 preguntas. Las claves no están en el vault ni en el archivo que reciben los sistemas; no deben entregarse a los agentes.

☑ Rúbrica documentada en Drive y disponible como `experiment/rubrica.md` en GitHub; plantilla vacía de calificación en `experiment/plantilla-evaluacion.csv`. Ninguno de estos archivos forma parte del corpus indexado.

☑ Guion redactado en Drive y archivo `video/guion.md` presente en GitHub. ☐ Verificar que la última versión en Drive y el Markdown del repositorio coincidan antes de entregar.

☑ Checklist editada en el documento original de Drive y sincronizada como `checklist.md` en GitHub (última auditoría de matrices, corpus, enlaces y estado del PDF de presentación).

☑ Cinco diagramas PNG y seis PDF originales publicados. ☑ Seis Markdown (183/183 encabezados de diapositiva) estructuralmente verificados, y 28 diapositivas gráficas relevantes revisadas visualmente. ⚠ Los diagramas visuales no quedan totalmente representados por el texto extraído (p. ej., 1.2 diap. 11/21 y 3.1 diap. 8/9). La diapositiva 31 de 1.2 ya se reconstruyó. ☐ Cotejar y transcribir fielmente las relaciones de los gráficos relevantes con Santiago antes de congelar nuevamente el corpus; NO modificar los archivos raw mientras B/C ejecuten las corridas definitivas. ☐ Publicar fuentes editables .drawio de los diagramas existentes si están disponibles.

☑ Se comprobaron 26 enlaces internos de los documentos principales del repositorio: no hay rutas internas rotas. ☑ Canva mantiene la presentación original con diez diapositivas. ☐ Volver a exportar `presentacion/presentacion.pdf` desde Canva: el PDF publicado precede la última actualización del diseño (no se puede certificar que contenga las diez). ☐ Añadir enlace del video cuando esté publicado y verificar su reproducción.

# 5. Información y evidencia de Tomás (B)

☑ Existen en GitHub archivos de API/CRUD, RAG, Docker y gateway MCP; eso prueba código escrito, NO ejecución integral.

◐ Existen evidencias de ejecución local en `docs/bitacora.md`: Docker Compose healthy, `scripts/smoke.sh`, `mcp_check.py` y RAG reindexado con corpus real. ☐ Confirmar reproducción de la demostración final y conservar sus registros reales.

☐ Demostrar operaciones de Fuente y Página y pruebas de permisos de MCP.

☐ Usar exactamente los mismos archivos Markdown revisados que KB-A, con referencias a documento y diapositiva. ☐ Obtener respuestas, citas, tokens y tiempos. ☐ Restaurar estado inicial entre preguntas o documentar el aislamiento equivalente.

☐ Compartir fragmentos reales de su demo y un hallazgo técnico verificable para guion/conclusiones.

# 6. Información y evidencia de Santiago (C)

☑ Estructura de vault publicada y seis Markdown reales con referencias por diapositiva. ☐ Santiago debe realizar el cotejo visual de láminas gráficas y mostrar ingesta, consulta con archivado y lint usando el corpus real; coordina el video.

☐ Demostrar con agentes ingesta, consulta y auditoría; guardar fuentes y registros.

☑ Agente Ingeniero de Sistemas y tres skills disponibles (`modelar`, `criterios-aceptacion`, `evaluar-iso`) con pruebas de instalación y ejemplos. ☐ Validar en demo las tres ejecuciones y las salidas reales correspondientes al caso requerido por el docente.

☐ Ejecutar las 15 preguntas sobre el mismo corpus y con estado controlado; compartir respuestas, citas, tiempos y tokens disponibles. ☐ Mostrar archivado de una respuesta como página en demostración separada.

☐ Compartir grabaciones/capturas auténticas para el video.

# 7. Reglas de cierre

No hay ganador entre KB-A y KB-B hasta ejecutar las mismas preguntas con las mismas fuentes y comparar evidencia verificable. No mezclar documentos sintéticos de prueba con fuentes académicas. No declarar cumplida una característica arquitectónica solo por haberla descrito. Separar evidencias de implementación de propuestas conceptuales. Cada casilla se actualizará cuando exista el archivo o la prueba correspondiente.

Documento: https://docs.google.com/document/d/1uFmCr0120qSVLiMvn05fTBuXrhV1pCGu08XgdMnWA38/edit

Presentación: https://www.canva.com/d/kGASGIjBrTgCsAa

Repositorio: https://github.com/DresssOrtiz/arquiwiki

Guion: https://docs.google.com/document/d/1ppXKEFwHOFFCjVWrD1GOWT3ME4-x5gSlOXaol0pQpt4/edit
