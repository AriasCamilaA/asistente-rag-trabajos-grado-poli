from docx import Document
from src import rag
class FakeCollection:
    def count(self): return 1
    def get(self): return {'metadatas':[{'program':'todos'}]}
    def query(self,**kwargs):
        self.filters=kwargs['where']
        return dict(ids=[[]],documents=[[]],metadatas=[[]],distances=[[]])


def test_bibliography_instruction_is_not_conclusion(tmp_path, monkeypatch):
    doc=Document()
    doc.add_heading('DISCUSIÓN Y CONCLUSIONES', level=1)
    doc.add_paragraph('Reflexiones acerca del aprendizaje logrado y recomendaciones futuras del proyecto.')
    doc.add_paragraph('En el siguiente apartado debe dar cuenta de TODOS los textos a los que efectivamente se hizo referencia.')
    doc.add_heading('REFERENCIAS', level=1)
    path=tmp_path/'fuente.docx';doc.save(path)
    monkeypatch.setattr(rag,'ROOT',tmp_path)
    sections=list(rag.extract({'format':'docx','local_path':'fuente.docx'}))
    conclusion=next(x[2] for x in sections if x[1]=='DISCUSIÓN Y CONCLUSIONES')
    assert 'TODOS los textos' not in conclusion
    assert any(x[1]=='REFERENCIAS' and 'TODOS los textos' in x[2] for x in sections)


def test_conclusion_query_is_scoped_to_etic_section(monkeypatch):
    col=FakeCollection()
    monkeypatch.setattr(rag,'collection',lambda:col)
    monkeypatch.setattr(rag,'embed',lambda *a,**k:[[.1]])
    rag.retrieve('¿Qué deben incluir las conclusiones ETIC?')
    assert {'section':{'$eq':'DISCUSIÓN Y CONCLUSIONES'}} in col.filters['$and']
    assert {'template':{'$eq':'ETIC'}} in col.filters['$and']
