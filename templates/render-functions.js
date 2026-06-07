function getDefaultDayIdx(){
  // Detecta se hoje é um dos dias do roteiro e auto-seleciona; senão volta pro dia 1 (chegada)
  const monthMap={Jan:0,Fev:1,Feb:1,Mar:2,Abr:3,Apr:3,Mai:4,May:4,Jun:5,Jul:6,Ago:7,Aug:7,Set:8,Sep:8,Out:9,Oct:9,Nov:10,Dez:11,Dec:11};
  const today=new Date();
  const tStr=today.toISOString().split('T')[0]; // YYYY-MM-DD
  for(let i=0;i<DAYS.length;i++){
    const m=DAYS[i].date.match(/(\d+)\/(\w+)/);
    if(!m) continue;
    const dayNum=parseInt(m[1]);
    const monthIdx=monthMap[m[2]];
    if(monthIdx===undefined) continue;
    const d=new Date(2026,monthIdx,dayNum);
    if(d.toISOString().split('T')[0]===tStr) return i;
  }
  return 0;
}
const state = { view:'guia', selIdx:getDefaultDayIdx(), search:'', expandStop:null, nivel:'profundo' };

function getPeriodoMeta(p){
  return {
    manha:{emoji:'🌅',label:'Manhã'},
    tarde:{emoji:'☀️',label:'Tarde'},
    noite:{emoji:'🌙',label:'Noite'}
  }[p];
}

