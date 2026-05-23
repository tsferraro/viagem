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
