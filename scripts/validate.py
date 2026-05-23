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
        'AUTH_KEY persistente':       "AUTH_KEY='roteiro_auth_v1'",
        'centerActiveTab':            'function centerActiveTab',
        'renderInnerContent':         'function renderInnerContent',
        'getMapsUrl mantém parens':   "replace(/[()]/g",
        'Popup color forçado white':  'color:#fff !important',
        'getDefaultDayIdx':           'function getDefaultDayIdx',
        'getWalkingTourUrl':          'function getWalkingTourUrl',
        'Walking tour flag':          'walking-tour-flag',
        'Search WT index':            "hay+=' walking tour '",
        'Overview WT button':         'ov-wt-btn',
        'Transit colapsável':         'stop-transit.collapsible',
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
    check_walking_tours(days_text)
    check_temaCurto(days_text)
    
    # Features
    print(f"\n{C.DIM}── Features-chave ──{C.END}")
    check_required_features(content)
    check_legend_no_dup(content)
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
