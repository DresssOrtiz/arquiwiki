# ArquiWiki: cobertura y estado de entrega

Arquitectura de Software · 25 de noviembre de 2026

☑ Contenido o evidencia disponible · ◐ Desarrollo provisional · ☐ Pendiente de validación o entrega.

## 1. Investigación y matrices

☑ Investigación de LLM Wiki, Obsidian, agentes de IA, MCP y RAG en el documento maestro.

☑ Investigación adicional: tipos de RAG, funcionamiento y evolución de LLM Wiki, casos de uso, mercado e ISO.

☑ Cinco matrices: SOLID, calidad ISO/IEC 25010:2023, tácticas, patrones y mercado laboral. La muestra laboral se limita a tres ofertas verificadas; Mercado Libre permanece sin evaluación.

☑ Matrices editables exportadas en [docs/matrices](docs/matrices/README.md). El documento maestro conserva las cinco matrices y nueve figuras; la exportación publicada requiere actualización.

## 2. Arquitectura y corpus

☑ Nueve diagramas en [docs/diagramas](docs/diagramas/): HLD; C4 Contexto, Contenedores, Componentes del Gateway, Dinámico y Despliegue; UML de paquetes API, Gateway y RAG.

☑ Seis PDF originales en [docs/corpus-original](docs/corpus-original/) y seis Markdown derivados en [raw](kb-wiki/vault/raw/), con 183/183 marcadores consecutivos.

◐ Revisión de fidelidad: control estructural/léxico de 183 páginas y revisión visual seleccionada de 50; quedan 133 sin revisión visual completa. Persisten pérdidas de relaciones gráficas, especialmente 1.2/11,21, 3.1/8-9 y 5.1/10,12-13. La corrección de 1.2/31 ya está incorporada y es posterior a la corrida.

☑ Cuatro muestras sintéticas conservadas fuera del corpus en [kb-wiki/muestras](kb-wiki/muestras/).

☐ Fuentes editables de los diagramas, si están disponibles.

## 3. Evaluación experimental

☑ Quince preguntas (5 puntuales, 4 de síntesis, 4 de aplicación, 2 de abstención), claves y rúbrica 0–10 disponibles fuera del corpus indexado en [experiment](experiment/README.md).

☑ Runner integrado mediante PR #7. Treinta respuestas históricas: quince por brazo, una repetición y cero errores de proceso. Control de línea base y modo de solo lectura de KB-A documentados.

◐ [Treinta calificaciones asistidas provisionales](experiment/results/calificacion-asistida-provisional.csv), con fuentes, justificaciones y observaciones; sin aprobación humana ni segundo evaluador. El CSV humano original conserva sus columnas de notas vacías.

☑ [Métricas descriptivas](experiment/results/metricas-experimento-provisional.json) y [análisis exploratorio](experiment/results/analisis-provisional.md). La corrida precede la corrección de corpus 1.2/31 y la del tokenizador RAG del PR #9; no demuestra un ganador definitivo ni significancia estadística.

☐ Validación humana de las calificaciones y definición del alcance final de las conclusiones.

☐ Costo de actualización y overhead controlado del CLI: sin registros de medición. Los incrementales sin cambios y el spike de desarrollo no sustituyen esos experimentos.

## 4. Implementación y pruebas documentadas

☑ PR #8: [evidencia del bloque B](docs/evidencia-B.md), con despliegue, CRUD de Fuente/Página, relación N:M, casos de error, autenticación/autorización MCP y recuperación RAG.

☑ PR #9: corrección del contador de tokens y ajuste de fragmentación. La verificación posterior registra 280 fragmentos y ninguno por encima de la ventana de 128 tokens; no corresponde a una repetición de las treinta respuestas.

☑ [Bitácora del bloque C](docs/bitacora.md): seis ingestas, lint, corrección y consultas con registros individuales. El estado `ok` de las 54 páginas es resultado del flujo automatizado, no una certificación de fidelidad al PDF.

☑ Agente Ingeniero de Sistemas y skills `modelar`, `criterios-aceptacion` y `evaluar-iso` implementados, con ejemplos y verificación documentada de precarga/criterios.

☐ Evidencia de una demostración completa de las tres skills sobre el requisito definitivo. Los ejemplos sintéticos no constituyen esa evidencia.

## 5. Documento, presentación y video

☑ Documento maestro con investigación, cinco matrices y nueve figuras; [PDF publicado](docs/investigacion.pdf) y fuente editable en Drive disponibles.

☐ Incorporación de resultados, discusión y conclusiones al documento maestro; nueva exportación desde la fuente original.

☑ Presentación original de diez diapositivas, con HLD y método 5/4/4/2.

☐ Actualización de resultados y estado de entrega en las láminas 9 y 10; nueva exportación desde el diseño original de Canva.

☑ [Guion](video/guion.md) con evidencias verificables y límites de la evaluación exploratoria.

☐ Grabaciones finales, demostración de archivado separada del experimento de solo lectura, demostración del requisito definitivo, montaje y publicación del video.

☐ Enlace público del video y comprobación de reproducción.

## 6. Límites de interpretación

La evidencia de implementación se distingue de las propuestas de diseño. Los resultados históricos se conservan separados de las verificaciones posteriores del corpus y del RAG. Una nueva evaluación requiere una versión común congelada y reconstrucción/reindexado de ambas bases; las cifras actuales describen la corrida exploratoria existente.

Fuentes originales: [Documento de investigación](https://docs.google.com/document/d/1uFmCr0120qSVLiMvn05fTBuXrhV1pCGu08XgdMnWA38/edit) · [Presentación](https://www.canva.com/d/kGASGIjBrTgCsAa) · [Guion original](https://docs.google.com/document/d/1ppXKEFwHOFFCjVWrD1GOWT3ME4-x5gSlOXaol0pQpt4/edit).
