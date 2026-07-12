// ============== RENDER ==============
// APP_MODE ("trip" | "city") é declarado no bloco DATA (shell.html) ANTES deste script.
// trip = viagem datada (date-strip DOW+dia, status bar com data real/AGORA/stats-de-dias).
// city = coletânea de cidade sem datas (abas = temas · sem data/AGORA/dias · mantém feito/mapa/busca).
const IS_TRIP = (typeof APP_MODE==='undefined') || APP_MODE==='trip';

function getDefaultDayIdx(){
  // Detecta se hoje é um dos dias do roteiro e auto-seleciona; senão volta pro dia 1 (chegada)
  const monthMap={Jan:0,Fev:1,Feb:1,Mar:2,Abr:3,Apr:3,Mai:4,May:4,Jun:5,Jul:6,Ago:7,Aug:7,Set:8,Sep:8,Out:9,Oct:9,Nov:10,Dez:11,Dec:11};
  const today=new Date();
  const tM=today.getMonth(), tD=today.getDate(); // compara em horário LOCAL (evita rolagem de dia via UTC)
  for(let i=0;i<DAYS.length;i++){
    const m=(DAYS[i].date||'').match(/(\d+)\/(\w+)/);
    if(!m) continue;
    const dayNum=parseInt(m[1]);
    const monthIdx=monthMap[m[2]];
    if(monthIdx===undefined) continue;
    if(dayNum===tD && monthIdx===tM) return i;
  }
  return 0;
}
const MONTH_MAP={Jan:0,Fev:1,Feb:1,Mar:2,Abr:3,Apr:3,Mai:4,May:4,Jun:5,Jul:6,Ago:7,Aug:7,Set:8,Sep:8,Out:9,Oct:9,Nov:10,Dez:11,Dec:11};

// Índice do dia do roteiro que é HOJE, ou -1 se hoje não é dia de viagem.
// Mesma lógica exata de getDefaultDayIdx (exact-date-match) mas retorna -1 (não 0) fora da viagem.
function getTodayTripIdx(){
  const today=new Date();
  const tM=today.getMonth(), tD=today.getDate(); // compara em horário LOCAL (evita rolagem de dia via UTC)
  for(let i=0;i<DAYS.length;i++){
    const m=(DAYS[i].date||'').match(/(\d+)\/(\w+)/);
    if(!m) continue;
    const dayNum=parseInt(m[1]);
    const monthIdx=MONTH_MAP[m[2]];
    if(monthIdx===undefined) continue;
    if(dayNum===tD && monthIdx===tM) return i;
  }
  return -1;
}

// ===== FEITO axis (execução durante a viagem, separado de reserva) =====
function isFeito(nome){ try{return localStorage.getItem('feito-'+nome)==='done';}catch(e){return false;} }
function setFeito(nome,val){ try{localStorage.setItem('feito-'+nome,val?'done':'undone');}catch(e){} }

// ===== Storage health · reservas/feitos vivem no localStorage · avisa quando o navegador NÃO vai persistir
// (modo privado, storage bloqueado, ou navegador embutido em app — que usa storage efêmero e limpa ao fechar).
// A persistência em si é correta (verificada end-to-end); este aviso cobre o caso "some ao fechar o app".
function storagePersists(){
  try{ const k='__probe'; localStorage.setItem(k,'1'); const ok=localStorage.getItem(k)==='1'; localStorage.removeItem(k); return ok; }
  catch(e){ return false; }
}
function isInAppBrowser(){
  const ua=navigator.userAgent||'';
  // webviews embutidas (WhatsApp/Instagram/FB/Telegram/etc) costumam descartar o localStorage ao fechar
  return /(FBAN|FBAV|FB_IAB|Instagram|Line\/|Twitter|WhatsApp|Telegram|Snapchat|Pinterest|MicroMessenger|GSA\/)/i.test(ua);
}
function maybeWarnStorage(){
  const broken=!storagePersists();
  const inApp=isInAppBrowser();
  if(!broken && !inApp) return;
  if(document.getElementById('storage-warn')) return;
  const msg = broken
    ? '⚠️ O navegador está em <strong>modo privado</strong> ou com o armazenamento bloqueado — reservas e “feitos” <strong>não vão ficar salvos</strong>. Abra no Safari/Chrome normal.'
    : '⚠️ Você abriu o link <strong>dentro de um app</strong> (WhatsApp, Instagram…). Assim o progresso <strong>some ao fechar</strong>. Toque em <strong>•••</strong> → “Abrir no Safari/Chrome”, ou Compartilhar → “Adicionar à Tela de Início”.';
  const bar=document.createElement('div');
  bar.id='storage-warn';
  bar.innerHTML='<div class="sw-txt">'+msg+'</div><button class="sw-x" aria-label="Fechar aviso">✕</button>';
  document.body.appendChild(bar);
  bar.querySelector('.sw-x').addEventListener('click',()=>bar.remove());
}

// hora "HH:MM" -> minutos; retorna null se inválido
function horaToMin(h){ const m=(h||'').match(/(\d{1,2}):(\d{2})/); if(!m) return null; return parseInt(m[1])*60+parseInt(m[2]); }

// Índice do stop "AGORA" · só se dayIdx é o dia de hoje E o relógio real está dentro da janela do dia.
function getNowStopIdx(day,dayIdx){
  if(getTodayTripIdx()!==dayIdx) return -1;
  const now=new Date();
  const nowMin=now.getHours()*60+now.getMinutes();
  const timed=day.stops.map((s,i)=>({i,m:horaToMin(s.hora)})).filter(x=>x.m!==null);
  if(!timed.length) return -1;
  // antes do primeiro ou depois de +3h do último → sem AGORA
  if(nowMin<timed[0].m) return -1;
  const last=timed[timed.length-1];
  if(nowMin>=last.m+180) return -1;
  for(let k=0;k<timed.length;k++){
    const start=timed[k].m;
    const end=k+1<timed.length?timed[k+1].m:last.m+180;
    if(nowMin>=start && nowMin<end) return timed[k].i;
  }
  return -1;
}

// Data de hoje formatada PT-BR: "1/Jul" (sempre correta, independente das datas da viagem)
const PT_MESES=['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'];
function hojeLabel(){
  const d=new Date();
  const mes=PT_MESES[d.getMonth()];
  return d.getDate()+'/'+mes.charAt(0).toUpperCase()+mes.slice(1);
}
// Dias da viagem já DECORRIDOS: quantos DAYS têm data estritamente ANTES de hoje.
// 0 antes da viagem começar · 11 depois de terminar (clamp natural pela contagem).
function diasElapsed(){
  const today=new Date();
  const tStr=today.toISOString().split('T')[0];
  let elapsed=0;
  for(let i=0;i<DAYS.length;i++){
    const m=(DAYS[i].date||'').match(/(\d+)\/(\w+)/);
    if(!m) continue;
    const monthIdx=MONTH_MAP[m[2]];
    if(monthIdx===undefined) continue;
    const d=new Date(2026,monthIdx,parseInt(m[1]));
    if(d.toISOString().split('T')[0]<tStr) elapsed++;
  }
  return elapsed;
}

const state = { view:'guia', selIdx:getDefaultDayIdx(), search:'', expandStop:null, ovFilter:'roteiro', ovShowPending:false,
  mapFilter:{ minStar:3, groups:new Set(['atracao','comida','loja','parque']), day:-1 } };

function getPeriodoMeta(p){
  return {
    manha:{emoji:'🌅',label:'Manhã'},
    tarde:{emoji:'☀️',label:'Tarde'},
    noite:{emoji:'🌙',label:'Noite'}
  }[p];
}

