#!/usr/bin/env python3
"""
audit.py — Crítico de conteúdo (skill critico-roteiro)

Portão de qualidade de CONTEÚDO. Dois modos:

  • ROTEIRO (default): audita data.json / index.html · 10 dimensões · /40
  • SCOUT (--scout):   audita levantamento .md da destination-scout · 5 dim · /20

Roda como gate dentro do pipeline de roteiro E da destination-scout; também
standalone pra melhorar conteúdo já feito.

Uso:
    python3 skills/critico-roteiro/audit.py <viagem>/data.json
    python3 skills/critico-roteiro/audit.py <viagem>/data.json --check-links
    python3 skills/critico-roteiro/audit.py <viagem>/index.html
    python3 skills/critico-roteiro/audit.py entregas/<slug>.md --scout [--terceiros]
    python3 skills/critico-roteiro/audit.py <arquivo> --json   # saída machine-readable

Exit: 0 = aprovado  ·  1 = não aprovado  ·  2 = erro de input
  roteiro: aprovado = nota≥28/40 E P0=0   ·   scout: aprovado = nota≥14/20 E P0=0

Rubrica completa: references/content-rubric.md
Fonte de verdade do veredito/preço-datado/fontes (não forkar):
    skills/destination-scout/references/mapping-rubric.md
"""

import re
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

# ---------------------------------------------------------------------------
# COLORS
# ---------------------------------------------------------------------------
class C:
    OK   = '\033[92m'
    WARN = '\033[93m'
    ERR  = '\033[91m'
    DIM  = '\033[2m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'
    END  = '\033[0m'

# ---------------------------------------------------------------------------
# FINDINGS
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    sev: int       # 0=P0 · 1=P1 · 2=P2 · 3=P3
    dim: int       # 1-10
    msg: str
    stop: str = ''

SEV_LABEL = {0: 'P0', 1: 'P1', 2: 'P2', 3: 'P3'}
SEV_COLOR = {0: C.ERR, 1: C.ERR, 2: C.WARN, 3: C.DIM}
SEV_DESC  = {
    0: 'BLOQUEIA deploy',
    1: 'Corrigir antes de entregar',
    2: 'Recomendado',
    3: 'Sugestão',
}

DIM_NAMES = {
    1:  'D1 Storytelling & Escrita',
    2:  'D2 Profundidade de Card',
    3:  'D3 Logística & Precisão',
    4:  'D4 Coords & Precisão',
    5:  'D5 Links & Verificação',
    6:  'D6 Adaptação ao Público',
    7:  'D7 Walking Tours',
    8:  'D8 Honestidade & Curadoria',
    9:  'D9 Cobertura & Schema',
    10: 'D10 Arco & Ritmo',
}

# ---------------------------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------------------------

def load_from_json(path: Path) -> Dict:
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def extract_from_html(content: str) -> Dict:
    result: Dict = {}

    def try_extract(pattern, fallback):
        m = re.search(pattern, content, re.DOTALL)
        if not m:
            return fallback
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            return fallback

    result['days']        = try_extract(r'const\s+DAYS\s*=\s*(\[[\s\S]*?\])\s*;', [])
    result['links_map']   = try_extract(r'const\s+LINKS_MAP\s*=\s*(\{[\s\S]*?\})\s*;', {})
    result['transit_map'] = try_extract(r'const\s+TRANSIT_MAP\s*=\s*(\{[\s\S]*?\})\s*;', {})
    return result

def load_data(path: Path) -> Dict:
    if path.suffix == '.json':
        return load_from_json(path)
    content = path.read_text(encoding='utf-8')
    return extract_from_html(content)

# ---------------------------------------------------------------------------
# DATA ACCESS HELPERS
# ---------------------------------------------------------------------------

def get_cards(data: Dict) -> List[Dict]:
    return [s for day in data.get('days', [])
              for s in day.get('stops', [])
              if s.get('tipo') == 'card']

def get_all_stops(data: Dict) -> List[Tuple[Dict, Dict]]:
    return [(s, day)
            for day in data.get('days', [])
            for s in day.get('stops', [])]

def get_transit_stops(data: Dict) -> List[Dict]:
    return [s for s, _ in get_all_stops(data) if s.get('tipo') == 'transit']

def get_opcoes_stops(data: Dict) -> List[Dict]:
    return [s for s, _ in get_all_stops(data) if s.get('tipo') == 'opcoes']

def get_wt_parts(data: Dict) -> List[Tuple[str, Dict]]:
    """Returns [(card_nome, wt_part), ...]"""
    parts = []
    for c in get_cards(data):
        for wt in c.get('walkingTours', []):
            parts.append((c.get('nome', ''), wt))
    return parts

# ---------------------------------------------------------------------------
# CONTENT HELPERS
# ---------------------------------------------------------------------------

IMPERDIVEL_BLACKLIST = {
    'incrível', 'lindo', 'belíssimo', 'imperdível!', 'ótimo', 'excelente',
    'incrivel', 'lindo!', 'must see', 'must-see', 'não perca', 'não deixe',
    'fantástico', 'épico', 'maravilhoso', 'impressionante',
}

PATERNALISM_RE = re.compile(
    r'não tem elevad|sem elevad|cuidado!|panic|metrô.*perig|elevador.*não',
    re.I
)

FACT_RE = re.compile(
    r'\d{3,4}|séc(ulo)?\s*(xix|xx|xxi|\d+)|fundad|criado|inaugur|construíd'
    r'|primeiro|última|históric|original|\d{2,4}\s*anos',
    re.I
)

PRICE_TIME_RE = re.compile(
    r'\d{1,2}h|\$|€|R\$|\d+\s*min|\d{1,2}:\d{2}|gratuito|grátis|gratis|free|\d+/pessoa',
    re.I
)

CUSTO_DATE_RE = re.compile(
    r'\(?\s*(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)[/\s]\d{4}\s*\)?'
    r'|\(\d{4}\)',
    re.I
)

VAGUE_DIST_RE = re.compile(r'\bperto\b|\bpróximo\b|\bpertinho\b|\bacesso fácil\b', re.I)

HYPE_RE = re.compile(r'\bincrível\b|\blindo\b|\bfantástico\b|\bépico\b|\bmaravilhoso\b', re.I)

HONESTY_RE = re.compile(
    r'pula sem culpa|turistada|superestimad|lotad|evitar|vale menos|não vale',
    re.I
)

# Marcadores de parada-a-parada: keycap (1️⃣), circled numbers (①), circled letters
# (Ⓐ-Ⓩ · convenção pra casar com as letras A,B,C… do Google Maps · 2026-07), ou "1. ".
NUM_DICA_RE = re.compile(r'[1-9]️⃣|[①②③④⑤⑥⑦⑧⑨]|[Ⓐ-Ⓩ]|\b[1-9]\. ')


def coord_4dec(coord: Optional[Dict]) -> bool:
    if not coord:
        return False
    def check(v):
        s = str(v)
        return '.' in s and len(s.split('.')[1]) >= 4
    return check(coord.get('lat', '')) and check(coord.get('lng', ''))

