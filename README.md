# Asistente RAG para trabajos de grado del Poli

MVP académico de Camila Alexandra Arias Ruiz para orientación documental de estudiantes de todos los pregrados y modalidades del Politécnico Grancolombiano. Integra un núcleo RAG, API y chat web local. No es un servicio oficial de la institución. La cobertura específica depende de las fuentes: el corpus del corte contiene cuatro fuentes, 140 fragmentos y apartados de trece programas virtuales, además de documentos generales y una plantilla particular.

## Instalación en Windows

### 1. Instalar herramientas y modelos

Instalar [Python 3.12](https://www.python.org/downloads/), [Git para Windows](https://git-scm.com/download/win), [Node.js 22 LTS](https://nodejs.org/en/download) y [Ollama para Windows](https://ollama.com/download/windows). Abrir Ollama desde Inicio y abrir una nueva terminal PowerShell para reconocer los comandos.

```powershell
py -3.12 --version
git --version
node --version
npm.cmd --version
ollama --version
ollama pull qwen3:4b
ollama pull embeddinggemma
ollama list
```

La instalación de dependencias Python no instala Ollama ni descarga modelos. Mantener Ollama disponible mientras se indexa y consulta. Si la aplicación no inicia el servicio, ejecutar `ollama serve` en otra terminal. El servicio se consulta en `http://127.0.0.1:11434`; no exponer ese puerto a internet. La instalación, las fuentes y los modelos necesitan internet y espacio disponible.

### 2. Obtener el proyecto y preparar Python

```powershell
git clone https://github.com/AriasCamilaA/asistente-rag-trabajos-grado-poli.git
cd asistente-rag-trabajos-grado-poli
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Los comandos usan el entorno llamado `.venv`, con punto inicial. No es necesario activarlo. Si ya se activó un entorno llamado `venv` o `.venv`, puede usarse `python` en lugar de `.\.venv\Scripts\python.exe`, comprobando antes `python --version`. No mezclar nombres de carpetas de entornos.

### 3. Descargar fuentes y construir el índice

```powershell
.\.venv\Scripts\python.exe -m src.rag fetch
.\.venv\Scripts\python.exe -m src.rag prepare
.\.venv\Scripts\python.exe -m src.rag index
```

`fetch` descarga las fuentes activas, incluido el [formato ETIC público](https://docs.google.com/document/d/1PnpQyZdOVSMS7cpWTau-sb3gmgzIZGGq/edit). `prepare` extrae y divide el contenido; `index` genera vectores y reconstruye `poli_pregrados_v3`. No se necesita copiar el formato manualmente mientras su enlace público siga disponible. Si una fuente deja de estar disponible, revisar su URL y autorización antes de actualizar la configuración.

### 4. Construir la interfaz

```powershell
npm.cmd ci --prefix frontend
npm.cmd run build --prefix frontend
```

Se fijan versiones en `frontend/package.json` y `package-lock.json`. La versión verificada es Next.js 15.5.29 con React 19.3.1. La exportación resultante queda en `frontend/out`; esta carpeta se genera localmente y no se publica en GitHub.

### 5. Iniciar la aplicación

Desde la raíz del repositorio, con Ollama abierto:

```powershell
.\.venv\Scripts\python.exe -m uvicorn src.api:app --host 127.0.0.1 --port 8000
```

Mantener esa terminal abierta y abrir **http://127.0.0.1:8000** en Edge. La documentación de la API está en **http://127.0.0.1:8000/docs**. No se necesita iniciar un segundo servidor para la interfaz compilada.

Seleccionar programa y modalidad cuando la pregunta requiera contexto particular. Consultar las fuentes desplegables de cada respuesta. El historial solo permanece en memoria de la página; las consultas son independientes y no se envían los mensajes anteriores al modelo. Limpiar la conversación o recargar elimina ese historial visible.

### 6. Volver a ejecutar y actualizar

Después de preparar la base y compilar la interfaz, basta con abrir Ollama e iniciar el comando de `uvicorn`. No repetir indexación por cada consulta. Para actualizar las fuentes, repetir `fetch`, `prepare` e `index`. Si cambia la extracción, repetir `prepare` e `index`; si cambia el modelo de embeddings, reconstruir el índice. Si cambia el frontend, repetir `npm.cmd ci --prefix frontend` cuando cambien dependencias y `npm.cmd run build --prefix frontend`.

La migración desde el corte anterior requiere repetir `prepare` e `index` para crear la colección `poli_pregrados_v3`; no se consulta automáticamente la colección antigua.

## Consulta por terminal

```powershell
.\.venv\Scripts\python.exe -m src.rag ask "¿Qué prerrequisitos exige el trabajo de grado?" --programa "Ingeniería Industrial" --modalidad virtual
.\.venv\Scripts\python.exe -m src.rag ask "¿Cuál es la extensión máxima del resumen ETIC?"
```

La consulta acotada sobre conclusiones ETIC devuelve literalmente la sección recuperada y se identifica como extractiva. Las demás consultas pasan por la generación o por los controles de aclaración y abstención. Esta ruta específica evita la reformulación imprecisa observada en el piloto; no demuestra fidelidad semántica para cualquier pregunta.

## Pruebas y evidencias del MVP

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```

Para repetir el piloto HTTP, iniciar la aplicación como se indicó antes y, en otra terminal desde la raíz del repositorio, ejecutar:

```powershell
.\.venv\Scripts\python.exe -m evaluacion.run_mvp
```

La ejecución del piloto escribe nuevos resultados en `evidencias/entrega_2/`. Guardar una copia de los reportes si se desea conservarlos antes de repetir. La evidencia registrada el 9 de noviembre de 2026 incluye **28 pruebas automatizadas aprobadas**, 18 consultas HTTP completadas, fuentes en 11 casos respondibles y abstención o aclaración en 7 casos negativos o ambiguos. La media HTTP fue 1,337 s en esa ejecución. Los casos conocidos se reutilizaron: estos resultados no representan una evaluación independiente ni la meta final de 50–80 preguntas. La ruta extractiva, la generación y la abstención tienen tiempos diferentes.

| Producto | Ubicación |
|---|---|
| API y contrato | `src/api.py`, `/docs` y `evidencias/entrega_2/openapi.json` |
| Interfaz | `frontend/app/` |
| Metodología y diseño | `docs/metodologia_desarrollo.md`, `docs/arquitectura.md` |
| Requisitos | `docs/requerimientos.md` |
| Fuentes e índice | `evidencias/entrega_2/inventario.json`, `reporte_corpus.json`, `reporte_indice.json` |
| Piloto final | `evidencias/entrega_2/respuestas_http.json`, `metricas_http.json`, `integracion_http.json` |
| Revisión de P07 | `evidencias/entrega_2/revision_cualitativa.md` y ejecuciones anteriores conservadas |

## Qué contiene GitHub y qué debe prepararse localmente

### Aclaración sobre las fuentes documentales

No se agregan al repositorio público los archivos completos de las fuentes institucionales, el formato ETIC, los fragmentos procesados ni el índice vectorial. Se publican las URLs y la configuración de las fuentes, el código de procesamiento y los inventarios con hashes y evidencias. Esta decisión separa los materiales institucionales del código del proyecto y evita redistribuir documentos sin una autorización verificada.

Las fuentes activas con URL, incluido el [formato ETIC público](https://docs.google.com/document/d/1PnpQyZdOVSMS7cpWTau-sb3gmgzIZGGq/edit), se obtienen automáticamente mediante `fetch`, sin iniciar sesión. No se publican copias completas de esos documentos en GitHub. Después se ejecutan `prepare` e `index` para construir la base local. Una vez preparada, las consultas reutilizan ese índice. Clonar GitHub no descarga una base precargada ni un modelo entrenado con esos documentos: el sistema aplica RAG sobre modelos preentrenados, sin modificar sus pesos.

**Clonar el repositorio no entrega una base precargada.** GitHub contiene código, instrucciones, el inventario de URLs/configuración y evidencias de las pruebas. No incluye los modelos de Ollama, los documentos completos, el corpus procesado ni la base ChromaDB. Las respuestas piloto publicadas son evidencias, no una base utilizada para contestar nuevas preguntas.

**Este proyecto no entrena Qwen3 con las fuentes.** Qwen3 y EmbeddingGemma se descargan ya preentrenados. La indexación transforma los fragmentos en vectores para recuperar información; en cada consulta, los fragmentos pertinentes se entregan como contexto a Qwen3. Sus pesos no se modifican. El conocimiento institucional utilizado reside en los documentos y el índice local.

| Elemento | ¿Se publica en GitHub? | ¿Cómo se obtiene? |
|---|---|---|
| Código, prompt y configuración de fuentes | Sí | Clonar el repositorio |
| Inventarios, hashes y resultados del piloto | Sí | Clonar; representan la ejecución registrada |
| Documentos institucionales completos | No | `fetch` descarga las URLs activas, incluido el formato ETIC público |
| Fragmentos y vectores | No | `prepare` e `index` |
| Modelos de lenguaje y embeddings | No | `ollama pull` |

La opción actual es mantener enlaces oficiales y un proceso de reconstrucción. Si se decide distribuir una versión precargada como entrega adicional, primero verificar autorización de redistribución de cada fuente y excluir documentos con datos personales. Ese paquete tendría que incluir corpus e índice compatibles, indicar versiones y explicar su actualización; no sería un modelo entrenado nuevo. El ZIP local del proyecto constituye un respaldo de la ejecución en el equipo de desarrollo y no forma parte de lo que descarga un clon de GitHub.

## Alcance y límites

ETIC no es obligatorio para todos los pregrados. No se transfieren requisitos entre carreras o modalidades; ante ausencia de una fuente aplicable se solicita contexto o se declara información insuficiente. La cobertura específica presencial sigue siendo limitada. Los documentos escaneados o de actualidad incierta permanecen excluidos del índice.

El MVP se ejecuta localmente con una consulta simultánea. La API rechaza entradas inválidas con 422 y solicitudes concurrentes con 429; informa fallos de servicio con mensajes controlados. No incorpora autenticación ni está preparado para exposición pública. No evalúa trabajos de estudiantes ni reemplaza al asesor.

Los registros de semanas 6–9 y `alcance_pregrados` corresponden a ejecuciones históricas y no se reescribieron como resultados del MVP. La evaluación amplia, la validación con usuarios y el análisis final continúan pendientes. Los documentos y páginas pueden cambiar después de la fecha de descarga.

El desarrollo contó con asistencia de IA y revisión de ejecución. La autora debe revisar contenido y evidencia y atender las indicaciones institucionales sobre declaración de estas herramientas.