function getMapsUrl(stop){
  if(stop.noMaps) return '';
  // Pra opcoes (3+ alternativas), usar nome da PRIMEIRA opção pra link específico
  let queryName=stop.nome;
  if(stop.tipo==='opcoes' && stop.opcoes && stop.opcoes.length>0){
    queryName=stop.opcoes[0].nome;
  }
  // Remove parens MAS mantém conteúdo (endereços como "144 MacDougal" ajudam a busca)
  const clean=queryName.replace(/[()]/g,'').replace(/[^\p{L}\p{N}\s\-'&.,/:!?]/gu,'').replace(/\s+/g,' ').trim();
  if(stop.coord) return `https://www.google.com/maps/search/${encodeURIComponent(clean)}/@${stop.coord.lat},${stop.coord.lng},17z`;
  return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(clean+' New York')}`;
}

// Monta URL de rota do Google Maps na forma path-segment (/dir/Nome1/Nome2/.../).
// Mostra os NOMES das paradas E desenha o trajeto (a forma ?origin=&waypoints= só marcava pins).
// Cada nome: parens removidos (conteúdo mantido) + ", New York, NY" pra geocodar certo · segmento URL-encoded.
// Total de segmentos capado em ~10 (amostra o miolo, mantém 1º + último).
// Monta URL de rota do Google Maps na forma oficial api=1, por COORDENADAS.
// Coord é exata (nomes vagos/eventos como "Fogos Macy's" caem no lugar errado).
// Waypoints intermediários capados em 9 (limite free da api=1): amostra o miolo,
// sempre mantendo origem (1º) e destino (último).
function dirCoordUrl(coords,mode='walking'){
  const pts=coords.filter(c=>c&&typeof c.lat==='number'&&typeof c.lng==='number');
  if(pts.length<2) return null;
  const origin=pts[0], dest=pts[pts.length-1];
  let mids=pts.slice(1,-1);
  const MAXW=9;
  if(mids.length>MAXW){
    const pick=[];
    for(let k=0;k<MAXW;k++){
      const idx=Math.round(k*(mids.length-1)/(MAXW-1));
      pick.push(mids[idx]);
    }
    mids=pick.filter((p,i,a)=>a.indexOf(p)===i);
  }
  const ll=c=>`${c.lat},${c.lng}`;
  let url=`https://www.google.com/maps/dir/?api=1&origin=${encodeURIComponent(ll(origin))}&destination=${encodeURIComponent(ll(dest))}`;
  if(mids.length) url+=`&waypoints=${encodeURIComponent(mids.map(ll).join('|'))}`;
  url+=`&travelmode=${mode}`;
  return url;
}

// Estima o modo de deslocamento do dia pela distância total + maior perna (haversine).
function dayTransport(day){
  const pts=day.stops.filter(s=>s.tipo!=='transit' && s.coord).map(s=>s.coord);
  if(pts.length<2) return 'walking';
  const haversine=(a,b)=>{
    const R=6371, toRad=x=>x*Math.PI/180;
    const dLat=toRad(b.lat-a.lat), dLng=toRad(b.lng-a.lng);
    const s=Math.sin(dLat/2)**2+Math.cos(toRad(a.lat))*Math.cos(toRad(b.lat))*Math.sin(dLng/2)**2;
    return 2*R*Math.asin(Math.sqrt(s));
  };
  let total=0, maxLeg=0;
  for(let i=1;i<pts.length;i++){
    const leg=haversine(pts[i-1],pts[i]);
    total+=leg; if(leg>maxLeg) maxLeg=leg;
  }
  return (total>5||maxLeg>2.5)?'driving':'walking';
}

function getRouteUrl(day){
  const stops=day.stops.filter(s=>s.tipo!=='transit' && s.coord);
  if(!stops.length) return '#';
  if(stops.length===1) return getMapsUrl(stops[0]);
  // Rota por coordenadas (exata) · opcoes usa a própria coord do stop
  return dirCoordUrl(stops.map(s=>s.coord),dayTransport(day)) || getMapsUrl(stops[0]);
}

// Limpa o nome de uma parada de walking tour p/ virar query geocodável:
// tira parênteses (mantém o endereço dentro), corta descrições após "·", normaliza espaços.
// Ex: "Trinity Church (89 Broadway · Hamilton's tomb)" → "Trinity Church 89 Broadway"
function wtStopQuery(nome){
  return (nome||'').replace(/[()]/g,' ').split('·')[0].replace(/\s+/g,' ').trim();
}
function getWalkingTourUrl(tour){
  if(!tour||tour.length<2) return '#';
  // Preferência: rota por NOME das paradas (legível no Google Maps) · exige MAPS_REGION p/ geocodar certo.
  const region=(typeof MAPS_REGION!=='undefined'&&MAPS_REGION)?(', '+MAPS_REGION):'';
  if(region){
    const names=tour.map(t=>wtStopQuery(t.nome)).filter(Boolean);
    if(names.length>=2)
      return `https://www.google.com/maps/dir/${names.map(n=>encodeURIComponent(n+region)).join('/')}/`;
  }
  // Fallback (sem região definida ou nomes ausentes): rota por COORDENADAS.
  return dirCoordUrl(tour.map(t=>t.coord),'walking') || '#';
}

function agoraPillHtml(isNow){ return isNow?'<span class="agora-pill"><span class="agora-dot"></span>Agora</span>':''; }

function renderCard(stop,isNow,done){
  const links=LINKS_MAP[stop.nome]||[];
  const riskLabel={green:'🟢 tranquilo',yellow:'⚠️ atenção',red:'🔴 alta atenção'};
  const riskBadge=stop.risco?`<span class="risk-pill risk-${stop.risco}">${riskLabel[stop.risco]}</span>`:'';
  let reservaBadge='';
  if(stop.reserva){
    const stored=localStorage.getItem(`reserva-${stop.nome}`);
    const defaultDone=stop.reserva==='reservado';
    const isDone=stored?stored==='done':defaultDone;
    reservaBadge=`<button class="reserva-badge ${isDone?'ok':'pending'}" data-reserva="${stop.nome.replace(/"/g,'&quot;')}" title="Clique pra alternar reserva">${isDone?'✅ RESERVADO':'☐ RESERVAR'}</button>`;
  }
  // Walking tour flag (busca + visual)
  let walkingTourFlag='';
  if(stop.walkingTours&&stop.walkingTours.length>0){
    const totalStops=stop.walkingTours.reduce((a,t)=>a+t.stops.length,0);
    const partsLabel=stop.walkingTours.length>1?`${stop.walkingTours.length} partes · ${totalStops} paradas`:`${totalStops} paradas`;
    const tourTitles=stop.walkingTours.map(t=>t.nome).join(' + ').replace(/"/g,'&quot;');
    walkingTourFlag=`<div class="walking-tour-flag" title="${tourTitles}">🚶 WALKING TOUR · ${partsLabel}</div>`;
  }
  return `<div class="stop-card" data-risco="${stop.risco||''}">
    <div class="chev">▼</div>
    ${walkingTourFlag}
    <div class="stop-head">
      <div class="stop-emoji-col">
        <div class="stop-emoji">${stop.emoji}</div>
      </div>
      <div class="stop-time-name">
        <div class="stop-time"><span class="tnum">${stop.hora}</span>${agoraPillHtml(isNow)}${riskBadge}${reservaBadge}${feitoChkHtml(stop.nome,done)}</div>
        <div class="stop-name">${stop.nome}</div>
        <div class="stop-cat">${stop.cat}</div>
      </div>
    </div>
    ${stop.sobre?`<div class="stop-body"><p>${stop.sobre}</p></div>`:''}
    ${stop.imperdivel?`<div class="stop-imperdivel"><strong>⭐ IMPERDÍVEL</strong>${stop.imperdivel}</div>`:''}
    ${stop.dicas?`<div class="stop-dicas">
      <div class="stop-dicas-title">💡 Dicas</div>
      <ul>${stop.dicas.map(d=>`<li>${d}</li>`).join('')}</ul>
    </div>`:''}
    ${(stop.duracao||stop.custo||stop.acessibilidade)?`<div class="stop-meta">
      ${stop.duracao?`<span>⏱️ ${stop.duracao}</span>`:''}
      ${stop.custo?`<span>💵 ${stop.custo}</span>`:''}
      ${stop.acessibilidade?`<span>♿ ${stop.acessibilidade}</span>`:''}
    </div>`:''}
    ${links.length?`<div class="stop-source-links">
      ${links.map(l=>`<a class="source-link ${l.type==='official'?'official':''}" href="${l.url}" target="_blank" rel="noopener">${l.type==='official'?'🌐':'📰'} ${l.label}</a>`).join('')}
    </div>`:''}
  </div>`;
}

function renderOpcoes(stop,isNow,done){
  return `<div class="stop-opcoes">
    <div class="chev">▼</div>
    <div class="stop-opcoes-head">
      <div class="stop-emoji-col">
        <div class="stop-opcoes-emoji">${stop.emoji}</div>
      </div>
      <div class="stop-opcoes-title">
        <div class="stop-time"><span class="tnum">${stop.hora}</span>${agoraPillHtml(isNow)}${feitoChkHtml(stop.nome,done)}</div>
        <div class="stop-opcoes-name">${stop.nome}</div>
        <div class="stop-opcoes-cat">${stop.cat}</div>
      </div>
    </div>
    ${stop.sobre?`<div class="stop-body" style="margin-top:6px;padding-top:6px"><p>${stop.sobre}</p></div>`:''}
    <div class="opcoes-list">
      ${stop.opcoes.map(o=>`<div class="opcao-item">
        <span class="opcao-name">${o.nome}</span>
        <span class="opcao-meta">${o.preco?'· '+o.preco:''} ${o.dist?'· '+o.dist:''}</span>
        <div class="opcao-desc">${o.desc}</div>
      </div>`).join('')}
    </div>
  </div>`;
}

// Destino de um transit: o próximo stop NÃO-transit no dia (nome com endereço/parens mantidos).
function nextStopName(day,idx){
  for(let j=idx+1;j<day.stops.length;j++){
    const s=day.stops[j];
    if(s.tipo!=='transit'){
      if(s.tipo==='opcoes' && s.opcoes && s.opcoes.length) return s.opcoes[0].nome;
      return s.nome;
    }
  }
  return null;
}

function renderTransit(stop,dest){
  const t=TRANSIT_MAP[stop.nome];
  const hasRoutes=t&&(t.ferry||t.metro||t.uber);
  const destStr=dest||stop.nome;
  const destAttr=destStr.replace(/"/g,'&quot;');
  const transitUrl=`https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(destStr+', New York, NY')}&travelmode=transit`;
  const uberLine=t&&t.uber?`<div class="route-option"><strong>🚕 Uber</strong> ${t.uber}<button class="route-act" type="button" data-copy="${destAttr}">📋 Copiar endereço</button></div>`:'';
  const metroLine=t&&t.metro?`<div class="route-option"><strong>🚇 Metrô</strong> ${t.metro}<a class="route-act" href="${transitUrl}" target="_blank" rel="noopener">🚇 Transporte público</a></div>`:'';
  return `<div class="stop-transit ${hasRoutes?'collapsible':''}">
    <div class="stop-transit-header">
      <span class="stop-transit-emoji">${stop.emoji}</span>
      <span class="stop-transit-time">${stop.hora}</span>
      <span class="stop-transit-name">${stop.nome}</span>
      ${hasRoutes?'<span class="stop-transit-chev">▼</span>':''}
    </div>
    ${stop.cat?`<div class="stop-transit-cat">${stop.cat}</div>`:''}
    ${hasRoutes?`<div class="stop-transit-routes">
      ${t.ferry?`<div class="route-option"><strong>⛴️ Ferry</strong> ${t.ferry}</div>`:''}
      ${metroLine}
      ${uberLine}
    </div>`:''}
  </div>`;
}

// Pill "Feito" rotulada · fica no meta do header (à direita, perto de hora/risco)
function feitoChkHtml(nome,done){
  return `<button class="feito-chk" data-feito="${nome.replace(/"/g,'&quot;')}" aria-label="${done?'Marcar como não-feito':'Marcar como feito'}" title="${done?'Feito — toque pra desfazer':'Marcar como feito'}"><span class="fc-gly">${done?'✓':'○'}</span> Feito</button>`;
}

function renderStop(stop,isNow,dest){
  // Transit: sem check feito · fica sempre na timeline
  if(stop.tipo==='transit') return renderTransit(stop,dest);
  const done=isFeito(stop.nome);
  const inner=stop.tipo==='card'?renderCard(stop,isNow,done):renderOpcoes(stop,isNow,done);
  return `<div class="stop-wrap${done?' is-feito':''}${isNow?' is-now':''}">${inner}</div>`;
}

function tripStats(){
  let days=DAYS.length, attractions=0, tours=0, totalReservas=0, doneReservas=0;
  let totalAttr=0, doneAttr=0, totalTours=0, doneTours=0;
  DAYS.forEach(d=>d.stops.forEach(s=>{
    if(s.tipo==='card'){ attractions++; totalAttr++; if(isFeito(s.nome)) doneAttr++; }
    if(s.walkingTours&&s.walkingTours.length){
      tours+=s.walkingTours.length;
      totalTours+=s.walkingTours.length;
      if(isFeito(s.nome)) doneTours+=s.walkingTours.length; // tour feito se o card-pai é feito
    }
    if(s.reserva){
      totalReservas++;
      const stored=localStorage.getItem(`reserva-${s.nome}`);
      const isDone=stored?stored==='done':s.reserva==='reservado';
      if(isDone) doneReservas++;
    }
  }));
  return {days,attractions,tours,totalReservas,doneReservas,
          totalAttr,doneAttr,totalTours,doneTours};
}

function renderStatusBar(){
  const st=tripStats();
  const expanded=(()=>{ try{return localStorage.getItem('statusExpanded')==='1';}catch(e){return false;} })();
  // Chip de reservas só quando NÃO estão todas completas (completas viram nota no rodapé)
  const reservasComplete=st.totalReservas>0 && st.doneReservas===st.totalReservas;
  const reservasChip=reservasComplete?'':`<button class="sb-chip" id="sb-reservas" title="Ver reservas pendentes">☐ Reservas <span class="tnum">${st.doneReservas}/${st.totalReservas}</span> <span class="sb-arr">›</span></button>`;

  if(!IS_TRIP){
    // Modo cidade (coletânea sem datas): sem "Hoje/data real", sem stat de Dias, sem AGORA.
    // Só mostra reservas (se houver pendentes) + stats de atrações/tours. Se nada, oculta a barra.
    const hasContent=(!reservasComplete && st.totalReservas>0) || st.totalAttr>0 || st.totalTours>0;
    if(!hasContent) return '';
    return `<div class="status-bar" id="status-bar">
    <div class="sb-row">
      ${reservasChip||'<span class="sb-day">📍 Passeios</span>'}
      <button class="sb-expand ${expanded?'open':''}" id="sb-expand" aria-expanded="${expanded}">stats <span class="sb-cx">▾</span></button>
    </div>
    <div class="sb-stats ${expanded?'open':''}" id="sb-stats">
      <button class="sb-stat" data-goto="afazer"><div class="sbs-num tnum">${st.doneAttr}<em> / ${st.totalAttr}</em></div><div class="sbs-lbl">Atrações</div></button>
      <button class="sb-stat" data-goto="afazer"><div class="sbs-num tnum">${st.doneTours}<em> / ${st.totalTours}</em></div><div class="sbs-lbl">Walking tours</div></button>
    </div>
  </div>`;
  }

  return `<div class="status-bar" id="status-bar">
    <div class="sb-row">
      <span class="sb-day">📅 Hoje · <span class="tnum">${hojeLabel()}</span></span>
      ${reservasChip}
      <button class="sb-expand ${expanded?'open':''}" id="sb-expand" aria-expanded="${expanded}">stats <span class="sb-cx">▾</span></button>
    </div>
    <div class="sb-stats ${expanded?'open':''}" id="sb-stats">
      <button class="sb-stat" data-goto="dia"><div class="sbs-num tnum">${diasElapsed()}<em> / ${st.days}</em></div><div class="sbs-lbl">Dias</div></button>
      <button class="sb-stat" data-goto="afazer"><div class="sbs-num tnum">${st.doneAttr}<em> / ${st.totalAttr}</em></div><div class="sbs-lbl">Atrações</div></button>
      <button class="sb-stat" data-goto="afazer"><div class="sbs-num tnum">${st.doneTours}<em> / ${st.totalTours}</em></div><div class="sbs-lbl">Walking tours</div></button>
    </div>
  </div>`;
}

// Nota "Reservas completas" no rodapé · aparece só quando todas as reservas estão feitas
function updateReservasNote(){
  const el=document.getElementById('reservas-note');
  if(!el) return;
  const st=tripStats();
  const complete=st.totalReservas>0 && st.doneReservas===st.totalReservas;
  el.innerHTML=complete?`<div class="reservas-done">✅ Reservas completas (${st.doneReservas}/${st.totalReservas})</div>`:'';
}

function renderDay(day){
  const periodos=['manha','tarde','noite'];
  const bigEmoji=(day.stops.find(s=>s.tipo==='card')||day.stops[0]||{}).emoji||'📍';
  const parts=(day.date||'').split(' ');
  const dow=parts[0]||'', dm=parts[1]||'';
  const nowIdx=getNowStopIdx(day,state.selIdx);

  // Checkáveis do dia (card/opcoes) · pra contagem ✓ X/Y
  const checkable=day.stops.filter(s=>s.tipo==='card'||s.tipo==='opcoes');
  const doneCount=checkable.filter(s=>isFeito(s.nome)).length;
  const doneKicker=checkable.length?`<span class="grp">✓ ${doneCount}/${checkable.length} feitas</span>`:'';

  // Kicker: trip mostra "Dia N de M" · city mostra o tema-curto (label do tema) sem contagem/data
  const kickerLabel=IS_TRIP?`🗽 Dia ${state.selIdx+1} de ${DAYS.length}`:`📍 ${day.temaCurto||day.tema.split('·')[0].trim()}`;
  const heroAndNota=`<div class="day-hero" style="--day-color:${day.cor};--day-grad-a:${day.gradA};--day-grad-b:${day.gradB}" data-bigemoji="${bigEmoji}">
      <div class="hero-inner">
        <span class="hero-kicker">${kickerLabel}${day.grupo?'<span class="grp">👥 Família junta</span>':doneKicker}</span>
        ${IS_TRIP?`<div class="hero-date">${dow} · ${dm}</div>`:''}
        <div class="hero-title">${day.tema}</div>
        <div class="hero-bairro">📍 ${day.bairro}</div>
      </div>
    </div>
    ${day.nota?`<div class="day-nota">${day.nota}</div>`:''}`;

  // Timeline: só stops NÃO-feitos (transit sempre fica) · feitos vão pra seção final
  const grouped={manha:[],tarde:[],noite:[]};
  day.stops.forEach((s,i)=>{
    if(!grouped[s.periodo]) return;
    const isCheckable=(s.tipo==='card'||s.tipo==='opcoes');
    if(isCheckable && isFeito(s.nome)) return; // vai pra Feitas hoje
    grouped[s.periodo].push({s,i});
  });

  const timeline=`<div class="timeline" style="--day-color:${day.cor};--day-grad-a:${day.gradA};--day-grad-b:${day.gradB}">
    ${periodos.filter(p=>grouped[p].length>0).map(p=>{
      const m=getPeriodoMeta(p);
      return `<div class="period">
        <div class="period-label"><span class="pe">${m.emoji}</span> ${m.label}</div>
        <div class="tl-stops">${grouped[p].map(({s,i})=>`<div class="tl-item${s.tipo==='transit'?' is-transit':''}">${renderStop(s,i===nowIdx,s.tipo==='transit'?nextStopName(day,i):null)}</div>`).join('')}</div>
      </div>`;
    }).join('')}
  </div>`;

  // Feitas hoje: stops checkáveis feitos, em ordem cronológica original
  const doneStops=day.stops.filter(s=>(s.tipo==='card'||s.tipo==='opcoes') && isFeito(s.nome));
  let feitas='';
  if(doneStops.length){
    const open=(()=>{ try{return localStorage.getItem('feitasOpen_'+state.selIdx)!=='0';}catch(e){return true;} })();
    feitas=`<div class="feitas-section ${open?'open':''}" style="--day-color:${day.cor}">
      <button class="feitas-head" id="feitas-head">
        <span class="fh-ico">✓</span>
        <span class="fh-txt">Feitas hoje (${doneStops.length})</span>
        <span class="fh-cx">▼</span>
      </button>
      <div class="feitas-list">
        ${doneStops.map(s=>{
          const nm=s.nome.replace(/"/g,'&quot;');
          return `<div class="feitas-item" data-jump="${nm}">
            <div class="fi-emoji">${s.emoji}</div>
            <div class="fi-txt"><div class="fi-name">${s.nome}</div><div class="fi-time"><span class="tnum">${s.hora}</span> · ${(s.cat||'').split('·')[0].trim()}</div></div>
            <button class="fi-undo" data-feito="${nm}" title="Desfazer">↺</button>
          </div>`;
        }).join('')}
      </div>
    </div>`;
  }

  return heroAndNota + timeline + feitas;
}

// Linha de tarefa (stop) clicável nos filtros A fazer / Feitas / pending
function ovTaskRow(stop,dayIdx,extraClass){
  const nm=stop.nome.replace(/"/g,'&quot;');
  const check=extraClass==='done'?'✓':(extraClass==='pend'?'☐':'○');
  return `<div class="ov-task ${extraClass||''}" data-idx="${dayIdx}" data-jump="${nm}">
    <div class="ot-emoji">${stop.emoji}</div>
    <div class="ot-txt"><div class="ot-name">${stop.nome}</div><div class="ot-meta"><span class="tnum">${stop.hora}</span> · ${(stop.cat||'').split('·')[0].trim()}</div></div>
    <div class="ot-check">${check}</div>
  </div>`;
}

// Agrupa stops por dia e renderiza (usado por A fazer / Feitas)
function ovDayGroups(predicate,doneClass){
  let html='',any=false;
  DAYS.forEach((d,i)=>{
    const matched=d.stops.filter(s=>(s.tipo==='card'||s.tipo==='opcoes') && predicate(s));
    if(!matched.length) return;
    any=true;
    html+=`<div class="ov-daygroup">
      <div class="ov-daygroup-h"><span class="dg-swatch" style="background:${d.cor}"></span>${d.tema}<span class="dg-date">${d.date}</span></div>
      ${matched.map(s=>ovTaskRow(s,i,doneClass)).join('')}
    </div>`;
  });
  return {html,any};
}

function renderOverview(){
  const filter=state.ovFilter||'roteiro';
  const seg=`<div class="ov-seg">
    <button class="ov-seg-btn ${filter==='roteiro'?'active':''}" data-filter="roteiro">Roteiro</button>
    <button class="ov-seg-btn ${filter==='afazer'?'active':''}" data-filter="afazer">A fazer</button>
    <button class="ov-seg-btn ${filter==='feitas'?'active':''}" data-filter="feitas">Feito</button>
  </div>`;

  // Seção pinada de reservas pendentes (só quando aberto pela chip ☐ Reservas)
  let pendingHtml='';
  if(state.ovShowPending){
    const pend=[];
    DAYS.forEach((d,i)=>d.stops.forEach(s=>{
      if(!s.reserva) return;
      const stored=localStorage.getItem(`reserva-${s.nome}`);
      const done=stored?stored==='done':s.reserva==='reservado';
      if(!done) pend.push({s,i});
    }));
    if(pend.length){
      pendingHtml=`<div class="ov-pending">
        <div class="ov-pending-h">☐ Reservas pendentes (${pend.length})</div>
        ${pend.map(({s,i})=>ovTaskRow(s,i,'pend')).join('')}
      </div>`;
    } else {
      pendingHtml=`<div class="ov-pending"><div class="ov-pending-h">☑ Reservas em dia</div><div style="font-size:13px;color:#7a5618">Nada pendente — todas as reservas marcadas.</div></div>`;
    }
  }

  const head=`<div class="ov-head">
      <h2>Toda a viagem</h2>
      <button class="ov-close" id="ov-close">Fechar ✕</button>
    </div>`;

  if(filter==='afazer'){
    const g=ovDayGroups(s=>!isFeito(s.nome),'pend');
    return head+pendingHtml+seg+(g.any?g.html:`<div class="ov-empty">🎉 Tudo feito! Nada na lista.</div>`);
  }
  if(filter==='feitas'){
    const g=ovDayGroups(s=>isFeito(s.nome),'done');
    return head+pendingHtml+seg+(g.any?g.html:`<div class="ov-empty">Nada marcado como feito ainda.<br>Use o toque ○ na borda dos cards durante a viagem.</div>`);
  }

  // filter === 'roteiro' (default)
  return head+pendingHtml+seg+`<div class="ov-grid">
    ${DAYS.map((d,i)=>{
      const cards=d.stops.filter(s=>s.tipo==='card');
      const main=cards.length?cards[0].nome:'—';
      const wtCards=cards.filter(c=>c.walkingTours&&c.walkingTours.length>0);
      const parts=(d.date||'').split(' ');
      const dm=(parts[1]||'').split('/')[0];
      const wtButtons=wtCards.map(c=>{
        const totalStops=c.walkingTours.reduce((a,t)=>a+t.stops.length,0);
        const wtShort=c.walkingTours.length===1
          ?c.walkingTours[0].nome.split('·')[0].trim()
          :c.nome.split('·')[0].trim();
        const partsLabel=c.walkingTours.length>1
          ?`${c.walkingTours.length} partes · ${totalStops} paradas`
          :`${totalStops} paradas`;
        return `<button class="ov-wt-btn" data-idx="${i}" data-stop="${c.nome.replace(/"/g,'&quot;')}" title="Ir pro card: ${c.nome}">🚶 ${wtShort} · ${partsLabel}</button>`;
      }).join('');
      return `<div class="ov-row clickable" data-idx="${i}">
        <div class="ov-daycol" style="--g1:${d.gradA};--g2:${d.gradB}">
          <span class="dow">${parts[0]}</span><span class="dnum tnum">${dm}</span>
        </div>
        <div class="ov-body">
          <div class="ov-tema">${d.tema}</div>
          <div class="ov-meta"><span>📍 ${d.bairro}</span>${d.grupo?'<span class="ov-grp">👥 família</span>':''}</div>
          <div class="ov-attr"><b>★</b> ${main}</div>
          ${wtButtons}
        </div>
      </div>`;
    }).join('')}
    </div>`;
}

function renderDayTabs(){
  return `<div class="daystrip-wrap"><div class="daystrip">${DAYS.map((d,i)=>{
    const labelCurto=d.temaCurto||d.tema.split('·')[0].trim();
    const parts=(d.date||'').split(' ');
    const dm=(parts[1]||'').split('/')[0];
    // trip: DOW grande + dia-número + tema-curto abaixo · city: só o rótulo do tema (sem data)
    const inner=IS_TRIP
      ?`<span class="dt-dow">${parts[0]||''}</span>
    <span class="dt-num tnum">${dm}</span>
    <span class="dt-tag">${labelCurto}</span>`
      :`<span class="dt-num" style="font-size:15px;letter-spacing:-.2px;line-height:1.15;text-align:center">${labelCurto}</span>`;
    return `<button class="day-tab ${i===state.selIdx?'active':''}" data-idx="${i}" style="--day-color:${d.cor}">
    ${inner}
    ${d.grupo?'<span class="group-dot">👥</span>':''}
  </button>`;
  }).join('')}</div></div>`;
}

function getBairroForCoord(lat, lng){
  // Detecção canônica de bairro por coordenadas
  if(lat>40.715 && lat<40.745 && lng>-73.97 && lng<-73.93) return '🏘️ Greenpoint / Williamsburg';
  if(lat>40.69 && lat<40.715 && lng>-74.00 && lng<-73.985) return '🌉 DUMBO / Brooklyn Bridge Park';
  if(lat>40.70 && lat<40.72 && lng>-74.02 && lng<-74.00) return '🗽 Lower Manhattan / Financial';
  if(lat>40.726 && lat<40.74 && lng>-74.01 && lng<-73.99) return '🎨 Greenwich Village / West Village';
  if(lat>40.74 && lat<40.76 && lng>-74.015 && lng<-73.99) return '🌿 Chelsea / Meatpacking / Hudson Yards';
  if(lat>40.75 && lat<40.77 && lng>-74.00 && lng<-73.97) return '🏢 Midtown';
  if(lat>40.76 && lat<40.79 && lng>-73.99 && lng<-73.96) return '🌳 Central Park / Upper West Side';
  if(lat>40.76 && lat<40.79 && lng>-73.97 && lng<-73.94) return '🏛️ Upper East Side';
  if(lat>40.55 && lat<40.60) return '🏖️ Brooklyn Sul';
  if(lat>40.68 && lat<40.70) return '🌴 Prospect Park area';
  return '📍 Outros';
}

function renderBairros(){
  const bairros={};
  DAYS.forEach((d,i)=>{
    d.stops.filter(s=>s.tipo==='card' && s.coord).forEach(s=>{
      const b=getBairroForCoord(s.coord.lat, s.coord.lng);
      if(!bairros[b]) bairros[b]=[];
      bairros[b].push({stop:s,date:d.date,dayIdx:i});
    });
  });
  // Ordenar bairros pela frequência (mais visitados primeiro)
  const sorted=Object.keys(bairros).sort((a,b)=>bairros[b].length-bairros[a].length);
  return `<div class="section-title">Por bairro</div>
  <div class="section-sub">${sorted.length} áreas · toque numa atração pra abrir no roteiro</div>
  <div class="bairros-list">
    ${sorted.map(b=>`<div class="bairro-block">
      <div class="bairro-name">${b}<span class="bairro-count">${bairros[b].length}</span></div>
      <div class="bairro-attrs">
        ${bairros[b].map(item=>`<div class="bairro-attr" data-idx="${item.dayIdx}">
          <div class="bairro-attr-emoji">${item.stop.emoji}</div>
          <div class="bairro-attr-txt">
            <div class="bairro-attr-name">${item.stop.nome}</div>
            <div class="bairro-attr-day">${item.date} · ${item.stop.hora}</div>
          </div>
        </div>`).join('')}
      </div>
    </div>`).join('')}
  </div>`;
}

// ============== HISTÓRIA & CURIOSIDADES (prosa por polo · estilo coletânea Marais) ==============
// Conteúdo vem do array HISTORIA [{titulo, prosa_html}] (fornecido pela destination-scout).
// A aba só aparece se HISTORIA tiver conteúdo (revelada no init()).
function renderHistoria(){
  if(typeof HISTORIA==='undefined' || !HISTORIA.length)
    return `<div class="hist-wrap"><div class="hist-empty">Sem conteúdo de história ainda.</div></div>`;
  return `<div class="hist-wrap">
    <div class="hist-head"><div class="hist-title">📖 História & Curiosidades</div>
      <div class="hist-sub">O porquê de cada lugar — leitura solta, sem mapa nem horário</div></div>
    ${HISTORIA.map((h,i)=>`<details class="hist-block" ${i===0?'open':''}>
      <summary class="hist-polo">${h.titulo}</summary>
      <div class="hist-prosa">${h.prosa_html||''}</div>
    </details>`).join('')}
  </div>`;
}

// ============== TUDO NO MAPA (mapa unificado · todos os POIs) ==============
// Sinais independentes (handoff §4.3): recompensa ★ = tamanho do pino · risco = anel colorido.
const POI_COLOR={atracao:'#2563eb',restaurante:'#ea580c',cafe:'#92400e',padaria:'#db2777',
  loja:'#7c3aed',bar:'#0891b2',parque:'#0d9488',mercado:'#64748b','food-hall':'#ca8a04'};
const POI_EMOJI={atracao:'🎯',restaurante:'🍽️',cafe:'☕',padaria:'🥐',loja:'🛍️',bar:'🍸',
  parque:'🌳',mercado:'🛒','food-hall':'🍴'};
const RISCO_RING={green:'#22c55e',yellow:'#eab308',red:'#ef4444'};
const STAR_SIZE={3:34,2:26,1:20,0:17};
const STAR_TXT={3:'⭐⭐⭐ Vale a viagem',2:'⭐⭐ Vale o desvio',1:'⭐ Se sobrar',0:'⏭️ Pula sem culpa'};
// grupos de filtro por categoria
const POI_GROUP={atracao:'atracao',restaurante:'comida',cafe:'comida',padaria:'comida',bar:'comida',
  mercado:'comida','food-hall':'comida',loja:'loja',parque:'parque'};
const GROUP_LABEL={atracao:'🎯 Atrações',comida:'🍴 Comida',loja:'🛍️ Lojas',parque:'🌳 Parques'};

// Achata todos os POIs da viagem (cards + itens de opcoes + paradas de walking tour).
function collectPOIs(){
  const out=[];
  DAYS.forEach((day,di)=>{
    day.stops.forEach(s=>{
      if(s.tipo==='transit') return;
      if(s.tipo==='card' && s.coord){
        out.push({nome:s.nome,poiCat:s.poiCat||'atracao',va:s.valeAPena,risco:s.risco,
          coord:s.coord,dia:day.date,di,mapsUrl:getMapsUrl(s),cat:s.cat||''});
        (s.walkingTours||[]).forEach(t=>t.stops.forEach(st=>{
          if(st.coord) out.push({nome:st.nome,poiCat:'atracao',va:undefined,risco:undefined,
            coord:st.coord,dia:day.date,di,mapsUrl:getMapsUrl({nome:st.nome,coord:st.coord}),cat:'Parada · '+t.nome});
        }));
      } else if(s.tipo==='opcoes'){
        (s.opcoes||[]).forEach(o=>{ if(o.coord) out.push({nome:o.nome,poiCat:o.poiCat||'restaurante',
          va:o.valeAPena,risco:undefined,coord:o.coord,dia:day.date,di,
          mapsUrl:getMapsUrl({nome:o.nome,coord:o.coord}),cat:o.desc||''}); });
      }
    });
  });
  // POIs extras (recomendações soltas · di=-1 → aparecem só com filtro de dia "todos")
  if(typeof EXTRAS!=='undefined') EXTRAS.forEach(e=>{ if(e.coord) out.push({
    nome:e.nome,poiCat:e.poiCat||'atracao',va:e.valeAPena,risco:e.risco,coord:e.coord,
    dia:'💡 Dica do chat',di:-1,mapsUrl:getMapsUrl({nome:e.nome,coord:e.coord}),cat:e.cat||''}); });
  return out;
}

let tudoMapInstance=null;
function renderTudoMapa(){
  const f=state.mapFilter;
  const tierBtn=(v,l)=>`<button class="tm-chip ${f.minStar===v?'on':''}" data-tier="${v}">${l}</button>`;
  const catBtn=g=>`<button class="tm-chip ${f.groups.has(g)?'on':''}" data-group="${g}">${GROUP_LABEL[g]}</button>`;
  const dayOpts=['<option value="-1">Todos os dias</option>']
    .concat(DAYS.map((d,i)=>`<option value="${i}" ${f.day===i?'selected':''}>${d.date}</option>`)).join('');
  setTimeout(plotTudoMapa,0);
  return `<div class="tudomapa-wrap">
    <div class="tm-head">
      <div class="tm-title">🗺️ Tudo no Mapa</div>
      <div class="tm-sub">Tamanho do pino = ★ recompensa · anel = 🟢🟡🔴 risco (eixos independentes)</div>
      <a class="tm-dl" href="pois.csv" download="pois.csv" target="_blank" rel="noopener">⬇️ Baixar CSV (pro Google My Maps · abre em nova aba)</a>
    </div>
    <div class="tm-filters">
      <div class="tm-row">${tierBtn(3,'⭐⭐⭐')}${tierBtn(2,'⭐⭐+')}${tierBtn(0,'Tudo')}</div>
      <div class="tm-row">${['atracao','comida','loja','parque'].map(catBtn).join('')}</div>
      <div class="tm-row"><select class="tm-day" id="tm-day">${dayOpts}</select>
        <button class="tm-chip tm-locate" id="tm-locate">📍 Onde estou</button></div>
    </div>
    <div id="tudo-map"></div>
  </div>`;
}

let userLoc=null;   // {lat,lng} da geolocalização (sessão)
function locateMe(){
  const btn=document.getElementById('tm-locate');
  if(!navigator.geolocation){ if(btn) btn.textContent='📍 Sem GPS'; return; }
  if(btn){ btn.textContent='📍 Localizando…'; btn.disabled=true; }
  navigator.geolocation.getCurrentPosition(pos=>{
    userLoc={lat:pos.coords.latitude,lng:pos.coords.longitude};
    if(btn){ btn.textContent='📍 Centralizar em mim'; btn.disabled=false; }
    plotTudoMapa();
    if(tudoMapInstance) tudoMapInstance.setView([userLoc.lat,userLoc.lng],15);
  },err=>{
    if(btn){ btn.textContent='📍 GPS negado'; btn.disabled=false; }
  },{enableHighAccuracy:true,timeout:10000,maximumAge:60000});
}

function plotTudoMapa(){
  const div=document.getElementById('tudo-map'); if(!div) return;
  if(tudoMapInstance){ tudoMapInstance.remove(); tudoMapInstance=null; }
  tudoMapInstance=L.map(div,{zoomControl:true,scrollWheelZoom:true});
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap',maxZoom:19}).addTo(tudoMapInstance);
  const f=state.mapFilter;
  const pois=collectPOIs().filter(p=>{
    const va=(p.va===undefined||p.va===null)?1:p.va;   // WT stops (sem va) = tier ⭐ · só no "Tudo", não poluem o default ⭐⭐⭐
    if(va<f.minStar) return false;
    if(!f.groups.has(POI_GROUP[p.poiCat]||'atracao')) return false;
    if(f.day>=0 && p.di!==f.day) return false;
    return true;
  });
  if(!pois.length){ tudoMapInstance.setView([40.75,-73.97],12);
    const el=document.getElementById('tm-count'); if(el) el.textContent='0'; return; }
  const pts=[];
  pois.forEach(p=>{
    const va=(p.va===undefined||p.va===null)?1:p.va;
    const size=STAR_SIZE[va]||20;
    const ring=RISCO_RING[p.risco]||'#cbd5e1';
    const color=POI_COLOR[p.poiCat]||'#2563eb';
    const icon=L.divIcon({className:'poi-marker',
      html:`<div class="poi-dot" style="width:${size}px;height:${size}px;background:${color};border-color:${ring};font-size:${Math.round(size*0.5)}px">${POI_EMOJI[p.poiCat]||'📍'}</div>`,
      iconSize:[size,size],iconAnchor:[size/2,size/2],popupAnchor:[0,-size/2]});
    const starLine=(p.va===undefined||p.va===null)?'':`<div class="pp-notes">${STAR_TXT[p.va]||''}</div>`;
    const riscoLine=p.risco?`<div class="pp-notes">Risco: ${({green:'🟢 tranquilo',yellow:'🟡 atenção',red:'🔴 alta atenção'})[p.risco]}</div>`:'';
    const popup=`<div class="pp-name">${p.nome}</div>
      <div class="pp-notes">${POI_EMOJI[p.poiCat]||''} ${p.dia}</div>
      ${starLine}${riscoLine}
      ${p.mapsUrl?`<a class="pp-link" style="background:${POI_COLOR[p.poiCat]||'#2563eb'}" href="${p.mapsUrl}" target="_blank" rel="noopener">📍 Abrir no Google Maps</a>`:''}`;
    L.marker([p.coord.lat,p.coord.lng],{icon}).bindPopup(popup,{maxWidth:240}).addTo(tudoMapInstance);
    pts.push([p.coord.lat,p.coord.lng]);
  });
  // Marcador "você está aqui" (se geolocalizado)
  if(userLoc){
    const meIcon=L.divIcon({className:'poi-marker',
      html:`<div class="me-dot"></div>`,iconSize:[18,18],iconAnchor:[9,9]});
    L.marker([userLoc.lat,userLoc.lng],{icon:meIcon,zIndexOffset:1000}).bindPopup('📍 Você está aqui').addTo(tudoMapInstance);
  }
  tudoMapInstance.fitBounds(pts,{padding:[40,40],maxZoom:15});
  const el=document.getElementById('tm-count'); if(el) el.textContent=pois.length;
  // bind filtros (idempotente)
  const wrap=div.closest('.tudomapa-wrap');
  if(wrap && !wrap.__bound){
    wrap.__bound=true;
    const lb=wrap.querySelector('#tm-locate'); if(lb) lb.addEventListener('click',locateMe);
    wrap.querySelectorAll('[data-tier]').forEach(b=>b.addEventListener('click',()=>{
      state.mapFilter.minStar=parseInt(b.dataset.tier);
      wrap.querySelectorAll('[data-tier]').forEach(x=>x.classList.toggle('on',x===b));
      plotTudoMapa();
    }));
    wrap.querySelectorAll('[data-group]').forEach(b=>b.addEventListener('click',()=>{
      const g=b.dataset.group; const gs=state.mapFilter.groups;
      if(gs.has(g)) gs.delete(g); else gs.add(g);
      b.classList.toggle('on',gs.has(g));
      plotTudoMapa();
    }));
    const sel=wrap.querySelector('#tm-day');
    if(sel) sel.addEventListener('change',()=>{ state.mapFilter.day=parseInt(sel.value); plotTudoMapa(); });
  }
}

let mapInstance=null;
function renderMap(){
  const day=DAYS[state.selIdx];
  const stops=day.stops.filter(s=>s.tipo!=='transit' && s.coord);
  // Cards do dia com walking tours (array de partes)
  const cardsWithTours=day.stops.filter(s=>s.walkingTours&&s.walkingTours.length>0);
  // Helper: limpa nome pra busca no Google Maps (mantém endereço entre parens)
  const cleanForSearch=nm=>nm.replace(/[()]/g,'').replace(/\s+/g,' ').trim();
  setTimeout(()=>{
    if(mapInstance){ mapInstance.remove(); mapInstance=null; }
    const div=document.getElementById('map');
    if(!div) return;
    mapInstance=L.map(div,{zoomControl:true,scrollWheelZoom:true});
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
      attribution:'© OpenStreetMap',maxZoom:19
    }).addTo(mapInstance);
    if(stops.length===0){ mapInstance.setView([40.72,-73.95],12); return; }
    const latlngs=stops.map(s=>[s.coord.lat,s.coord.lng]);
    stops.forEach((s,i)=>{
      const isOpcoes=s.tipo==='opcoes' && s.opcoes && s.opcoes.length>0;
      const principalName=isOpcoes?s.opcoes[0].nome.split('(')[0].trim():'';
      const popupHtml=`<div class="pp-time" style="color:${day.cor}">${s.hora}</div>
        <div class="pp-name">${s.nome}</div>
        <div class="pp-notes">${s.cat||''}</div>
        ${isOpcoes?`<div class="pp-notes" style="margin-top:6px"><strong>📍 Principal:</strong> ${principalName}</div>`:''}
        ${getMapsUrl(s)?`<a class="pp-link" style="background:${day.cor}" href="${getMapsUrl(s)}" target="_blank" rel="noopener">📍 Abrir no Google Maps</a>`:''}`;
      const numIcon=L.divIcon({
        className:'wt-marker',
        html:`<div style="background:${day.cor};color:#fff;border:2px solid #fff">${i+1}</div>`,
        iconSize:[24,24],iconAnchor:[12,12],popupAnchor:[0,-12]
      });
      L.marker([s.coord.lat,s.coord.lng],{icon:numIcon})
        .bindPopup(popupHtml,{maxWidth:240})
        .addTo(mapInstance);
    });
    if(latlngs.length>1){
      L.polyline(latlngs,{color:day.cor,weight:3,opacity:0.7,dashArray:'6,8'}).addTo(mapInstance);
    }
    // WALKING TOURS: cor fixa ROXA (#6d5efc) · distinta da cor do dia (marcadores + linha)
    const WT_COLOR='#6d5efc';
    cardsWithTours.forEach(card=>{
      card.walkingTours.forEach((tour,partIdx)=>{
        const tourStops=tour.stops;
        const tourLatLngs=tourStops.map(t=>[t.coord.lat,t.coord.lng]);
        // Polyline: Parte 1 tracejada normal · Parte 2 tracejada mais fina
        const dashStyle=partIdx===0?'4,5':'2,6';
        L.polyline(tourLatLngs,{color:WT_COLOR,weight:2.5,opacity:0.85,dashArray:dashStyle}).addTo(mapInstance);
        // Marcadores: Parte 1 preenchidos roxo · Parte 2 contorno roxo
        const markerStyle=partIdx===0
          ?`background:${WT_COLOR};color:#fff;border:2px solid #fff`
          :`background:#fff;color:${WT_COLOR};border:2px solid ${WT_COLOR}`;
        tourStops.forEach(t=>{
          const icon=L.divIcon({
            className:'wt-marker',
            html:`<div style="${markerStyle}">${t.n}</div>`,
            iconSize:[24,24],iconAnchor:[12,12],popupAnchor:[0,-12]
          });
          const searchName=cleanForSearch(t.nome);
          const url=`https://www.google.com/maps/search/${encodeURIComponent(searchName)}/@${t.coord.lat},${t.coord.lng},17z`;
          const popupHtml=`<div class="pp-time" style="color:${day.cor}">${tour.nome.split('·')[0].trim()} · parada ${t.n}</div>
            <div class="pp-name">${t.nome}</div>
            <a class="pp-link" style="background:${day.cor}" href="${url}" target="_blank" rel="noopener">📍 Abrir no Google Maps</a>`;
          L.marker([t.coord.lat,t.coord.lng],{icon})
            .bindPopup(popupHtml,{maxWidth:240})
            .addTo(mapInstance);
        });
      });
    });
    // Ajustar bounds incluindo walking tours
    const allLatLngs=[...latlngs];
    cardsWithTours.forEach(c=>c.walkingTours.forEach(t=>t.stops.forEach(s=>allLatLngs.push([s.coord.lat,s.coord.lng]))));
    mapInstance.fitBounds(allLatLngs,{padding:[40,40]});
  },50);
  const legend=stops.map((s,i)=>{const u=getMapsUrl(s);const inner=`<div class="stop-num" style="background:${day.cor}">${i+1}</div><span class="legend-hora">${s.hora}</span><span class="legend-nome">${s.nome.split('(')[0].trim()}</span>${u?'<span class="legend-go">↗</span>':''}`;return u?`<a class="stop-legend-item" href="${u}" target="_blank" rel="noopener" title="Abrir ${s.nome.split('(')[0].trim()} no Google Maps">${inner}</a>`:`<div class="stop-legend-item">${inner}</div>`;}).join('');
  // 1 botão por parte de walking tour
  const tourButtons=cardsWithTours.flatMap(card=>
    card.walkingTours.map(t=>
      `<a class="gmaps-btn walking-tour-btn" href="${getWalkingTourUrl(t.stops)}" target="_blank" rel="noopener">🚶 ${t.nome} · ${t.stops.length} paradas</a>`
    )
  ).join('');
  return `<div class="map-section" style="--day-color:${day.cor}">
    ${stops.length?`<div class="stop-legend">${legend}</div>`:''}
    <div id="map"></div>
    <div class="map-cta">
      <a class="gmaps-btn" href="${getRouteUrl(day)}" target="_blank" rel="noopener">🗺️ Abrir rota do dia no Google Maps (${dayTransport(day)==='driving'?'carro':'a pé'})</a>
      ${tourButtons}
      <span class="map-hint">Clique nos marcadores pros detalhes${cardsWithTours.length?' · pontos pequenos cheios = parte 1 · contorno = parte 2':''}</span>
    </div>
  </div>`;
}

