import json
import pytest
from src import rag

HITS=[{'id':'chunk1','text':'La extensión máxima del resumen es 300 palabras.','distance':0.1,'metadata':{'document_id':'formato','title':'Formato','source':'local','section':'Resumen','page':0}}]

@pytest.mark.parametrize('payload',[{'answer':'Una respuesta','sources':['F99'],'insufficient':False},{'answer':'Una respuesta','sources':[],'insufficient':False},{'answer':'No sé','sources':['F1'],'insufficient':True}])
def test_invalid_reference_or_abstention_never_returns_citation(monkeypatch,payload):
    monkeypatch.setattr(rag,'retrieve',lambda _:HITS)
    monkeypatch.setattr(rag,'ollama',lambda *args:{'message':{'content':json.dumps(payload)}})
    result=rag.ask('¿Extensión?')
    assert result['insufficient'] is True
    assert result['sources']==[]

def test_valid_citation_is_mapped_to_document(monkeypatch):
    monkeypatch.setattr(rag,'retrieve',lambda _:HITS)
    monkeypatch.setattr(rag,'ollama',lambda *args:{'message':{'content':json.dumps({'answer':'300 palabras','sources':['F1'],'insufficient':False})}})
    result=rag.ask('¿Extensión?')
    assert result['sources'][0]['document_id']=='formato'
    assert result['insufficient'] is False
