#!/usr/bin/env python3
"""
audit.py — Crítico de conteúdo (skill critico-roteiro)

Linter de CONTEÚDO com camada de julgamento. Dois modos:

  • ROTEIRO (default): audita data.json / index.html · 10 dimensões · /40
  • SCOUT (--scout):   audita levantamento .md da destination-scout · 5 dim · /20

A nota tem DUAS metades, reportadas separadas porque têm confiabilidade diferente:
  • MECÂNICO  (dims D2·D3·D4·D5·D9): checagem verificável (campo presente, preço
    datado, coord 4-casas, link vivo, schema). O regex é autoridade — número confiável.
  • JULGAMENTO (dims D1·D6·D7·D8·D10 · marcadas ⚖️): o regex só flagra falha grosseira
    e dá um PISO; se a prosa encanta / o veredito está calibrado é o Claude que decide
    no checklist manual. NÃO trate o número dessas como veredito de qualidade.

Roda como gate no pipeline de roteiro E da destination-scout; também standalone.
No deploy (deploy.sh) roda com --deploy-gate: BLOQUEIA só em P0 (erro objetivo);
nota < aprovação vira aviso alto, não bloqueio (a régua de 32 é enforçada no LOOP da
sessão, não no push — heurística mole não deve brickar o acesso da família ao roteiro).

Uso:
    python3 skills/critico-roteiro/audit.py <viagem>/data.json
    python3 skills/critico-roteiro/audit.py <viagem>/data.json --check-links
    python3 skills/critico-roteiro/audit.py <viagem>/index.html
    python3 skills/critico-roteiro/audit.py <viagem>/index.html --deploy-gate   # usado no deploy.sh
    python3 skills/critico-roteiro/audit.py entregas/<slug>.md --scout [--terceiros]
    python3 skills/critico-roteiro/audit.py <arquivo> --json   # saída machine-readable

Exit: 0 = aprovado  ·  1 = não aprovado  ·  2 = erro de input
  roteiro: aprovado = nota≥32/40 E P0=0   ·   scout: aprovado = nota≥16/20 E P0=0
  --deploy-gate: exit≠0 só se P0>0 (ou VIAGEM_STRICT=1 e nota<aprovação)

Rubrica completa: references/content-rubric.md
Fonte de verdade do veredito/preço-datado/fontes (não forkar):
    skills/destination-scout/references/mapping-rubric.md
"""

import re
import os
import sys
import json
import urllib.request
import urllib.error
import unicodedata
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
    station: str = ''   # 🔧/🔎/✍️/🤔 · preenchido por assign_stations() (ver §ROTEAMENTO)
    hint: str = ''      # "o que bom parece" · nos 🔧 determinísticos, o patch colável

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

# Metade MECÂNICA (regex é autoridade · número confiável) vs metade de JULGAMENTO
# (regex é só piso · Claude confirma no checklist · marcada ⚖️). Ver docstring.
MECHANICAL_DIMS = {2, 3, 4, 5, 9}
JUDGMENT_DIMS   = {1, 6, 7, 8, 10}

def dim_label(idx: int) -> str:
    mark = ' ⚖️' if idx in JUDGMENT_DIMS else ''
    return DIM_NAMES[idx] + mark

# ---------------------------------------------------------------------------
# ROTEAMENTO · grader → router
# ---------------------------------------------------------------------------
# O audit diagnostica; sem roteamento ele para aí. Cada achado é despachado pra
# UMA estação de conserto. A taxonomia HERDA o split mecânico/julgamento — não
# inventa outro eixo:
#
#   MECHANICAL_DIMS → 🔧 corrigir (determinístico) · 🔎 pesquisar (falta um fato)
#   JUDGMENT_DIMS   → ✍️ reescrever (falta escrita)  · 🤔 você decide (julgamento)
#
# ⚠️ GUARDA ANTI-GOODHART — a regra que governa os hints:
# "subir a nota" só é alvo legítimo na metade MECÂNICA, onde o regex é autoridade.
# Perseguir o número das dims ⚖️ otimiza o proxy (inflar `sobre` até 150 chars,
# salpicar ano de 4 dígitos) e a nota sobe sem o roteiro melhorar. Por isso nenhum
# hint de dim ⚖️ manda "faça X pra subir a nota" — manda o que a PROSA precisa ter.
# Quem valida a metade ⚖️ é o checklist manual, nunca o número.

ST_FIX      = '🔧'   # determinístico — o hint traz o patch pronto pra colar
ST_RESEARCH = '🔎'   # falta um fato externo (preço, coord, URL, história)
ST_REWRITE  = '✍️'   # o fato existe, falta a escrita (padrão Marais)
ST_HUMAN    = '🤔'   # julgamento do Tobia — o script sinaliza, não decide

STATION_DESC = {
    ST_FIX:      'Corrigir · determinístico (patch pronto no hint)',
    ST_RESEARCH: 'Pesquisar · falta fato externo',
    ST_REWRITE:  'Reescrever · padrão Marais',
    ST_HUMAN:    'Você decide · julgamento (nunca vira patch)',
}

# (regex na msg, estação, hint). Primeira que casar vence; sem match cai no default
# da metade. Roteia POR MENSAGEM em vez de tocar os ~60 call-sites de F.append() —
# mantém os auditores intactos e a tabela de roteamento legível num lugar só.
ROUTING = [
    # --- 🔧 determinístico (conserto não precisa de fato novo) ---------------
    (r'distância vaga|perto/próximo', ST_FIX,
     'trocar por distância medida — ex: "banheiro a 300m", "a 1,2 km da base"'),
    (r'endereço entre parens|parens', ST_FIX,
     'nome: "Nome do Lugar (Rua Tal 123)" — o parêntese é o que faz o Maps acertar'),
    (r'esperado 2-4|sem preco ou dist', ST_FIX,
     '"opcoes": [{"nome":"…","desc":"…","preco":"$$","dist":"5 min a pé"}] · 2-4 itens'),
    (r'dia sem tema', ST_FIX, '"tema": "<Bairro> · <o que define o dia>"'),
    (r'paternalista', ST_FIX,
     'remover o aviso — Tobia mora em Paris (princípio #2: não patronizar metrô)'),
    (r'dicas numeradas|numeração', ST_FIX,
     'numerar as dicas 1️⃣2️⃣3️⃣ (ou Ⓐ Ⓑ Ⓒ) pra casar com os pinos do mapa'),
    (r'markdown', ST_FIX,
     'trocar **bold** por <strong>bold</strong> — o template não converte markdown'),

    # --- 🤔 julgamento do Tobia (NUNCA vira patch automático) ----------------
    (r'pesadas|ritmo família|corrido pra esse público', ST_HUMAN,
     'ALERTA, não corte: o peso do dia depende do público e da dinâmica. Você decide'),
    (r'ordem temporal', ST_HUMAN,
     'reordenar é decisão de plano do dia — confira se a sequência faz sentido no chão'),
    (r'green|pula sem culpa|crítica rara', ST_HUMAN,
     'algum stop aqui é fraco de verdade? se for, diga na prosa ("pula sem culpa")'),

    # --- 🔎 falta fato externo ----------------------------------------------
    (r'sem data|datad|mês/ano', ST_RESEARCH,
     'web_search do preço atual → gravar com "(mês/ano)". Sem data, o preço apodrece'),
    (r'TRANSIT_MAP', ST_RESEARCH,
     'pesquisar a rota real (linha, tempo, preço) → entrada no transit_map'),
    (r'casas decimais|coord', ST_RESEARCH,
     'web_search da coord (4 casas). Não confirmou → coord_unverified: true, NUNCA chute'),
    (r'LINKS_MAP|link|HTTP|4xx|404', ST_RESEARCH,
     'web_search do site oficial → confirmar 2xx ANTES de gravar. Morto: remover'),
    (r'acessibilidade', ST_RESEARCH,
     'pesquisar o acesso real (degraus? elevador? carrinho passa?) — detalhe concreto'),
    (r'duracao ausente|custo ausente', ST_RESEARCH,
     'valor real → duracao como range ("45min-1h"); custo real ou "Gratuito"'),
    (r'sem fato', ST_RESEARCH,
     'pesquisar a história (fundação, personagem, lenda) — é o insumo do `sobre`'),

    # --- ✍️ o fato existe, falta a escrita ----------------------------------
    (r'imperdivel genérico|hipérbole|hype', ST_REWRITE,
     'imperdivel = O QUE OBSERVAR (o detalhe que o distraído perde), não adjetivo'),
    (r'sobre médio|padrão-ouro ≥150|raso', ST_REWRITE,
     'contar a história (data/personagem/lenda). NÃO encher linguiça pra bater char count'),
]