function renderSearch(query){
  const q=query.toLowerCase().trim();
  if(!q) return '';
  const results=[];
  DAYS.forEach((d,i)=>{
    d.stops.forEach(s=>{
      let hay=`${s.nome} ${s.cat||''} ${s.sobre||''} ${d.bairro} ${d.tema}`;
      // Indexar walking tour: nomes das partes + nomes das paradas + dicas
      if(s.walkingTours&&s.walkingTours.length>0){
        hay+=' walking tour ';
        s.walkingTours.forEach(t=>{
          hay+=t.nome+' '+(t.descricao||'')+' ';
          t.stops.forEach(p=>hay+=p.nome+' ');
        });
      }
      // Indexar dicas também (curiosidades como "Hamilton", "Dylan", "Anchorage")
      if(s.dicas) hay+=' '+s.dicas.join(' ');
      if(hay.toLowerCase().includes(q)){
        results.push({stop:s,day:d,idx:i});
      }
    });
  });
  if(results.length===0){
    return `<div class="search-result-empty">Nenhum resultado pra "${query}"</div>`;
  }
  return results.slice(0,12).map(r=>{
    const wtBadge=r.stop.walkingTours?'<span class="search-wt-tag">🚶 WALKING TOUR</span>':'';
    return `<div class="search-result" data-idx="${r.idx}">
    <div class="search-result-name">${r.stop.emoji} ${r.stop.nome}${wtBadge}</div>
    <div class="search-result-meta">${r.day.date} · ${r.stop.hora} · ${r.day.bairro}</div>
  </div>`;
  }).join('');
}

