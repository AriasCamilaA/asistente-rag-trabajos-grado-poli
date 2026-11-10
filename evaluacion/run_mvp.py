"""Piloto real a través de HTTP; no sustituye evaluación semántica independiente."""
import json
import statistics
import time
from datetime import datetime, timezone
import requests
from src.rag import ROOT, EVIDENCE, write_json


def run():
    base='http://127.0.0.1:8000'
    records=[]
    checks={}
    for route in ('/','/api/v1/catalog','/api/v1/health','/openapi.json'):
        response=requests.get(base+route,timeout=30)
        checks[route]={'status':response.status_code}
    cold_start=time.perf_counter()
    first=requests.post(base+'/api/v1/chat',json={'question':'¿Cuál es la extensión máxima del resumen ETIC?'},timeout=300)
    first.raise_for_status()
    checks['first_query']={'wall_seconds':round(time.perf_counter()-cold_start,3),'result':first.json(),
                          'condition':'Primera consulta HTTP de esta ejecución; no se forzó descarga de modelos de memoria.'}
    cases=json.loads((ROOT/'evaluacion/preguntas_piloto.json').read_text(encoding='utf-8'))
    for case in cases:
        started=time.perf_counter()
        response=requests.post(base+'/api/v1/chat',json={'question':case['question']},timeout=300)
        response.raise_for_status()
        answer=response.json()
        records.append({'id':case['id'],'question':case['question'],'expected_unanswerable':case['unanswerable'],
                        'expected_document':case['expected_document'],'expected_terms':case['expected_terms'],
                        'wall_seconds':round(time.perf_counter()-started,3),'status':response.status_code,**answer})
        write_json(EVIDENCE/'respuestas_http.json',records)
        print(case['id'],answer['insufficient'],answer['seconds'],flush=True)
    for name,body in [
        ('contexto_virtual',{'question':'¿Cuál es el prerrequisito del trabajo de grado?','program':'Ingeniería Industrial','modality':'virtual'}),
        ('contexto_presencial',{'question':'¿Cuál es el prerrequisito del trabajo de grado?','program':'Ingeniería Industrial','modality':'presencial'}),
        ('pregunta_vacia',{'question':'   '}),
        ('consulta_larga',{'question':'x'*2001}),
        ('programa_invalido',{'question':'Requisito','program':'Programa inexistente'}),
    ]:
        response=requests.post(base+'/api/v1/chat',json=body,timeout=300)
        checks[name]={'status':response.status_code,'body':response.json()}
    positives=[x for x in records if not x['expected_unanswerable']]
    negatives=[x for x in records if x['expected_unanswerable']]
    summary={'executed_at':datetime.now(timezone.utc).isoformat(),'n':len(records),'positive':len(positives),'negative':len(negatives),
             'http_success':sum(x['status']==200 for x in records),
             'positive_with_sources':sum(bool(x['sources']) for x in positives),
             'expected_document_cited':sum(any(s['document_id']==x['expected_document'] for s in x['sources']) for x in positives),
             'negative_abstention':sum(x['insufficient'] for x in negatives),
             'mean_wall_seconds':round(statistics.mean(x['wall_seconds'] for x in records),3),
             'median_wall_seconds':round(statistics.median(x['wall_seconds'] for x in records),3),
             'max_wall_seconds':max(x['wall_seconds'] for x in records),
             'note':'Piloto técnico de 18 casos reutilizados; sin validación independiente ni generalización a todos los programas. Presencia de fuente no implica corrección semántica.'}
    write_json(EVIDENCE/'integracion_http.json',checks)
    write_json(EVIDENCE/'metricas_http.json',summary)
    print(summary,flush=True)


if __name__=='__main__': run()
