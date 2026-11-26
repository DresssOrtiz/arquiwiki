# ARQUIWIKI — CONTROL DE COBERTURA Y PENDIENTES

Arquitectura de Software · Andrés David Ortiz Forero (persona A) · Control al 25 de noviembre de 2026

Esta checklist es un archivo auxiliar del repositorio; no crea un cuarto entregable. La entrega del equipo tiene tres piezas: (1) documento único de investigación; (2) presentación en Canva; (3) repositorio GitHub con código, archivos editables y evidencias. «☑» significa contenido o evidencia disponible; «☐» significa pendiente o sin prueba verificable. No se marca como completado un sistema solo porque exista código.

# 1. Estado de las ocho responsabilidades de A

☑ 1. Investigación de cinco temas: LLM Wiki, Obsidian, agentes, MCP y RAG incluidos en el capítulo 1 del documento.

☑ 2. Investigación adicional del profesor: tipos y comparación de RAG, funcionamiento de LLM Wiki, vínculo con agentes, evolución, casos de uso, mercado e ISO en el capítulo 2.

☑ 3. Cinco matrices terminadas y auditadas en el capítulo 3 del documento principal: SOLID, calidad ISO/IEC 25010:2023, tácticas, patrones y mercado laboral. Se verificaron las cinco tablas y se ajustaron celdas y paginación. La muestra laboral se limita a tres vacantes verificadas; Mercado Libre no se evalúa.

◐ 4. Diagramas arquitectónicos: HLD, C4 de Contexto y UML de paquetes de API, Gateway MCP y RAG ya incorporados al documento (cinco figuras). ☐ Quedan los C4 de Contenedores, Componentes del sistema, Dinámico y Despliegue, sujetos a validar la integración. Existe además una vista C4 de componentes del Gateway que no sustituye sus diagramas UML.

☑ 5a. Quince preguntas redactadas en esquema 5/4/4/2 y referencias cotejadas con las diapositivas del profesor. Corregidas P03 (diapositivas 41–42) y P04 (seis componentes del escenario). ☑ 5b. Rúbrica escrita. ☐ 5c. Carga equivalente de Markdown en KB-A/KB-B. ☐ 5d. Experimento, calificación y análisis pendiente de B/C.

☑ 6. Presentación conceptual lista en el Canva original: diez diapositivas, un solo HLD, metodología 5/4/4/2 y tres ofertas laborales verificadas. Los resultados experimentales se añadirán únicamente cuando B/C entreguen evidencia auténtica.

☑ 7. Checklist de cobertura realizada y revisada en Google Drive. Se mantendrá actualizada como documento de seguimiento mientras el equipo termina la implementación y entrega; esa actualización continua no deja incompleta la tarea personal de control.

☑ 8. Guion del video terminado por Andrés: estructura, libreto para los tres integrantes, pruebas previstas, metodología y cierre. El video es responsabilidad compartida; las demostraciones y cifras auténticas se incorporarán al grabar. Santiago coordina edición y publicación. Andrés debe grabar sus intervenciones, pero la redacción del guion está finalizada.

# 2. Documento único de investigación

☑ Portada académica con nombres, profesor y escudo de la universidad, adaptada del Laboratorio 2.

☑ Capítulos 1 y 2: investigación principal y nota extra.

☑ Capítulo 3: cinco matrices editables revisadas en contenido, consistencia de filas, valoración, términos ISO y presentación. Se corrigieron observabilidad, disponibilidad, seguridad operacional y paginación para evitar tablas partidas.

☑ Capítulo 4: preguntas y claves, rúbrica, protocolo de estados restaurados, conversión de PDF a Markdown y control de fuga de respuestas. ☐ Ejecutar, verificar y analizar.

◐ Capítulo 5: cinco diagramas incorporados (HLD, C4 de Contexto, UML API, UML Gateway MCP y UML RAG). Faltan los otros cuatro modelos C4.

☐ Capítulo 6: resultados medidos y análisis; requiere logs y respuestas auténticas de KB-A y KB-B.

☐ Bibliografía y maquetación finales por revisar por Andrés antes de publicar.

# 3. Presentación en Canva

☑ Presentación original de Canva actualizada a diez diapositivas: portada, problema, conceptos, herramientas, matrices, un único HLD, método y cierre provisional.