def has_parens(name: str) -> bool:
    return '(' in name and ')' in name

def imp_is_generic(text: str) -> bool:
    if not text:
        return True
    t = text.lower().strip().rstrip('!.')
    return len(text) < 20 or any(bad in t for bad in IMPERDIVEL_BLACKLIST)

def custo_is_paid(custo: str) -> bool:
    if not custo:
        return False
    return not any(w in custo.lower() for w in ['gratuito', 'grátis', 'gratis', 'free', '0 '])

def duracao_is_range(s: str) -> bool:
    return bool(s) and ('-' in s or ' a ' in s.lower())

# ---------------------------------------------------------------------------
# DIMENSION AUDITORS
# ---------------------------------------------------------------------------

def d1_storytelling(data: Dict, F: List[Finding]) -> int:
    """D1 · Storytelling & Escrita (padrão Marais + prose-guide)"""
    cards = get_cards(data)
    if not cards:
        return 2

    score = 0

    # Proxy 1: avg sobre length ≥ 150
    sobres = [c.get('sobre', '') for c in cards if c.get('sobre')]
    avg_len = sum(len(s) for s in sobres) / len(sobres) if sobres else 0
    if avg_len >= 150:
        score += 1
    else:
        F.append(Finding(2, 1,
            f'sobre médio: {avg_len:.0f} chars — padrão-ouro ≥150 '
            f'(história/curiosidade com fato concreto)'))

    # Proxy 2: % sobre com indicador factual (ano, data, nome)
    with_fact = sum(1 for c in cards if FACT_RE.search(c.get('sobre', '')))
    pct_fact  = with_fact / len(cards) if cards else 0
    if pct_fact >= 0.5:
        score += 1
    elif pct_fact < 0.25:
        F.append(Finding(2, 1,
            f'sobre sem fato verificável em {len(cards)-with_fact}/{len(cards)} cards '
            f'(sem ano/fundação/nome específico — risco de conteúdo genérico)'))

    # Proxy 3: imperdivel não-genérico em ≥80% que têm o campo
    cards_imp = [c for c in cards if c.get('imperdivel')]
    generic   = [c for c in cards_imp if imp_is_generic(c.get('imperdivel', ''))]
    if not cards_imp:
        pct_miss = 1 - (len(cards_imp) / len(cards))
        if pct_miss > 0.5:
            F.append(Finding(2, 1,
                f'imperdivel ausente em {len(cards)-len(cards_imp)}/{len(cards)} cards '
                f'— campo crucial pra guiar "o que observar"'))
    elif len(generic) / len(cards_imp) <= 0.15:
        score += 1
    else:
        for c in generic[:3]:
            F.append(Finding(1, 1,
                f'imperdivel genérico: "{c.get("imperdivel","")[:70]}"',
                stop=c.get('nome', '')))

    # Proxy 4: WT cards com dicas numeradas
    wt_cards    = [c for c in cards if c.get('walkingTours')]
    if wt_cards:
        wt_numbered = sum(1 for c in wt_cards
                          if any(NUM_DICA_RE.search(d) for d in c.get('dicas', [])))
        if wt_numbered / len(wt_cards) >= 0.5:
            score += 1
        else:
            F.append(Finding(3, 1,
                f'WT cards sem dicas numeradas parada-a-parada '
                f'({len(wt_cards)-wt_numbered}/{len(wt_cards)} cards) '
                f'— numeração 1️⃣2️⃣ reflete pins do mapa'))
    else:
        score += 1  # sem WT: N/A

    return min(4, score)


def d2_profundidade(data: Dict, F: List[Finding]) -> int:
    """D2 · Profundidade de Card (quality bar dos campos)"""
    cards = get_cards(data)
    if not cards:
        return 2

    per_card = []
    for c in cards:
        name  = c.get('nome', '(sem nome)')
        pts   = 0.0

        # sobre ≥ 100 chars
        sobre = c.get('sobre', '')
        if len(sobre) >= 100:
            pts += 1
        elif len(sobre) >= 40:
            pts += 0.5
        elif not sobre:
            F.append(Finding(1, 2, 'sobre ausente', stop=name))

        # imperdivel ≥ 25 chars e não genérico
        imp = c.get('imperdivel', '')
        if imp and len(imp) >= 25 and not imp_is_generic(imp):
            pts += 1
        elif not imp:
            F.append(Finding(2, 2, 'imperdivel ausente', stop=name))

        # dicas ≥ 2 com hora/preço
        dicas = c.get('dicas', [])
        if len(dicas) >= 2:
            pts += 1 if PRICE_TIME_RE.search(' '.join(dicas)) else 0.5
            if not PRICE_TIME_RE.search(' '.join(dicas)):
                F.append(Finding(2, 2,
                    'dicas sem hora/preço/atalho específico', stop=name))
        elif len(dicas) == 1:
            pts += 0.5
            F.append(Finding(2, 2, 'apenas 1 dica (mínimo: 2)', stop=name))
        else:
            F.append(Finding(1, 2, 'dicas ausentes', stop=name))

        # duracao range
        dur = c.get('duracao', '')
        if duracao_is_range(dur):
            pts += 1
        elif dur:
            pts += 0.5
        else:
            F.append(Finding(2, 2, 'duracao ausente', stop=name))

        # custo presente
        custo = c.get('custo', '')
        if custo:
            pts += 1
        else:
            F.append(Finding(2, 2, 'custo ausente', stop=name))

        # acessibilidade ≥ 20 chars — P3 pra green (D6 cuida de yellow/red com P1)
        acess = c.get('acessibilidade', '')
        risco = c.get('risco', 'green')
        if len(acess) >= 20:
            pts += 1
        elif risco not in ('yellow', 'red'):
            F.append(Finding(3, 2,
                f'acessibilidade ausente (risco={risco})', stop=name))

        per_card.append(pts)

    avg = sum(per_card) / len(per_card)
    return min(4, round(avg * 4 / 6))


