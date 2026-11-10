# Arquitectura del MVP

Navegador con React y Next.js → FastAPI en 127.0.0.1:8000 → núcleo RAG → ChromaDB local y Ollama en 127.0.0.1:11434.

La exportación estática frontend/out se sirve desde FastAPI, después de declarar las rutas API. Los comandos fetch, prepare e index se ejecutan por terminal y no se exponen por HTTP. No se necesita CORS ni un puerto adicional para la demostración compilada.

## Preparación

Fuentes públicas → descarga y SHA-256 → extracción → limpieza → fragmentos con página o sección → embeddings → colección poli_pregrados_v3.

## Consulta

1. Validar longitud, programa y modalidad.
2. Rechazar con 429 si existe una generación en curso.
3. Filtrar metadatos y recuperar hasta cuatro fragmentos.
4. Aplicar aclaración o abstención cuando corresponde.
5. Para conclusiones ETIC específicas, devolver la sección literal identificada como extractiva.
6. En las demás consultas, generar JSON con Qwen3 y validar referencias y estructura.
7. Devolver texto, fuentes, fragmentos y estado al navegador.

## Contrato

GET /api/v1/catalog devuelve programas, modalidades y cobertura. GET /api/v1/health comprueba Ollama, modelos e índice. POST /api/v1/chat recibe question, program y modality, y devuelve answer, sources, insufficient, seconds y model. OpenAPI está disponible en /openapi.json y /docs.

## Límites

El servicio se enlaza a loopback. No incorpora autenticación ni aislamiento entre usuarios para exposición pública. Una consulta simultánea es el límite del prototipo; el historial vive en memoria de la página y cada pregunta se resuelve independientemente. No se guardan consultas web en archivos de aplicación; el evaluador sí registra las preguntas del piloto.
