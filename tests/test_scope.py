from src import rag

class FakeCollection:
    def count(self):return 3
    def get(self):return {'metadatas':[{'program':'Ingeniería Industrial'},{'program':'Ingeniería de Software'},{'program':'todos'}]}
    def query(self,**kwargs):
        self.filters=kwargs['where']
        return dict(ids=[[]],documents=[[]],metadatas=[[]],distances=[[]])

def test_industrial_virtual_excludes_other_programs_and_templates(monkeypatch):
    collection=FakeCollection()
    monkeypatch.setattr(rag,'collection',lambda:collection)
    monkeypatch.setattr(rag,'embed',lambda *a,**k:[[0.1]])
    rag.retrieve('Trabajo de grado Ingeniería Industrial virtual')
    assert collection.filters=={'$and':[{'program':{'$in':['todos','Ingeniería Industrial']}},{'modality':{'$in':['todas','virtual']}},{'template':{'$eq':'ninguno'}}]}

def test_no_program_only_retrieves_institutional_rules(monkeypatch):
    collection=FakeCollection()
    monkeypatch.setattr(rag,'collection',lambda:collection)
    monkeypatch.setattr(rag,'embed',lambda *a,**k:[[0.1]])
    rag.retrieve('¿Cuál es el prerrequisito?')
    assert collection.filters['$and'][0]=={'program':{'$in':['todos']}}

def test_etic_is_opt_in(monkeypatch):
    collection=FakeCollection()
    monkeypatch.setattr(rag,'collection',lambda:collection)
    monkeypatch.setattr(rag,'embed',lambda *a,**k:[[0.1]])
    rag.retrieve('¿Qué pide el formato ETIC?')
    assert collection.filters=={'program':{'$in':['todos']}}
