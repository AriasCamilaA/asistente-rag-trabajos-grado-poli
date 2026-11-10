import pytest
import requests
from fastapi.testclient import TestClient
from src import api

client = TestClient(api.app)


@pytest.fixture(autouse=True)
def catalog(monkeypatch):
    monkeypatch.setattr(api, 'catalog_data', lambda: {'programs': ['Ingeniería Industrial'], 'documents': 4, 'chunks': 139})


@pytest.mark.parametrize('body', [
    {'question': ''}, {'question': '   '}, {'question': 'x'*2001},
    {'question': 'hola', 'modality': 'remota'},
    {'question': 'hola', 'program': 'Otro'}, {'question': 'hola', 'extra': True},
])
def test_invalid_input_never_calls_model(monkeypatch, body):
    def forbidden(*args, **kwargs):
        pytest.fail('No debe invocar el modelo')
    monkeypatch.setattr(api.rag, 'ask', forbidden)
    assert client.post('/api/v1/chat', json=body).status_code == 422


def test_context_and_abstention_round_trip(monkeypatch):
    def ask(question, program, modality):
        assert (question, program, modality) == ('Requisito', 'Ingeniería Industrial', 'presencial')
        return {'answer': 'Falta evidencia', 'sources': [], 'insufficient': True, 'seconds': .1, 'model': 'prueba'}
    monkeypatch.setattr(api.rag, 'ask', ask)
    result = client.post('/api/v1/chat', json={'question':'Requisito', 'program':'Ingeniería Industrial', 'modality':'presencial'})
    assert result.status_code == 200
    assert result.json()['insufficient'] is True


@pytest.mark.parametrize('exception,status', [(requests.Timeout('ruta privada'),504), (requests.ConnectionError('secreto'),503), (ValueError('ruta privada'),503), (RuntimeError('secreto'),500)])
def test_errors_are_sanitized_and_lock_released(monkeypatch, exception, status):
    def fail(*a, **k): raise exception
    monkeypatch.setattr(api.rag,'ask',fail)
    result=client.post('/api/v1/chat',json={'question':'Hola'})
    assert result.status_code == status
    assert 'secreto' not in result.text and 'ruta privada' not in result.text
    assert not api.inference_lock.locked()


def test_busy_request_is_rejected():
    api.inference_lock.acquire()
    try:
        assert client.post('/api/v1/chat', json={'question':'hola'}).status_code == 429
    finally:
        api.inference_lock.release()


def test_catalog_endpoint():
    assert client.get('/api/v1/catalog').json()['programs'] == ['Ingeniería Industrial']
