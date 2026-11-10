# Metodología de desarrollo incremental

El desarrollo individual se organiza en cuatro incrementos: I1 núcleo documental, I2 API, I3 interfaz e I4 integración. Cada incremento recorre análisis, diseño, implementación y pruebas. El producto se acepta al contrastar sus criterios con archivos, ejecuciones y registros observables.

| Incremento | Análisis y diseño | Implementación | Aceptación |
|---|---|---|---|
| I1 | Fuentes, metadatos y filtros | src/rag.py | Corpus no vacío, ámbito delimitado y fuentes trazables |
| I2 | Contrato HTTP y estados de error | src/api.py | Entradas inválidas rechazadas y errores saneados |
| I3 | Componentes y estados del chat | frontend/app/ | Carga, respuesta, contexto, historial temporal y fuentes |
| I4 | Flujo completo local | Exportación Next.js servida por FastAPI | Consulta real por navegador y piloto HTTP |

La ruta acotada de conclusiones ETIC devuelve literalmente la sección recuperada; se identifica como extractiva. Las demás consultas usan generación o controles de abstención. El historial no se envía al modelo. La evaluación amplia, validación independiente y pruebas de utilidad con estudiantes permanecen pendientes.

Referencia metodológica: NASA, SWE-019 Software Life Cycle, https://swehb.nasa.gov/spaces/7150/pages/16449735/SWE-019%2B-%2BSoftware%2BLife%2BCycle.