SEV_WEIGHT = {0: 100, 1: 3, 2: 2, 3: 1}   # P0 domina a fila; resto conforme severidade


def route_finding(f: Finding) -> Tuple[str, str]:
    for pat, st, hint in ROUTING:
        if re.search(pat, f.msg, re.I):
            return st, hint
    if f.dim in MECHANICAL_DIMS:
        return ST_RESEARCH, 'gap objetivo — buscar o dado que falta e gravar com fonte'
    return ST_REWRITE, 'confirme no checklist ⚖️ e ajuste a PROSA (o número não é o alvo)'


def assign_stations(findings: List[Finding]) -> None:
    """Despacha cada achado pra sua estação. Idempotente."""
    for f in findings:
        if not f.station:
            f.station, f.hint = route_finding(f)


def is_heavy_card(s: Dict) -> bool:
    """Card 'pesado' = âncora do dia (vs filler). UMA definição, dois usos: o alerta
    de ritmo (D6) e o peso na priorização de conserto."""
    if s.get('tipo') != 'card':
        return False
    if s.get('risco') in ('yellow', 'red'):
        return True
    if s.get('walkingTours'):
        return True
    return bool(re.search(r'\d+\s*h', s.get('duracao', '')))


def build_stop_index(data: Dict) -> Dict[str, Dict]:
    """nome do stop → {dia, peso}. Peso = âncora(2) vs filler(1)."""
    idx: Dict[str, Dict] = {}
    for day in data.get('days', []):
        for s in day.get('stops', []):
            nome = s.get('nome', '')
            if nome:
                idx[nome] = {'dia': day.get('date', ''),
                             'peso': 2 if is_heavy_card(s) else 1}
    return idx

# ---------------------------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------------------------

class _RawFloat(float):
    """Float que lembra o texto original do JSON. Bug ago/2026 (MEMORY): coord_4dec
    usava str() e lia 41.8440 como 3 casas — o round-trip por float perde o zero à
    direita. Guardar o texto bruto resolve sem mudar nenhuma aritmética (é float)."""
    def __new__(cls, s):
        obj = super().__new__(cls, s)
        obj.raw = s
        return obj


def load_from_json(path: Path) -> Dict:
    with open(path, encoding='utf-8') as f:
        return json.load(f, parse_float=_RawFloat)

