#!/usr/bin/env python3
"""
validate.py — Validador do roteiro-viagem

Roda checks de sanidade antes de commit/push.
Exit code 0 = tudo ok · != 0 = bloqueia deploy.

Uso:
    python3 validate.py /path/to/index.html
"""

import re
import sys
import json
import subprocess
from pathlib import Path

# ---------------------------------------------------------
# COLORS
# ---------------------------------------------------------
class C:
    OK   = '\033[92m'   # green
    WARN = '\033[93m'   # yellow
    ERR  = '\033[91m'   # red
    DIM  = '\033[2m'    # dim
    END  = '\033[0m'    # reset
    BOLD = '\033[1m'    # bold

errors   = []
warnings = []

def err(msg):
    errors.append(msg)
    print(f"{C.ERR}✗{C.END} {msg}")

def warn(msg):
    warnings.append(msg)
    print(f"{C.WARN}⚠{C.END}  {msg}")

def ok(msg):
    print(f"{C.OK}✓{C.END} {msg}")

# ---------------------------------------------------------
# CHECKS
# ---------------------------------------------------------

def check_file_exists(path):
    if not path.exists():
        err(f"Arquivo não existe: {path}")
        return False
    return True

# Limites de tamanho · viagens longas (25+ dias) com JSON pretty-printed cabem aqui
# JSON pretty escolhido como default (edit mobile-friendly) sem otimização prematura
MAX_SIZE_WARN = 500  # KB — só sinaliza (bandwidth ainda OK pra mobile 4G)
MAX_SIZE_ERR  = 1500 # KB — quase nunca atinge · indica algo errado (loop, dado duplicado)

def check_size(content):
    size_kb = len(content) // 1024
    if size_kb > MAX_SIZE_ERR:
        err(f"Arquivo muito grande: {size_kb}KB (limite {MAX_SIZE_ERR}KB · provavelmente bug)")
    elif size_kb > MAX_SIZE_WARN:
        warn(f"Arquivo grande: {size_kb}KB (>{MAX_SIZE_WARN}KB · considere --minify no build.py)")
    else:
        ok(f"Tamanho: {size_kb}KB")

def check_html_balance(content):
    open_divs  = len(re.findall(r'<div[\s>]', content))
    close_divs = len(re.findall(r'</div>', content))
    if open_divs != close_divs:
        err(f"<div> desbalanceadas: {open_divs} abertas vs {close_divs} fechadas")
    else:
        ok(f"HTML divs balanceadas: {open_divs}")

    # Tags críticas que devem ser exatamente 1
    for tag in ['html', 'head', 'body']:
        opens  = len(re.findall(rf'<{tag}[\s>]', content))
        closes = len(re.findall(rf'</{tag}>', content))
        if opens != 1 or closes != 1:
            err(f"<{tag}> deve ter exatamente 1 abertura e 1 fechamento (achei {opens}/{closes})")