function centerActiveTab(){
  setTimeout(()=>{
    const active=document.querySelector('.day-tab.active');
    if(active) active.scrollIntoView({behavior:'smooth',inline:'center',block:'nearest'});
  },80);
}

function renderInnerContent(){
  // Re-render apenas conteúdo do dia (sem rebuildar os tabs)
  const inner=document.getElementById('inner-content');
  if(!inner) return;
  if(state.view==='guia'){
    inner.innerHTML=renderDay(DAYS[state.selIdx]);
  } else if(state.view==='mapa'){
    inner.innerHTML=renderMap();
  }
  bindCardHandlers();
}

function bindCardHandlers(){
  document.querySelectorAll('.stop-card, .stop-opcoes, .stop-transit.collapsible').forEach(c=>{
    if(c.__bound) return;
    c.__bound=true;
    c.addEventListener('click',e=>{
      if(e.target.closest('a, button')) return;
      c.classList.toggle('expanded');
    });
  });
  document.querySelectorAll('[data-reserva]').forEach(b=>{
    if(b.__bound) return;
    b.__bound=true;
    b.addEventListener('click',e=>{
      e.stopPropagation();
      const name=b.dataset.reserva;
      const wasDone=b.classList.contains('ok');
      const willBeDone=!wasDone;
      try{ localStorage.setItem(`reserva-${name}`,willBeDone?'done':'pending'); }catch(e){}
      b.classList.toggle('ok',willBeDone);
      b.classList.toggle('pending',!willBeDone);
      b.textContent=willBeDone?'✅ RESERVADO':'☐ RESERVAR';
      // Reservas afetam o chip do topo (some quando 4/4) e a nota do rodapé
      const sb=document.getElementById('status-bar');
      if(sb && state.view==='guia'){ sb.outerHTML=renderStatusBar(); bindStatusBar(); }
      updateReservasNote();
    });
  });
  // Transit · botão "Copiar endereço" (copia destino pro clipboard, com fallback)
  document.querySelectorAll('[data-copy]').forEach(b=>{
    if(b.__bound) return;
    b.__bound=true;
    b.addEventListener('click',e=>{
      e.stopPropagation();
      const txt=b.dataset.copy;
      const flash=()=>{
        const orig=b.innerHTML;
        b.innerHTML='copiado ✓';
        setTimeout(()=>{ b.innerHTML=orig; },1500);
      };
      const fallback=()=>{
        try{
          const ta=document.createElement('textarea');
          ta.value=txt; ta.style.position='fixed'; ta.style.opacity='0';
          document.body.appendChild(ta); ta.focus(); ta.select();
          document.execCommand('copy'); document.body.removeChild(ta);
        }catch(err){}
        flash();
      };
      if(navigator.clipboard&&navigator.clipboard.writeText){
        navigator.clipboard.writeText(txt).then(flash,fallback);
      } else { fallback(); }
    });
  });
  // FEITO check toggle (card/opcoes) + botão desfazer na seção Feitas
  document.querySelectorAll('[data-feito]').forEach(b=>{
    if(b.__bound) return;
    b.__bound=true;
    b.addEventListener('click',e=>{
      e.stopPropagation();
      const name=b.dataset.feito;
      setFeito(name,!isFeito(name));
      renderInnerContent(); // stop migra pra/de Feitas hoje
      // Stats de Atrações/Tours mudam · atualiza status bar (se aberto)
      const sb=document.getElementById('status-bar');
      if(sb && state.view==='guia'){ sb.outerHTML=renderStatusBar(); bindStatusBar(); }
    });
  });
  // Cabeçalho "Feitas hoje": colapsar
  const fh=document.getElementById('feitas-head');
  if(fh && !fh.__bound){
    fh.__bound=true;
    fh.addEventListener('click',()=>{
      const sec=fh.closest('.feitas-section');
      const open=sec.classList.toggle('open');
      try{ localStorage.setItem('feitasOpen_'+state.selIdx,open?'1':'0'); }catch(e){}
    });
  }
  // Item feito clicável (menos o botão undo): re-marca como não-feito não · só desfaz via undo.
  document.querySelectorAll('.feitas-item[data-jump]').forEach(it=>{
    if(it.__bound) return;
    it.__bound=true;
    it.addEventListener('click',e=>{
      if(e.target.closest('[data-feito]')) return; // undo trata sozinho
    });
  });
  if(state.expandStop){
    // Expande o card OU o bloco de opções cujo nome bate
    document.querySelectorAll('.stop-card .stop-name, .stop-opcoes .stop-opcoes-name').forEach(el=>{
      if(el.textContent.trim()===state.expandStop){
        const card=el.closest('.stop-card, .stop-opcoes');
        card.classList.add('expanded');
        setTimeout(()=>card.scrollIntoView({behavior:'smooth',block:'center'}),150);
      }
    });
    state.expandStop=null;
  } else if(state.view==='guia'){
    // AGORA: auto-scroll pro stop atual (se houver) no load do dia
    const nowEl=document.querySelector('.stop-wrap.is-now');
    if(nowEl){
      setTimeout(()=>nowEl.scrollIntoView({behavior:'smooth',block:'center'}),200);
    }
  }
  maybeShowFeitoHint();
}