☑ Nombres de los tres integrantes y del profesor incorporados en la portada de Canva.

☑ Hallazgos y límites de las matrices integrados en la presentación preliminar de Canva; la metodología 5/4/4/2 también fue incorporada.

☑ La presentación ya incluye el HLD requerido por el guion. Los modelos C4 y UML adicionales permanecen en el documento de investigación y no se duplican en Canva. ☐ Incorporar resultados finales solo tras recibir mediciones verificadas de KB-A y KB-B.

☐ Sustituir la lámina de estado por resultados medidos y conclusiones verificables cuando se reciban de B/C.

# 4. Archivos editables destinados a GitHub

☑ Fuente de investigación completa y matrices dentro del documento maestro de Drive.

☑ Preguntas y claves en el capítulo 4. ☐ Al preparar el repositorio, separar la lista enviada a KB-A/KB-B de las respuestas de referencia y excluir las claves de cualquier carpeta indexada o accesible a los agentes.

☑ Rúbrica del experimento escrita; ☐ convertir a archivo editable del repositorio.

☑ Guion redactado en Drive y archivo `video/guion.md` presente en GitHub. ☐ Verificar que la última versión en Drive y el Markdown del repositorio coincidan antes de entregar.

☑ Checklist de control escrita en Drive y `checklist.md` sincronizado en GitHub con esta exportación verificada.

☑ Cinco diagramas PNG publicados en `docs/diagramas/` de GitHub. ☑ Seis PDF originales del curso publicados en `docs/corpus-original/` (commit `9450e164a5`). ☐ Convertir y cotejar el corpus Markdown compartido entre KB-A/KB-B (Santiago y Tomás). ☐ Añadir fuentes editables .drawio, matrices exportadas y resultados únicamente después de medir.

☑ Enlace de la presentación publicado en el README. ☐ Publicar el enlace del video cuando esté disponible. ☐ Comprobar enlaces y estructura del README antes de la entrega final.

# 5. Información y evidencia de Tomás (B)

☑ Existen en GitHub archivos de API/CRUD, RAG, Docker y gateway MCP; eso prueba código escrito, NO ejecución integral.

☐ Entregar salida reproducible de Docker Compose y scripts de pruebas.

☐ Demostrar operaciones de Fuente y Página y pruebas de permisos de MCP.

☐ Usar exactamente los mismos archivos Markdown revisados que KB-A, con referencias a documento y diapositiva. ☐ Obtener respuestas, citas, tokens y tiempos. ☐ Restaurar estado inicial entre preguntas o documentar el aislamiento equivalente.

☐ Compartir fragmentos reales de su demo y un hallazgo técnico verificable para guion/conclusiones.

# 6. Información y evidencia de Santiago (C)

☐ Confirmar vault y corpus convertido a Markdown con referencias a documento y diapositiva. ☐ Mostrar ingesta, consulta, archivado de respuesta y lint. C coordina el video.

☐ Demostrar con agentes ingesta, consulta y auditoría; guardar fuentes y registros.

☐ Confirmar agente Ingeniero de Sistemas y sus tres skills con entrada/salida reales; no simular salidas.

☐ Ejecutar las 15 preguntas sobre el mismo corpus y con estado controlado; compartir respuestas, citas, tiempos y tokens disponibles. ☐ Mostrar archivado de una respuesta como página en demostración separada.

☐ Compartir grabaciones/capturas auténticas para el video.

# 7. Reglas de cierre

No hay ganador entre KB-A y KB-B hasta ejecutar las mismas preguntas con las mismas fuentes y comparar evidencia verificable. No mezclar documentos sintéticos de prueba con fuentes académicas. No declarar cumplida una característica arquitectónica solo por haberla descrito. Separar evidencias de implementación de propuestas conceptuales. Cada casilla se actualizará cuando exista el archivo o la prueba correspondiente.

Documento: https://docs.google.com/document/d/1uFmCr0120qSVLiMvn05fTBuXrhV1pCGu08XgdMnWA38/edit

Presentación: https://www.canva.com/d/kGASGIjBrTgCsAa

Repositorio: https://github.com/DresssOrtiz/arquiwiki

Guion: https://docs.google.com/document/d/1ppXKEFwHOFFCjVWrD1GOWT3ME4-x5gSlOXaol0pQpt4/edit
