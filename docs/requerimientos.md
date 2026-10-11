# Requerimientos y criterios de aceptación

El anteproyecto propone 14 requerimientos funcionales y 8 no funcionales. Esta entrega implementa el núcleo técnico hasta semana 9.

| Requerimiento | Criterio verificable | Estado previsto de esta entrega |
|---|---|---|
| RF04 y RF05 Procesar y recuperar | Consulta en español devuelve hasta cuatro fragmentos con ID y metadatos | Núcleo por terminal |
| RF06 Generar | Qwen3 4B recibe solo contexto recuperado e instrucciones especializadas | Núcleo por terminal |
| RF08 Fuentes | Toda fuente devuelta coincide con un fragmento recuperado | Validación estructural |
| RF09 Ausencia de evidencia | Mensaje explícito cuando no hay evidencia o las referencias son inválidas | Control y prueba piloto |
| RF12 Evidencia técnica | Reportes JSON reproducibles con latencia y configuración | Implementado para piloto |
| RF13 Actualizar corpus | Descarga, preparación y reconstrucción explícita del índice | Administración por comandos |
| RF14 Evaluación | Ejecutar piloto con preguntas positivas, negativas y adversarial | Piloto de 12 casos |
| RF01-RF03 RF07 RF10 RF11 | Acceso web, conversación, historial y nuevas preguntas | Semanas 10-12 |
| RNF02 Trazabilidad | Documento, URL, sección/página, versión | Metadatos por fragmento |
| RNF04 Seguridad | Sin claves ni información de estudiantes en corpus público | Revisión de archivos publicados |
| RNF05 Mantenibilidad | Funciones separadas de extracción, embeddings, recuperación y generación | Código modular inicial |
| RNF01 Rendimiento | Registrar latencia observada antes de fijar un SLA | Medición piloto |
| RNF03 RNF07 | Disponibilidad y usabilidad web | Pendientes de interfaz |
| RNF06 | Incorporar nuevas fuentes con inventario y reindexación | Proceso manual |
| RNF08 | Abstención ante falta de evidencia | Control inicial; requiere evaluación amplia |

La meta final de al menos 80 % de respuestas correctas y sustentadas se evaluará en semanas 13-14 con 50-80 preguntas. La recuperación de un documento no prueba que todos los hechos de una respuesta estén sustentados. La validez de una referencia tampoco prueba por sí sola exactitud semántica.