def check_js_syntax(content):
    """Extrai cada bloco <script> e roda node --check"""
    scripts = re.findall(r'<script(?:\s[^>]*)?>([\s\S]*?)</script>', content)
    scripts_with_code = [s for s in scripts if s.strip() and 'src=' not in s[:200]]
    
    if not scripts_with_code:
        warn("Nenhum bloco <script> com código inline encontrado")
        return

    for i, script in enumerate(scripts_with_code, 1):
        if 'leaflet' in script.lower()[:200] or len(script) < 50:
            continue
        # Salvar em temp e rodar node --check
        tmp = Path('/tmp/_validate_script.js')
        tmp.write_text(script)
        try:
            result = subprocess.run(
                ['node', '--check', str(tmp)],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode != 0:
                err(f"Script #{i} tem erro de sintaxe JS:\n{result.stderr[:300]}")
            else:
                ok(f"Script #{i} ({len(script)} chars) sintaxe OK")
        except FileNotFoundError:
            warn("node não disponível — pulando JS syntax check")
            return
        except subprocess.TimeoutExpired:
            warn(f"Script #{i} timeout no --check")
        finally:
            if tmp.exists():
                tmp.unlink()

def extract_days_array(content):
    """Extrai o array DAYS via regex pra checks de dados.
    Funciona pra DAYS minificado JSON (sem espaços, sem newlines) ou pretty-printed."""
    m = re.search(r'const\s+DAYS\s*=\s*(\[[\s\S]*?\])\s*;', content)
    if not m:
        warn("Não consegui extrair DAYS — pulando checks de dados")
        return None
    return m.group(1)

def check_coords(days_text):
    if not days_text:
        return
    # Aceita JS object literal (coord: {lat:}) E JSON ("coord":{"lat":})
    coords = re.findall(r'"?coord"?\s*:\s*\{\s*"?lat"?\s*:\s*(-?\d+\.?\d*)\s*,\s*"?lng"?\s*:\s*(-?\d+\.?\d*)\s*\}', days_text)
    if not coords:
        warn("Nenhuma coord encontrada em DAYS")
        return

    invalid = []
    for lat_str, lng_str in coords:
        lat, lng = float(lat_str), float(lng_str)
        if not (-90 <= lat <= 90):
            invalid.append(f"lat {lat} fora de [-90, 90]")
        if not (-180 <= lng <= 180):
            invalid.append(f"lng {lng} fora de [-180, 180]")

    if invalid:
        for inv in invalid[:5]:
            err(f"Coord inválida: {inv}")
        if len(invalid) > 5:
            err(f"... +{len(invalid)-5} coords inválidas")
    else:
        ok(f"Todas {len(coords)} coords em range válido")

def check_enums(days_text):
    if not days_text:
        return
    # Padrão flex: aceita JS literal (key:) E JSON ("key":)
    def find_enum(field):
        return re.findall(rf'"?{field}"?\s*:\s*["\'](\w+)["\']', days_text)

    # tipo deve ser card | opcoes | transit
    tipos = find_enum('tipo')
    invalid_tipos = [t for t in tipos if t not in {'card', 'opcoes', 'transit'}]
    if invalid_tipos:
        err(f"tipo inválido: {set(invalid_tipos)}")
    else:
        ok(f"Todos {len(tipos)} 'tipo' válidos (card/opcoes/transit)")

    # risco deve ser green | yellow | red
    riscos = find_enum('risco')
    invalid_riscos = [r for r in riscos if r not in {'green', 'yellow', 'red'}]
    if invalid_riscos:
        err(f"risco inválido: {set(invalid_riscos)}")
    else:
        ok(f"Todos {len(riscos)} 'risco' válidos")

    # periodo deve ser manha | tarde | noite
    periodos = find_enum('periodo')
    invalid_p = [p for p in periodos if p not in {'manha', 'tarde', 'noite'}]
    if invalid_p:
        err(f"periodo inválido: {set(invalid_p)}")
    else:
        ok(f"Todos {len(periodos)} 'periodo' válidos")

    # reserva deve ser reservado | pendente
    reservas = find_enum('reserva')
    invalid_r = [r for r in reservas if r not in {'reservado', 'pendente'}]
    if invalid_r:
        err(f"reserva inválido: {set(invalid_r)}")
    elif reservas:
        ok(f"Todas {len(reservas)} 'reserva' válidas")

# Classificação de POI (mapa unificado · handoff §4/§6):
#  - poiCat ∈ enum(9)
#  - valeAPena ∈ {0,1,2,3} OBRIGATÓRIO em card + item de opcoes · PROIBIDO em transit
#  - coord em item de opcoes: se presente, 4 casas decimais (missing → warn até popular tudo)
POI_CATS = {'atracao','restaurante','cafe','padaria','loja','bar','parque','mercado','food-hall'}
def _dec4(v):
    s = repr(float(v)); return '.' in s and len(s.split('.')[1]) >= 4
def check_poi_classification(days_text):
    if not days_text:
        return
    try:
        days = json.loads(days_text)
    except Exception:
        warn("check_poi_classification: DAYS não é JSON parseável (minificado?) — pulando")
        return
    bad_cat, missing_va, forbidden_va, opt_coord_bad, opt_no_coord = [], [], [], [], []
    def check_cat_va(obj, ctx):
        pc = obj.get('poiCat')
        if pc is not None and pc not in POI_CATS: bad_cat.append((ctx, pc))
        va = obj.get('valeAPena')
        if va is None: missing_va.append(ctx)
        elif va not in (0,1,2,3): bad_cat.append((ctx, f'valeAPena={va}'))
    for day in days:
        for s in day.get('stops', []):
            t, nome = s.get('tipo'), s.get('nome','?')[:32]
            if t == 'card':
                check_cat_va(s, nome)
            elif t == 'opcoes':
                if 'valeAPena' in s or 'poiCat' in s: forbidden_va.append(f'{nome} (stop opcoes)')
                for o in s.get('opcoes', []):
                    onome = o.get('nome','?')[:32]
                    check_cat_va(o, onome)
                    c = o.get('coord')
                    if not c: opt_no_coord.append(onome)
                    elif not (_dec4(c.get('lat',0)) and _dec4(c.get('lng',0))): opt_coord_bad.append(onome)
            elif t == 'transit':
                if s.get('valeAPena') is not None or s.get('poiCat') is not None:
                    forbidden_va.append(f'{nome} (transit)')
    if bad_cat: err(f"poiCat/valeAPena inválido: {bad_cat[:5]}")
    if missing_va: err(f"valeAPena AUSENTE em {len(missing_va)} card/opção (obrigatório): {missing_va[:5]}")
    if forbidden_va: err(f"valeAPena/poiCat PROIBIDO presente: {forbidden_va[:5]}")
    if opt_coord_bad: err(f"coord de opção com <4 casas: {opt_coord_bad[:5]}")
    if opt_no_coord: warn(f"{len(opt_no_coord)} opção(ões) ainda sem coord (pino não aparece no mapa): {opt_no_coord[:5]}")
    if not (bad_cat or missing_va or forbidden_va or opt_coord_bad):
        ok(f"Classificação POI ok (poiCat/valeAPena) · {len(opt_no_coord)} opção(ões) sem coord ainda")

def check_walking_tours(days_text):
    if not days_text:
        return
    # Conta sub-paradas em walking tours (aceita JS literal e JSON)
    tour_stops = re.findall(r'\{\s*"?n"?\s*:\s*\d+\s*,\s*"?nome"?\s*:', days_text)
    if not tour_stops:
        return

    # Conta tours por partições
    parts = re.findall(r'"?nome"?\s*:\s*["\']([^"\']+)["\']\s*,\s*"?descricao"?\s*:', days_text)
    ok(f"Walking tours: {len(parts)} partes · {len(tour_stops)} sub-paradas")

def check_temaCurto(days_text):
    if not days_text:
        return
    curtos = re.findall(r'"?temaCurto"?\s*:\s*["\']([^"\']+)["\']', days_text)
    long_ones = [c for c in curtos if len(c) > 15]
    if long_ones:
        for l in long_ones:
            warn(f"temaCurto longo ({len(l)} chars): \"{l}\" — recomendado ≤ 15")
    else:
        ok(f"Todos {len(curtos)} temaCurto ≤ 15 chars")

def check_no_manual_stars(days_text):
    """Bloqueia ⭐ digitada à mão nos campos de texto do DAYS.

    A recompensa é um EIXO DE DADO (`valeAPena` 0-3), renderizado pelo template como
    pill no header do card e como tamanho de pino no "Tudo no Mapa". Escrever ⭐ na
    prosa cria uma segunda fonte de verdade que não filtra, não ordena e fica
    inconsistente — o card com ⭐ digitada parece classificado e o resto parece sem
    classificação, mesmo quando TODOS têm valeAPena preenchido.

    Guardrail criado ago/2026: o Tobia viu "⭐⭐⭐" no card da Rondinara (Córsega),
    perguntou por que só ali, e a resposta era que eu tinha digitado à mão num campo
    `cat`. Era a única ocorrência em 13 dias.

    Correto: preencher `valeAPena` e deixar o template renderizar.
    """
    if not days_text:
        return
    STAR_RE = re.compile(r'⭐|⏭️')
    hits = []
    def scan(obj, ctx):
        if isinstance(obj, str):
            if STAR_RE.search(obj):
                hits.append((ctx, obj[:50]))
        elif isinstance(obj, list):
            for x in obj:
                scan(x, ctx)
        elif isinstance(obj, dict):
            for k, v in obj.items():
                if k in ('emoji',):
                    continue
                scan(v, k)
    try:
        scan(json.loads(days_text), 'DAYS')
    except Exception:
        hits = [('(DAYS)', m) for m in STAR_RE.findall(days_text)]
    if hits:
        preview = [f'"{t}" [{c[:22]}]' for c, t in hits[:4]]
        err(f"⭐ digitada à mão em {len(hits)} campo(s) do DAYS · recompensa é dado "
            f"(valeAPena 0-3), o template renderiza a pill sozinho · remova do texto: {preview}")
    else:
        ok("Sem ⭐ manual no texto · recompensa vem de valeAPena")


def check_no_raw_markdown(days_text):
    """Bloqueia markdown cru (**bold**) nos campos de texto do DAYS.
    O template injeta dicas/sobre/imperdivel via innerHTML SEM converter markdown
    (render-functions.js) — então **texto** renderiza como asterisco LITERAL no app.
    Convenção do repo (CLAUDE.md): usar HTML cru <strong>/<em>, nunca markdown.
    Guardrail criado no aprofundamento NYC (2026-07-12): 56 pares ** em 11 cards
    passaram batido pelo audit/validate e renderizavam asterisco na tela da família.
    Escaneia só o DAYS (dados), não o HTML inteiro — evita falso-positivo com o
    operador ** de exponenciação no JS do template (ex: Math.sin(x)**2)."""
    if not days_text:
        return
    BOLD_RE = re.compile(r'\*\*(.+?)\*\*')
    hits = []
    def scan(obj, ctx):
        if isinstance(obj, str):
            for m in BOLD_RE.findall(obj):
                hits.append((ctx, m[:40]))
        elif isinstance(obj, list):
            for x in obj:
                scan(x, ctx)
        elif isinstance(obj, dict):
            c = obj.get('nome', ctx)
            for v in obj.values():
                scan(v, c)
    try:
        scan(json.loads(days_text), '?')
    except Exception:
        # DAYS minificado / não-JSON → fallback regex no texto cru dos dados
        hits = [('(DAYS)', m[:40]) for m in BOLD_RE.findall(days_text)]
    if hits:
        preview = [f'"{m}" [{c[:30]}]' for c, m in hits[:5]]
        err(f"markdown cru **bold** em {len(hits)} lugar(es) do DAYS · o template "
            f"renderiza asterisco literal · trocar por <strong>…</strong>: {preview}")
    else:
        ok("Sem markdown cru (**bold**) · texto usa HTML <strong>/<em>")

def check_links_alive(content, timeout=5):
    """Checa LINKS_MAP entries via HTTP HEAD. Opcional · só roda com --check-links.
    Marca como warning (não bloqueia) URLs que retornam 4xx/5xx ou timeout."""
    try:
        import urllib.request
        import urllib.error
    except ImportError:
        warn("urllib não disponível · pulando check de links")
        return

    # Extrai LINKS_MAP urls
    m = re.search(r'const\s+LINKS_MAP\s*=\s*(\{[\s\S]*?\})\s*;', content)
    if not m:
        return
    urls = re.findall(r'"url"\s*:\s*"(https?://[^"]+)"', m.group(1))
    if not urls:
        return

    print(f"  Checando {len(urls)} URLs em LINKS_MAP (HEAD timeout {timeout}s)...")
    broken = []
    for url in urls:
        try:
            req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status >= 400:
                    broken.append((url, f"HTTP {resp.status}"))
        except urllib.error.HTTPError as e:
            if e.code >= 400:
                broken.append((url, f"HTTP {e.code}"))
        except Exception as e:
            broken.append((url, f"err: {str(e)[:80]}"))

    if broken:
        for url, reason in broken[:10]:
            warn(f"Link possivelmente quebrado: {url} ({reason})")
        if len(broken) > 10:
            warn(f"... +{len(broken)-10} URLs com problema")
    else:
        ok(f"Todas {len(urls)} URLs em LINKS_MAP respondem OK")

def check_legend_no_dup(content):
    """Detecta duplicação do semáforo na legenda · pills 🟢🟡🔴 já são renderizados
    automaticamente pelo template (shell.html). Repetir em legend_notes_html polui.
    Bug recorrente: pais-sardenha (2026-05-23 fix) + Sprockhovel-2026 (2026-05-23 re-fix)."""
    m = re.search(r'class="legend-content">\s*<div class="row">.*?</div>\s*<div class="text">\s*(.*?)\s*</div>', content, re.DOTALL)
    if not m:
        warn("legend-content não encontrada (template mudou?)")
        return
    notes = m.group(1)
    redundant_patterns = [
        ('🟢 Verde', '🟢 Verde'),
        ('🟡 Amarelo', '🟡 Amarelo'),
        ('🔴 Vermelho', '🔴 Vermelho'),
        ('🟢 tranquilo', '🟢 tranquilo (já no pill acima)'),
        ('⚠️ atenção', '⚠️ atenção (já no pill acima)'),
        ('🔴 alta atenção', '🔴 alta atenção (já no pill acima)'),
    ]
    found = [label for p, label in redundant_patterns if p in notes]
    if found:
        err(f"Legenda duplicada: '{', '.join(found)}' em legend_notes_html · "
            f"pills semáforo já renderizados pelo template · remova essas strings do data.json")
    else:
        ok("Legenda sem duplicação · pills + notes complementares")

def check_maps_query(days_text):
    """BLOQUEIA texto que não é lugar sendo mandado pro Google Maps.

    Bug ago/2026 (dois prints do Tobia, em campo): o pino do card "Walking tour Cidadela ·
    com os avós" abria o Maps no meio do mar, e a rota do walking tour devolvia "Can't seem
    to find that place" porque uma parada virava a busca "Porte de Gênes entrada principal".
    O template agora limpa o nome (corta no "·", descarta parêntese descritivo), mas nome de
    card que descreve uma ATIVIDADE nunca vira lugar por limpeza — precisa de `mapsQuery`
    explícito ou `noMaps`.
    """
    if not days_text:
        return
    try:
        days = json.loads(days_text)
    except Exception:
        return
    # mesma limpeza do template (placeQuery)
    addr = re.compile(r"\d|\b(via|viale|vico|corso|piazza|piazzetta|largo|lungomare|lungofiume|"
                      r"localit[àa]|rua|avenida|rue|quai|avenue|boulevard|place|str|street|road|km)\b", re.I)
    def place_query(nome):
        s = str(nome or '').split('·')[0]
        s = re.sub(r'\([^)]*\)', lambda m: ' ' + m.group(0)[1:-1] + ' ' if addr.search(m.group(0)) else ' ', s)
        s = re.sub(r"[^\w\s\-'&.,/]", ' ', s, flags=re.UNICODE)
        return re.sub(r'\s+', ' ', s).strip()
    # nomes que descrevem atividade/logística, não lugar
    nao_lugar = re.compile(r'^(walking tour|check[- ]?(in|out)|caf[ée] da manh|despedida|fim da viagem|'
                           r'tarde livre|retorno|volta a|chegada|encontro|layby|boat tour|sesta)', re.I)
    ruins = []
    for day in days:
        for s in day.get('stops', []):
            if s.get('tipo') != 'card' or s.get('noMaps') or (s.get('mapsQuery') or '').strip():
                continue
            q = place_query(s.get('nome'))
            if not q or nao_lugar.match(q):
                ruins.append((s.get('nome', '?')[:40], q))
    if ruins:
        amostra = ' · '.join(f'"{n}" → busca {q!r}' for n, q in ruins[:3])
        err(f"{len(ruins)} card(s) mandariam texto sem sentido pro Google Maps: {amostra} · "
            f"corrija com \"mapsQuery\": \"<nome do lugar>\" ou \"noMaps\": true")
    else:
        ok("Nenhum card manda texto sem sentido pro Maps (mapsQuery/noMaps onde precisa)")


def check_wt_maps_query(days_text):
    """BLOQUEIA parada sem `mapsQuery` em walking tour e em ROAD TRIP.

    Pedido do Tobia (ago/2026), depois de dois prints em campo: *"force pra sempre verificar
    uma a uma nos walking tours ou roadtrips"*. Road trip aqui é a estrutura da skill
    `road-trip-designer`: **dia com `transport: "driving"`** (+ `baseCoord`/`baseName`) — o
    análogo de carro do walking tour. NÃO é "todo dia com dois pontos".

    Por que bloquear só nessas duas: são os dois casos em que o app monta uma ROTA de vários
    pontos encadeados. Sem `mapsQuery` em todos, a rota cai pra coordenada em silêncio e o
    Google Maps mostra "Dropped pin" — funciona, e é inútil pra quem está dirigindo.
    Exigir o campo obriga a decidir o nome ponto a ponto, que é metade da verificação; a
    outra metade (o Maps acha esse nome?) é o `FACTCHECK.md` §4a.

    Dia comum de rota vira AVISO: ganha nome quando alguém preencher, sem travar a entrega.
    Fora da regra sempre: `transit`, `noMaps` e cards 🔄 ALT.
    """
    if not days_text:
        return
    try:
        days = json.loads(days_text)
    except Exception:
        return

    def alvo(s):
        opts = s.get('opcoes') or []
        return opts[0] if (s.get('tipo') == 'opcoes' and opts) else s

    def sem_query(s):
        a = alvo(s)
        if a.get('noMaps'):
            return False
        return not ((a.get('mapsQuery') or '') or (s.get('mapsQuery') or '')).strip()

    def roteaveis(day):
        return [s for s in day.get('stops', [])
                if s.get('tipo') != 'transit' and s.get('coord') and not s.get('noMaps')
                and not (s.get('nome') or '').startswith('🔄')]

    sem_wt, sem_rt, sem_dia, tours, rts = [], [], [], 0, 0
    for day in days:
        for s in day.get('stops', []):
            for t in s.get('walkingTours', []):
                tours += 1
                for w in t.get('stops', []):
                    if not (w.get('mapsQuery') or '').strip():
                        sem_wt.append(f"{t.get('nome','?')[:22]} · {w.get('nome','?')[:26]}")
        pts = roteaveis(day)
        if len(pts) < 2:
            continue
        faltando = [f"[{day.get('date','?')}] {s.get('nome','?')[:34]}" for s in pts if sem_query(s)]
        if day.get('transport') == 'driving':      # road trip · a skill road-trip-designer
            rts += 1
            sem_rt += faltando
        else:                                       # dia comum · aviso, não trava
            sem_dia += faltando

    if sem_wt:
        err(f"{len(sem_wt)} parada(s) de WALKING TOUR sem mapsQuery — a rota cai pra coordenada "
            f'("Dropped pin" no Maps): {" · ".join(sem_wt[:3])}'
            + (f" · +{len(sem_wt)-3}" if len(sem_wt) > 3 else ""))
    elif tours:
        ok(f"Walking tours: todas as paradas com mapsQuery ({tours} tour(s))")

    if sem_rt:
        err(f"{len(sem_rt)} ponto(s) de ROAD TRIP (dia driving) sem mapsQuery — a rota do dia "
            f'vira "Dropped pin": {" · ".join(sem_rt[:3])}'
            + (f" · +{len(sem_rt)-3}" if len(sem_rt) > 3 else ""))
    elif rts:
        ok(f"Road trips: todos os pontos com mapsQuery ({rts} dia(s) driving)")

    if sem_dia:
        warn(f"{len(sem_dia)} ponto(s) de rota em dia comum sem mapsQuery — a rota funciona por "
             f'coordenada, mas o Maps mostra "Dropped pin": {sem_dia[0]}'
             + (f" · +{len(sem_dia)-1}" if len(sem_dia) > 1 else ""))


def check_no_hardcoded_region(content):
    """BLOQUEIA literal de cidade/região cravado na construção de URL do Google Maps.

    Bug ago/2026 (reportado em campo, na Córsega): o template tinha `destStr+', New York, NY'`
    em renderTransit e `clean+' New York'` no fallback de getMapsUrl — valor da PRIMEIRA viagem
    cristalizado no template. Resultado: o botão de transporte público de um roteiro na Córsega
    buscava "Praia de Rondinara, New York, NY". Passou pelo validate sem ninguém notar.

    A regra: o sufixo de região vem SEMPRE do global MAPS_REGION (via regionSuffix()), nunca de
    literal. O check varre só as linhas que montam URL de Maps — a prosa dos DAYS pode citar
    qualquer cidade à vontade, e um roteiro de NYC não é falso-positivo.
    """
    if 'MAPS_REGION' not in content:
        # Build anterior a ago/2026. Avisa (rotas por nome geocodam sem região), mas não
        # bloqueia: quem só está corrigindo uma dica num roteiro antigo não deve travar aqui.
        warn("MAPS_REGION ausente · HTML gerado por template antigo · rebuild com build.py "
             "depois de adicionar maps_region ao data.json")
        return

    # Sufixo suspeito: literal que começa com vírgula ou espaço e segue com nome próprio
    # — a forma exata de ", New York, NY" e " New York".
    suffix_re = re.compile(r"""(['"])([,\s][ ]*[A-ZÀ-Þ][A-Za-zÀ-ÿ.'\-, ]{2,30})\1""")
    offenders = []
    for i, raw in enumerate(content.split('\n'), 1):
        # tira comentário de linha · o (?<!:) evita comer a URL a partir de "https://"
        line = re.sub(r'(?<!:)//.*$', '', raw)
        if not re.search(r'google\.com/maps|encodeURIComponent', line):
            continue
        if 'MAPS_REGION' in line or 'regionSuffix' in line:
            continue                               # já usa a fonte certa
        for _, lit in suffix_re.findall(line):
            offenders.append((i, lit.strip()))

    if offenders:
        amostra = ' · '.join(f'linha {n}: "{lit}"' for n, lit in offenders[:3])
        err(f"Região hardcoded na URL do Maps ({len(offenders)} ocorrência(s)): {amostra} · "
            f"o sufixo de região tem que vir de MAPS_REGION/regionSuffix(), nunca de literal")
    else:
        ok("Sem região hardcoded nas URLs do Maps · sufixo vem de MAPS_REGION")


def check_alt_cards_excluded_from_route(content, days_text):
    """Cards 🔄 ALT devem ser EXCLUÍDOS da rota do dia (getRouteUrl).
    Convenção: cards de alternativa começam com '🔄' no nome.
    Bug Sprockhovel 2026-05-23: ALT Valenciennes virou destino da rota do sábado.
    Só verifica se a viagem usa cards 🔄 (evita ruído nas viagens antigas sem alts)."""
    has_alt_cards = '🔄' in days_text
    has_filter = 'startsWith(\'🔄\')' in content or 'startsWith("🔄")' in content
    if not has_alt_cards:
        return  # viagem sem alternativas · skip silencioso
    if has_filter:
        ok("getRouteUrl exclui cards 🔄 ALT da rota do dia")
    else:
        err("Viagem usa cards 🔄 ALT mas getRouteUrl NÃO os filtra · rota do dia vai pegar destino errado · regenerar HTML com template atual")

def check_required_features(content):
    """Verifica que features-chave existem no HTML"""
    required = {
        # Invariantes que sobrevivem à arquitetura "editorial trip journal" (redesign 2026-07)
        'AUTH_KEY persistente':       "AUTH_KEY='roteiro_auth_v1'",
        'APP_MODE (trip/city)':       'const APP_MODE',
        'centerActiveTab':            'function centerActiveTab',
        'renderInnerContent':         'function renderInnerContent',
        'getMapsUrl respeita mapsQuery': "mapsQueryOf",
        'Nome limpo pro Maps (placeQuery)': "function placeQuery",
        'Rótulo A/B/C de walking tour': "function wtLabel",
        'Popup color forçado white':  'color:#fff !important',
        'getDefaultDayIdx':           'function getDefaultDayIdx',
        'getWalkingTourUrl':          'function getWalkingTourUrl',
        'WT URL por nome de parada':  'wtStopQuery',
        'Walking tour flag':          'walking-tour-flag',
        'Search WT index':            "hay+=' walking tour '",
        'Overview WT button':         'ov-wt-btn',
        'Transit colapsável':         'stop-transit.collapsible',
        # Novos invariantes da arquitetura nova
        'Status bar':                 'function renderStatusBar',
        'dayTransport (modo do dia)': 'function dayTransport',
        'AGORA (getNowStopIdx)':      'function getNowStopIdx',
        'Feito axis (isFeito)':       'function isFeito',
        'Feito axis (localStorage)':  "'feito-'",
        'Rota por coord (api=1)':     'api=1',
        'Rota com travelmode':        'travelmode=',
        # Relato de campo · a caixa e a fila offline. O envio pode falhar (sem
        # sinal, sem URL), mas a GRAVAÇÃO local não pode sumir num rebuild.
        'Relato · caixa no dia':      'function renderRelato',
        'Relato · fila localStorage': "RELATOS_KEY='relatos_v1'",
    }
    
    for name, pattern in required.items():
        if pattern in content:
            ok(f"Feature presente: {name}")
        else:
            err(f"Feature FALTANDO: {name} (esperava '{pattern}')")

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    do_check_links = "--check-links" in flags

    if len(args) < 1:
        print(f"{C.BOLD}Uso:{C.END} python3 validate.py /path/to/index.html [--check-links]")
        print("")
        print("  --check-links: HEAD HTTP em cada URL do LINKS_MAP (warning, não bloqueia)")
        sys.exit(2)

    path = Path(args[0])
    print(f"\n{C.BOLD}=== Validando {path.name} ==={C.END}\n")

    if not check_file_exists(path):
        sys.exit(2)

    content = path.read_text(encoding='utf-8')
    
    # Estrutura
    print(f"{C.DIM}── Estrutura ──{C.END}")
    check_size(content)
    check_html_balance(content)
    
    # JS
    print(f"\n{C.DIM}── JavaScript ──{C.END}")
    check_js_syntax(content)
    
    # Dados
    print(f"\n{C.DIM}── Dados ──{C.END}")
    days_text = extract_days_array(content)
    check_coords(days_text)
    check_enums(days_text)
    check_poi_classification(days_text)
    check_walking_tours(days_text)
    check_temaCurto(days_text)
    check_no_manual_stars(days_text)
    check_maps_query(days_text)
    check_wt_maps_query(days_text)
    check_no_raw_markdown(days_text)

    # Features
    print(f"\n{C.DIM}── Features-chave ──{C.END}")
    check_required_features(content)
    check_legend_no_dup(content)
    check_no_hardcoded_region(content)
    check_alt_cards_excluded_from_route(content, days_text)

    # Links (opcional)
    if do_check_links:
        print(f"\n{C.DIM}── Links externos (LINKS_MAP) ──{C.END}")
        check_links_alive(content)
    
    # Resumo
    print(f"\n{C.BOLD}=== Resumo ==={C.END}")
    if errors:
        print(f"{C.ERR}✗ {len(errors)} erro(s){C.END}")
        for e in errors:
            print(f"  {C.ERR}•{C.END} {e}")
    if warnings:
        print(f"{C.WARN}⚠ {len(warnings)} aviso(s){C.END}")
    if not errors and not warnings:
        print(f"{C.OK}✓ Tudo limpo · pronto pra commit{C.END}")
    
    sys.exit(1 if errors else 0)

if __name__ == '__main__':
    main()