function getMapsUrl(stop){
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

function getRouteUrl(day){
  // V1.5: filtra ALT cards (nome iniciando com 🔄) — alternativas não fazem parte da rota
  // principal do dia. Bug Sprockhovel 2026-05-23 (Valenciennes ALT puxava rota pra direção oposta).
  const stops=day.stops.filter(s=>s.tipo!=='transit' && s.coord && !s.nome.startsWith('🔄'));
  if(!stops.length) return '#';
  if(stops.length===1) return getMapsUrl(stops[0]);
  const queryName=s=>{
    let n=s.nome;
    if(s.tipo==='opcoes' && s.opcoes?.length) n=s.opcoes[0].nome;
    return n.replace(/[()]/g,'').replace(/\s+/g,' ').trim();
  };
  const origin=encodeURIComponent(queryName(stops[0]));
  const dest=encodeURIComponent(queryName(stops[stops.length-1]));
  const mid=stops.slice(1,-1).map(s=>encodeURIComponent(queryName(s))).join('|');
  let url=`https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${dest}&travelmode=walking`;
  if(mid) url+=`&waypoints=${mid}`;
  return url;
}

function getWalkingTourUrl(tour){
  // V1.5: usa NOME com endereço (parens removidos só na query, conteúdo mantido) em vez de
  // coords puras · coords puras mostravam "Com alfinete" no Maps · bug Sprockhovel 2026-05-23
  // (mesmo bug que getRouteUrl V1.4 corrigiu, mas só lá · walking tour ficou pra trás).
  if(!tour||tour.length<2) return '#';
  const queryName=t=>t.nome.replace(/[()]/g,'').replace(/\s+/g,' ').trim();
  const origin=encodeURIComponent(queryName(tour[0]));
  const dest=encodeURIComponent(queryName(tour[tour.length-1]));
  const mid=tour.slice(1,-1).map(t=>encodeURIComponent(queryName(t))).join('|');
  let url=`https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${dest}&travelmode=walking`;
  if(mid) url+=`&waypoints=${mid}`;
  return url;
}

function renderCard(stop){
  const links=LINKS_MAP[stop.nome]||[];
  const riskLabel={green:'🟢 tranquilo',yellow:'⚠️ atenção',red:'🔴 alta atenção'};
  const riskBadge=stop.risco?`<span class="risk-pill risk-${stop.risco}">${riskLabel[stop.risco]}</span>`:'';
  let reservaBadge='';
  if(stop.reserva){
    const stored=localStorage.getItem(`reserva-${stop.nome}`);
    const defaultDone=stop.reserva==='reservado';
    const isDone=stored?stored==='done':defaultDone;
    reservaBadge=`<button class="reserva-badge ${isDone?'ok':'pending'}" data-reserva="${stop.nome.replace(/"/g,'&quot;')}" title="Clique pra alternar">${isDone?'☑ FEITO':'☐ RESERVAR'}</button>`;
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
    <div class="stop-head">
      <div class="stop-emoji">${stop.emoji}</div>
      <div class="stop-time-name">
        <div class="stop-time">${stop.hora}${reservaBadge}</div>
        ${walkingTourFlag}
        <div class="stop-name">${stop.nome}</div>
        <div class="stop-cat">${stop.cat}${riskBadge}</div>
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

function renderOpcoes(stop){
  return `<div class="stop-opcoes">
    <div class="stop-opcoes-head">
      <div class="stop-opcoes-emoji">${stop.emoji}</div>
      <div class="stop-opcoes-title">
        <div class="stop-time">${stop.hora}</div>
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

function renderTransit(stop){
  const t=TRANSIT_MAP[stop.nome];
  const hasRoutes=t&&(t.ferry||t.metro||t.uber);
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
      ${t.metro?`<div class="route-option"><strong>🚇 Metrô</strong> ${t.metro}</div>`:''}
      ${t.uber?`<div class="route-option"><strong>🚕 Uber</strong> ${t.uber}</div>`:''}
    </div>`:''}
  </div>`;
}

function renderStop(stop){
  if(stop.tipo==='card') return renderCard(stop);
  if(stop.tipo==='opcoes') return renderOpcoes(stop);
  return renderTransit(stop);
}

function renderDay(day){
  const periodos=['manha','tarde','noite'];
  // Toggle Básico↔Profundo: se o dia tem stops marcados essencial, mostra o seletor.
  // Básico = só os essenciais · Profundo = tudo.
  const hasNiveis=day.stops.some(s=>s.essencial);
  const basico=hasNiveis && state.nivel==='basico';
  const visStops=basico?day.stops.filter(s=>s.essencial):day.stops;
  const grouped={manha:[],tarde:[],noite:[]};
  visStops.forEach(s=>{ if(grouped[s.periodo]) grouped[s.periodo].push(s); });
  const toggle=hasNiveis?`<div class="nivel-toggle">
      <span class="nivel-label">Versão:</span>
      <button class="nivel-btn ${basico?'':'active'}" data-nivel="profundo">🔬 Profundo</button>
      <button class="nivel-btn ${basico?'active':''}" data-nivel="basico">⚡ Básico</button>
    </div>`:'';

  return `<div class="day-card" style="--day-color:${day.cor};--day-grad-a:${day.gradA};--day-grad-b:${day.gradB}">
    <div class="day-banner">
      <div class="date">${day.date}</div>
      <h2>${day.tema}</h2>
      <div class="bairro">📍 ${day.bairro}${day.grupo?' · 👥 grupo':''}</div>
    </div>
    ${day.nota?`<div class="day-nota">${day.nota}</div>`:''}
    ${toggle}
    <div class="periodos">
      ${periodos.filter(p=>grouped[p].length>0).map(p=>{
        const m=getPeriodoMeta(p);
        return `<div class="periodo">
          <div class="periodo-header"><span class="emoji">${m.emoji}</span> ${m.label}</div>
          <div class="periodo-stops">${grouped[p].map(renderStop).join('')}</div>
        </div>`;
      }).join('')}
    </div>
  </div>`;
}

function renderOverview(){
  return `<table>
    <colgroup>
      <col class="col-date"><col class="col-tema"><col class="col-attr"><col class="col-bairro">
    </colgroup>
    <thead><tr><th>Data</th><th>Tema</th><th>Atração principal</th><th>Bairro</th></tr></thead>
    <tbody>
      ${DAYS.map((d,i)=>{
        const cards=d.stops.filter(s=>s.tipo==='card');
        const main=cards.length?cards[0].nome:'—';
        const wtCards=cards.filter(c=>c.walkingTours&&c.walkingTours.length>0);
        const parts=d.date.split(' ');
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
        return `<tr class="clickable" data-idx="${i}">
          <td class="ov-date"><span class="ov-date-pill"><strong>${parts[0]}</strong><small>${parts[1]}</small></span></td>
          <td class="ov-tema">${d.tema}</td>
          <td class="ov-attr"><div class="ov-main">${main}</div>${wtButtons}</td>
          <td class="ov-bairro">${d.bairro}</td>
        </tr>`;
      }).join('')}
    </tbody>
  </table>`;
}

function renderDayTabs(){
  return `<div class="day-tabs-wrap"><div class="day-tabs">${DAYS.map((d,i)=>{
    const labelCurto=d.temaCurto||d.tema.split('·')[0].trim();
    // dt-date: junta os tokens disponíveis (data datada "Sex 5/Set" OU só emoji "👶" em coletâneas
    // sem data) · evita imprimir "undefined" quando o campo date tem 1 token só.
    const dtDate=d.date.split(' ').slice(0,2).join(' ');
    return `<button class="day-tab ${i===state.selIdx?'active':''}" data-idx="${i}" style="--day-color:${d.cor}">
    <span class="dt-date">${dtDate}</span>${labelCurto}
    ${d.grupo?'<span class="group-dot">👥</span>':''}
  </button>`;
  }).join('')}</div></div>`;
}

function getBairroForCoord(lat, lng){
  // Detecção dinâmica de bairro por coordenadas, baseada em BAIRROS_CONFIG (injetado pela skill via build.py).
  // BAIRROS_CONFIG = [{nome, latMin, latMax, lngMin, lngMax}, ..., {nome, fallback:true}]
  if (typeof BAIRROS_CONFIG === 'undefined' || !Array.isArray(BAIRROS_CONFIG)) return '📍 Outros';
  for (const b of BAIRROS_CONFIG){
    if (b.fallback) continue;
    if (lat >= b.latMin && lat <= b.latMax && lng >= b.lngMin && lng <= b.lngMax) return b.nome;
  }
  const fb = BAIRROS_CONFIG.find(b => b.fallback);
  return fb ? fb.nome : '📍 Outros';
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
  return `<div class="bairros-list">
    ${sorted.map(b=>`<div class="bairro-block">
      <div class="bairro-name">${b} <span style="margin-left:auto;font-size:12px;color:#9ca3af;font-weight:500">${bairros[b].length} atrações</span></div>
      <div class="bairro-attrs">
        ${bairros[b].map(item=>`<div class="bairro-attr" data-idx="${item.dayIdx}">
          <div class="bairro-attr-name">${item.stop.emoji} ${item.stop.nome}</div>
          <div class="bairro-attr-day">${item.date} · ${item.stop.hora}</div>
        </div>`).join('')}
      </div>
    </div>`).join('')}
  </div>`;
}

let mapInstance=null;
function renderMap(){
  const day=DAYS[state.selIdx];
  // hideStopMarkers: quando o dia INTEIRO é a própria walking tour (cada card = uma parada
  // numerada), esconde os pins comuns pra não duplicar com os marcadores numerados do WT.
  const hideStops=!!day.hideStopMarkers;
  const stops=day.stops.filter(s=>s.tipo!=='transit' && s.coord);
  // Cards do dia com walking tours (array de partes)
  const cardsWithTours=day.stops.filter(s=>s.walkingTours&&s.walkingTours.length>0);
  // Helper: limpa nome pra busca no Google Maps (mantém endereço entre parens)
  const cleanForSearch=nm=>nm.replace(/[()]/g,'').replace(/\s+/g,' ').trim();
  // Numeração SEQUENCIAL contínua das paradas de walking tour (atravessa TODAS as partes).
  // Antes cada parte reiniciava em 1 → pino "1" repetia na parte 2 e a legenda (1..N) não batia.
  // Agora wtSeq.n é global (1..N) e bate com a legenda · partIdx define o estilo (parte 1 cheia · 2+ contorno).
  const wtSeq=[];
  cardsWithTours.forEach(card=>{
    card.walkingTours.forEach((tour,partIdx)=>{
      tour.stops.forEach(t=>{
        wtSeq.push({n:wtSeq.length+1,nome:t.nome,coord:t.coord,partIdx,partName:tour.nome.split('·')[0].trim()});
      });
    });
  });
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
    if(!hideStops){
      stops.forEach((s,i)=>{
        const isOpcoes=s.tipo==='opcoes' && s.opcoes && s.opcoes.length>0;
        const principalName=isOpcoes?s.opcoes[0].nome.split('(')[0].trim():'';
        const popupHtml=`<div class="pp-time" style="color:${day.cor}">${s.hora}</div>
          <div class="pp-name">${s.nome}</div>
          <div class="pp-notes">${s.cat||''}</div>
          ${isOpcoes?`<div class="pp-notes" style="margin-top:6px"><strong>📍 Principal:</strong> ${principalName}</div>`:''}
          <a class="pp-link" style="background:${day.cor}" href="${getMapsUrl(s)}" target="_blank" rel="noopener">📍 Abrir no Google Maps</a>`;
        L.marker([s.coord.lat,s.coord.lng])
          .bindPopup(popupHtml,{maxWidth:240})
          .addTo(mapInstance);
      });
      if(latlngs.length>1){
        L.polyline(latlngs,{color:day.cor,weight:3,opacity:0.7,dashArray:'6,8'}).addTo(mapInstance);
      }
    }
    // WALKING TOURS: polyline por parte (Parte 1 tracejada normal · Parte 2+ mais fina)
    cardsWithTours.forEach(card=>{
      card.walkingTours.forEach((tour,partIdx)=>{
        const tourLatLngs=tour.stops.map(t=>[t.coord.lat,t.coord.lng]);
        const dashStyle=partIdx===0?'4,5':'2,6';
        L.polyline(tourLatLngs,{color:day.cor,weight:2.5,opacity:0.85,dashArray:dashStyle}).addTo(mapInstance);
      });
    });
    // Marcadores numerados SEQUENCIAIS (1..N contínuo) · Parte 1 cheios · Parte 2+ contorno
    wtSeq.forEach(item=>{
      const markerStyle=item.partIdx===0
        ?`background:${day.cor};color:#fff;border:2px solid #fff`
        :`background:#fff;color:${day.cor};border:2px solid ${day.cor}`;
      const icon=L.divIcon({
        className:'wt-marker',
        html:`<div style="${markerStyle}">${item.n}</div>`,
        iconSize:[24,24],iconAnchor:[12,12],popupAnchor:[0,-12]
      });
      const searchName=cleanForSearch(item.nome);
      const url=`https://www.google.com/maps/search/${encodeURIComponent(searchName)}/@${item.coord.lat},${item.coord.lng},17z`;
      const popupHtml=`<div class="pp-time" style="color:${day.cor}">${item.partName} · parada ${item.n}</div>
        <div class="pp-name">${item.nome}</div>
        <a class="pp-link" style="background:${day.cor}" href="${url}" target="_blank" rel="noopener">📍 Abrir no Google Maps</a>`;
      L.marker([item.coord.lat,item.coord.lng],{icon})
        .bindPopup(popupHtml,{maxWidth:240})
        .addTo(mapInstance);
    });
    // Ajustar bounds incluindo walking tours
    const allLatLngs=[...latlngs,...wtSeq.map(item=>[item.coord.lat,item.coord.lng])];
    mapInstance.fitBounds(allLatLngs,{padding:[40,40]});
  },50);
  // Legenda: quando o dia É a própria walking tour (hideStopMarkers), usa a sequência contínua
  // das paradas WT (bate 1..N com os pinos numerados). Senão, lista os stops do dia (com hora).
  let legend;
  if(hideStops && wtSeq.length){
    legend=wtSeq.map(item=>{
      const dotStyle=item.partIdx===0
        ?`background:${day.cor};color:#fff`
        :`background:#fff;color:${day.cor};border:1.5px solid ${day.cor}`;
      return `<div class="stop-legend-item"><div class="stop-num" style="${dotStyle}">${item.n}</div><span class="legend-nome">${item.nome.split('(')[0].trim()}</span></div>`;
    }).join('');
  } else {
    legend=stops.map((s,i)=>`<div class="stop-legend-item"><div class="stop-num" style="background:${day.cor}">${i+1}</div><span class="legend-hora">${s.hora}</span><span class="legend-nome">${s.nome.split('(')[0].trim()}</span></div>`).join('');
  }
  // 1 botão por parte de walking tour
  const tourButtons=cardsWithTours.flatMap(card=>
    card.walkingTours.map(t=>
      `<a class="gmaps-btn walking-tour-btn" href="${getWalkingTourUrl(t.stops)}" target="_blank" rel="noopener">🚶 ${t.nome} · ${t.stops.length} paradas</a>`
    )
  ).join('');
  return `<div class="map-section">
    ${(stops.length||wtSeq.length)?`<div class="stop-legend">${legend}</div>`:''}
    <div id="map"></div>
    <div class="map-cta">
      <a class="gmaps-btn" href="${getRouteUrl(day)}" target="_blank" rel="noopener">🗺️ Abrir rota do dia no Google Maps (walking)</a>
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
      b.textContent=willBeDone?'☑ FEITO':'☐ RESERVAR';
    });
  });
  document.querySelectorAll('.nivel-btn').forEach(b=>{
    if(b.__bound) return;
    b.__bound=true;
    b.addEventListener('click',e=>{
      e.stopPropagation();
      if(state.nivel===b.dataset.nivel) return;
      state.nivel=b.dataset.nivel;
      renderInnerContent();
    });
  });
  if(state.expandStop){
    document.querySelectorAll('.stop-card .stop-name').forEach(el=>{
      if(el.textContent.trim()===state.expandStop){
        const card=el.closest('.stop-card');
        card.classList.add('expanded');
        setTimeout(()=>card.scrollIntoView({behavior:'smooth',block:'center'}),150);
      }
    });
    state.expandStop=null;
  }
}

function render(){
  let content='';
  if(state.view==='guia'||state.view==='mapa'){
    const tabsHtml=renderDayTabs();
    const innerHtml=state.view==='guia'?renderDay(DAYS[state.selIdx]):renderMap();
    content=tabsHtml+'<div id="inner-content">'+innerHtml+'</div>';
  } else if(state.view==='bairros'){
    content=renderBairros();
  }
  document.getElementById('content').innerHTML=content;
  
  // Day tab clicks (com SOFT re-render — não rebuilda tabs)
  const dayTabsEl=document.querySelector('.day-tabs');
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
  // Main tabs
  document.querySelectorAll('.main-tab').forEach(b=>{
    b.addEventListener('click',()=>{
      state.view=b.dataset.view;
      document.querySelectorAll('.main-tab').forEach(t=>t.classList.toggle('active',t.dataset.view===state.view));
      render();
    });
  });
  // Bairros clicks
  document.querySelectorAll('.bairro-attr').forEach(b=>{
    b.addEventListener('click',()=>{
      state.selIdx=parseInt(b.dataset.idx);
      state.view='guia';
      state.expandStop=b.querySelector('.bairro-attr-name').textContent.replace(/^[\p{Emoji}\s]+/u,'').trim();
      document.querySelectorAll('.main-tab').forEach(t=>t.classList.toggle('active',t.dataset.view==='guia'));
      render();
      window.scrollTo({top:0,behavior:'smooth'});
    });
  });
  bindCardHandlers();
  centerActiveTab();
}

function init(){
  document.getElementById('overview').innerHTML=renderOverview();
  
  // Legenda: collapse persistente
  const fl=document.getElementById('footer-legend');
  const cb=document.getElementById('legend-cb');
  if(localStorage.getItem('legendRead')==='1'){
    fl.classList.add('collapsed');
    cb.checked=true;
  }
  cb.addEventListener('change',()=>{
    try{ localStorage.setItem('legendRead',cb.checked?'1':'0'); }catch(e){}
    fl.classList.toggle('collapsed',cb.checked);
  });
  
  // Overview toggle
  document.getElementById('overview-toggle').addEventListener('click',()=>{
    const ov=document.getElementById('overview');
    const tg=document.getElementById('overview-toggle');
    const open=ov.classList.toggle('show');
    tg.classList.toggle('open',open);
  });
  // Overview row/button click
  document.getElementById('overview').addEventListener('click',e=>{
    // Botão de walking tour: navega + auto-expand do card específico
    const wtBtn=e.target.closest('.ov-wt-btn');
    if(wtBtn){
      e.stopPropagation();
      state.selIdx=parseInt(wtBtn.dataset.idx);
      state.view='guia';
      state.expandStop=wtBtn.dataset.stop;
      document.querySelectorAll('.main-tab').forEach(t=>t.classList.toggle('active',t.dataset.view==='guia'));
      document.getElementById('overview').classList.remove('show');
      document.getElementById('overview-toggle').classList.remove('open');
      render();
      window.scrollTo({top:0,behavior:'smooth'});
      return;
    }
    // Linha clicável: navega pro dia (primeiro card)
    const tr=e.target.closest('tr.clickable');
    if(tr){
      state.selIdx=parseInt(tr.dataset.idx);
      state.view='guia';
      document.querySelectorAll('.main-tab').forEach(t=>t.classList.toggle('active',t.dataset.view==='guia'));
      document.getElementById('overview').classList.remove('show');
      document.getElementById('overview-toggle').classList.remove('open');
      render();
      window.scrollTo({top:0,behavior:'smooth'});
    }
  });
  
  // Search
  const si=document.getElementById('search');
  const sr=document.getElementById('search-results');
  const sc=document.getElementById('search-clear');
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
      document.querySelectorAll('.main-tab').forEach(t=>t.classList.toggle('active',t.dataset.view==='guia'));
      si.value='';
      sc.classList.remove('show');
      sr.classList.remove('show');
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
  
  render();
}