// First-run: mostra uma dica sutil no primeiro check ○ · some ao tocar ou após alguns segundos
function maybeShowFeitoHint(){
  if(state.view!=='guia') return;
  let seen=false; try{ seen=localStorage.getItem('hintFeito')==='1'; }catch(e){}
  if(seen) return;
  const firstChk=document.querySelector('.tl-stops .stop-wrap:not(.is-feito) .feito-chk');
  if(!firstChk) return;
  const wrap=firstChk.closest('.stop-wrap');
  if(!wrap || wrap.querySelector('.feito-hint')) return;
  const dismiss=()=>{
    try{ localStorage.setItem('hintFeito','1'); }catch(e){}
    const h=wrap.querySelector('.feito-hint'); if(h) h.remove();
  };
  const hint=document.createElement('div');
  hint.className='feito-hint';
  hint.textContent='Toque ✓ pra marcar como feito';
  hint.addEventListener('click',dismiss);
  wrap.appendChild(hint);
  firstChk.addEventListener('click',dismiss,{once:true});
  setTimeout(dismiss,5000);
}

function render(){
  let content='';
  if(state.view==='guia'||state.view==='mapa'){
    const heroHtml=state.view==='guia'?renderStatusBar():'';
    const tabsHtml=renderDayTabs();
    const innerHtml=state.view==='guia'?renderDay(DAYS[state.selIdx]):renderMap();
    content=heroHtml+tabsHtml+'<div id="inner-content">'+innerHtml+'</div>';
  } else if(state.view==='bairros'){
    content=renderBairros();
  } else if(state.view==='tudomapa'){
    content=renderTudoMapa();
  } else if(state.view==='historia'){
    content=renderHistoria();
  }
  document.getElementById('content').innerHTML=content;
  
  // Day tab clicks (com SOFT re-render — não rebuilda tabs)
  const dayTabsEl=document.querySelector('.daystrip');
  if(dayTabsEl){
    dayTabsEl.addEventListener('click',e=>{
      const tab=e.target.closest('.day-tab');
      if(!tab) return;
      const idx=parseInt(tab.dataset.idx);
      if(idx===state.selIdx) return;
      state.selIdx=idx;
      // Atualiza apenas a classe active (sem re-render dos tabs)
      dayTabsEl.querySelectorAll('.day-tab').forEach(t=>t.classList.toggle('active',parseInt(t.dataset.idx)===idx));
      renderInnerContent();
      centerActiveTab();
    });
  }
  // Bairros clicks
  document.querySelectorAll('.bairro-attr').forEach(b=>{
    b.addEventListener('click',()=>{
      state.selIdx=parseInt(b.dataset.idx);
      state.view='guia';
      state.expandStop=b.querySelector('.bairro-attr-name').textContent.replace(/^[\p{Emoji}\s]+/u,'').trim();
      syncTabbar();
      render();
      window.scrollTo({top:0,behavior:'smooth'});
    });
  });
  bindStatusBar();
  bindCardHandlers();
  centerActiveTab();
}