def d3_logistica(data: Dict, F: List[Finding]) -> int:
    """D3 · Logística & Precisão (mapping-rubric: km, ingresso datado, TRANSIT_MAP)"""
    score = 0

    # TRANSIT_MAP completeness
    transit = get_transit_stops(data)
    tmap    = data.get('transit_map', {})
    if transit:
        covered = sum(1 for s in transit if s.get('nome', '') in tmap)
        pct     = covered / len(transit)
        if pct >= 0.7:
            score += 2
        elif pct >= 0.4:
            score += 1
            F.append(Finding(2, 3,
                f'TRANSIT_MAP incompleto: {covered}/{len(transit)} transit stops cobertos'))
        else:
            F.append(Finding(1, 3,
                f'TRANSIT_MAP muito incompleto: {covered}/{len(transit)} stops cobertos '
                f'— rotas de metrô/uber/ferry ausentes'))
    else:
        score += 2  # sem transit stops: N/A

    # custo datado em cards pagos
    paid = [c for c in get_cards(data) if custo_is_paid(c.get('custo', ''))]
    if paid:
        dated  = sum(1 for c in paid if CUSTO_DATE_RE.search(c.get('custo', '')))
        pct_dt = dated / len(paid)
        if pct_dt >= 0.7:
            score += 1
        elif pct_dt < 0.3:
            F.append(Finding(2, 3,
                f'custo sem data de referência em {len(paid)-dated}/{len(paid)} cards pagos '
                f'— mapping-rubric exige "(mês/ano)" ex: "~$20 (jun/2026)"'))
    else:
        score += 1  # sem cards pagos: N/A

    # Sem "perto/próximo" vagos em dicas
    vague = []
    for c in get_cards(data):
        for dica in c.get('dicas', []):
            if VAGUE_DIST_RE.search(dica):
                vague.append((c.get('nome', ''), dica[:70]))
                break
    if not vague:
        score += 1
    else:
        for name, dica in vague[:3]:
            F.append(Finding(2, 3,
                f'distância vaga ("perto/próximo") — usar km: "{dica}"',
                stop=name))

    return min(4, score)


def d4_coords(data: Dict, F: List[Finding]) -> int:
    """D4 · Coords & Precisão (4 casas, range, parens, unverified)"""
    score = 0

    # 4 casas decimais em todos stops com coord
    all_stops_list = get_all_stops(data)
    bad_dec = [(s.get('nome', ''), s.get('coord')) for s, _ in all_stops_list
               if s.get('coord') and not coord_4dec(s.get('coord'))]
    if not bad_dec:
        score += 2
    elif len(bad_dec) <= 2:
        score += 1
        for name, c in bad_dec:
            F.append(Finding(2, 4, f'coord com <4 casas decimais: lat={c.get("lat")}, lng={c.get("lng")}',
                             stop=name))
    else:
        for name, c in bad_dec[:3]:
            F.append(Finding(1, 4, f'coord com <4 casas decimais: {c}', stop=name))

    # WT stop names com endereço (parens)
    wt_parts = get_wt_parts(data)
    wt_total  = sum(len(wt.get('stops', [])) for _, wt in wt_parts)
    wt_parens = sum(
        sum(1 for s in wt.get('stops', []) if has_parens(s.get('nome', '')))
        for _, wt in wt_parts
    )
    if wt_total > 0:
        if wt_parens / wt_total >= 0.6:
            score += 1
        else:
            F.append(Finding(2, 4,
                f'WT stops sem endereço em parens: {wt_total-wt_parens}/{wt_total} '
                f'— "(119 MacDougal)" ajuda Google Maps acertar'))
    else:
        score += 1  # sem WT: N/A

    # coord_unverified sem aviso explícito
    unverified = [s.get('nome', '') for s, _ in all_stops_list
                  if s.get('coord_unverified') is True]
    if not unverified:
        score += 1
    else:
        for name in unverified[:3]:
            F.append(Finding(1, 4, 'coord marcada coord_unverified:true — validar com web_search antes de entregar', stop=name))

    return min(4, score)


