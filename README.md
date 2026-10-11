# Asistente RAG para trabajos de grado del Poli

Prototipo académico de Camila Alexandra Arias Ruiz, Ingeniería de Software, Politécnico Grancolombiano. Implementa el avance técnico hasta la semana 9 del anteproyecto: fuentes, corpus, embeddings, recuperación y generación local. No representa un servicio oficial de la institución.

## Ejecución en Windows

Requiere Python 3.12, Git y Ollama con `qwen3:4b` y `embeddinggemma`. El desarrollo se verificó con el runtime Python 3.12 incluido en Codex, sin instalar Python globalmente. Para ejecutarlo fuera de Codex puede instalarse Python 3.12 desde python.org.

```powershell
git clone https://github.com/AriasCamilaA/asistente-rag-trabajos-grado-poli.git
cd asistente-rag-trabajos-grado-poli
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull qwen3:4b
ollama pull embeddinggemma
```

Colocar una copia autorizada del formato ETIC original en `data/raw/formato_etic.docx`. El formato no se publica en este repositorio. Mantener Ollama abierto, luego:

```powershell
.\.venv\Scripts\python.exe -m src.rag fetch
.\.venv\Scripts\python.exe -m src.rag prepare
.\.venv\Scripts\python.exe -m src.rag index
.\.venv\Scripts\python.exe -m src.rag ask "¿Cuál es la extensión máxima del resumen ETIC?"
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe -m evaluacion.run_pilot
```

`fetch` descarga fuentes y registra hashes; `prepare` conserva página/sección; `index` reconstruye la colección ChromaDB; `ask` devuelve JSON con respuesta, fuentes y tiempo. Las consultas no se envían a servicios comerciales de IA. Las descargas sí necesitan internet.

## Evidencias por semana

| Semana | Evidencia |
|---|---|
| 5 | Requerimientos y arquitectura derivados del anteproyecto en `docs/` |
| 6 | `data/sources.json`, `docs/criterios_fuentes.md`, `evidencias/semana_06/inventario.json` |
| 7 | Procesamiento en `src/rag.py` y reporte de corpus en `evidencias/semana_07/` |
| 8 | Reporte del índice y prueba de recuperación en `evidencias/semana_08/` |
| 9 | Prompt, generación, respuestas reales y métricas piloto en `evidencias/semana_09/` |

El corpus inicial consta de 19 fragmentos procedentes de tres fuentes incluidas. El piloto tiene 12 preguntas y no reemplaza la evaluación final de 50-80 preguntas prevista para semanas 13-14. El reporte distingue recuperación, presencia de fuentes, abstención, latencia y revisión cualitativa. La API y la interfaz web corresponden a semanas 10-12.

## Reproducibilidad y límites

Los archivos institucionales, el corpus completo y los vectores quedan localmente y están excluidos de Git. Se publican scripts y reportes para reconstruirlos. Una nueva descarga puede cambiar el hash de una página web, incluso sin cambios sustantivos; verificar su contenido y volver a ejecutar el piloto después de reindexar.

No se evalúan trabajos de estudiantes, no se inventan requisitos ni se sustituye al asesor. La cobertura inicial es Ingeniería de Software virtual. No se extrapolan reglas de otras carreras. Las fuentes escaneadas o con actualidad incierta permanecen en el inventario como excluidas.

El código se desarrolló con asistencia de IA y revisión de ejecución. La autora debe revisar el contenido y cumplir las instrucciones de su institución sobre declaración del uso de estas herramientas.
