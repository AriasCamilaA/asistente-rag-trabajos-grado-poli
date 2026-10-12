import json
from src import rag

def test_fetch_downloads_configured_local_source_without_manual_copy(tmp_path,monkeypatch):
    source={'id':'etic_formato','include':True,'format':'docx','url':'https://example.org/formato.docx','local_path':'data/raw/formato_etic.docx'}
    (tmp_path/'data').mkdir()
    (tmp_path/'data/sources.json').write_text(json.dumps([source]),encoding='utf8')
    class Response:
        content=b'contenido de prueba'
        def raise_for_status(self):pass
    monkeypatch.setattr(rag,'ROOT',tmp_path)
    monkeypatch.setattr(rag,'EVIDENCE',tmp_path/'evidencias')
    monkeypatch.setattr(rag.requests,'get',lambda *a,**k:Response())
    manifest=rag.fetch()
    assert (tmp_path/'data/raw/formato_etic.docx').read_bytes()==Response.content
    assert manifest[0]['local_path']=='data/raw/formato_etic.docx'
    assert manifest[0]['sha256']
