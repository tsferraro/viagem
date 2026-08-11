#!/usr/bin/env python3
"""
regen-landing.py — Regenera o index.html da raiz com lista de todas as viagens

Lê cada subpasta que NÃO é reservada (archive/scripts/templates/references/skills/entregas),
verifica se tem index.html + SLUG.txt, e monta a landing.

Uso:
    python3 scripts/regen-landing.py [/path/repo]

Roda automaticamente em:
- scripts/deploy.sh  (após copiar HTML + SLUG.txt da viagem)
- scripts/wrap-up.sh (no protocolo de encerramento)
"""

import os, re, sys

RESERVED = {'archive', 'scripts', 'templates', 'references', 'skills', 'entregas', 'fontes', '.git', 'nyc-lab-bold', 'nyc-lab-evo', 'nyc-lab-hibrido'}

# Map de mês PT-BR (3 letras) → número
MONTH_MAP = {'jan':1, 'fev':2, 'mar':3, 'abr':4, 'mai':5, 'jun':6,
             'jul':7, 'ago':8, 'set':9, 'out':10, 'nov':11, 'dez':12}

def parse_chronologic_key(slug, meta):
    """Extrai (ano, mes, dia) pra ordenação cronológica · prioriza META (mais preciso).
    Padrões META suportados:
      - '3-13 Julho 2026'        → dia 3, mês julho
      - '27/Jul → 08/Ago'        → dia 27, mês jul
      - '06/Ago → 21/Ago · 16 d' → dia 6, mês ago
      - '5 setembro 2026'        → dia 5, mês setembro
      - 'Julho 2026'             → dia 1, mês julho
    Fallback: slug ('*-<mes3letras><ano>'). Sem nada parseável: (9999,99,99) vai no fim."""
    import re as _re
    ml = (meta or '').lower().strip()
    sl = (slug or '').lower()

    # 1 · Pegar ano do slug primeiro (mais confiável que meta)
    ano_m = _re.search(r'(\d{4})$', sl)
    ano = int(ano_m.group(1)) if ano_m else 9999

    # 2 · Pegar mês: tentar meta primeiro, depois slug
    mes = 99
    # Procura abreviação 3 letras OU nome completo no meta
    mes_meses = {**MONTH_MAP,
                 'janeiro':1, 'fevereiro':2, 'março':3, 'marco':3, 'abril':4, 'maio':5, 'junho':6,
                 'julho':7, 'agosto':8, 'setembro':9, 'outubro':10, 'novembro':11, 'dezembro':12}
    for nome_mes, num in sorted(mes_meses.items(), key=lambda x: -len(x[0])):
        if _re.search(rf'\b{nome_mes}\b', ml):
            mes = num
            break
    # Se não achou no meta, pega do slug
    if mes == 99:
        slug_m = _re.search(r'([a-z]{3})\d{4}$', sl)
        if slug_m: mes = MONTH_MAP.get(slug_m.group(1), 99)

    # 3 · Pegar dia inicial do meta: primeiro número 1-31 seguido de separador
    dia = 99
    if ml:
        # Aceita "3-13", "27/Jul", "06/Ago", "5 setembro", "5 de junho"
        m_dia = _re.search(r'(?:^|[^0-9])(\d{1,2})[/\-–\s]', ' ' + ml)
        if m_dia:
            d = int(m_dia.group(1))
            if 1 <= d <= 31: dia = d

    if ano == 9999 and mes == 99: return (9999, 99, 99)
    return (ano, mes, dia)

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/repos/viagem')
    if not os.path.isdir(root):
        print(f'❌ Repo não encontrado: {root}', file=sys.stderr)
        sys.exit(2)

    viagens = []
    for d in sorted(os.listdir(root)):
        if d in RESERVED or d.startswith('.'): continue
        full = os.path.join(root, d)
        html = os.path.join(full, 'index.html')
        slug_f = os.path.join(full, 'SLUG.txt')
        if not (os.path.isdir(full) and os.path.exists(html)): continue
        slug = open(slug_f).read().strip() if os.path.exists(slug_f) else d
        city_f = os.path.join(full, 'CITY.txt')
        city = open(city_f).read().strip() if os.path.exists(city_f) else None
        with open(html) as f: c = f.read()
        # Suporta 2 layouts: antigo (<h1>/class="sub") e novo template (brand-title/brand-sub/brand-mark)
        h1 = re.search(r'class="brand-title">([^<]+)<', c) or re.search(r'<h1[^>]*>([^<]+)</h1>', c)
        sub = re.search(r'class="brand-sub">([^<]+)<', c) or re.search(r'class="sub">([^<]+)</div>', c)
        brand = re.search(r'class="brand-mark">([^<]+)<', c)  # emoji separado no novo design
        nome = (h1.group(1) if h1 else d).strip()
        meta = (sub.group(1) if sub else '').strip()
        emoji = '✈️'
        nome_clean = nome
        if brand and brand.group(1).strip():
            # novo design: emoji vem do brand-mark, nome fica inteiro
            emoji = brand.group(1).strip()
        elif nome and ord(nome[0]) > 127:
            # design antigo: 1º char(es) não-ASCII do <h1>
            i = 0
            while i < len(nome) and ord(nome[i]) > 127:
                i += 1
            emoji = nome[:i].strip()
            nome_clean = nome[i:].lstrip(' ·-—').strip() or d
        viagens.append({'subdir': d, 'slug': slug, 'nome': nome_clean, 'meta': meta, 'emoji': emoji, 'city': city})

    def render_card(v):
        return f'''  <a class="viagem-card" href="./{v['subdir']}/">
    <span class="viagem-chev">›</span>
    <div class="viagem-emoji">{v['emoji']}</div>
    <div class="viagem-nome">{v['nome']}</div>
    <div class="viagem-meta">{v['meta']}</div>
  </a>'''

    def render_section(title, items):
        inner = '\n'.join(render_card(v) for v in items)
        return f'<section class="trip-section">\n<h2>{title}</h2>\n<div class="viagens">\n{inner}\n</div>\n</section>'

    # Emoji por cidade (seções tipo "Paris · passeios") · default 📍
    CITY_EMOJI = {'Paris': '🗼', 'Nova York': '🗽', 'Lisboa': '🇵🇹'}

    # Viagens sem cidade = trips datados (ordem cronológica) · com cidade = coletâneas de passeios
    sem_cidade = [v for v in viagens if not v.get('city')]
    sem_cidade.sort(key=lambda v: parse_chronologic_key(v['slug'], v['meta']))

    from collections import OrderedDict
    grupos = OrderedDict()
    for v in viagens:
        if v.get('city'):
            grupos.setdefault(v['city'], []).append(v)

    STYLE = '''*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#f3f4f6;color:#111827;line-height:1.6;padding:24px 16px;max-width:560px;margin:0 auto;min-height:100vh}
h1{font-size:24px;font-weight:700;letter-spacing:-0.5px;margin-bottom:6px}
.sub{color:#6b7280;font-size:14px;margin-bottom:28px}
h2{font-size:14px;font-weight:600;color:#6b7280;text-transform:uppercase;letter-spacing:0.5px;margin:28px 0 12px}
.viagens{display:flex;flex-direction:column;gap:10px}
.viagem-card{display:block;background:#fff;border-radius:12px;padding:18px 20px;text-decoration:none;color:#111827;box-shadow:0 1px 3px rgba(0,0,0,0.05);transition:transform 0.15s,box-shadow 0.15s}
.viagem-card:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,0,0,0.08)}
.viagem-emoji{font-size:28px;margin-bottom:6px}
.viagem-nome{font-size:18px;font-weight:700;letter-spacing:-0.3px}
.viagem-meta{font-size:13px;color:#6b7280;margin-top:3px}
.viagem-chev{float:right;color:#9ca3af;font-size:18px;margin-top:6px}
.footer{margin-top:40px;padding-top:20px;border-top:1px solid #e5e7eb;font-size:12px;color:#9ca3af;text-align:center}
.footer a{color:#6b7280;text-decoration:none}
.search-box{position:relative;margin-bottom:24px}
.search-box input{width:100%;background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px 14px 42px;font-size:15px;font-family:inherit;color:#111827;box-shadow:0 1px 3px rgba(0,0,0,0.05);outline:none}
.search-box input:focus{border-color:#9ca3af}
.search-box .ico{position:absolute;left:15px;top:50%;transform:translateY(-50%);font-size:16px;opacity:.6}
.search-empty{display:none;color:#9ca3af;font-size:14px;text-align:center;padding:24px 0}'''

    SCRIPT = '''<script>
// Busca · filtra os cards de viagem/passeio por nome + descrição
(function(){
  var input=document.getElementById('trip-search');
  var empty=document.getElementById('search-empty');
  if(!input) return;
  input.addEventListener('input',function(){
    var q=input.value.toLowerCase().trim();
    var anyVisible=false;
    document.querySelectorAll('.trip-section').forEach(function(sec){
      var secVisible=false;
      sec.querySelectorAll('.viagem-card').forEach(function(card){
        var hit=!q||card.textContent.toLowerCase().indexOf(q)>=0;
        card.style.display=hit?'':'none';
        if(hit) secVisible=true;
      });
      sec.style.display=secVisible?'':'none';
      if(secVisible) anyVisible=true;
    });
    empty.style.display=anyVisible?'none':'block';
  });
})();
</script>'''

    def page(title, h1, sub, body):
        return ('<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n'
                '<meta charset="UTF-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n'
                '<meta name="robots" content="noindex,nofollow">\n'
                f'<title>{title}</title>\n<style>\n{STYLE}\n</style>\n</head>\n<body>\n'
                f'<h1>{h1}</h1>\n<div class="sub">{sub}</div>\n\n'
                '<div class="search-box">\n  <span class="ico">🔍</span>\n'
                '  <input type="text" id="trip-search" placeholder="Buscar passeio..." autocomplete="off">\n</div>\n'
                '<div class="search-empty" id="search-empty">Nada encontrado.</div>\n\n'
                f'{body}\n\n'
                '<div class="footer">\n  Roteiros gerados pela skill '
                '<a href="https://github.com/tsferraro/viagem" target="_blank">roteiro-viagem</a>\n</div>\n\n'
                f'{SCRIPT}\n</body>\n</html>\n')

    ARCHIVE = ('<h2>📦 Arquivo</h2>\n<div class="viagens">\n'
               '  <a class="viagem-card" href="./archive/">\n'
               '    <span class="viagem-chev">›</span>\n'
               '    <div class="viagem-emoji">📋</div>\n'
               '    <div class="viagem-nome">Viagens passadas</div>\n'
               '    <div class="viagem-meta">Histórico completo</div>\n  </a>\n</div>')

    def slugify(s):
        import unicodedata
        s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
        return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

    def render_city_card(emoji, cidade, n, fname):
        plural = 'passeio' if n == 1 else 'passeios'
        return (f'  <a class="viagem-card" href="./{fname}">\n'
                f'    <span class="viagem-chev">›</span>\n'
                f'    <div class="viagem-emoji">{emoji}</div>\n'
                f'    <div class="viagem-nome">{cidade}</div>\n'
                f'    <div class="viagem-meta">{n} {plural} · página separada pra compartilhar</div>\n  </a>')

    # 1 · Landing principal · viagens datadas inline · cada CIDADE vira 1 card → sua página
    # (os roteiros da cidade NÃO aparecem aqui · só na página da seção · pedido Tobia 2026-06-07)
    sections = []
    if sem_cidade:
        sections.append(render_section('✈️ Viagens', sem_cidade))
    city_cards = []
    for cidade in sorted(grupos):
        emoji = CITY_EMOJI.get(cidade, '📍')
        fname = slugify(cidade) + '.html'
        city_cards.append(render_city_card(emoji, cidade, len(grupos[cidade]), fname))
    if city_cards:
        sections.append('<section class="trip-section">\n<h2>🌍 Cidades</h2>\n'
                        '<div class="viagens">\n' + '\n'.join(city_cards) + '\n</div>\n</section>')
    body_main = '\n\n'.join(sections) + '\n\n' + ARCHIVE
    with open(os.path.join(root, 'index.html'), 'w') as f:
        f.write(page('🗺️ Roteiros · Família Ferraro', '🗺️ Roteiros',
                     'Família Ferraro · viagens em planejamento e ativas', body_main))

    # 2 · Uma página STANDALONE por cidade (link separado pra compartilhar · só os passeios daquela cidade)
    city_pages = []
    for cidade in sorted(grupos):
        items = sorted(grupos[cidade], key=lambda v: v['nome'])
        emoji = CITY_EMOJI.get(cidade, '📍')
        body_city = render_section(f'{emoji} {cidade} · passeios', items)
        fname = slugify(cidade) + '.html'
        with open(os.path.join(root, fname), 'w') as f:
            f.write(page(f'{emoji} {cidade} · Passeios', f'{emoji} {cidade}',
                         f'Passeios da Família Ferraro em {cidade}', body_city))
        city_pages.append(fname)

    extra = f' · páginas por cidade: {", ".join(city_pages)}' if city_pages else ''
    print(f'✓ Landing regenerada com {len(viagens)} viagem(ns): {", ".join(v["subdir"] for v in viagens)}{extra}')

if __name__ == '__main__':
    main()
