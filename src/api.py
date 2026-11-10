"""API local y publicación estática del MVP. Ejecutar con uvicorn en loopback."""
import json
import logging
import threading
from pathlib import Path
from typing import Literal

import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, field_validator
from src import rag

app = FastAPI(title='Asistente de trabajos de grado del Poli', version='0.2.0')
inference_lock = threading.Lock()
logger = logging.getLogger(__name__)


class Query(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    question: str = Field(min_length=1, max_length=2000)
    program: str | None = Field(default=None, max_length=120)
    modality: Literal['virtual', 'presencial'] | None = None

    @field_validator('question')
    @classmethod
    def meaningful_question(cls, value):
        if not value.strip():
            raise ValueError('Consulta vacía')
        return value.strip()


class Source(BaseModel):
    citation: str
    document_id: str
    title: str
    source: str
    section: str
    page: int
    scope: str
    program: str = 'todos'
    modality: str = 'todas'
    version: str = ''
    excerpt: str = ''


class Answer(BaseModel):
    answer: str
    sources: list[Source]
    insufficient: bool
    seconds: float
    model: str


def catalog_data():
    path = rag.ROOT/'data/processed/chunks.json'
    corpus = json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
    programs = sorted({x['metadata']['program'] for x in corpus if x['metadata']['program'] != 'todos'})
    return {'programs': programs, 'modalities': ['virtual', 'presencial'],
            'documents': len({x['metadata']['document_id'] for x in corpus}),
            'chunks': len(corpus), 'notice': 'La cobertura específica depende de las fuentes disponibles. ETIC no es universal.'}


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={'detail': 'Revisa la consulta (1 a 2000 caracteres), el programa y la modalidad.'})


@app.get('/api/v1/catalog')
def catalog():
    return catalog_data()


@app.get('/api/v1/health')
def health():
    models, service = [], False
    try:
        response = requests.get(rag.OLLAMA+'/api/tags', timeout=3)
        response.raise_for_status()
        models = [x['name'] for x in response.json().get('models', [])]
        service = True
    except (requests.RequestException, ValueError, KeyError):
        pass
    indexed = False
    if (rag.ROOT/'data/chroma/chroma.sqlite3').exists():
        try:
            indexed = rag.collection().count() > 0
        except Exception:
            logger.exception('No se pudo comprobar el índice')
    missing = [x for x in [rag.EMBED_MODEL, rag.CHAT_MODEL] if x not in models]
    return {'ready': service and indexed and not missing, 'ollama': service,
            'index': indexed, 'missing_models': missing, 'version': '0.2.0'}


@app.post('/api/v1/chat', response_model=Answer)
def chat(query: Query):
    known = catalog_data()['programs']
    if query.program and query.program not in known:
        raise HTTPException(422, 'Selecciona un programa del catálogo; usa consulta general si no aparece.')
    if not inference_lock.acquire(blocking=False):
        raise HTTPException(429, 'Hay una consulta en proceso. Inténtalo cuando termine.')
    try:
        result = rag.ask(query.question, program=query.program, modality=query.modality)
        return Answer.model_validate(result)
    except requests.Timeout:
        raise HTTPException(504, 'La generación superó el tiempo de espera. Inténtalo nuevamente.') from None
    except requests.RequestException:
        raise HTTPException(503, 'Ollama no está disponible o falta un modelo. Revisa el servicio y los modelos.') from None
    except (FileNotFoundError, ValueError):
        raise HTTPException(503, 'La base local no está preparada. Ejecuta fetch, prepare e index.') from None
    except Exception:
        logger.exception('Fallo durante consulta')
        raise HTTPException(500, 'No fue posible completar la consulta. Revisa el estado del servicio.') from None
    finally:
        inference_lock.release()


# API declarada antes del montaje para conservar rutas y documentación OpenAPI.
static = Path(__file__).resolve().parents[1]/'frontend/out'
if static.exists():
    app.mount('/', StaticFiles(directory=static, html=True), name='frontend')
