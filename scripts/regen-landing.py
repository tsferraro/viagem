#!/usr/bin/env python3
"""
regen-landing.py — Regenera o index.html da raiz com lista de todas as viagens

Lê cada subpasta que NÃO é reservada (archive/scripts/templates/references/skills),
verifica se tem index.html + SLUG.txt, e monta a landing.

Uso:
    python3 scripts/regen-landing.py [/path/repo]

Roda automaticamente em:
- scripts/deploy.sh  (após copiar HTML + SLUG.txt da viagem)
- scripts/wrap-up.sh (no protocolo de encerramento)
"""

import os, re, sys

RESERVED = {'archive', 'scripts', 'templates', 'references', 'skills', '.git'}

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
        with open(html) as f: c = f.read()
        h1 = re.search(r'<h1>([^<]+)</h1>', c)
        sub = re.search(r'class="sub">([^<]+)</div>', c)
        nome = (h1.group(1) if h1 else d).strip()
        meta = (sub.group(1) if sub else '').strip()
        # Extrai emoji (1º char não-ASCII) se houver
        emoji = '✈️'
        nome_clean = nome
        if nome and ord(nome[0]) > 127:
            i = 0
            while i < len(nome) and ord(nome[i]) > 127:
                i += 1
            emoji = nome[:i].strip()
            nome_clean = nome[i:].lstrip(' ·-—').strip() or d
        viagens.append({'subdir': d, 'slug': slug, 'nome': nome_clean, 'meta': meta, 'emoji': emoji})

    # Ordenação cronológica · próxima viagem primeiro (ascendente por ano/mês/dia)
    viagens.sort(key=lambda v: parse_chronologic_key(v['slug'], v['meta']))

    cards = '\n'.join(
        f'''  <a class="viagem-card" href="./{v['subdir']}/">
    <span class="viagem-chev">›</span>
    <div class="viagem-emoji">{v['emoji']}</div>
    <div class="viagem-nome">{v['nome']}</div>
    <div class="viagem-meta">{v['meta']}</div>
  </a>'''
        for v in viagens
    )

    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<title>🗺️ Roteiros · Família Ferraro</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#f3f4f6;color:#111827;line-height:1.6;padding:24px 16px;max-width:560px;margin:0 auto;min-height:100vh}}
h1{{font-size:24px;font-weight:700;letter-spacing:-0.5px;margin-bottom:6px}}
.sub{{color:#6b7280;font-size:14px;margin-bottom:28px}}
h2{{font-size:14px;font-weight:600;color:#6b7280;text-transform:uppercase;letter-spacing:0.5px;margin:28px 0 12px}}
.viagens{{display:flex;flex-direction:column;gap:10px}}
.viagem-card{{display:block;background:#fff;border-radius:12px;padding:18px 20px;text-decoration:none;color:#111827;box-shadow:0 1px 3px rgba(0,0,0,0.05);transition:transform 0.15s,box-shadow 0.15s}}
.viagem-card:hover{{transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,0,0,0.08)}}
.viagem-emoji{{font-size:28px;margin-bottom:6px}}
.viagem-nome{{font-size:18px;font-weight:700;letter-spacing:-0.3px}}
.viagem-meta{{font-size:13px;color:#6b7280;margin-top:3px}}
.viagem-chev{{float:right;color:#9ca3af;font-size:18px;margin-top:6px}}
.footer{{margin-top:40px;padding-top:20px;border-top:1px solid #e5e7eb;font-size:12px;color:#9ca3af;text-align:center}}
.footer a{{color:#6b7280;text-decoration:none}}
</style>
</head>
<body>
<h1>🗺️ Roteiros</h1>
<div class="sub">Família Ferraro · viagens em planejamento e ativas</div>

<h2>✈️ Viagens</h2>
<div class="viagens">
{cards}
</div>

<h2>📦 Arquivo</h2>
<div class="viagens">
  <a class="viagem-card" href="./archive/">
    <span class="viagem-chev">›</span>
    <div class="viagem-emoji">📋</div>
    <div class="viagem-nome">Viagens passadas</div>
    <div class="viagem-meta">Histórico completo</div>
  </a>
</div>

<div class="footer">
  Roteiros gerados pela skill <a href="https://github.com/tsferraro/viagem" target="_blank">itinerary-builder</a>
</div>
</body>
</html>
'''
    with open(os.path.join(root, 'index.html'), 'w') as f: f.write(html)
    print(f'✓ Landing regenerada com {len(viagens)} viagem(ns): {", ".join(v["subdir"] for v in viagens)}')

if __name__ == '__main__':
    main()