// Abre o Resumo com filtro/pending · rerenderiza o sheet e mostra
function openOverviewSheet(filter,showPending){
  state.ovFilter=filter||'roteiro';
  state.ovShowPending=!!showPending;
  const ovEl=document.getElementById('overview');
  const ovBtn=document.getElementById('overview-toggle');
  ovEl.innerHTML=renderOverview();
  ovEl.classList.add('show');
  ovBtn.classList.add('active');
  window.scrollTo({top:0,behavior:'smooth'});
}

function bindStatusBar(){
  const exp=document.getElementById('sb-expand');
  const stats=document.getElementById('sb-stats');
  if(exp && !exp.__bound){
    exp.__bound=true;
    exp.addEventListener('click',()=>{
      const open=stats.classList.toggle('open');
      exp.classList.toggle('open',open);
      exp.setAttribute('aria-expanded',open);
      try{ localStorage.setItem('statusExpanded',open?'1':'0'); }catch(e){}
    });
  }
  const chip=document.getElementById('sb-reservas');
  if(chip && !chip.__bound){
    chip.__bound=true;
    chip.addEventListener('click',()=>openOverviewSheet('roteiro',true));
  }
  document.querySelectorAll('.sb-stat[data-goto]').forEach(b=>{
    if(b.__bound) return;
    b.__bound=true;
    b.addEventListener('click',()=>{
      if(b.dataset.goto==='afazer'){ openOverviewSheet('afazer',false); return; }
      if(b.dataset.goto==='dia'){
        // Pula pro dia de hoje se estivermos dentro da viagem · senão no-op
        const idx=getTodayTripIdx();
        if(idx>=0 && idx!==state.selIdx){
          state.selIdx=idx; state.view='guia'; syncTabbar(); render();
          window.scrollTo({top:0,behavior:'smooth'});
        }
        return;
      }
    });
  });
}

