# Requisitos y trazabilidad del MVP

| ID | Criterio de aceptación | Componente | Evidencia |
|---|---|---|---|
| RF01 | Consulta institucional devuelve respuesta y procedencia | rag.ask y API chat | respuestas_http.json |
| RF02 | Programa y modalidad no transfieren reglas entre contextos | retrieve y selectores | test_scope.py e integracion_http.json |
| RF03 | Fuentes muestran título, sección, página aplicable, URL y extracto | Source y componente sources | Interfaz y contrato OpenAPI |
| RF04 | Falta de evidencia produce aclaración o abstención | Guardas y validación | Casos negativos P09–P12 y P15–P17 |
| RF05 | Chat muestra carga, historial temporal y limpieza | React | navegador.md y capturas |
| RF06 | Catálogo y preparación pueden consultarse | API catalog y health | integracion_http.json |
| RNF01 | Consulta de 1–2000 caracteres; contexto válido | Pydantic | test_api.py |
| RNF02 | Errores sin rutas o secretos y bloqueo liberado | API | test_api.py |
| RNF03 | Código separado de documentos y modelos | .gitignore y comandos | Inventario y README |
| RNF04 | Un solo origen local sin exponer Ollama | Despliegue | API y exportación estática |

El público objetivo incluye todos los pregrados; el corpus no demuestra cobertura específica de todos los programas. ETIC es particular. La utilidad con usuarios y el desempeño a escala no son criterios demostrados en este corte.
