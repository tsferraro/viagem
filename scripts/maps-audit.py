#!/usr/bin/env python3
"""
maps-audit.py — audita TODA URL de Google Maps que o app gera, a partir do HTML já buildado.

POR QUE ISTO EXISTE
-------------------
Em ago/2026 o Tobia abriu o app em campo e mandou prints: o pino de um card caía no meio do
mar e a rota do walking tour dizia "Can't seem to find that place". Nada disso aparecia no
`validate.py` nem no `audit.py` — os dois liam o *dado*, e o defeito só existia na *URL final*.
Depois de consertado, a mesma técnica (imprimir a URL montada) achou mais três:

  · "Viale Aldo Moro 201/A" criava um waypoint fantasma — a "/" separa segmentos em /dir/a/b/c
  · a rota de um dia ia "Porto di Cala Gonone → Porto di Cala Gonone" (rota de zero metro)
  · MAXW estava fora de escopo em getRouteUrl — ReferenceError que só quebraria no celular

A lição: **o que precisa ser conferido é a URL, não o campo do JSON.** Este script monta as
URLs exatamente como o app monta (executando as funções do template no Node) e as classifica.

USO
---
    python3 scripts/maps-audit.py <viagem>/index.html          # relatório completo
    python3 scripts/maps-audit.py <viagem>/index.html --quiet  # só problemas (pra CI)
    python3 scripts/maps-audit.py <viagem>/index.html --urls   # imprime as URLs pra abrir

Exit: 0 = sem problema · 1 = problema encontrado · 2 = erro de execução.

O QUE ELE **NÃO** FAZ
---------------------
Não abre o Google Maps nem confirma que o lugar existe — isso é trabalho do protocolo
`skills/critico-roteiro/FACTCHECK.md` (seção "Conferência de lugar"). Aqui se garante que a
URL é *bem formada e específica*; lá se garante que ela *leva ao lugar certo*.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

C_OK, C_ERR, C_WARN, C_DIM, C_END, C_BOLD = (
    '\033[92m', '\033[91m', '\033[93m', '\033[2m', '\033[0m', '\033[1m')

# Funções do template que precisam ser extraídas pra montar as URLs como o app monta.
FUNCS = ['ADDR_HINT', 'MAXW', 'placeQuery', 'mapsQueryOf', 'regionSuffix', 'haversine',
         'dayTransport', 'dirCoordUrl', 'getMapsUrl', 'wtStopQuery', 'getWalkingTourUrl',
         'getRouteUrl']

# Query que descreve uma ATIVIDADE/refeição em vez de um lugar.
GENERICA = re.compile(
    r'^(almo[çc]o|jantar|caf[ée]|picnic|casa|quiosques|bares|sandes|padaria|walking tour|'
    r'check[- ]?(in|out)|despedida|fim da viagem|tarde livre|retorno|volta a|chegada|'
    r'encontro|layby|boat tour|sesta|jantar leve)\b', re.I)

JS_RUNNER = r'''
const fs=require('fs');
const src=fs.readFileSync(process.argv[2],'utf8');
const html=fs.readFileSync(process.argv[3],'utf8');
const mDays=html.match(/const DAYS\s*=\s*(\[[\s\S]*?\]);\s*\n/);
if(!mDays){ console.log(JSON.stringify({erro:'DAYS não encontrado'})); process.exit(0); }
const DAYS=JSON.parse(mDays[1]);
const MAPS_REGION=(html.match(/const MAPS_REGION\s*=\s*"([^"]*)"/)||['',''])[1];
const FUNCS=JSON.parse(process.argv[4]);
let code='';
for(const n of FUNCS){
  const m=src.match(new RegExp('(?:^|\\n)(?:const '+n+'\\s*=[^\\n;]*;|function '+n+'\\([\\s\\S]*?\\n\\})','m'));
  if(m) code+=m[0]+'\n';
}
let F;
try{ F=new Function('MAPS_REGION','DAYS',code+';return {getMapsUrl,getRouteUrl,getWalkingTourUrl};')(MAPS_REGION,DAYS); }
catch(e){ console.log(JSON.stringify({erro:'template não executa: '+e.message})); process.exit(0); }
const out={maps_region:MAPS_REGION,rotas:[],cards:[],opcoes:[],tours:[],dias_coords:[],tours_coords:[]};
const safe=(fn,ctx)=>{ try{ return fn(); }catch(e){ return 'ERRO: '+e.message+' @ '+ctx; } };
DAYS.forEach((d,di)=>{
  out.rotas.push({dia:d.date, url:safe(()=>F.getRouteUrl(d),'rota '+d.date)});
  d.stops.forEach(s=>{
    if(s.tipo==='card') out.cards.push({nome:s.nome, url:safe(()=>F.getMapsUrl(s),s.nome)});
    if(s.tipo==='opcoes') (s.opcoes||[]).forEach(o=>out.opcoes.push(
      {nome:o.nome, url:safe(()=>F.getMapsUrl({...o,coord:o.coord||s.coord}),o.nome)}));
    (s.walkingTours||[]).forEach(t=>out.tours.push({
      nome:t.nome, n:(t.stops||[]).length,
      comQuery:(t.stops||[]).filter(w=>(w.mapsQuery||'').trim()).length,
      url:safe(()=>F.getWalkingTourUrl(t.stops),t.nome)}));
    (s.walkingTours||[]).forEach(t=>out.tours_coords.push({
      grupo:'walking tour '+JSON.stringify(t.nome),
      stops:(t.stops||[]).filter(w=>w.coord).map(w=>({nome:w.nome,lat:w.coord.lat,lng:w.coord.lng}))}));
  });
  out.dias_coords.push({grupo:'dia '+d.date,
    stops:(d.stops||[]).filter(s=>s.tipo==='card'&&s.coord&&!s.noMaps)
      .map(s=>({nome:s.nome,lat:s.coord.lat,lng:s.coord.lng}))});
});
console.log(JSON.stringify(out));
'''


def query_de(url):
    """Extrai o texto que efetivamente vai pro Google Maps."""
    if not url or url == '#':
        return None, 'sem-link'
    if url.startswith('ERRO:'):
        return url, 'erro'
    s = url
    try:
        from urllib.parse import unquote
        s = unquote(url)
    except Exception:
        pass
    m = re.search(r'maps/search/([^/@]+)', s) or re.search(r'[?&]query=([^&]+)', s)
    if m:
        return m.group(1), 'busca'
    if '/dir/?api=1' in s:
        return s, 'rota-coord'
    m = re.search(r'maps/dir/(.+?)/?$', s)
    if m:
        return m.group(1), 'rota-nome'
    return s, 'outro'


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = {a for a in sys.argv[1:] if a.startswith('--')}
    if not args:
        print(__doc__)
        return 2
    html = Path(args[0])
    tpl = Path(__file__).resolve().parent.parent / 'templates' / 'render-functions.js'
    if not html.exists() or not tpl.exists():
        print(f"{C_ERR}✗{C_END} arquivo não encontrado: {html if not html.exists() else tpl}")
        return 2

    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as f:
        f.write(JS_RUNNER)
        runner = f.name
    try:
        r = subprocess.run(['node', runner, str(tpl), str(html), json.dumps(FUNCS)],
                           capture_output=True, text=True, timeout=60)
    except FileNotFoundError:
        print(f"{C_WARN}⚠{C_END}  node não disponível — não dá pra montar as URLs")
        return 2
    finally:
        Path(runner).unlink(missing_ok=True)
    if r.returncode != 0:
        print(f"{C_ERR}✗{C_END} runner falhou:\n{r.stderr[:400]}")
        return 2
    data = json.loads(r.stdout)
    if data.get('erro'):
        print(f"{C_ERR}✗{C_END} {data['erro']}")
        return 2

    quiet, show_urls = '--quiet' in flags, '--urls' in flags
    problemas = []
    print(f"\n{C_BOLD}=== Maps audit · {html.parent.name} ==={C_END}"
          f"  {C_DIM}(MAPS_REGION={data['maps_region']!r}){C_END}\n")

    # ── rotas do dia
    coord = [x for x in data['rotas'] if query_de(x['url'])[1] == 'rota-coord']
    erros_rota = [x for x in data['rotas'] if str(x['url']).startswith('ERRO:')]
    for x in erros_rota:
        problemas.append(f"rota de {x['dia']} estourou: {x['url']}")
    for x in data['rotas']:
        q, tipo = query_de(x['url'])
        if tipo == 'rota-nome':
            pts = q.split('/')
            for i, p in enumerate(pts):
                if i and p == pts[i - 1]:
                    problemas.append(f"rota de {x['dia']} repete o ponto {p!r}")
                if re.match(r'^[A-Z],\s', p):
                    problemas.append(f"rota de {x['dia']} tem waypoint fantasma {p!r} (barra na query?)")
    print(f"  {'✓' if not coord else '⚠'} Rotas do dia: "
          f"{len(data['rotas']) - len(coord)} por nome · {len(coord)} por coordenada"
          + (f"  {C_DIM}({', '.join(x['dia'] for x in coord[:4])}){C_END}" if coord else ""))

    # ── walking tours
    wt_coord = [t for t in data['tours'] if query_de(t['url'])[1] == 'rota-coord']
    parciais = [t for t in data['tours'] if 0 < t['comQuery'] < t['n']]
    for t in parciais:
        problemas.append(f"walking tour {t['nome']!r} tem mapsQuery em {t['comQuery']}/{t['n']} "
                         f"paradas — cai pra coordenada em silêncio")
    print(f"  {'✓' if not wt_coord else '⚠'} Walking tours: "
          f"{len(data['tours']) - len(wt_coord)} por nome · {len(wt_coord)} por coordenada")

    # ── coordenada idêntica em stops distintos (mesmo dia · mesmo walking tour)
    # Caso Tophet/MAB (auditoria 2026-08-08): dois stops de WT com a MESMA coord
    # passavam invisíveis — a rota vai por nome, então ninguém olhava as coords,
    # mas são elas que desenham os pinos do mapa in-app. Coord repetida = ou um
    # dos stops está no lugar errado, ou é copy-paste não conferido. Bloqueia.
    # No nível do dia só compara CARDS: transit compartilha coord com o destino
    # por design, e opcoes herda a coord do stop — não são suspeitos.
    dup_coords = []
    for g in data.get('tours_coords', []) + data.get('dias_coords', []):
        vistos = {}
        for s in g['stops']:
            key = (s['lat'], s['lng'])
            if key in vistos and vistos[key] != s['nome']:
                dup_coords.append((g['grupo'], vistos[key], s['nome'], key))
            else:
                vistos.setdefault(key, s['nome'])
    for grupo, a, b, (lat, lng) in dup_coords:
        problemas.append(f"{grupo}: coord idêntica ({lat}, {lng}) em {a!r} e {b!r} "
                         f"— um dos dois está no lugar errado (caso Tophet/MAB)")
    print(f"  {'✓' if not dup_coords else '✗'} Coords: "
          f"{len(dup_coords)} ponto(s) repetido(s) entre stops distintos")

    # ── buscas (cards + opções)
    genericas, vazias = [], []
    for grupo in ('cards', 'opcoes'):
        for x in data[grupo]:
            q, tipo = query_de(x['url'])
            if tipo == 'erro':
                problemas.append(f"{x['nome']}: {q}")
            elif tipo == 'busca':
                if GENERICA.match(q.strip()):
                    genericas.append((x['nome'], q))
                elif len(q.strip()) < 3:
                    vazias.append((x['nome'], q))
    for nome, q in genericas:
        problemas.append(f"{nome!r} busca {q!r} — descreve a atividade, não o lugar "
                         f"(use mapsQuery ou noMaps)")
    for nome, q in vazias:
        problemas.append(f"{nome!r} gera busca vazia/curta {q!r}")
    print(f"  {'✓' if not (genericas or vazias) else '✗'} Buscas: "
          f"{len(data['cards'])} cards · {len(data['opcoes'])} opções · "
          f"{len(genericas)} genérica(s)")

    if show_urls:
        print(f"\n{C_BOLD}--- URLs (abra pra conferir) ---{C_END}")
        for x in data['rotas']:
            print(f"  [{x['dia']}] {x['url']}")
        for t in data['tours']:
            print(f"  [WT {t['nome'][:24]}] {t['url']}")

    print()
    if problemas:
        print(f"{C_ERR}✗ {len(problemas)} problema(s){C_END}")
        for p in problemas[:20]:
            print(f"  {C_ERR}•{C_END} {p}")
        if len(problemas) > 20:
            print(f"  {C_DIM}… +{len(problemas)-20}{C_END}")
        return 1
    print(f"{C_OK}✓ nenhuma URL malformada, genérica ou repetida{C_END}")
    if coord or wt_coord:
        print(f"{C_DIM}  (rotas por coordenada funcionam, mas o Maps mostra \"Dropped pin\" "
              f"em vez do nome — preencha mapsQuery pra melhorar){C_END}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