def extract_from_html(content: str) -> Dict:
    result: Dict = {}

    def try_extract(pattern, fallback):
        m = re.search(pattern, content, re.DOTALL)
        if not m:
            return fallback
        try:
            return json.loads(m.group(1), parse_float=_RawFloat)
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
        # Usa o texto bruto do JSON quando disponível (_RawFloat) — "41.8440" tem
        # 4 casas mesmo que str(float) devolva "41.844".
        s = getattr(v, 'raw', str(v))
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

        # P0 · card tipo=card completamente vazio (sem sobre + sem imperdivel + sem dicas)
        # — não é "raso", é lixo estrutural: BLOQUEIA deploy (content-rubric §severidade)
        if (not c.get('sobre') and not c.get('imperdivel')
                and not c.get('dicas')):
            F.append(Finding(0, 2,
                'card tipo=card VAZIO (sem sobre + imperdivel + dicas) — sem valor pro viajante',
                stop=name))

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

    # coord_unverified = P1 forte (não P0): desconta ponto e aparece alto, mas NÃO
    # bloqueia deploy — miradouro/vista é aproximado por natureza e a flag é honesta.
    # Resolver: web_search e confirmar, OU remover a flag conscientemente. Quem quer
    # barra máxima usa VIAGEM_STRICT=1 no deploy (bloqueia qualquer nota < aprovação).
    unverified = [s.get('nome', '') for s, _ in all_stops_list
                  if s.get('coord_unverified') is True]
    if not unverified:
        score += 1
    else:
        for name in unverified[:3]:
            F.append(Finding(1, 4, 'coord coord_unverified:true — validar com web_search ou remover a flag conscientemente', stop=name))

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
        # rastreia quais URLs são 'official' — link oficial morto é P0 (engana mais
        # que ausência); review/outro morto é P1.
        official_urls = {l['url'] for links in lmap.values() for l in links
                         if l.get('url') and l.get('type') == 'official'}
        all_urls = [l['url'] for links in lmap.values() for l in links if l.get('url')]
        print(f"  {C.DIM}Checando {len(all_urls)} URLs via HTTP HEAD...{C.END}")
        broken = []  # (url, reason, is_official)
        for url in all_urls:
            try:
                req = urllib.request.Request(
                    url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    if resp.status >= 400:
                        broken.append((url, f'HTTP {resp.status}', url in official_urls))
            except urllib.error.HTTPError as e:
                if e.code >= 400:
                    broken.append((url, f'HTTP {e.code}', url in official_urls))
            except Exception as e:
                broken.append((url, f'err: {str(e)[:60]}', url in official_urls))

        if not broken:
            score += 2
        else:
            if len(broken) <= 2:
                score += 1
            for url, reason, is_off in broken[:6]:
                sev = 0 if is_off else 1
                tag = ' [OFICIAL]' if is_off else ''
                F.append(Finding(sev, 5,
                    f'link quebrado{tag}: {url} ({reason}) — remover do LINKS_MAP'))
            if len(broken) > 6:
                F.append(Finding(1, 5, f'... +{len(broken)-6} URLs com problema'))
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

    # Dia de chegada/saída ≤ 3 cards. Bug ago/2026: um `break` incondicional fazia o
    # loop examinar SÓ o primeiro dia — o último dia (partida) nunca era olhado e o
    # `else` dava +1 grátis. Agora os DOIS dias são examinados; o ponto só vem se
    # nenhum dos dois estiver pesado.
    if days:
        borda = [days[0]] + ([days[-1]] if len(days) > 1 else [])
        pesados = []
        for day in borda:
            note  = (day.get('nota', '') + day.get('tema', '')).lower()
            is_travel = any(w in note for w in ['chegada', 'partida', 'saída', 'voo', 'pouso'])
            n_cards   = sum(1 for s in day.get('stops', []) if s.get('tipo') == 'card')
            if is_travel and n_cards > 3:
                pesados.append((day.get('date', ''), n_cards))
        if pesados:
            for date, n in pesados:
                F.append(Finding(2, 6,
                    f'dia de viagem ({date}) tem {n} cards — pesado pra dia chegada/saída'))
        else:
            score += 1

    # Pacing advisory · NÃO pontua · NÃO bloqueia — só alerta pra Tobia decidir.
    # Especialistas em viagem c/ criança pequena: 1-2 atividades "pesadas"/dia,
    # ancoradas na janela da criança. Aqui é SINAL, não corte automático: o peso
    # do dia depende do público e da dinâmica familiar — quem decide é o Tobia.
    for day in days:
        heavy_n = sum(1 for s in day.get('stops', []) if is_heavy_card(s))
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


# Padrões que marcam AFIRMAÇÃO A PROVAR — não cor de prosa. HONESTIDADE SOBRE O ALCANCE
# (auditoria 2026-08-08): dos 4 erros de campo de ago/2026, o regex pega DOIS — "operador
# único" (via "únic[oa]") e "séc. XVI" (via DATA_HIST_RE). Os outros dois FICAM DE FORA
# por decisão: "ponto mais ao sul" é POSIÇÃO relativa ("mais ao/à" não está na lista de
# adjetivos) e "mirante" é FUNÇÃO de lugar — cobrir função/posição por regex geraria mar
# de falso positivo sem provar nada (relatório da auditoria §3: invenção fluente satisfaz
# qualquer padrão de texto). Essas duas classes são responsabilidade do FACTCHECK.md
# (verificação contra o mundo, não contra o texto).
SUPERLATIVO_RE = re.compile(
    r'\b(?:'
    # com ou SEM artigo — "Maior lagoa salobra da Sardenha" e "maior população
    # europeia" abriam frase sem artigo e escapavam da versão anterior. Foi
    # exatamente assim que "maior população europeia de flamingos" (falso: é
    # Molentargius, a ~100km) sobreviveu ao gate.
    r'maior(?:es)?|menor(?:es)?|melhor(?:es)?|pior(?:es)?|[uú]nic[oa]s?'
    r'|primeir[oa]s?|[uú]ltim[oa]s?'
    r'|mais\s+(?:antig|alt|nov|larg|long|profund|important|preserv|visit|bonit|barat|car)\w*'
    r'|somente\s+(?:um|uma)|apenas\s+(?:um|uma)|the\s+only'
    r')\b', re.I)

# Data histórica ou século. Deliberadamente ESTREITO pra não afogar o gate em ruído:
#  · século em romano ("séc. XIII")
#  · ano com era explícita ("VIII a.C.", "1º d.C.")
#  · ano de 3-4 dígitos ATÉ 2019 — de 2020 em diante é carimbo de referência
#    "(ago/2026)", não afirmação histórica.
DATA_HIST_RE = re.compile(
    r'\b(?:s[ée]c(?:ulo)?\.?\s*[IVXLCM]+'
    r'|\d{1,4}\s*(?:a\.?\s?C\.?|d\.?\s?C\.?)'
    r'|1[0-9]{3}|20[01][0-9])\b')


def _strip_html(t: str) -> str:
    return re.sub(r'<[^>]+>', ' ', t or '')


def _claims_sem_fonte(texto: str) -> List[str]:
    """Devolve os trechos que são afirmação a provar. Vazio = nada a cobrar."""
    t = _strip_html(texto)
    achados = []
    for m in SUPERLATIVO_RE.finditer(t):
        achados.append(t[max(0, m.start()-30):m.end()+40].strip())
    for m in DATA_HIST_RE.finditer(t):
        achados.append(t[max(0, m.start()-30):m.end()+40].strip())
    return achados


# ---------------------------------------------------------------------------
# DÍVIDA DE PROVENIÊNCIA · baseline (padrão lint clássico)
# ---------------------------------------------------------------------------
# A REGRA ZERO entrou em ago/2026 com dois roteiros JÁ EM USO em campo. Aplicá-la
# retroativamente bloquearia o deploy dos dois — e com isso a correção urgente que
# chega do próprio campo, que é justamente o mecanismo que descobre os furos.
#
# Solução: item sem proveniência que JÁ EXISTIA quando a regra entrou vira DÍVIDA
# REGISTRADA (P2, visível, contada). Qualquer item NOVO ou ALTERADO é P0/P1 cheio.
#
# A dívida só encolhe: `--baseline` recusa crescer o arquivo (ver main()). Item que
# some do roteiro some da dívida — o audit avisa quando há entrada morta.
#
# Arquivo: <viagem>/.proveniencia-debt.json  ·  {"itens": ["card:Nome", "historia:Título", ...]}

def _debt_path(src: Optional[str]) -> Optional[Path]:
    if not src:
        return None
    return Path(src).parent / '.proveniencia-debt.json'


def load_debt(src: Optional[str]) -> set:
    p = _debt_path(src)
    if not p or not p.exists():
        return set()
    try:
        return set(json.loads(p.read_text(encoding='utf-8')).get('itens', []))
    except Exception:
        return set()

# ---------------------------------------------------------------------------
# PROVENIÊNCIA · nasceu do "Loggia · mirador sul" (ago/2026)
# ---------------------------------------------------------------------------
# Um card descrevia um mirante que NÃO EXISTE, com prosa detalhada sobre o calcário
# mudando de cor. Nome real de Bonifacio ("loggia" é o pórtico da Sainte-Marie-Majeure),
# função inventada. Passou por validate, audit E factcheck — e estava numa PARADA DE
# WALKING TOUR, ou seja, virou rota que dois avós iam seguir no Maps.
#
# A lição não é "pesquise mais": é que texto vindo de fonte e texto vindo de memória
# saíam com a mesma cara. Sem marca de proveniência, ninguém — nem o autor na revisão
# seguinte — distingue os dois. Por isso isto é MECÂNICO, não conselho:
#
#   · parada de walking tour sem `mapsQuery`   → P0 (validate já bloqueia; aqui reforça)
#   · card ⭐⭐⭐ sem `fontes` nem `links_map`   → P0: é o que a família vai priorizar
#   · card ⭐⭐ sem proveniência                → P1
#
# `fontes` = [{"o": "Office de Tourisme de Bonifacio", "u": "https://..."}]

# ---------------------------------------------------------------------------
# CLAIMS COBERTOS · a fonte tem que sustentar A FRASE, não só existir
# ---------------------------------------------------------------------------
# Erro de 2026-08-04 (pego pelo Tobia): o card do Stagno di Càbras recebeu uma URL
# do SardegnaTurismo e continuou dizendo "maior população europeia de flamingos"
# (é Molentargius, a ~100km) e vendendo agosto como temporada (o pico é outono).
# Anexar `fontes` passou no gate; a afirmação seguiu falsa.
#
# Diagnóstico: `fontes` no nível do CARD é grosso demais. Premia o campo presente,
# não a verdade. Goodhart — e a nota subiu enquanto o conteúdo continuava errado.
#
# Correção: cada afirmação verificável tem que ser NOMEADA na fonte que a prova:
#   "fontes": [{"o": "SardegnaTurismo", "u": "https://...",
#               "prova": ["22 km²", "outono à primavera"]}]
# O audit extrai as afirmações da prosa e cobra que cada uma apareça em algum
# `prova`. Não é possível provar verdade por regex — o que isto garante é que
# nenhuma afirmação fica SEM ALGUÉM TER DITO onde a checou.

SAZONAL_RE = re.compile(
    r'\b(?:jan(?:eiro)?|fev(?:ereiro)?|mar[çc]o|abr(?:il)?|maio|junho|julho|agosto|set(?:embro)?'
    r'|out(?:ubro)?|nov(?:embro)?|dez(?:embro)?|ver[ãa]o|inverno|outono|primavera'
    r'|o\s+ano\s+todo|temporada|alta\s+esta[çc][ãa]o|baixa\s+esta[çc][ãa]o)\b', re.I)

# Número COM unidade — preço, medida, contagem, horário. É a classe que mais apodrece.
NUMERO_RE = re.compile(
    r'\b\d[\d.,]*\s*(?:km²|km2|km|m²|m2|ha|metros?|m\b|€|euros?|h\b|h\d{2}|min|'
    r'casais|degraus|habitantes|s[ée]culos?|anos?)', re.I)

def _norm(t: str) -> str:
    t = unicodedata.normalize('NFD', (t or '').lower())
    t = ''.join(ch for ch in t if unicodedata.category(ch) != 'Mn')
    return re.sub(r'\s+', ' ', t)

def _claims_estruturados(texto: str) -> List[Tuple[str, str]]:
    """[(tipo, trecho_chave)] · o trecho é o que precisa aparecer em algum `prova`."""
    t = _strip_html(texto)
    out, vistos = [], set()
    for tipo, rx in (('superlativo', SUPERLATIVO_RE), ('data', DATA_HIST_RE),
                     ('número', NUMERO_RE), ('época', SAZONAL_RE)):
        for mm in rx.finditer(t):
            chave = mm.group(0).strip()
            k = (tipo, _norm(chave))
            if k in vistos:
                continue
            vistos.add(k)
            out.append((tipo, chave))
    return out

def _provas(obj) -> List[str]:
    ps = []
    for f in (obj.get('fontes') or []):
        pv = f.get('prova')
        if isinstance(pv, str):
            ps.append(pv)
        elif isinstance(pv, list):
            ps.extend(str(x) for x in pv)
    return [_norm(p) for p in ps]

def check_claims_cobertos(data: Dict, F: List[Finding], debt: Optional[set] = None) -> List[str]:
    """Cobra claim-a-claim nos cards que o viajante age em cima (⭐⭐ e ⭐⭐⭐)."""
    debt = debt or set()
    pendentes: List[str] = []
    for c in get_cards(data):
        if c.get('tipo') != 'card':
            continue
        va = c.get('valeAPena')
        if va not in (2, 3):
            continue
        texto = ' '.join([c.get('cat', ''), c.get('sobre', ''), c.get('imperdivel', '')]
                         + list(c.get('dicas', [])))
        claims = _claims_estruturados(texto)
        if not claims:
            continue
        provas = _provas(c)
        desc = [f'{tipo}: "{ch}"' for tipo, ch in claims
                if not any(_norm(ch) in p for p in provas)]
        if not desc:
            continue
        nome = c.get('nome', '(sem nome)')
        chave = f'claimcov:{nome}'
        pendentes.append(chave)
        na_divida = chave in debt
        sev = 2 if na_divida else (0 if va == 3 else 1)
        F.append(Finding(sev, 5,
            f'{len(desc)} afirmação(ões) do card SEM fonte nomeada que as sustente — '
            f'ex: {" · ".join(desc[:3])}' + (' [dívida registrada]' if na_divida else ''),
            stop=nome, station='🔎',
            hint='cada afirmação entra em `prova`: '
                 '"fontes":[{"o":"<fonte>","u":"...","prova":["22 km²","outono à primavera"]}]'))
    return pendentes


# ---------------------------------------------------------------------------
# SCHEMA DE `fontes` · unificado em 2026-08-09 (Lote 3 da auditoria · R9 lite)
# ---------------------------------------------------------------------------
# Havia 3 formatos divergentes documentados (source-credibility.md · data-schema.md ·
# o formato real {o,u,prova}). Unificado: {o, u, tier, data, prova[]} com
# tier ∈ {oficial, editorial, campo, diretorio, crowd}. tier+data existem porque a
# auditoria mostrou que fonte SEO-farm satisfazia tem_fonte() — sem tier, o gate não
# tem como nem AVISAR que a fonte é lixo. AVISA (P3), nunca bloqueia: dados antigos
# seguem válidos; a régua vale pra item novo/alterado.

FONTE_TIERS = {'oficial', 'editorial', 'campo', 'diretorio', 'crowd'}

def check_fontes_schema(data: Dict, F: List[Finding]) -> None:
    sem: List[str] = []

    def olha(nome, obj):
        for f in (obj.get('fontes') or []):
            if not isinstance(f, dict):
                continue
            if f.get('tier') not in FONTE_TIERS or not f.get('data'):
                sem.append(nome or '(sem nome)')
                return

    for c in get_cards(data):
        olha(c.get('nome', ''), c)
    for day in data.get('days', []) or []:
        for st in day.get('stops', []) or []:
            for o in st.get('opcoes', []) or []:
                olha(o.get('nome', ''), o)
    for h in data.get('historia', []) or []:
        olha(h.get('titulo', ''), h)
    for e in data.get('extras', []) or []:
        olha(e.get('nome', ''), e)

    if sem:
        F.append(Finding(3, 5,
            f'{len(sem)} item(ns) com `fontes` sem tier/data no schema unificado '
            f'{{o, u, tier, data, prova[]}} · tier ∈ oficial/editorial/campo/diretorio/crowd '
            f'— ex: {" · ".join(sem[:3])}',
            station='🔧',
            hint='"fontes": [{"o": "<órgão>", "u": "https://...", "tier": "oficial", '
                 '"data": "2026-08"}] — régua: references/source-credibility.md'))


def check_proveniencia(data: Dict, F: List[Finding], debt: Optional[set] = None) -> List[str]:
    debt = debt or set()
    # TODO item sem proveniência HOJE — em dívida ou não. É isto que o --baseline grava,
    # pra que a dívida ENCOLHA quando um item ganha fonte. (Bug ago/2026: gravava a união
    # com a dívida antiga, então ela nunca diminuía.)
    sem_fonte_hoje: List[str] = []

    def sev(chave: str, cheia: int) -> int:
        """P0/P1 pra item novo · P2 'dívida registrada' pro que já existia."""
        sem_fonte_hoje.append(chave)
        return 2 if chave in debt else cheia

    def marca(chave: str) -> str:
        return ' [dívida registrada]' if chave in debt else ''

    cards = get_cards(data)
    links_map = data.get('links_map', {}) or {}

    def tem_fonte(c) -> bool:
        if c.get('fontes'):
            return True
        return bool(links_map.get(c.get('nome', '')))

    def isento(c) -> bool:
        """Card de pura logística não afirma nada sobre o mundo — não há fonte a citar.
        Critério: `noMaps: true` (semântica já existente = "não é lugar nenhum": check-in,
        café da manhã, despedida, fim da viagem) E zero afirmação a provar no texto.
        Se tiver superlativo ou data, deixa de ser logística e volta a precisar de fonte."""
        if not c.get('noMaps'):
            return False
        texto = ' '.join([c.get('sobre', ''), c.get('imperdivel', '')] + list(c.get('dicas', [])))
        return not _claims_sem_fonte(texto)

    sem_fonte_3, sem_fonte_2 = [], []
    for c in cards:
        if c.get('tipo') != 'card':
            continue
        if isento(c):
            continue
        va = c.get('valeAPena')
        if va == 3 and not tem_fonte(c):
            sem_fonte_3.append(c.get('nome', '(sem nome)'))
        elif va == 2 and not tem_fonte(c):
            sem_fonte_2.append(c.get('nome', '(sem nome)'))

    for nome in sem_fonte_3:
        k = f'card:{nome}'
        F.append(Finding(sev(k, 0), 5,
            'card ⭐⭐⭐ SEM PROVENIÊNCIA (nem `fontes` nem entrada em links_map) — '
            'recomendação de topo tem que dizer de onde veio' + marca(k),
            stop=nome, station='🔎',
            hint='"fontes": [{"o": "<órgão oficial/guia T1>", "u": "https://..."}]'))
    for nome in sem_fonte_2[:5]:
        k = f'card:{nome}'
        F.append(Finding(sev(k, 1), 5,
            'card ⭐⭐ sem proveniência registrada (`fontes` ou links_map)' + marca(k),
            stop=nome, station='🔎',
            hint='"fontes": [{"o": "<fonte>", "u": "https://..."}]'))
    if len(sem_fonte_2) > 5:
        F.append(Finding(1, 5,
            f'+{len(sem_fonte_2)-5} outros cards ⭐⭐ sem proveniência'))

    # Paradas de walking tour: viram ROTA que alguém segue a pé. Sem query de Maps,
    # a parada pode nem existir e ninguém descobre até estar na rua.
    for card_nome, wt in get_wt_parts(data):
        for st in wt.get('stops', []):
            if not st.get('mapsQuery'):
                # parada de WT NUNCA entra em dívida: é rota física, o dano é imediato
                F.append(Finding(0, 7,
                    f'parada de WT "{st.get("nome","?")}" SEM mapsQuery — '
                    'a parada vira rota a pé; sem query não dá pra provar que o lugar existe',
                    stop=card_nome, station='🔎',
                    hint='"mapsQuery": "<nome buscável e inequívoco do lugar>"'))

    # ── HISTÓRIA & CURIOSIDADES ──────────────────────────────────────────────
    # A superfície mais narrativa do app: milhares de chars de afirmação histórica,
    # sem preço nem horário pra parecerem suspeitos. É onde invenção passa mais fácil,
    # porque nada ali tem cara de dado. Por isso proveniência aqui é P0.
    for h in (data.get('historia') or []):
        titulo = h.get('titulo', '(polo sem título)')
        if not h.get('fontes'):
            k = f'historia:{titulo}'
            F.append(Finding(sev(k, 0), 1,
                f'polo de História "{titulo}" SEM `fontes` — '
                f'{len(_strip_html(h.get("prosa_html","")))} chars de afirmação histórica sem proveniência',
                stop=titulo, station='🔎',
                hint='"fontes": [{"o": "<órgão/museu/guia T1>", "u": "https://..."}]'))

    # ── ITENS DE `opcoes` (restaurantes, bares, cafés) ───────────────────────
    # Caso Le Lido (ago/2026): estabelecimento descrito na cidade errada, com confiança.
    # Recomendação de negócio tem o mesmo peso de um card.
    op3, op2 = [], []
    for day in data.get('days', []):
        for st in day.get('stops', []):
            for o in st.get('opcoes', []) or []:
                tem = bool(o.get('fontes')) or bool(links_map.get(o.get('nome', '')))
                # "Jantar em casa", "picnic do mercado": não é estabelecimento, não há
                # fonte a citar. Mesmo critério dos cards de logística: noMaps + zero claim.
                if tem or (o.get('noMaps') and not _claims_sem_fonte(
                        f"{o.get('nome','')} {o.get('desc','')}")):
                    continue
                alvo = op3 if o.get('valeAPena') == 3 else (op2 if o.get('valeAPena') == 2 else None)
                if alvo is not None:
                    alvo.append((o.get('nome', '?'), st.get('nome', '')))
                    if o.get('valeAPena') in (2, 3):
                        sev(f'opcao:{o.get("nome","?")}', 0)  # registra pro baseline
    for nome, ctx in op3[:6]:
        k = f'opcao:{nome}'
        F.append(Finding(sev(k, 0), 5,
            f'opção ⭐⭐⭐ "{nome}" SEM proveniência — recomendação de estabelecimento '
            'precisa de fonte que confirme nome E localização (caso Le Lido)',
            stop=ctx, station='🔎', hint='"fontes": [{"o": "<guia/site oficial>", "u": "https://..."}]'))
    # Sumário: só conta o que NÃO está em dívida — senão o rollup ressuscita como P0
    # tudo que o baseline acabou de congelar.
    resto3 = [n for n, _ in op3[6:] if f'opcao:{n}' not in debt]
    if resto3:
        F.append(Finding(0, 5, f'+{len(resto3)} outras opções ⭐⭐⭐ sem proveniência'))
    resto2 = [n for n, _ in op2 if f'opcao:{n}' not in debt]
    if resto2:
        F.append(Finding(1, 5, f'{len(resto2)} opções ⭐⭐ sem proveniência registrada'))
    em_divida = len(op3) + len(op2) - len(resto3) - len(resto2)
    if em_divida:
        F.append(Finding(2, 5, f'{em_divida} opções sem proveniência [dívida registrada]'))

    # ── EXTRAS ──────────────────────────────────────────────────────────────
    for e in (data.get('extras') or []):
        if e.get('valeAPena', 0) >= 2 and not (e.get('fontes') or links_map.get(e.get('nome', ''))):
            F.append(Finding(1, 5, f'extra "{e.get("nome","?")}" sem proveniência', station='🔎'))

    # ── AFIRMAÇÃO A PROVAR sem fonte (superlativo · data histórica) ──────────
    # Generaliza os 4 erros de campo de ago/2026. Superlativo e data são as duas
    # categorias que mais apodrecem e que guia turístico mais repete sem checar.
    for c in cards:
        if c.get('tipo') != 'card' or tem_fonte(c) or isento(c):
            continue
        texto = ' '.join([c.get('sobre', ''), c.get('imperdivel', '')] + list(c.get('dicas', [])))
        cl = _claims_sem_fonte(texto)
        if cl:
            k = f'claims:{c.get("nome","")}'
            F.append(Finding(sev(k, 1), 5,
                f'{len(cl)} afirmação(ões) a PROVAR sem fonte (superlativo/data) — '
                f'ex: "{cl[0][:70]}…"' + marca(k),
                stop=c.get('nome', ''), station='🔎',
                hint='ou registra `fontes`, ou reescreve sem a afirmação — nunca deixa como cor de prosa'))

    # Devolvido pro --baseline: SÓ o que ainda está sem proveniência (a dívida encolhe).
    return sorted(set(sem_fonte_hoje))


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
    """D9 · Cobertura & Schema (completude de conteúdo · o structural fica no validate.py)

    NÃO re-checa temaCurto/enums/coord-range: isso é dono do validate.py (uma fonte
    de verdade pro estrutural). D9 cuida do que é conteúdo: dia sem card, opcoes bem
    formadas, nota do dia."""
    days  = data.get('days', [])
    score = 0

    # Todos dias com ≥1 card (vale 2 pts — é o sinal de cobertura mais forte)
    ARRIVAL_RE = re.compile(r'chegada|saída|voo|partida|regresso|volta', re.I)
    no_card_days = [(d.get('date', ''), d.get('tema', '')) for d in days
                    if not any(s.get('tipo') == 'card' for s in d.get('stops', []))]
    if not no_card_days:
        score += 2
    else:
        for date, tema in no_card_days[:2]:
            sev = 2 if ARRIVAL_RE.search(tema) else 1
            F.append(Finding(sev, 9, f'dia sem nenhum stop tipo=card: {date}'))

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

APPROVAL_MIN = 32  # régua elevada 28→32 (Tobia 2026-07-01): 28 carimbava roteiros
                   # com 3-8 P1s não corrigidos. Aspira-se 36+ (Excelente).

def score_band(total: int) -> Tuple[str, str]:
    if total >= 36:
        return 'Excelente', C.OK
    if total >= 32:
        return 'Bom', C.CYAN
    if total >= 28:
        return 'Aceitável', C.WARN
    return 'Ruim', C.ERR

def is_approved(total: int, findings: List[Finding]) -> bool:
    return total >= APPROVAL_MIN and not any(f.sev == 0 for f in findings)

def split_scores(dim_scores: Dict[int, int]) -> Tuple[int, int]:
    """Retorna (mecânico, julgamento) — as duas metades da nota /40."""
    mech = sum(s for i, s in dim_scores.items() if i in MECHANICAL_DIMS)
    judg = sum(s for i, s in dim_scores.items() if i in JUDGMENT_DIMS)
    return mech, judg

# ---------------------------------------------------------------------------
# LOOP FECHADO · --diff (re-audita antes/depois de um lote de patch)
# ---------------------------------------------------------------------------
# Toda fase (patch da A, pesquisa da C, reescrita da D) fecha o loop aqui:
# aplica o lote → roda `audit.py depois.json --diff antes.json` → o modo mostra
# o que resolveu, o que apareceu de novo, e ASSERE que o mecânico não regrediu.
# Regra dura: a metade MECÂNICA nunca pode cair — lá o número é verdade, então
# queda = o patch quebrou algo objetivo. A metade ⚖️ pode oscilar (é proxy), mas
# a gente MOSTRA a oscilação em vez de esconder no agregado — é o modo de falha
# clássico (mecânico +3 mascarando julgamento −1, total "saudável", roteiro pior).

def audit_roteiro(data: Dict, check_links: bool = False,
                  debt: Optional[set] = None) -> Tuple[Dict[int, int], List[Finding], List[str]]:
    """Roda as 10 dimensões + checks transversais e devolve
    (dim_scores, findings já roteados, pendentes de proveniência).
    ÚNICA FONTE DE VERDADE da lista de auditores — main() e --diff chamam aqui.
    (Bug ago/2026: main() duplicava a lista, check novo não rodava pelo CLI; e o
    --diff rodava os checks transversais SEM a dívida, inflando severidades no diff.)
    Função pura — sem prints. main() imprime; --diff chama duas vezes."""
    findings: List[Finding] = []
    auditors = [
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
    dim_scores = {i: fn() for i, fn in auditors}
    # Transversal: não pontua dimensão, só levanta achado. Proveniência é pré-requisito
    # de tudo — sem ela, nota alta só mede se o texto SOA bem (ver comentário do check).
    pendentes = check_proveniencia(data, findings, debt)
    pendentes += check_claims_cobertos(data, findings, debt)
    check_fontes_schema(data, findings)
    assign_stations(findings)
    return dim_scores, findings, pendentes


def _finding_key(f: Finding) -> Tuple:
    """Identidade estável de um achado entre dois runs. Números são zerados porque
    contadores mudam ('1/1 cards' → '2/3 cards') sem o achado ser 'outro'."""
    base = re.sub(r'\d+', '#', f.msg)
    return (f.dim, f.stop, base)


def compute_diff(before: List[Finding], after: List[Finding]):
    b = {_finding_key(f): f for f in before}
    a = {_finding_key(f): f for f in after}
    resolved = [b[k] for k in b if k not in a]          # sumiu → consertado
    new      = [a[k] for k in a if k not in b]          # apareceu → efeito colateral?
    kept     = [a[k] for k in a if k in b]              # intacto
    return resolved, new, kept


def print_diff(bs: Dict[int, int], bf: List[Finding],
               as_: Dict[int, int], af: List[Finding]) -> bool:
    """Mostra o delta. Retorna True se houve REGRESSÃO (mecânico caiu ou surgiu
    P0/P1 mecânico novo) — o caller usa pro exit code."""
    b_mech, b_judg = split_scores(bs)
    a_mech, a_judg = split_scores(as_)
    b_tot, a_tot   = sum(bs.values()), sum(as_.values())
    resolved, new, kept = compute_diff(bf, af)

    def delta(x):
        d = f'+{x}' if x > 0 else (str(x) if x < 0 else '±0')
        col = C.OK if x > 0 else (C.ERR if x < 0 else C.DIM)
        return f'{col}{d}{C.END}'

    print(f"\n{C.BOLD}=== 🔁 Diff de conteúdo (loop fechado) ==={C.END}\n")
    print(f"  Total      {b_tot:>2}/40 → {a_tot:>2}/40  ({delta(a_tot-b_tot)})")
    print(f"  🔩 Mecânico {b_mech:>2}/20 → {a_mech:>2}/20  ({delta(a_mech-b_mech)})"
          f"  {C.DIM}número é verdade{C.END}")
    print(f"  ⚖️  Julgamento {b_judg:>2}/20 → {a_judg:>2}/20  ({delta(a_judg-b_judg)})"
          f"  {C.DIM}proxy — confirme na prosa{C.END}")
    print(f"\n  {C.OK}✓ resolvido: {len(resolved)}{C.END}   "
          f"{C.ERR}✧ novo: {len(new)}{C.END}   {C.DIM}• intacto: {len(kept)}{C.END}")

    if resolved:
        print(f"\n{C.OK}Resolvido{C.END}")
        for f in resolved[:8]:
            where = f' [{f.stop[:36]}]' if f.stop else ''
            print(f"  ✓ {C.DIM}{f.msg[:64]}{where}{C.END}")
    if new:
        print(f"\n{C.ERR}Novo (efeito colateral?){C.END}")
        for f in new[:8]:
            where = f' [{f.stop[:36]}]' if f.stop else ''
            print(f"  {SEV_LABEL[f.sev]} {f.station} {f.msg[:60]}{C.DIM}{where}{C.END}")

    # --- veredito de regressão
    mech_regress = a_mech < b_mech
    new_mech_pf  = [f for f in new if f.dim in MECHANICAL_DIMS and f.sev <= 1]
    regressed    = mech_regress or bool(new_mech_pf)

    print()
    if regressed:
        why = []
        if mech_regress:      why.append(f'mecânico caiu {b_mech}→{a_mech}')
        if new_mech_pf:       why.append(f'{len(new_mech_pf)} P0/P1 mecânico novo')
        print(f"{C.ERR}✗ REGRESSÃO: {' · '.join(why)} — o lote quebrou algo objetivo{C.END}")
    elif a_judg < b_judg:
        print(f"{C.WARN}⚠ mecânico ok, mas julgamento caiu {b_judg}→{a_judg} — "
              f"o agregado esconde isso. Confirme a prosa antes de fechar{C.END}")
    else:
        print(f"{C.OK}✓ sem regressão — mecânico não caiu, nenhum P0/P1 objetivo novo{C.END}")
    return regressed


def run_diff(after_path: Path, before_path: Path, check_links: bool, json_out: bool) -> None:
    for p in (after_path, before_path):
        if not p or not p.exists():
            print(f"{C.ERR}✗{C.END} --diff precisa de 2 arquivos: <depois> --diff <antes>")
            sys.exit(2)
    # A dívida de proveniência de cada arquivo entra no diff também — senão um
    # self-diff mostra severidades diferentes do modo normal (bug ago/2026).
    bs, bf, _  = audit_roteiro(load_data(before_path), check_links, load_debt(str(before_path)))
    as_, af, _ = audit_roteiro(load_data(after_path), check_links, load_debt(str(after_path)))
    b_mech, _ = split_scores(bs)
    a_mech, _ = split_scores(as_)
    resolved, new, kept = compute_diff(bf, af)
    new_mech_pf = [f for f in new if f.dim in MECHANICAL_DIMS and f.sev <= 1]
    regressed   = a_mech < b_mech or bool(new_mech_pf)

    if json_out:
        b_m, b_j = split_scores(bs); a_m, a_j = split_scores(as_)
        print(json.dumps({
            'mode': 'diff',
            'before': {'total': sum(bs.values()), 'mechanical': b_m, 'judgment': b_j},
            'after':  {'total': sum(as_.values()), 'mechanical': a_m, 'judgment': a_j},
            'resolved': len(resolved), 'new': len(new), 'kept': len(kept),
            'regressed': regressed,
            'new_findings': [{'sev': SEV_LABEL[f.sev], 'dim': f.dim, 'station': f.station,
                              'msg': f.msg, 'stop': f.stop} for f in new],
        }, ensure_ascii=False, indent=2))
    else:
        print_diff(bs, bf, as_, af)

    sys.exit(1 if regressed else 0)

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

    # Dimension scores table — separadas por confiabilidade
    mech, judg = split_scores(dim_scores)

    def _row(idx):
        s     = dim_scores[idx]
        bar   = '█' * s + '░' * (4 - s)
        color = C.OK if s >= 3 else (C.WARN if s >= 2 else C.ERR)
        print(f"  {color}{bar}{C.END} {s}/4  {dim_label(idx)}")

    print(f"\n{C.BOLD}=== Mecânico · {mech}/20 "
          f"{C.DIM}(regex é autoridade · número confiável){C.END} ===\n")
    for idx in sorted(d for d in dim_scores if d in MECHANICAL_DIMS):
        _row(idx)

    print(f"\n{C.BOLD}=== Julgamento ⚖️ · {judg}/20 "
          f"{C.DIM}(regex = piso · Claude confirma no checklist){C.END} ===\n")
    for idx in sorted(d for d in dim_scores if d in JUDGMENT_DIMS):
        _row(idx)

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
    mech, judg = split_scores(dim_scores)
    print('─' * 62)
    ok_color = C.OK if is_approved(total, findings) else C.ERR
    # R3 (auditoria 2026-08-08): a nota mede FORMA, não verdade — um roteiro 100%
    # falso tirou 35/40. Ela é rodapé, nunca manchete de entrega.
    print(f"{C.BOLD}★ FORMA: {ok_color}{total}/40{C.END}"
          f" {C.DIM}(não mede verdade — ver FACTCHECK){C.END}"
          f" · {bcolor}{band}{C.END}"
          f" {C.DIM}(mec {mech}/20 · julg⚖️ {judg}/20){C.END}"
          f"  |  P0: {pcnts[0]}  P1: {pcnts[1]}  P2: {pcnts[2]}  P3: {pcnts[3]}")

    if is_approved(total, findings):
        print(f"{C.OK}✓ Forma aprovada{C.END} "
              f"{C.DIM}(confirme as dims ⚖️ no checklist · verdade é o FACTCHECK, não esta nota){C.END}")
    elif pcnts[0] > 0:
        print(f"{C.ERR}✗ Bloqueado: {pcnts[0]} P0(s) — erro objetivo, corrigir antes de continuar{C.END}")
    else:
        print(f"{C.WARN}⚠ Iterar: nota {total}/40 < {APPROVAL_MIN} — corrigir P1s listados acima{C.END}")
    print()


def print_json_result(dim_scores: Dict[int, int], findings: List[Finding]) -> None:
    total = sum(dim_scores.values())
    band, _  = score_band(total)
    mech, judg = split_scores(dim_scores)
    out = {
        'mode':          'roteiro',
        'score':         total,
        'max':           40,
        'mechanical':    mech,   # /20 · confiável
        'judgment':      judg,   # /20 · proxy, Claude confirma
        'approval_min':  APPROVAL_MIN,
        'band':          band,
        'approved':      is_approved(total, findings),
        'p0':            sum(1 for f in findings if f.sev == 0),
        'dimensions': {DIM_NAMES[i]: s for i, s in sorted(dim_scores.items())},
        'findings': [
            {
                'sev':     SEV_LABEL[f.sev],
                'dim':     DIM_NAMES.get(f.dim, str(f.dim)),
                'half':    'mechanical' if f.dim in MECHANICAL_DIMS else 'judgment',
                'msg':     f.msg,
                'stop':    f.stop,
                'station': f.station,   # 🔧 corrigir · 🔎 pesquisar · ✍️ reescrever · 🤔 decidir
                'hint':    f.hint,      # o que bom parece (patch colável nos 🔧)
            }
            for f in findings
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def print_suggest(findings: List[Finding], data: Dict) -> None:
    """Visão de CONSERTO (--suggest): despacha os achados por estação, prioriza
    ponderado e lista os patches prontos. É o que transforma o grader em coach."""
    if not findings:
        print(f"\n{C.OK}✓ Nada a rotear — zero achados.{C.END}\n")
        return

    idx = build_stop_index(data)

    print(f"\n{C.BOLD}=== 🛠️  Plano de conserto (--suggest) ==={C.END}\n")

    # --- por estação
    by_st: Dict[str, List[Finding]] = {}
    for f in findings:
        by_st.setdefault(f.station, []).append(f)
    print(f"{C.BOLD}Por estação{C.END}")
    for st in (ST_FIX, ST_RESEARCH, ST_REWRITE, ST_HUMAN):
        fs = by_st.get(st, [])
        if fs:
            print(f"  {st}  {len(fs):>2} achado(s) — {C.DIM}{STATION_DESC[st]}{C.END}")
    print(f"\n  {C.DIM}⚠️  Perseguir o número só vale nas dims MECÂNICAS. Nas ⚖️, o alvo é a"
          f" prosa —\n     confirmada no checklist, não no score.{C.END}\n")

    # --- top-5 cards (ponderado: severidade × peso do card)
    scores: Dict[str, int] = {}
    for f in findings:
        if not f.stop:
            continue
        peso = idx.get(f.stop, {}).get('peso', 1)
        scores[f.stop] = scores.get(f.stop, 0) + SEV_WEIGHT[f.sev] * peso
    if scores:
        print(f"{C.BOLD}Top 5 cards (severidade × peso do card){C.END}")
        for nome, sc in sorted(scores.items(), key=lambda kv: -kv[1])[:5]:
            meta = idx.get(nome, {})
            tag  = '⚓ âncora' if meta.get('peso') == 2 else 'filler'
            sts  = ''.join(sorted({f.station for f in findings if f.stop == nome}))
            n    = sum(1 for f in findings if f.stop == nome)
            print(f"  {sc:>4} pts · {n} achado(s) {sts:<6} {nome[:44]} {C.DIM}({tag}){C.END}")
        print()

    # --- heat map por dia (densidade ponderada · NÃO é nota)
    per_day: Dict[str, int] = {}
    for f in findings:
        dia = idx.get(f.stop, {}).get('dia', '') if f.stop else ''
        if dia:
            per_day[dia] = per_day.get(dia, 0) + SEV_WEIGHT[f.sev]
    if per_day:
        mx = max(per_day.values())
        print(f"{C.BOLD}Densidade por dia{C.END} {C.DIM}(triagem — NÃO é nota por dia:"
              f" D9/D10 só existem no roteiro inteiro){C.END}")
        for dia, sc in sorted(per_day.items(), key=lambda kv: -kv[1])[:6]:
            bar = '█' * max(1, round(sc / mx * 22))
            print(f"  {dia:<12} {C.WARN}{bar}{C.END} {sc}")
        print()

    # --- patches prontos (só os 🔧 determinísticos)
    fixes = by_st.get(ST_FIX, [])
    if fixes:
        print(f"{C.BOLD}🔧 Patches prontos pra colar{C.END} {C.DIM}(determinísticos){C.END}")
        for f in fixes[:8]:
            where = f' [{f.stop[:38]}]' if f.stop else ''
            print(f"  • {C.DIM}{f.msg[:66]}{where}{C.END}")
            print(f"    → {f.hint}")
        if len(fixes) > 8:
            print(f"  {C.DIM}… +{len(fixes)-8} outro(s) — veja no --json{C.END}")
        print()

    # --- o que precisa de pesquisa (a alavanca dominante)
    res = by_st.get(ST_RESEARCH, [])
    if res:
        print(f"{C.BOLD}🔎 Fila de pesquisa{C.END} {C.DIM}(cada valor volta com fonte + data ·"
              f" não confirmou = [a confirmar] / coord_unverified){C.END}")
        for f in res[:6]:
            where = f' [{f.stop[:38]}]' if f.stop else ''
            print(f"  • {C.DIM}{f.msg[:66]}{where}{C.END}\n    → {f.hint}")
        if len(res) > 6:
            print(f"  {C.DIM}… +{len(res)-6} outro(s) — veja no --json{C.END}")
        print()

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
# Veredito do scout · DOIS vocabulários aceitos (Lote 7d · 2026-08-09).
#   novo   🏆 entra · ⚠️ talvez · ⏭️ pula
#   antigo 🟢 faça  · 🟡 depende · 🔴 pula  (entregas até 2026-08-09 · não serão reescritas)
# A troca aconteceu porque 🟢🟡🔴 é também o `risco` do roteiro, que mede ATRITO — as mesmas
# três cores diziam duas coisas diferentes e um lugar podia ser "🟢 e 🔴 ao mesmo tempo".
VERDICT_NOVO_RE = re.compile(r'🏆|⏭️?')
VERDICT_TALVEZ_RE = re.compile(r'⚠️?')
VERDICT_ANTIGO_RE = re.compile(r'🟢|🟡|🔴')


def count_verdicts(text: str) -> int:
    """Conta vereditos aceitando os dois vocabulários.

    O ⚠️ só conta como veredito "talvez" num doc que JÁ usa o vocabulário novo (tem 🏆/⏭️).
    Sem essa condição, os ⚠️ de alerta de segurança ("⚠️ cabeça d'água"), que o scout sempre
    usou, seriam contados como veredito e inflariam o check em entregas antigas — o gate
    passaria a aprovar levantamento sem crítica nenhuma."""
    novo = len(VERDICT_NOVO_RE.findall(text))
    antigo = len(VERDICT_ANTIGO_RE.findall(text))
    talvez = len(VERDICT_TALVEZ_RE.findall(text)) if novo else 0
    return novo + antigo + talvez
FONTES_RE       = re.compile(r'^#{1,4}\s*(fontes|refer[êe]ncias|sources)\b', re.I | re.M)
ARMADILHA_RE    = re.compile(r'armadilha|cilada|turistada|superestimad|pula sem culpa|fila inútil|não vale a pena', re.I)
KM_MIN_RE       = re.compile(r'\d+\s?(km|min|minutos|h\b|horas)', re.I)
SABOR_RE        = re.compile(r'sabor|ingrediente|prato típico|endêmic|assinatura|especialidade|típic', re.I)
ANCHOR_RE       = re.compile(r'âncora|estar na porta', re.I)
CONFIRMAR_RE    = re.compile(r'\[a confirmar\]|\[confirmar\]', re.I)


def detect_mini_plano(text: str) -> bool:
    """Mini-plano = 1 bloco/meia-diária com âncora fixa, sem tabela de veredito."""
    has_table  = bool(re.search(r'esfor[çc]o.*recompensa', text, re.I))
    n_verdicts = count_verdicts(text)
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
    """S2 · Veredito 🏆⚠️⏭️ (ou 🟢🟡🔴 antigo) + honestidade (armadilhas, anti-hype)."""
    n_verdicts    = count_verdicts(text)
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
        F.append(Finding(2, 2, f'poucos vereditos 🏆⚠️⏭️ ({n_verdicts}) — cada atração precisa do seu, calibrado ao perfil'))
    else:
        F.append(Finding(1, 2, 'nenhum veredito 🏆⚠️⏭️ (nem 🟢🟡🔴 antigo) — levantamento sem crítica vira folder de agência'))
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


SCOUT_APPROVAL_MIN = 16  # 80% de 20 — mesma barra proporcional do roteiro (32/40)

def scout_band(total: int) -> Tuple[str, str]:
    if total >= 18:
        return 'Excelente', C.OK
    if total >= 16:
        return 'Bom', C.CYAN
    if total >= 12:
        return 'Aceitável', C.WARN
    return 'Ruim', C.ERR


def scout_approved(total: int, findings: List[Finding]) -> bool:
    return total >= SCOUT_APPROVAL_MIN and not any(f.sev == 0 for f in findings)


SCOUT_CHECKLIST = """
┌──────────────────────────────────────────────────────────────────────────┐
│  CHECKLIST MANUAL · levantamento scout (julgamento humano)               │
├──────────────────────────────────────────────────────────────────────────┤
│  Perfil & Calibração                                                     │
│  [ ] veredito 🏆⚠️⏭️ calibrado ao PERFIL informado (não genérico)?     │
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
        print(f"{C.WARN}⚠ Iterar: nota {total}/20 < {SCOUT_APPROVAL_MIN} — corrigir P1s listados acima{C.END}")
    print()


def print_json_scout(dim_scores: Dict[int, int], findings: List[Finding]) -> None:
    total = sum(dim_scores.values())
    band, _ = scout_band(total)
    out = {
        'mode':          'scout',
        'score':         total,
        'max':           20,
        'approval_min':  SCOUT_APPROVAL_MIN,
        'band':          band,
        'approved':      scout_approved(total, findings),
        'p0':            sum(1 for f in findings if f.sev == 0),
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
    deploy_gate   = '--deploy-gate'   in flags
    suggest       = '--suggest'       in flags
    write_baseline = '--baseline'     in flags
    path_arg      = args[0] if args else None
    if deploy_gate:
        no_checklist = True   # gate de deploy é compacto (sem checklist manual)

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
        print("  --deploy-gate   Modo deploy.sh: compacto · bloqueia só em P0 · nota baixa = aviso")
        print("  --suggest       Plano de CONSERTO: roteia cada achado (🔧/🔎/✍️/🤔) + top-5 + patches")
        print("  --diff <antes>  Loop fechado: <depois>.json --diff <antes>.json · delta + regressão")
        print("                  (VIAGEM_STRICT=1 no env também bloqueia nota < aprovação)")
        sys.exit(2)

    path = Path(args[0])
    if not path.exists():
        print(f"{C.ERR}✗{C.END} Arquivo não existe: {path}")
        sys.exit(2)

    # Desvio pro modo scout (auditoria de levantamento .md · rubrica /20)
    if '--scout' in flags:
        run_scout(path, flags, json_out, no_checklist)
        return

    # Desvio pro loop fechado (compara antes/depois · assere não-regressão)
    if '--diff' in flags:
        before = Path(args[1]) if len(args) > 1 else None
        run_diff(path, before, check_links, json_out)
        return

    verbose = not json_out and not deploy_gate  # deploy-gate = compacto (só a ★ line)

    if verbose:
        print(f"\n{C.BOLD}=== Auditando conteúdo: {path.name} ==={C.END}\n")

    try:
        data = load_data(path)
    except Exception as e:
        print(f"{C.ERR}✗{C.END} Erro ao carregar dados: {e}")
        sys.exit(2)

    if verbose:
        n_days  = len(data.get('days', []))
        n_cards = len(get_cards(data))
        n_wt    = len(get_wt_parts(data))
        print(f"{C.DIM}  {n_days} dias · {n_cards} cards · {n_wt} partes de walking tour{C.END}\n")
        print(f"{C.DIM}── Rodando 10 dimensões ──{C.END}")

    # UMA fonte de verdade: audit_roteiro() roda dimensões + checks transversais.
    # (Bug ago/2026, consertado: main() duplicava a lista de auditores — check novo
    # registrado em audit_roteiro NÃO rodava pelo CLI.)
    debt = load_debt(path_arg)
    dim_scores, findings, pendentes = audit_roteiro(data, check_links, debt)

    if verbose:
        for dim_idx in sorted(dim_scores):
            s = dim_scores[dim_idx]
            color = C.OK if s >= 3 else (C.WARN if s >= 2 else C.ERR)
            icon  = '✓' if s >= 3 else ('⚠' if s >= 2 else '✗')
            print(f"  {color}{icon}{C.END} {dim_label(dim_idx)}: {s}/4")

    if write_baseline:
        p = _debt_path(path_arg)
        # A dívida SÓ ENCOLHE. Item novo sem fonte nunca entra por aqui — seria
        # transformar o baseline em desculpa, que é o modo clássico de morrer do lint.
        novos = [k for k in pendentes if k not in debt]
        if debt and novos:
            print(f"{C.ERR}✗ --baseline recusado{C.END}: {len(novos)} item(ns) NOVO(s) sem "
                  f"proveniência não entram na dívida — pesquise a fonte:")
            for k in novos[:10]:
                print(f"    · {k}")
            sys.exit(2)
        p.write_text(json.dumps({
            "_": "Dívida de proveniência congelada quando a REGRA ZERO entrou (2026-08-04). "
                 "SÓ ENCOLHE: item novo sem fonte é P0/P1 e não entra aqui. "
                 "Ver CLAUDE.md · REGRA ZERO e FACTCHECK.md §0.",
            "itens": pendentes,
        }, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"{C.OK}✓{C.END} dívida registrada em {p} · {len(pendentes)} item(ns)")
        sys.exit(0)

    # Linha informativa da dívida SÓ em modo verbose — em --json NADA além do objeto
    # JSON pode ir pro stdout (bug ago/2026: esta linha quebrava json.load do caller).
    if debt and verbose:
        print(f"{C.DIM}  dívida de proveniência herdada: {len(debt)} item(ns) "
              f"(P2 · só encolhe · ver .proveniencia-debt.json){C.END}")

    total    = sum(dim_scores.values())
    n_p0     = sum(1 for f in findings if f.sev == 0)
    approved = is_approved(total, findings)

    # --- Modo gate de deploy: compacto · bloqueia SÓ em P0 (ou VIAGEM_STRICT) ---
    if deploy_gate:
        strict = os.environ.get('VIAGEM_STRICT', '') == '1'
        mech, judg = split_scores(dim_scores)
        band, _ = score_band(total)
        blocked = n_p0 > 0 or (strict and not approved)
        print(f"{C.BOLD}★ FORMA (gate deploy): {total}/40 · {band}{C.END} "
              f"{C.DIM}(não mede verdade — ver FACTCHECK){C.END} "
              f"(mec {mech}/20 · julg⚖️ {judg}/20) | P0:{n_p0} P1:{sum(1 for f in findings if f.sev==1)}")
        if n_p0 > 0:
            for f in findings:
                if f.sev == 0:
                    stop = f' [{f.stop}]' if f.stop else ''
                    print(f"  {C.ERR}P0{C.END} {f.msg}{stop}")
        if blocked:
            why = f'{n_p0} P0' if n_p0 > 0 else f'nota {total}<{APPROVAL_MIN} (VIAGEM_STRICT)'
            print(f"{C.ERR}✗ deploy BLOQUEADO: {why}{C.END}")
            sys.exit(1)
        if not approved:
            print(f"{C.WARN}⚠ nota {total}/40 < {APPROVAL_MIN} — passa no gate mas revise "
                  f"(a régua de {APPROVAL_MIN} é do loop da sessão, não do push){C.END}")
        else:
            print(f"{C.OK}✓ passa no gate de deploy{C.END}")
        sys.exit(0)

    # --- Modo normal (pipeline/standalone) ---
    if json_out:
        print_json_result(dim_scores, findings)
    else:
        print_report(dim_scores, findings, show_checklist=not no_checklist)
        if suggest:
            print_suggest(findings, data)

    sys.exit(0 if approved else 1)


if __name__ == '__main__':
    main()
