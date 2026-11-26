# ARQUIWIKI — CONTROL DE COBERTURA Y PENDIENTES

Arquitectura de Software · Andrés David Ortiz Forero (persona A) · Control al 25 de noviembre de 2026

Esta checklist es un archivo auxiliar del repositorio; no crea un cuarto entregable. La entrega del equipo tiene tres piezas: (1) documento único de investigación; (2) presentación en Canva; (3) repositorio GitHub con código, archivos editables y evidencias. «☑» significa contenido o evidencia disponible; «☐» significa pendiente o sin prueba verificable. No se marca como completado un sistema solo porque exista código.

# 1. Estado de las ocho responsabilidades de A

☑ 1. Investigación de cinco temas: LLM Wiki, Obsidian, agentes, MCP y RAG incluidos en el capítulo 1 del documento.

☑ 2. Investigación adicional del profesor: tipos y comparación de RAG, funcionamiento de LLM Wiki, vínculo con agentes, evolución, casos de uso, mercado e ISO en el capítulo 2.

◐ 3. Cinco matrices desarrolladas y corregidas en Drive. Se corrigieron celdas cruzadas entre SOLID, compatibilidad y modificabilidad; la oferta de Mercado Libre queda sin evaluar. ☑ Auditoría de contenido completada y avance preliminar aprobado. ☐ Revisión editorial final del formato por Andrés. ☐ Documentar búsquedas en Indeed y Computrabajo si se mantiene ese alcance.

◐ 4. Diagramas arquitectónicos: HLD, C4 de Contexto y UML de paquetes de API, Gateway MCP y RAG ya incorporados al documento (cinco figuras). ☐ Quedan los C4 de Contenedores, Componentes del sistema, Dinámico y Despliegue, sujetos a validar la integración. Existe además una vista C4 de componentes del Gateway que no sustituye sus diagramas UML.

☑ 5a. Quince preguntas redactadas en esquema 5/4/4/2 y referencias cotejadas con las diapositivas del profesor. Corregidas P03 (diapositivas 41–42) y P04 (seis componentes del escenario). ☑ 5b. Rúbrica escrita. ☐ 5c. Carga equivalente de Markdown en KB-A/KB-B. ☐ 5d. Experimento, calificación y análisis pendiente de B/C.

☑ 6a. Presentación preliminar de diez diapositivas con portada, resultados conceptuales y método 5/4/4/2 actualizados. ☑ 6b. HLD integrado en la presentación. ☐ Seleccionar otros modelos pertinentes e incorporar resultados reales cuando estén disponibles.

☑ 7a. Checklist de cobertura actualizada con requisitos del curso, roles y evidencias. ☐ 7b. Verificación final contra implementación, video y tag público.

☑ 8a. Guion desarrollado con intervenciones de los tres integrantes, CRUD completo de Fuente y Página, consulta archivada de la wiki, pruebas y método. ☐ 8b. Ajustar nombres de rutas y resultados con evidencia de B/C. ☐ 8c. Grabar la narración de A. La coordinación, edición y publicación final corresponden a C.

# 2. Documento único de investigación

☑ Portada académica con nombres, profesor y escudo de la universidad, adaptada del Laboratorio 2.

☑ Capítulos 1 y 2: investigación principal y nota extra.

◐ Capítulo 3: cinco matrices editables y justificación revisada parcialmente; ☑ Celdas cruzadas corregidas y auditadas. ☐ Revisar anchos y saltos de tabla para la entrega final.

☑ Capítulo 4: preguntas y claves, rúbrica, protocolo de estados restaurados, conversión de PDF a Markdown y control de fuga de respuestas. ☐ Ejecutar, verificar y analizar.

◐ Capítulo 5: cinco diagramas incorporados (HLD, C4 de Contexto, UML API, UML Gateway MCP y UML RAG). Faltan los otros cuatro modelos C4.

☐ Capítulo 6: resultados medidos y análisis; requiere logs y respuestas auténticas de KB-A y KB-B.

☐ Bibliografía y maquetación finales por revisar por Andrés antes de publicar.

# 3. Presentación en Canva

☑ Presentación inicial existente en Canva: portada conceptual, objetivo, base de conocimiento, RAG, LLM Wiki, Obsidian/agentes/MCP, matrices, método y cierre provisional.

☑ Nombres de los tres integrantes y del profesor incorporados en la portada de Canva.

☑ Hallazgos y límites de las matrices integrados en la presentación preliminar de Canva; la metodología 5/4/4/2 también fue incorporada.

☑ Diagramas HLD, C4 Contexto y tres UML incorporados en el documento de investigación. ☑ HLD integrado en Canva. ☐ Seleccionar e integrar otros modelos pertinentes y actualizar las conclusiones con datos reales cuando existan.

☐ Sustituir la lámina de estado por resultados medidos y conclusiones verificables cuando se reciban de B/C.

# 4. Archivos editables destinados a GitHub

☑ Fuente de investigación completa y matrices dentro del documento maestro de Drive.

☑ Preguntas y claves en el capítulo 4. ☐ Al preparar el repositorio, separar la lista enviada a KB-A/KB-B de las respuestas de referencia y excluir las claves de cualquier carpeta indexada o accesible a los agentes.

☑ Rúbrica del experimento escrita; ☐ convertir a archivo editable del repositorio.

☑ Guion redactado en Drive y archivo `video/guion.md` presente en GitHub. ☐ Verificar que la última versión en Drive y el Markdown del repositorio coincidan antes de entregar.

☑ Checklist de control escrita en Drive y `checklist.md` publicado en GitHub. ☐ Sincronizar el archivo de GitHub con la última versión de Drive y verificarla.

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
