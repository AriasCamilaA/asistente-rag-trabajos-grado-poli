'use client';
import {useEffect, useRef, useState} from 'react';

function publicLink(value) { try { const u=new URL(value); return u.protocol==='https:' ? u.href : null; } catch { return null; } }

export default function Chat() {
  const [catalog,setCatalog]=useState(null), [health,setHealth]=useState(null);
  const [program,setProgram]=useState(''), [modality,setModality]=useState('');
  const [question,setQuestion]=useState(''), [messages,setMessages]=useState([]);
  const [busy,setBusy]=useState(false), [error,setError]=useState('');
  const last=useRef(null);
  async function check() {
    try { const [c,h]=await Promise.all([fetch('/api/v1/catalog'),fetch('/api/v1/health')]);
      if(!c.ok || !h.ok) throw Error('No se pudo consultar el servicio.');
      setCatalog(await c.json());setHealth(await h.json());setError('');
    } catch { setHealth(null);setError('No hay conexión con el servicio. Comprueba que esté iniciado y vuelve a verificar.'); }
  }
  useEffect(()=>{check();},[]);
  useEffect(()=>{last.current?.scrollIntoView({behavior:'smooth',block:'nearest'});},[messages,busy]);
  async function submit(event) {
    event.preventDefault(); if(busy || !question.trim()) return;
    const text=question.trim(), context=[program||'Consulta general',modality||'Sin modalidad'].join(' · ');
    setBusy(true);setError('');setMessages(m=>[...m,{role:'user',text,context}]);setQuestion('');
    try { const res=await fetch('/api/v1/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:text,program:program||null,modality:modality||null})});
      const data=await res.json(); if(!res.ok) throw Error(typeof data.detail==='string'?data.detail:'No se pudo completar la consulta.');
      setMessages(m=>[...m,{role:'assistant',...data}]);
    } catch(e) {setError(e.message==='Failed to fetch'?'Se perdió la conexión. Verifica el servicio y vuelve a intentar.':e.message);setQuestion(text);}
    finally {setBusy(false);}
  }
  return <div className="shell">
    <aside><a className="brand" href="/">P<span>ORIENTACIÓN DE GRADO</span></a><p className="eyebrow">PROTOTIPO ACADÉMICO</p><h1>Tu consulta,<br/>con fuentes.</h1><p>Orientación documental para estudiantes de pregrado del Politécnico Grancolombiano.</p>
      <section className="context"><h2>Contexto de la consulta</h2><label htmlFor="program">Programa</label><select id="program" value={program} onChange={e=>setProgram(e.target.value)} disabled={busy}><option value="">Consulta general</option>{catalog?.programs.map(p=><option key={p}>{p}</option>)}</select><label htmlFor="modality">Modalidad</label><select id="modality" value={modality} onChange={e=>setModality(e.target.value)} disabled={busy}><option value="">Sin especificar</option><option value="virtual">Virtual</option><option value="presencial">Presencial</option></select><small>Si tu programa no aparece, usa consulta general. Las reglas particulares requieren fuentes del programa y la modalidad.</small></section>
      <div className="coverage"><strong>Cobertura documental</strong><p>{catalog?`${catalog.documents} fuentes · ${catalog.chunks} fragmentos`:'Consultando catálogo…'}</p><small>La cobertura presencial es limitada. El formato ETIC no aplica automáticamente a todos los programas.</small></div>
      <footer>Desarrollado por Camila Alexandra Arias Ruiz.<br/>Proyecto académico independiente.</footer>
    </aside>
    <main><header><div><span className="eyebrow">ASISTENTE DOCUMENTAL</span><h2>Hablemos de tu trabajo de grado</h2></div><span className={'status '+(health?.ready?'ready':'')} role="status">{health?.ready?'● Servicio disponible':'○ Servicio por verificar'}</span></header>
      <div className="notice">Este prototipo orienta a partir de documentos. Confirma requisitos y vigencia con tu asesor o coordinación. Evita compartir datos personales.</div>
      {!health?.ready && <div className="service-note">Revisa que Ollama y los modelos estén disponibles y que la base local esté preparada. <button onClick={check} disabled={busy}>Verificar servicio</button></div>}
      <section className="conversation" aria-label="Conversación" aria-live="polite">
        {messages.length===0 && <div className="welcome"><div className="mark">↗</div><h3>¿Qué necesitas consultar?</h3><p>Pregunta por etapas, requisitos o estructura del informe. Cada consulta se resuelve con el contexto seleccionado; las preguntas se procesan de forma independiente.</p><div className="examples">{['¿Cuáles son las opciones de grado?','¿Cuál es la extensión máxima del resumen ETIC?','¿Qué debe incluir la sección de conclusiones ETIC?'].map(q=><button key={q} onClick={()=>setQuestion(q)}>{q}<span>↗</span></button>)}</div></div>}
        {messages.map((m,i)=><article key={i} className={'message '+m.role}><div className="message-label">{m.role==='user'?'TU CONSULTA':'ASISTENTE'}{m.insufficient?' · Información insuficiente':''}</div>{m.role==='user'?<><p>{m.text}</p><small>{m.context}</small></>:<><p>{m.answer}</p>{m.sources?.length>0 && <div className="sources"><h3>Fuentes de la respuesta</h3>{m.sources.map((s,j)=><details key={j}><summary><span>{s.citation}</span> {s.title}</summary><p>{s.section}{s.page>0?` · Página ${s.page}`:''}</p><small>{s.program} · {s.modality}</small>{s.excerpt && <blockquote>{s.excerpt}</blockquote>}{publicLink(s.source) && <a href={publicLink(s.source)} target="_blank" rel="noopener noreferrer">Consultar documento ↗</a>}</details>)}</div>}<small>Respuesta en {m.seconds.toFixed(2)} s · Verifica el respaldo en las fuentes.</small></>}</article>)}
        {busy && <p className="loading" role="status">Consultando documentos y preparando la respuesta…</p>}<div ref={last}/>
      </section>
      <div className="composer">{error && <div className="error" role="alert">{error}</div>}<form onSubmit={submit}><label className="sr-only" htmlFor="question">Escribe tu pregunta</label><textarea id="question" placeholder="Escribe tu pregunta sobre el trabajo de grado…" value={question} onChange={e=>setQuestion(e.target.value)} maxLength={2000} rows={2} disabled={busy}/><div className="compose-bottom"><span>{question.length}/2000 · Historial temporal de esta página</span><button type="submit" disabled={busy||!question.trim()}> {busy?'Consultando…':'Enviar consulta ↑'}</button></div></form><button className="clear" disabled={busy||messages.length===0} onClick={()=>{setMessages([]);setError('');}}>Limpiar conversación</button></div>
    </main></div>;
}
