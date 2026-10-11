"""Prueba piloto; coincidencias léxicas no equivalen a exactitud académica."""
import json
from datetime import datetime, timezone
from src.rag import ROOT, retrieve, ask, write_json

def run():
    cases=json.loads((ROOT/'evaluacion/preguntas_piloto.json').read_text(encoding='utf-8'))
    retrieval=[];generation=[]
    for case in cases:
        print(case['id'],flush=True)
        hits=retrieve(case['question'])
        retrieval.append({'id':case['id'],'question':case['question'],'expected_document':case['expected_document'],'hit_at_4':None if case['unanswerable'] else any(x['metadata']['document_id']==case['expected_document'] for x in hits),'retrieved':[{'id':h['id'],'document_id':h['metadata']['document_id'],'distance':h['distance']} for h in hits]})
        response=ask(case['question'])
        generation.append({'id':case['id'],'expected_unanswerable':case['unanswerable'],'expected_terms':case['expected_terms'],'lexical_match':None if case['unanswerable'] else all(t.lower() in response['answer'].lower() for t in case['expected_terms']),**response})
        write_json(ROOT/'evidencias/semana_08/recuperacion_piloto.json',retrieval)
        write_json(ROOT/'evidencias/semana_09/respuestas_piloto.json',generation)
    supported=[x for x in retrieval if x['hit_at_4'] is not None]
    outside=[x for x in generation if x['expected_unanswerable']]
    write_json(ROOT/'evidencias/semana_09/metricas_piloto.json',{'executed_at':datetime.now(timezone.utc).isoformat(),'n':len(cases),'answerable':len(supported),'unanswerable':len(outside),'hit_at_4':sum(x['hit_at_4'] for x in supported)/len(supported),'abstention_unanswerable':sum(x['insufficient'] for x in outside)/len(outside),'source_presence_answerable':sum(bool(x['sources']) for x in generation if not x['expected_unanswerable'])/len(supported),'mean_seconds':sum(x['seconds'] for x in generation)/len(generation),'note':'Prueba piloto técnica, no evaluación final de 50-80 preguntas; coincidencia lexical no demuestra exactitud ni fundamentación.'})

if __name__=='__main__':
    run()