def d5_links(data: Dict, F: List[Finding], check_links: bool) -> int:
    """D5 · Links & Verificação (LINKS_MAP, official, HTTP check)"""
    lmap  = data.get('links_map', {})
    score = 0

    if not lmap:
        F.append(Finding(2, 5,
            'LINKS_MAP vazio — cards sem links externos (official + reviews). '
            'Adicionar ao menos sites oficiais das atrações principais'))
        return 0

    score += 1

    # Tem entradas type:official
    has_official = any(
        any(l.get('type') == 'official' for l in links)
        for links in lmap.values()
    )
    if has_official:
        score += 1
    else:
        F.append(Finding(2, 5,
            'LINKS_MAP sem entradas type="official" — faltam links ao site oficial das atrações'))

    if check_links:
        all_urls = [l['url'] for links in lmap.values() for l in links if l.get('url')]
        print(f"  {C.DIM}Checando {len(all_urls)} URLs via HTTP HEAD...{C.END}")
        broken = []
        for url in all_urls:
            try:
                req = urllib.request.Request(
                    url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    if resp.status >= 400:
                        broken.append((url, f'HTTP {resp.status}'))
            except urllib.error.HTTPError as e:
                if e.code >= 400:
                    broken.append((url, f'HTTP {e.code}'))
            except Exception as e:
                broken.append((url, f'err: {str(e)[:60]}'))

        if not broken:
            score += 2
        elif len(broken) <= 2:
            score += 1
            for url, reason in broken:
                F.append(Finding(1, 5, f'link quebrado: {url} ({reason}) — remover do LINKS_MAP'))
        else:
            for url, reason in broken[:5]:
                F.append(Finding(1, 5, f'link quebrado: {url} ({reason})'))
            if len(broken) > 5:
                F.append(Finding(1, 5, f'... +{len(broken)-5} URLs com problema'))
    else:
        score += 1  # assume ok sem verificar
        F.append(Finding(3, 5,
            'links não verificados via HTTP — rodar com --check-links pra detectar 4xx/5xx'))

    return min(4, score)


def d6_adaptacao(data: Dict, F: List[Finding]) -> int:
    """D6 · Adaptação ao Público (família, filha 3a, sem paternalismo)"""
    cards         = get_cards(data)
    all_stops_lst = get_all_stops(data)
    days          = data.get('days', [])
    score         = 0

    # acessibilidade em cards risco yellow/red
    risky = [c for c in cards if c.get('risco') in ('yellow', 'red')]
    if risky:
        with_a = sum(1 for c in risky
                     if len(c.get('acessibilidade', '')) >= 15)
        pct = with_a / len(risky)
        if pct >= 0.85:
            score += 1
        else:
            missing = [c.get('nome', '') for c in risky
                       if len(c.get('acessibilidade', '')) < 15]
            for name in missing[:3]:
                F.append(Finding(1, 6,
                    'acessibilidade ausente/rasa em card risco yellow/red', stop=name))
    else:
        score += 1  # sem cards arriscados: N/A

    # Sem paternalismo
    pat_hits = []
    for stop, _ in all_stops_lst:
        text = (stop.get('sobre', '') + ' '
                + ' '.join(stop.get('dicas', []))
                + ' ' + stop.get('cat', ''))
        if PATERNALISM_RE.search(text):
            pat_hits.append(stop.get('nome', ''))
    if not pat_hits:
        score += 1
    else:
        for name in pat_hits[:2]:
            F.append(Finding(2, 6, 'aviso paternalista detectado (metrô sem elevador etc.)', stop=name))

    # ≤ 6 cards por dia
    overloaded = [(d.get('date', ''), sum(1 for s in d.get('stops', []) if s.get('tipo') == 'card'))
                  for d in days
                  if sum(1 for s in d.get('stops', []) if s.get('tipo') == 'card') > 6]
    if not overloaded:
        score += 1
    else:
        for date, n in overloaded[:2]:
            F.append(Finding(2, 6, f'{n} cards em {date} — ritmo família: máx 6 por dia (c/ filha 3a)'))

    # Dia de chegada/saída ≤ 3 cards
    if days:
        for day in [days[0], days[-1]]:
            note  = (day.get('nota', '') + day.get('tema', '')).lower()
            is_travel = any(w in note for w in ['chegada', 'partida', 'saída', 'voo', 'pouso'])
            n_cards   = sum(1 for s in day.get('stops', []) if s.get('tipo') == 'card')
            if is_travel and n_cards > 3:
                F.append(Finding(2, 6,
                    f'dia de viagem ({day.get("date","")}) tem {n_cards} cards — pesado pra dia chegada/saída'))
            else:
                score += 1
            break  # só o primeiro

    # Pacing advisory · NÃO pontua · NÃO bloqueia — só alerta pra Tobia decidir.
    # Especialistas em viagem c/ criança pequena: 1-2 atividades "pesadas"/dia,
    # ancoradas na janela da criança. Aqui é SINAL, não corte automático: o peso
    # do dia depende do público e da dinâmica familiar — quem decide é o Tobia.
    def _is_heavy(s: Dict) -> bool:
        if s.get('tipo') != 'card':
            return False
        if s.get('risco') in ('yellow', 'red'):
            return True
        if s.get('walkingTours'):
            return True
        return bool(re.search(r'\d+\s*h', s.get('duracao', '')))
    for day in days:
        heavy_n = sum(1 for s in day.get('stops', []) if _is_heavy(s))
        if heavy_n > 2:
            F.append(Finding(3, 6,
                f'{heavy_n} atrações "pesadas" em {day.get("date","")} — pode ser '
                f'corrido pra esse público; avalie remanejar (alerta, NÃO corte automático)'))

    return min(4, score)


def d7_walking_tours(data: Dict, F: List[Finding]) -> int:
    """D7 · Walking Tours (partition, numeração, parens, storytelling)"""
    cards    = get_cards(data)
    wt_cards = [c for c in cards if c.get('walkingTours')]
    wt_parts = get_wt_parts(data)

    if not wt_cards:
        return 4  # sem WT no roteiro — N/A, não penalizar

    score = 0

    # Partes com 4-8 stops
    bad_parts = [(name, wt) for name, wt in wt_parts
                 if not (4 <= len(wt.get('stops', [])) <= 8)]
    if not bad_parts:
        score += 1
    else:
        for name, wt in bad_parts[:2]:
            n = len(wt.get('stops', []))
            sev = 1 if n > 8 else 2
            F.append(Finding(sev, 7,
                f'WT parte "{wt.get("nome","")}" tem {n} stops '
                f'({"particionar em 2 partes ~6" if n > 8 else "muito curto (<4)"})',
                stop=name))

    # Dicas numeradas em WT cards
    numbered = sum(1 for c in wt_cards
                   if any(NUM_DICA_RE.search(d) for d in c.get('dicas', [])))
    if numbered / len(wt_cards) >= 0.5:
        score += 1
    else:
        F.append(Finding(2, 7,
            f'WT cards sem dicas numeradas parada-a-parada: '
            f'{len(wt_cards)-numbered}/{len(wt_cards)}'))

    # WT stops com endereço em parens
    wt_total  = sum(len(wt.get('stops', [])) for _, wt in wt_parts)
    wt_parens = sum(
        sum(1 for s in wt.get('stops', []) if has_parens(s.get('nome', '')))
        for _, wt in wt_parts
    )
    if wt_total == 0 or wt_parens / wt_total >= 0.5:
        score += 1
    else:
        F.append(Finding(2, 7,
            f'{wt_total-wt_parens}/{wt_total} WT stops sem endereço em parens '
            f'— "(119 MacDougal)" melhora precisão do Google Maps'))

    # Partition correta quando total > 8
    for c in wt_cards:
        wts   = c.get('walkingTours', [])
        total = sum(len(w.get('stops', [])) for w in wts)
        if total > 8 and len(wts) == 1:
            F.append(Finding(1, 7,
                f'{total} stops em parte única — particionar em 2 partes de ~6',
                stop=c.get('nome', '')))
        else:
            score = min(score + 1, 4)
            break

    return min(4, score)


def d8_honestidade(data: Dict, F: List[Finding]) -> int:
    """D8 · Honestidade & Curadoria (risco distribuição, pula sem culpa, anti-hype)"""
    cards = get_cards(data)
    if not cards:
        return 2

    score = 0

    # risco distribution — não tudo green
    riscos    = [c.get('risco', 'green') for c in cards]
    pct_green = riscos.count('green') / len(riscos)
    if pct_green < 0.9:
        score += 2
    elif pct_green < 1.0:
        score += 1
        F.append(Finding(3, 8,
            f'risco: {riscos.count("green")}/{len(riscos)} green '
            f'— considerar yellow em dias lotados/quentes'))
    else:
        F.append(Finding(1, 8,
            f'todos {len(riscos)} cards são risco=green — implausível '
            f'(locais cheios, calor, multidão merecem yellow/red)'))

    # "pula sem culpa" ou crítica honesta presente
    all_dicas_text = ' '.join(
        d for c in cards for d in c.get('dicas', [])
    ) + ' '.join(c.get('sobre', '') for c in cards)

    if HONESTY_RE.search(all_dicas_text):
        score += 1
    else:
        F.append(Finding(3, 8,
            'nenhuma crítica honesta encontrada ("pula sem culpa", "turistada", "lotado") '
            '— consultor crítico deve sinalizar atrações fracas'))

    # zero hipérbole em imperdivel
    hype_cards = [c for c in cards if HYPE_RE.search(c.get('imperdivel', '') or '')]
    if not hype_cards:
        score += 1
    elif len(hype_cards) <= 2:
        for c in hype_cards:
            F.append(Finding(3, 8,
                f'imperdivel com hipérbole genérica: "{c.get("imperdivel","")[:70]}" '
                f'— descrever o que observar, não adjetivar',
                stop=c.get('nome', '')))
    else:
        F.append(Finding(2, 8,
            f'{len(hype_cards)} imperdivel com hipérbole '
            f'("incrível/fantástico") — trocar por "o que observar"'))

    return min(4, score)


def d9_cobertura(data: Dict, F: List[Finding]) -> int:
    """D9 · Cobertura & Schema (completude estrutural)"""
    days  = data.get('days', [])
    score = 0

    # Todos dias com ≥1 card
    ARRIVAL_RE = re.compile(r'chegada|saída|voo|partida|regresso|volta', re.I)
    no_card_days = [(d.get('date', ''), d.get('tema', '')) for d in days
                    if not any(s.get('tipo') == 'card' for s in d.get('stops', []))]
    if not no_card_days:
        score += 1
    else:
        for date, tema in no_card_days[:2]:
            sev = 2 if ARRIVAL_RE.search(tema) else 1
            F.append(Finding(sev, 9, f'dia sem nenhum stop tipo=card: {date}'))

    # temaCurto ≤ 15
    long_tc = [(d.get('date', ''), d.get('temaCurto', '')) for d in days
               if len(d.get('temaCurto', '')) > 15]
    if not long_tc:
        score += 1
    else:
        for date, tc in long_tc[:2]:
            F.append(Finding(2, 9,
                f'temaCurto longo ({len(tc)} chars): "{tc}" — máx 15',
                stop=date))

    # opcoes bem formadas (2-4 items com preco+dist)
    bad_op = 0
    for op in get_opcoes_stops(data):
        opts = op.get('opcoes', [])
        if not (2 <= len(opts) <= 4):
            bad_op += 1
            F.append(Finding(2, 9,
                f'{len(opts)} opção(ões) (esperado 2-4)',
                stop=op.get('nome', '')))
        else:
            missing = [o for o in opts if not (o.get('preco') and o.get('dist'))]
            if missing:
                bad_op += 1
                F.append(Finding(2, 9, 'opção sem preco ou dist', stop=op.get('nome', '')))
    if bad_op == 0:
        score += 1

    # nota presente em maioria dos dias (big picture signal)
    with_nota = sum(1 for d in days if d.get('nota'))
    pct_nota  = with_nota / len(days) if days else 1
    if pct_nota >= 0.6:
        score += 1
    else:
        F.append(Finding(3, 9,
            f'nota ausente em {len(days)-with_nota}/{len(days)} dias '
            f'— campo que estabelece big picture do dia'))

    return min(4, score)


def d10_arco(data: Dict, F: List[Finding]) -> int:
    """D10 · Arco & Ritmo (big picture, ordem temporal, ritmo família)"""
    days  = data.get('days', [])
    score = 0
    if not days:
        return 0

    # Todos dias com tema
    no_tema = [d.get('date', '') for d in days if not d.get('tema')]
    if not no_tema:
        score += 1
    else:
        for d in no_tema[:2]:
            F.append(Finding(1, 10, f'dia sem tema: {d}'))

    # Ordem temporal manha→tarde→noite
    PERIOD = {'manha': 0, 'tarde': 1, 'noite': 2}
    bad_ord = []
    for day in days:
        ps = [PERIOD.get(s.get('periodo', 'manha'), 0)
              for s in day.get('stops', []) if s.get('periodo')]
        inversions = sum(1 for i in range(len(ps)-1) if ps[i] > ps[i+1])
        if inversions > 1:
            bad_ord.append(day.get('date', ''))
    if not bad_ord:
        score += 1
    else:
        for d in bad_ord[:2]:
            F.append(Finding(2, 10, f'ordem temporal inconsistente em {d} (manha→tarde→noite)'))

    # ≤ 5 cards/dia (ritmo família)
    heavy = [(d.get('date', ''), sum(1 for s in d.get('stops', []) if s.get('tipo') == 'card'))
             for d in days
             if sum(1 for s in d.get('stops', []) if s.get('tipo') == 'card') > 5]
    if not heavy:
        score += 1
    else:
        for date, n in heavy[:2]:
            F.append(Finding(2, 10,
                f'{n} cards em {date} — ritmo família: máx 5 cards/dia (filha 3a)'))

    # Sequência geográfica — proxy: dar ponto por default (requer julgamento humano)
    score += 1

    return min(4, score)

# ---------------------------------------------------------------------------
# SCORING & REPORT
# ---------------------------------------------------------------------------

def score_band(total: int) -> Tuple[str, str]:
    if total >= 36:
        return 'Excelente', C.OK
    if total >= 28:
        return 'Bom', C.CYAN
    if total >= 20:
        return 'Aceitável', C.WARN
    return 'Ruim', C.ERR

def is_approved(total: int, findings: List[Finding]) -> bool:
    return total >= 28 and not any(f.sev == 0 for f in findings)

MANUAL_CHECKLIST = """
┌──────────────────────────────────────────────────────────────────────────┐
│  CHECKLIST MANUAL · dimensões que exigem julgamento humano               │
├──────────────────────────────────────────────────────────────────────────┤
│  D1 Storytelling                                                         │
│  [ ] sobre conta história/curiosidade (data, personagem, lenda)?        │
│  [ ] imperdivel = "o que observar" (detalhe concreto que distraído      │
│      perde), não platitude genérica?                                     │
│  [ ] dicas narram parada-a-parada (guia que encanta pra gorjeta)?       │
│  [ ] zero floreio vazio ("paraíso indescritível", "energia mágica")?    │
│                                                                          │
│  D6 Adaptação ao Público                                                 │
│  [ ] ritmo de filha 3a respeitado (sombra, banheiro, colo, cadência)?  │
│  [ ] elo mais restritivo calibra os vereditos?                           │
│  [ ] atrações família têm kids-friendly destacado?                       │
│                                                                          │
│  D7 Walking Tours                                                        │
│  [ ] ângulo único por WT (não genérico "conheça o bairro")?             │
│  [ ] rubrica de valor (alto/médio/baixo) justificada antes do WT?       │
│  [ ] storytelling parada-a-parada presente?                              │
│                                                                          │
│  D8 Honestidade                                                          │
│  [ ] atrações fracas/turistadas com "pula sem culpa"?                   │
│  [ ] armadilhas sinalizadas (fila inútil, foto enganosa, caro+fraco)?   │
│  [ ] todo card tem info que o viajante usa (não filler)?                 │
│                                                                          │
│  D10 Arco                                                                │
│  [ ] big picture de cada dia claro no tema/nota?                        │
│  [ ] sequência geográfica eficiente (sem backtrack óbvio)?              │
│  [ ] roteiro como um todo tem ritmo saudável (não maratonar)?           │
└──────────────────────────────────────────────────────────────────────────┘
"""


def print_report(dim_scores: Dict[int, int], findings: List[Finding],
                 show_checklist: bool = True) -> None:
    total = sum(dim_scores.values())
    band, bcolor = score_band(total)

    pcnts = {0: 0, 1: 0, 2: 0, 3: 0}
    for f in findings:
        pcnts[f.sev] += 1

    # Dimension scores table
    print(f"\n{C.BOLD}=== Dimensões de Conteúdo ==={C.END}\n")
    for idx in sorted(dim_scores):
        s      = dim_scores[idx]
        bar    = '█' * s + '░' * (4 - s)
        color  = C.OK if s >= 3 else (C.WARN if s >= 2 else C.ERR)
        print(f"  {color}{bar}{C.END} {s}/4  {DIM_NAMES[idx]}")

    # Findings grouped by severity
    grouped: Dict[int, List[Finding]] = {0: [], 1: [], 2: [], 3: []}
    for f in findings:
        grouped[f.sev].append(f)

    if any(grouped.values()):
        print(f"\n{C.BOLD}=== Achados ({len(findings)} total) ==={C.END}\n")
        for sev in [0, 1, 2, 3]:
            if not grouped[sev]:
                continue
            lbl   = SEV_LABEL[sev]
            color = SEV_COLOR[sev]
            desc  = SEV_DESC[sev]
            print(f"{color}{lbl} — {desc}{C.END}")
            for f in grouped[sev]:
                stop_str = f' [{f.stop[:45]}]' if f.stop else ''
                print(f"  • {f.msg}{C.DIM}{stop_str}{C.END}")
            print()

    # Manual checklist
    if show_checklist:
        print(MANUAL_CHECKLIST)

    # Summary line
    print('─' * 62)
    ok_color = C.OK if is_approved(total, findings) else C.ERR
    print(f"{C.BOLD}★ Conteúdo: {ok_color}{total}/40{C.END}"
          f" · {bcolor}{band}{C.END}"
          f"  |  P0: {pcnts[0]}  P1: {pcnts[1]}  P2: {pcnts[2]}  P3: {pcnts[3]}")

    if is_approved(total, findings):
        print(f"{C.OK}✓ Aprovado pra entrega{C.END}")
    elif pcnts[0] > 0:
        print(f"{C.ERR}✗ Bloqueado: {pcnts[0]} P0(s) — corrigir antes de continuar{C.END}")
    else:
        print(f"{C.WARN}⚠ Iterar: nota {total}/40 < 28 — corrigir P1s listados acima{C.END}")
    print()


def print_json_result(dim_scores: Dict[int, int], findings: List[Finding]) -> None:
    total = sum(dim_scores.values())
    band, _  = score_band(total)
    out = {
        'mode':       'roteiro',
        'score':      total,
        'max':        40,
        'band':       band,
        'approved':   is_approved(total, findings),
        'dimensions': {DIM_NAMES[i]: s for i, s in sorted(dim_scores.items())},
        'findings': [
            {
                'sev':  SEV_LABEL[f.sev],
                'dim':  DIM_NAMES.get(f.dim, str(f.dim)),
                'msg':  f.msg,
                'stop': f.stop,
            }
            for f in findings
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

# ---------------------------------------------------------------------------
# SCOUT MODE · auditoria dos levantamentos .md da destination-scout
# ---------------------------------------------------------------------------
# Mesmos princípios do roteiro (anti-invenção, veredito, honestidade), aplicados
# ao formato .md (prosa + tabelas). Fonte de verdade das regras:
# skills/destination-scout/references/mapping-rubric.md — este modo NÃO forka as
# regras, só as VERIFICA no outro formato. 5 dimensões · /20.

SCOUT_DIM_NAMES = {
    1: 'S1 Anti-invenção & Preços',
    2: 'S2 Veredito & Honestidade',
    3: 'S3 Logística & Precisão',
    4: 'S4 Fontes & Verificação',
    5: 'S5 Estrutura & Cobertura',
}

PRICE_AMOUNT_RE = re.compile(r'(?:R\$|US\$|€|\$)\s?\d[\d.,]*', re.I)
VERDICT_RE      = re.compile(r'🟢|🟡|🔴')
FONTES_RE       = re.compile(r'^#{1,4}\s*(fontes|refer[êe]ncias|sources)\b', re.I | re.M)
ARMADILHA_RE    = re.compile(r'armadilha|cilada|turistada|superestimad|pula sem culpa|fila inútil|não vale a pena', re.I)
KM_MIN_RE       = re.compile(r'\d+\s?(km|min|minutos|h\b|horas)', re.I)
SABOR_RE        = re.compile(r'sabor|ingrediente|prato típico|endêmic|assinatura|especialidade|típic', re.I)
ANCHOR_RE       = re.compile(r'âncora|estar na porta', re.I)
CONFIRMAR_RE    = re.compile(r'\[a confirmar\]|\[confirmar\]', re.I)


def detect_mini_plano(text: str) -> bool:
    """Mini-plano = 1 bloco/meia-diária com âncora fixa, sem tabela de veredito."""
    has_table  = bool(re.search(r'esfor[çc]o.*recompensa', text, re.I))
    n_verdicts = len(VERDICT_RE.findall(text))
    has_anchor = bool(ANCHOR_RE.search(text))
    return n_verdicts < 2 and not has_table and has_anchor


def logistica_portion(text: str) -> str:
    """Só o bloco de mapeamento/logística (antes de 'História') — a prosa histórica
    tem 'perto'/'próximo' em sentido não-geográfico (ex: 'lugar perto do pântano')."""
    m = re.search(r'^#{1,4}\s*hist[óo]ria', text, re.I | re.M)
    return text[:m.start()] if m else text


def s1_precos(text: str, F: List[Finding]) -> int:
    """S1 · Anti-invenção: todo preço datado (mapping-rubric: '~R$50, jan/2026')."""
    prices = PRICE_AMOUNT_RE.findall(text)
    dated  = len(CUSTO_DATE_RE.findall(text))
    if not prices:
        return 3  # sem preços citados: raso mas não há invenção a punir
    ratio = min(1.0, dated / len(prices))
    if ratio >= 0.7:
        return 4
    if ratio >= 0.4:
        F.append(Finding(2, 1,
            f'~{len(prices)-dated}/{len(prices)} preços sem data — mapping-rubric exige "(mês/ano)"'))
        return 2
    F.append(Finding(1, 1,
        f'maioria dos preços sem data ({dated}/{len(prices)} datados) — preço apodrece sem data de referência'))
    return 1


def s2_veredito(text: str, F: List[Finding], is_mini: bool) -> int:
    """S2 · Veredito 🟢🟡🔴 + honestidade (armadilhas, anti-hype)."""
    n_verdicts    = len(VERDICT_RE.findall(text))
    has_armadilha = bool(ARMADILHA_RE.search(text))
    hype          = len(HYPE_RE.findall(text))

    if is_mini:
        # mini-plano não dá veredito por atração; valoriza honestidade na prosa
        score = 2
        if has_armadilha or re.search(r'fechad|não programem|encarem|opciona|degraus', text, re.I):
            score += 1
        if hype <= 2:
            score += 1
        else:
            F.append(Finding(3, 2, f'{hype} termos de hype vazio ("incrível/lindo") — prose-guide pede factual'))
        return min(4, score)

    score = 0
    if n_verdicts >= 3:
        score += 2
    elif n_verdicts >= 1:
        score += 1
        F.append(Finding(2, 2, f'poucos vereditos 🟢🟡🔴 ({n_verdicts}) — cada atração precisa do seu, calibrado ao perfil'))
    else:
        F.append(Finding(1, 2, 'nenhum veredito 🟢🟡🔴 — levantamento sem crítica vira folder de agência'))
    if has_armadilha:
        score += 1
    else:
        F.append(Finding(2, 2, 'sem callout de armadilha/turistada — mapping-rubric: "o valor é DIZER o que ninguém diz"'))
    if hype <= 2:
        score += 1
    else:
        F.append(Finding(3, 2, f'{hype} termos de hype vazio — prose-guide pede factual, sem floreio'))
    return min(4, score)


def s3_logistica_scout(text: str, F: List[Finding]) -> int:
    """S3 · Logística: distância quantificada (km/min, não 'perto') + ingresso/reserva/horário."""
    logtext = logistica_portion(text)  # ignora 'perto' da prosa histórica
    vague = len(VAGUE_DIST_RE.findall(logtext))
    quant = len(KM_MIN_RE.findall(logtext))
    score = 0
    if quant >= 3:
        score += 2
    elif quant >= 1:
        score += 1
    else:
        F.append(Finding(1, 3, 'nenhuma distância/tempo quantificado (km/min) — mapping-rubric: "não perto, número"'))
    if vague == 0:
        score += 1
    else:
        F.append(Finding(2, 3, f'{vague} distância(s) vaga(s) ("perto/próximo") — trocar por km/min'))
    if re.search(r'ingresso|reserva|horário|entrada até|abre|fecha|gratuito', text, re.I):
        score += 1
    else:
        F.append(Finding(2, 3, 'sem menção a ingresso/reserva/horário — logística obrigatória (mapping-rubric)'))
    return min(4, score)


def s4_fontes(text: str, F: List[Finding], relax: bool) -> int:
    """S4 · Fontes citadas. Obrigatória no macro-interno; OPCIONAL pra-terceiros/mini (decisão Tobia)."""
    if FONTES_RE.search(text):
        return 4
    if relax:
        return 4  # pra-terceiros/mini: lista de URLs fica no chat, não se manda pra mãe — não penaliza
    F.append(Finding(1, 4,
        'sem seção Fontes — obrigatória no levantamento macro (verificabilidade); use --terceiros se for pra terceiros/mini'))
    return 1


def s5_estrutura(text: str, F: List[Finding], is_mini: bool) -> int:
    """S5 · Estrutura & cobertura (ordem, sabores-assinatura, clusters)."""
    score = 0
    if is_mini:
        if ANCHOR_RE.search(text):
            score += 2
        else:
            F.append(Finding(1, 5, 'mini-plano sem âncora fixa clara no topo (compromisso + horário)'))
        if re.search(r'como chegar', text, re.I):
            score += 1
        else:
            F.append(Finding(2, 5, 'mini-plano sem "como chegar (da base)"'))
        if re.search(r'\d{1,2}[h:]\d{0,2}', text):
            score += 1  # faixas de horário
        return min(4, score)

    if re.search(r'^#{1,3}\s*resumo', text, re.I | re.M):
        score += 1
    else:
        F.append(Finding(2, 5, 'sem "Resumo" no topo (big picture antes do detalhe — princípio #4)'))
    m_map  = re.search(r'atra[çc][õo]es|mapeamento|esfor[çc]o', text, re.I)
    m_hist = re.search(r'hist[óo]ria|curiosidad', text, re.I)
    if m_map and m_hist and m_map.start() < m_hist.start():
        score += 1
    elif m_hist and not m_map:
        F.append(Finding(1, 5, 'história sem bloco de mapeamento antes (ordem fixa: mapeamento → história)'))
    else:
        score += 1
    if re.search(r'restaurante|onde comer|almo[çc]o|gastronomia', text, re.I):
        if SABOR_RE.search(text):
            score += 1
        else:
            F.append(Finding(2, 5, 'restaurantes sem sabor-assinatura/ingrediente local (mapping-rubric §sabores)'))
    else:
        score += 1  # sem seção de comida: N/A
    if re.search(r'cluster|combinar no mesmo dia|agrupa|núcleo geográfic', text, re.I):
        score += 1
    else:
        F.append(Finding(3, 5, 'sem clusters geográficos ("o que combinar no mesmo dia") — ponte pro roteiro'))
    # Régua única scout↔app (2026-07-12): tabela esforço×recompensa deve emitir a coluna
    # Recompensa ★ (vira valeAPena no app · mapping-rubric §2 eixos). Advisory (P2, não
    # muda score) pra não reprovar entregas anteriores ao padrão.
    if re.search(r'esfor[çc]o\s*×\s*recompensa', text, re.I) and '★' not in text:
        F.append(Finding(2, 5,
            'tabela esforço×recompensa sem coluna "Recompensa ★" — padrão 2026-07-12: '
            'scout emite os 2 eixos (★=valeAPena · esforço=risco) pro app consumir sem reavaliar'))
    return min(4, score)


def audit_scout(text: str, F: List[Finding], is_mini: bool, relax_fontes: bool) -> Dict[int, int]:
    return {
        1: s1_precos(text, F),
        2: s2_veredito(text, F, is_mini),
        3: s3_logistica_scout(text, F),
        4: s4_fontes(text, F, relax_fontes or is_mini),
        5: s5_estrutura(text, F, is_mini),
    }


def scout_band(total: int) -> Tuple[str, str]:
    if total >= 18:
        return 'Excelente', C.OK
    if total >= 14:
        return 'Bom', C.CYAN
    if total >= 10:
        return 'Aceitável', C.WARN
    return 'Ruim', C.ERR


def scout_approved(total: int, findings: List[Finding]) -> bool:
    return total >= 14 and not any(f.sev == 0 for f in findings)


SCOUT_CHECKLIST = """
┌──────────────────────────────────────────────────────────────────────────┐
│  CHECKLIST MANUAL · levantamento scout (julgamento humano)               │
├──────────────────────────────────────────────────────────────────────────┤
│  Perfil & Calibração                                                     │
│  [ ] veredito 🟢🟡🔴 calibrado ao PERFIL informado (não genérico)?      │
│  [ ] distâncias medidas a partir da BASE certa?                          │
│                                                                          │
│  Prosa (bloco História & Curiosidades)                                   │
│  [ ] gancho narrativo + factual (sem "paraíso indescritível")?          │
│  [ ] micro-história por atração (data, lenda, personagem)?              │
│                                                                          │
│  Honestidade                                                             │
│  [ ] turistada/superestimado dito sem diplomacia?                        │
│  [ ] sabores-assinatura reais (ingrediente endêmico), não genérico?     │
└──────────────────────────────────────────────────────────────────────────┘
"""


def print_report_scout(dim_scores: Dict[int, int], findings: List[Finding],
                       show_checklist: bool = True) -> None:
    total = sum(dim_scores.values())
    band, bcolor = scout_band(total)
    pcnts = {0: 0, 1: 0, 2: 0, 3: 0}
    for f in findings:
        pcnts[f.sev] += 1

    print(f"\n{C.BOLD}=== Dimensões do Levantamento ==={C.END}\n")
    for idx in sorted(dim_scores):
        s     = dim_scores[idx]
        bar   = '█' * s + '░' * (4 - s)
        color = C.OK if s >= 3 else (C.WARN if s >= 2 else C.ERR)
        print(f"  {color}{bar}{C.END} {s}/4  {SCOUT_DIM_NAMES[idx]}")

    grouped: Dict[int, List[Finding]] = {0: [], 1: [], 2: [], 3: []}
    for f in findings:
        grouped[f.sev].append(f)
    if any(grouped.values()):
        print(f"\n{C.BOLD}=== Achados ({len(findings)} total) ==={C.END}\n")
        for sev in [0, 1, 2, 3]:
            if not grouped[sev]:
                continue
            print(f"{SEV_COLOR[sev]}{SEV_LABEL[sev]} — {SEV_DESC[sev]}{C.END}")
            for f in grouped[sev]:
                stop_str = f' [{f.stop[:45]}]' if f.stop else ''
                print(f"  • {f.msg}{C.DIM}{stop_str}{C.END}")
            print()

    if show_checklist:
        print(SCOUT_CHECKLIST)

    print('─' * 62)
    ok_color = C.OK if scout_approved(total, findings) else C.ERR
    print(f"{C.BOLD}★ Levantamento: {ok_color}{total}/20{C.END}"
          f" · {bcolor}{band}{C.END}"
          f"  |  P0: {pcnts[0]}  P1: {pcnts[1]}  P2: {pcnts[2]}  P3: {pcnts[3]}")
    if scout_approved(total, findings):
        print(f"{C.OK}✓ Aprovado pra entrega{C.END}")
    elif pcnts[0] > 0:
        print(f"{C.ERR}✗ Bloqueado: {pcnts[0]} P0(s) — corrigir antes de continuar{C.END}")
    else:
        print(f"{C.WARN}⚠ Iterar: nota {total}/20 < 14 — corrigir P1s listados acima{C.END}")
    print()


def print_json_scout(dim_scores: Dict[int, int], findings: List[Finding]) -> None:
    total = sum(dim_scores.values())
    band, _ = scout_band(total)
    out = {
        'mode':       'scout',
        'score':      total,
        'max':        20,
        'band':       band,
        'approved':   scout_approved(total, findings),
        'dimensions': {SCOUT_DIM_NAMES[i]: s for i, s in sorted(dim_scores.items())},
        'findings': [
            {'sev': SEV_LABEL[f.sev], 'dim': SCOUT_DIM_NAMES.get(f.dim, str(f.dim)),
             'msg': f.msg, 'stop': f.stop}
            for f in findings
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def run_scout(path: Path, flags: List[str], json_out: bool, no_checklist: bool) -> None:
    if path.suffix != '.md':
        print(f"{C.ERR}✗{C.END} Modo --scout espera um .md da destination-scout (recebi '{path.suffix}')")
        sys.exit(2)
    text    = path.read_text(encoding='utf-8')
    is_mini = detect_mini_plano(text)
    relax   = '--terceiros' in flags
    kind    = 'mini-plano' if is_mini else 'levantamento macro'
    fontes  = 'Fontes opcional' if (relax or is_mini) else 'Fontes obrigatória'
    tflag   = '  (--terceiros)' if relax else ''

    findings: List[Finding] = []
    if not json_out:
        print(f"\n{C.BOLD}=== Auditando levantamento (scout): {path.name} ==={C.END}\n")
        print(f"{C.DIM}  modo: {kind} · {fontes}{tflag}{C.END}\n")
        print(f"{C.DIM}── Rodando 5 dimensões (scout) ──{C.END}")

    dim_scores = audit_scout(text, findings, is_mini, relax)

    if json_out:
        print_json_scout(dim_scores, findings)
    else:
        for idx in sorted(dim_scores):
            s     = dim_scores[idx]
            color = C.OK if s >= 3 else (C.WARN if s >= 2 else C.ERR)
            icon  = '✓' if s >= 3 else ('⚠' if s >= 2 else '✗')
            print(f"  {color}{icon}{C.END} {SCOUT_DIM_NAMES[idx]}: {s}/4")
        print_report_scout(dim_scores, findings, show_checklist=not no_checklist)

    total = sum(dim_scores.values())
    sys.exit(0 if scout_approved(total, findings) else 1)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> None:
    args  = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = [a for a in sys.argv[1:] if a.startswith('--')]
    check_links   = '--check-links'   in flags
    json_out      = '--json'          in flags
    no_checklist  = '--no-checklist'  in flags

    if not args:
        base = 'python3 skills/critico-roteiro/audit.py'
        print(f"{C.BOLD}Uso:{C.END}")
        print(f"  {base} <viagem>/data.json [--check-links] [--json]   # roteiro (/40)")
        print(f"  {base} <viagem>/index.html [--check-links]           # roteiro (fallback HTML)")
        print(f"  {base} entregas/<slug>.md --scout [--terceiros]      # levantamento scout (/20)")
        print()
        print("  --scout         Audita um .md da destination-scout (levantamento macro ou mini-plano)")
        print("  --terceiros     (com --scout) modo pra-terceiros: seção Fontes vira opcional")
        print("  --check-links   Verifica URLs em LINKS_MAP via HTTP HEAD (lento; ~5s/URL)")
        print("  --json          Saída JSON machine-readable além do relatório")
        print("  --no-checklist  Omite checklist manual (útil em CI)")
        sys.exit(2)

    path = Path(args[0])
    if not path.exists():
        print(f"{C.ERR}✗{C.END} Arquivo não existe: {path}")
        sys.exit(2)

    # Desvio pro modo scout (auditoria de levantamento .md · rubrica /20)
    if '--scout' in flags:
        run_scout(path, flags, json_out, no_checklist)
        return

    if not json_out:
        print(f"\n{C.BOLD}=== Auditando conteúdo: {path.name} ==={C.END}\n")

    try:
        data = load_data(path)
    except Exception as e:
        print(f"{C.ERR}✗{C.END} Erro ao carregar dados: {e}")
        sys.exit(2)

    findings: List[Finding] = []

    AUDITORS = [
        (1,  lambda: d1_storytelling(data, findings)),
        (2,  lambda: d2_profundidade(data, findings)),
        (3,  lambda: d3_logistica(data, findings)),
        (4,  lambda: d4_coords(data, findings)),
        (5,  lambda: d5_links(data, findings, check_links)),
        (6,  lambda: d6_adaptacao(data, findings)),
        (7,  lambda: d7_walking_tours(data, findings)),
        (8,  lambda: d8_honestidade(data, findings)),
        (9,  lambda: d9_cobertura(data, findings)),
        (10, lambda: d10_arco(data, findings)),
    ]

    if not json_out:
        n_days  = len(data.get('days', []))
        n_cards = len(get_cards(data))
        n_wt    = len(get_wt_parts(data))
        print(f"{C.DIM}  {n_days} dias · {n_cards} cards · {n_wt} partes de walking tour{C.END}\n")
        print(f"{C.DIM}── Rodando 10 dimensões ──{C.END}")

    dim_scores: Dict[int, int] = {}
    for dim_idx, auditor in AUDITORS:
        s = auditor()
        dim_scores[dim_idx] = s
        if not json_out:
            color = C.OK if s >= 3 else (C.WARN if s >= 2 else C.ERR)
            icon  = '✓' if s >= 3 else ('⚠' if s >= 2 else '✗')
            print(f"  {color}{icon}{C.END} {DIM_NAMES[dim_idx]}: {s}/4")

    if json_out:
        print_json_result(dim_scores, findings)
    else:
        print_report(dim_scores, findings, show_checklist=not no_checklist)

    total = sum(dim_scores.values())
    sys.exit(0 if is_approved(total, findings) else 1)


if __name__ == '__main__':
    main()
