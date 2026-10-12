# Asistente RAG para trabajos de grado del Poli

Prototipo académico de Camila Alexandra Arias Ruiz para los estudiantes de todos los pregrados y modalidades del Politécnico Grancolombiano. Implementa el avance técnico hasta la semana 9 del anteproyecto: fuentes, corpus, embeddings, recuperación y generación local. No representa un servicio oficial de la institución.

## Instalación y primera ejecución en Windows

### 1. Instalar Python, Git y Ollama

1. Instalar [Python 3.12](https://www.python.org/downloads/) y [Git para Windows](https://git-scm.com/download/win).
2. Descargar Ollama desde su [página oficial para Windows](https://ollama.com/download/windows), elegir la descarga manual y ejecutar `OllamaSetup.exe`.
3. Abrir Ollama desde el menú Inicio. La aplicación ejecuta el servicio en segundo plano. Cerrar y volver a abrir PowerShell después de instalarlo para que reconozca el comando.
4. Comprobar la instalación y descargar los dos modelos del proyecto:

```powershell
ollama --version
ollama pull qwen3:4b
ollama pull embeddinggemma
ollama list
```

La descarga de modelos necesita internet y espacio disponible. El proyecto usa modelos locales; no requiere iniciar sesión en Ollama ni contratar una API de IA. Mantener el servicio abierto mientras se prepara el índice o se consulta el chatbot. Si no se inicia desde la aplicación, ejecutar `ollama serve` en otra terminal y dejarla abierta.

Referencia de instalación y servicio: [documentación oficial de Ollama para Windows](https://docs.ollama.com/windows). El código se conecta a `http://127.0.0.1:11434`.

### 2. Clonar el repositorio e instalar sus dependencias

```powershell
git clone https://github.com/AriasCamilaA/asistente-rag-trabajos-grado-poli.git
cd asistente-rag-trabajos-grado-poli
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Ollama se instala por separado: `pip install -r requirements.txt` no instala Ollama ni descarga sus modelos.

### 3. Preparar las fuentes y construir el índice una vez

El comando `fetch` descarga las fuentes activas, incluido el [formato ETIC original disponible públicamente](https://docs.google.com/document/d/1PnpQyZdOVSMS7cpWTau-sb3gmgzIZGGq/edit). No es necesario cargarlo manualmente. La configuración registra su enlace de consulta y su enlace de descarga; el archivo se guarda en `data/raw/formato_etic.docx`.

```powershell
.\.venv\Scripts\python.exe -m src.rag fetch
.\.venv\Scripts\python.exe -m src.rag prepare
.\.venv\Scripts\python.exe -m src.rag index
```

| Comando | Función | Resultado local |
|---|---|---|
| `fetch` | Descargar las fuentes activas con URL y registrar procedencia y hashes | `data/raw/` y `evidencias/alcance_pregrados/inventario.json` |
| `prepare` | Extraer texto y dividirlo conservando sección, página, programa y modalidad | `data/processed/chunks.json` |
| `index` | Calcular embeddings y reconstruir la colección `poli_pregrados_v2` | `data/chroma/` |
| `ask` | Consultar el índice existente y generar una respuesta con fuentes | JSON en la terminal |

### 4. Consultar después de la preparación inicial

```powershell
.\.venv\Scripts\python.exe -m src.rag ask "¿Qué prerrequisitos exige el trabajo de grado?" --programa "Ingeniería Industrial" --modalidad virtual
.\.venv\Scripts\python.exe -m src.rag ask "¿Cuál es la extensión máxima del resumen ETIC?"
```

En ejecuciones posteriores basta con mantener Ollama disponible y ejecutar `ask`, siempre que continúen presentes los modelos y `data/chroma/`. No se necesita descargar las fuentes ni reconstruir el índice para cada pregunta. La consulta utiliza el contenido de la última indexación, aunque una página institucional haya cambiado después.

Cuando se actualicen las fuentes, repetir `fetch`, `prepare` e `index` y revisar las respuestas. Si solo cambia la extracción o segmentación, repetir `prepare` e `index`. Si cambia el modelo de embeddings, reconstruir el índice. El comando `index` reconstruye la colección; no conserva una mezcla de versiones anteriores.

### 5. Ejecutar las comprobaciones

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe -m evaluacion.run_pilot
```

El piloto requiere el índice y Ollama preparados. Escribe resultados nuevos en `evidencias/alcance_pregrados/`. Las consultas del proyecto se procesan localmente; la instalación, la descarga de modelos y la descarga de fuentes sí necesitan internet.

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

## Evidencias por semana

| Semana | Evidencia |
|---|---|
| 5 | Requerimientos y arquitectura derivados del anteproyecto en `docs/` |
| 6 | `data/sources.json`, `docs/criterios_fuentes.md`, `evidencias/semana_06/inventario.json` |
| 7 | Procesamiento en `src/rag.py` y reporte de corpus en `evidencias/semana_07/` |
| 8 | Reporte del índice y prueba de recuperación en `evidencias/semana_08/` |
| 9 | Prompt, generación, respuestas reales y métricas piloto en `evidencias/semana_09/` |

El piloto histórico restringido utilizó 19 fragmentos de tres fuentes y 12 preguntas. La versión ampliada utiliza 139 fragmentos de cuatro fuentes y 18 preguntas y no reemplaza la evaluación final de 50-80 preguntas prevista para semanas 13-14. El reporte distingue recuperación, presencia de fuentes, abstención, latencia y revisión cualitativa. La API y la interfaz web corresponden a semanas 10-12.

## Reproducibilidad y límites

Los archivos institucionales, el corpus completo y los vectores quedan localmente y están excluidos de Git. Se publican scripts y reportes para reconstruirlos. Una nueva descarga puede cambiar el hash de una página web, incluso sin cambios sustantivos; verificar su contenido y volver a ejecutar el piloto después de reindexar.

No se evalúan trabajos de estudiantes, no se inventan requisitos ni se sustituye al asesor. La cobertura inicial es pregrados del Politécnico Grancolombiano. No se extrapolan reglas de otras carreras. Las fuentes escaneadas o con actualidad incierta permanecen en el inventario como excluidas.

El código se desarrolló con asistencia de IA y revisión de ejecución. La autora debe revisar el contenido y cumplir las instrucciones de su institución sobre declaración del uso de estas herramientas.


Actualización de alcance: el público objetivo son todos los pregrados y modalidades del Politécnico Grancolombiano. La cobertura documental específica depende del programa. El corpus distingue programa, modalidad y plantilla; ETIC no es universal. Las evidencias anteriores de semanas 6–9 corresponden al piloto histórico restringido. La nueva ejecución se registra en evidencias/alcance_pregrados. Para consultar un programa puede usarse --programa y --modalidad. La cobertura específica presencial requiere fuentes propias; el chatbot se abstiene ante requisitos no documentados.


Corpus ampliado: cuatro fuentes, 139 fragmentos y 13 apartados de programas virtuales. Fuentes generales para orientación institucional y abstención cuando falta una fuente específica. Ejemplo: `python -m src.rag ask "¿Qué prerrequisito exige el trabajo de grado?" --programa "Ingeniería Industrial" --modalidad virtual`. Diez pruebas unitarias y 18 casos piloto; resultados en evidencias/alcance_pregrados.