function syncTabbar(){
  document.querySelectorAll('.tab-btn').forEach(t=>t.classList.toggle('active',t.dataset.view===state.view));
}

function init(){
  maybeWarnStorage();
  // revela a aba História só se houver conteúdo
  if(typeof HISTORIA!=='undefined' && HISTORIA.length){
    const th=document.getElementById('tab-historia'); if(th) th.style.display='';
  }
  document.getElementById('overview').innerHTML=renderOverview();
  
  // Legenda: aberta + desmarcada no 1º acesso · SÓ o "Já li" colapsa · persiste entre sessões
  const fl=document.getElementById('footer-legend');
  const cb=document.getElementById('legend-cb');
  if(localStorage.getItem('legendRead')==='1'){ cb.checked=true; fl.classList.add('collapsed'); }
  cb.addEventListener('change',()=>{
    try{ localStorage.setItem('legendRead',cb.checked?'1':'0'); }catch(e){}
    fl.classList.toggle('collapsed',cb.checked);
  });
  updateReservasNote();
  
  // Bottom tab bar
  document.querySelectorAll('.tab-btn').forEach(b=>{
    b.addEventListener('click',()=>{
      closeOverview();
      state.view=b.dataset.view;
      syncTabbar();
      render();
      window.scrollTo({top:0,behavior:'smooth'});
    });
  });

  // Overview sheet
  const ovEl=document.getElementById('overview');
  const ovBtn=document.getElementById('overview-toggle');
  function closeOverview(){ ovEl.classList.remove('show'); ovBtn.classList.remove('active'); }
  window.closeOverview=closeOverview;
  ovBtn.addEventListener('click',()=>{
    const isOpen=ovEl.classList.contains('show');
    if(isOpen){ closeOverview(); return; }
    closeHelp();
    // Abre sempre no filtro Roteiro, sem seção pending
    openOverviewSheet('roteiro',false);
  });
  ovEl.addEventListener('click',e=>{
    if(e.target.id==='ov-close'){ closeOverview(); return; }
    // Segmented control (Roteiro · A fazer · Feitas)
    const seg=e.target.closest('.ov-seg-btn');
    if(seg){
      state.ovFilter=seg.dataset.filter;
      state.ovShowPending=false; // trocar de aba dispensa o pinned de reservas
      ovEl.innerHTML=renderOverview();
      window.scrollTo({top:0,behavior:'smooth'});
      return;
    }
    // Task row (A fazer / Feitas / Reservas pendentes): navega + expand
    const task=e.target.closest('.ov-task[data-jump]');
    if(task){
      state.selIdx=parseInt(task.dataset.idx);
      state.view='guia';
      state.expandStop=task.dataset.jump;
      syncTabbar();
      closeOverview();
      render();
      window.scrollTo({top:0,behavior:'smooth'});
      return;
    }
    // Botão de walking tour: navega + auto-expand do card específico
    const wtBtn=e.target.closest('.ov-wt-btn');
    if(wtBtn){
      e.stopPropagation();
      state.selIdx=parseInt(wtBtn.dataset.idx);
      state.view='guia';
      state.expandStop=wtBtn.dataset.stop;
      syncTabbar();
      closeOverview();
      render();
      window.scrollTo({top:0,behavior:'smooth'});
      return;
    }
    // Linha clicável: navega pro dia
    const tr=e.target.closest('.ov-row.clickable');
    if(tr){
      state.selIdx=parseInt(tr.dataset.idx);
      state.view='guia';
      syncTabbar();
      closeOverview();
      render();
      window.scrollTo({top:0,behavior:'smooth'});
    }
  });

  // Search (toggle panel + results)
  const si=document.getElementById('search');
  const sr=document.getElementById('search-results');
  const sc=document.getElementById('search-clear');
  const sw=document.getElementById('search-wrap');
  const sBtn=document.getElementById('search-btn');
  sBtn.addEventListener('click',()=>{
    const open=sw.classList.toggle('show');
    sBtn.classList.toggle('active',open);
    if(open){ closeOverview(); closeHelp(); setTimeout(()=>si.focus(),60); }
    else { sr.classList.remove('show'); }
  });
  si.addEventListener('input',()=>{
    const v=si.value;
    sc.classList.toggle('show',v.length>0);
    if(v.length>=2){
      sr.innerHTML=renderSearch(v);
      sr.classList.add('show');
    } else {
      sr.classList.remove('show');
    }
  });
  sr.addEventListener('click',e=>{
    const r=e.target.closest('.search-result');
    if(r){
      state.selIdx=parseInt(r.dataset.idx);
      state.view='guia';
      state.expandStop=r.querySelector('.search-result-name').textContent.replace(/^[\p{Emoji}\s]+/u,'').trim();
      syncTabbar();
      si.value='';
      sc.classList.remove('show');
      sr.classList.remove('show');
      sw.classList.remove('show');
      sBtn.classList.remove('active');
      render();
      window.scrollTo({top:0,behavior:'smooth'});
    }
  });
  sc.addEventListener('click',()=>{
    si.value='';
    sc.classList.remove('show');
    sr.classList.remove('show');
  });
  document.addEventListener('click',e=>{
    if(!e.target.closest('.search-wrap')) sr.classList.remove('show');
  });

  // Ajuda · sheet de dicas (sempre acessível pelo ❓)
  const helpEl=document.getElementById('help-sheet');
  const helpBtn=document.getElementById('help-btn');
  function closeHelp(){ helpEl.classList.remove('show'); helpBtn.classList.remove('active'); }
  helpBtn.addEventListener('click',()=>{
    const open=helpEl.classList.toggle('show');
    helpBtn.classList.toggle('active',open);
    if(open){ closeOverview(); window.scrollTo({top:0,behavior:'smooth'}); }
  });
  helpEl.addEventListener('click',e=>{ if(e.target.id==='help-close') closeHelp(); });

  // Swipe entre dias (Guia + Mapa) · toque no mapa Leaflet mantém o pan
  (function(){
    const area=document.getElementById('content');
    let x0=null,y0=null,onMap=false;
    area.addEventListener('touchstart',e=>{
      const t=e.touches[0]; x0=t.clientX; y0=t.clientY;
      onMap=!!(e.target.closest && e.target.closest('#map'));
    },{passive:true});
    area.addEventListener('touchend',e=>{
      if(x0===null) return;
      const startX=x0; x0=null;
      if(onMap) return;                                  // deixa o mapa fazer pan
      if(state.view!=='guia' && state.view!=='mapa') return;
      const t=e.changedTouches[0], dx=t.clientX-startX, dy=t.clientY-y0;
      if(Math.abs(dx)<60 || Math.abs(dx)<Math.abs(dy)*1.8) return;   // horizontal claro
      const next=state.selIdx+(dx<0?1:-1);               // arrastar p/ esquerda = próximo dia
      if(next<0 || next>=DAYS.length) return;
      state.selIdx=next;
      document.querySelectorAll('.day-tab').forEach(tb=>tb.classList.toggle('active',parseInt(tb.dataset.idx)===next));
      renderInnerContent();
      centerActiveTab();
    },{passive:true});
  })();

  render();
}