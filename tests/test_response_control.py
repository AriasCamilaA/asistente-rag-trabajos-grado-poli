import json
import pytest
from src import rag

HITS=[{'id':'chunk1','text':'La extensión máxima del resumen es 300 palabras.','distance':0.1,'metadata':{'document_id':'formato','title':'Formato','source':'local','section':'Resumen','page':0,'scope':'ETIC','program':'todos','modality':'todas'}}]

@pytest.mark.parametrize('payload',[{'answer':'Una respuesta','sources':['F99'],'insufficient':False},{'answer':'Una respuesta','sources':[],'insufficient':False},{'answer':'No sé','sources':['F1'],'insufficient':True}])
def test_invalid_reference_or_abstention_never_returns_citation(monkeypatch,payload):
    monkeypatch.setattr(rag,'retrieve',lambda *args,**kwargs:HITS)
    monkeypatch.setattr(rag,'ollama',lambda *args:{'message':{'content':json.dumps(payload)}})
    result=rag.ask('¿Extensión?')
    assert result['insufficient'] is True
    assert result['sources']==[]

def test_valid_citation_is_mapped_to_document(monkeypatch):
    monkeypatch.setattr(rag,'retrieve',lambda *args,**kwargs:HITS)
    monkeypatch.setattr(rag,'ollama',lambda *args:{'message':{'content':json.dumps({'answer':'300 palabras','sources':['F1'],'insufficient':False})}})
    result=rag.ask('¿Extensión?')
    assert result['sources'][0]['document_id']=='formato'
    assert result['insufficient'] is False
    # La consulta explícita de la plantilla no afirma su aplicabilidad al programa.
    contextual=rag.ask('¿Extensión del resumen ETIC?',program='Ingeniería Industrial',modality='virtual')
    assert contextual['insufficient'] is False
    assert contextual['sources'][0]['document_id']=='formato'

def test_unsupported_etic_version_is_rejected(monkeypatch):
    monkeypatch.setattr(rag,'retrieve',lambda *a,**k:HITS)
    monkeypatch.setattr(rag,'ollama',lambda *a:{'message':{'content':json.dumps({'answer':'ETIC 2.0 exige estos puntos','sources':['F1'],'insufficient':False})}})
    assert rag.ask('¿Qué exige ETIC?')['insufficient'] is True

def test_etic_conclusion_returns_literal_evidence(monkeypatch):
    hit={**HITS[0],'text':'La pertinencia de esta misma para la ejecución del proyecto.',
         'metadata':{**HITS[0]['metadata'],'section':'DISCUSIÓN Y CONCLUSIONES','template':'ETIC'}}
    monkeypatch.setattr(rag,'retrieve',lambda *a,**k:[hit])
    def forbidden(*a,**k): pytest.fail('La ruta extractiva no debe reformular con el modelo')
    monkeypatch.setattr(rag,'ollama',forbidden)
    result=rag.ask('¿Qué deben incluir las conclusiones ETIC?')
    assert result['answer'].endswith(hit['text'])
    assert result['model']=='extractivo: sección ETIC'
