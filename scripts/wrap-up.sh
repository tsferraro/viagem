#!/usr/bin/env bash
# wrap-up.sh — Protocolo de encerramento de sessão da skill itinerary-builder
#
# Uso: scripts/wrap-up.sh [/path/repo]
#
# Roda ao final de qualquer sessão que mexeu em roteiros:
#   1. git diff · mostra tudo que mudou
#   2. validate.py em cada HTML modificado
#   3. Regenera landing index.html (lista atual de viagens ativas)
#   4. Confirma git status limpo · sem branch isolada
#   5. curl HEAD nas URLs · confirma 200 OK
#   6. Imprime resumo das URLs ao Tobia
#
# NÃO atualiza MEMORY.md automaticamente — isso requer interação humana (lições subjetivas).
# Skill deve PERGUNTAR ao Tobia se quer adicionar lição ao MEMORY.md antes de chamar este script.

set -e

REPO_DIR="${1:-$HOME/repos/viagem}"
cd "$REPO_DIR"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VALIDATE_PY="$SCRIPT_DIR/validate.py"

echo "═══ 1 · Git status ═══════════════════════════════"
git status --short
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
  echo "⚠️  Você está em '$CURRENT_BRANCH' (não main). Considere merge."
fi
echo ""

echo "═══ 2 · Validate HTMLs modificados ═══════════════"
CHANGED_HTMLS=$(git diff --name-only HEAD origin/main 2>/dev/null | grep -E 'index\.html$' || true)
UNCOMMITTED_HTMLS=$(git status --porcelain | grep -E '^.[ M].*index\.html$' | awk '{print $NF}' || true)
ALL_HTMLS=$(echo -e "$CHANGED_HTMLS\n$UNCOMMITTED_HTMLS" | sort -u | grep -v '^$' || true)

if [ -z "$ALL_HTMLS" ]; then
  echo "ℹ️  Nenhum HTML modificado desde último push"
else
  for h in $ALL_HTMLS; do
    [ "$h" = "index.html" ] && continue  # landing não passa pelo validate da viagem
    if [ -f "$h" ]; then
      echo "→ $h"
      python3 "$VALIDATE_PY" "$h" 2>&1 | tail -3
    fi
  done
fi
echo ""

echo "═══ 3 · Regenerar landing (index.html no root) ═══"
python3 - <<'PYEOF'
import os, re
ROOT = os.path.expanduser('~/repos/viagem')
viagens = []
for d in sorted(os.listdir(ROOT)):
    if d in ('archive', 'scripts', 'templates', 'references', 'skills', '.git'): continue
    full = os.path.join(ROOT, d)
    html = os.path.join(full, 'index.html')
    slug_file = os.path.join(full, 'SLUG.txt')
    if not (os.path.isdir(full) and os.path.exists(html)): continue
    slug = open(slug_file).read().strip() if os.path.exists(slug_file) else d
    with open(html) as f: content = f.read()
    title_m = re.search(r'<title>([^<]+)</title>', content)
    sub_m = re.search(r'class="sub">([^<]+)</div>', content)
    h1_m = re.search(r'<h1>([^<]+)</h1>', content)
    nome = (h1_m.group(1) if h1_m else (title_m.group(1) if title_m else d)).strip()
    meta = (sub_m.group(1) if sub_m else '').strip()
    emoji_m = re.match(r'^([^\w\s]+)', nome)
    emoji = emoji_m.group(1).strip() if emoji_m else '✈️'
    nome_clean = nome.replace(emoji, '').strip().lstrip('·').strip() if emoji != '✈️' else nome
    viagens.append({'subdir': d, 'slug': slug, 'nome': nome_clean, 'meta': meta, 'emoji': emoji})

cards = ''
for v in viagens:
    cards += f'''  <a class="viagem-card" href="./{v['subdir']}/">
    <span class="viagem-chev">›</span>
    <div class="viagem-emoji">{v['emoji']}</div>
    <div class="viagem-nome">{v['nome']}</div>
    <div class="viagem-meta">{v['meta']}</div>
  </a>
'''

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
{cards}</div>

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
with open(os.path.join(ROOT, 'index.html'), 'w') as f: f.write(html)
print(f'✓ Landing regenerada com {len(viagens)} viagens: {", ".join(v["subdir"] for v in viagens)}')
PYEOF
echo ""

echo "═══ 4 · Commit + push ═════════════════════════════"
git add -A
if git diff --cached --quiet; then
  echo "ℹ️  Nada novo pra commitar"
else
  echo "Mudanças pendentes:"
  git diff --cached --name-only
  echo ""
  read -p "Commit message (Enter usa default 'chore: wrap-up sessão'): " MSG
  MSG=${MSG:-"chore: wrap-up sessão"}
  git commit -m "$MSG"
  git push origin main
fi
echo ""

echo "═══ 5 · URLs ao vivo ══════════════════════════════"
sleep 5  # propagar Pages
echo "Landing:  https://tsferraro.github.io/viagem"
curl -sI https://tsferraro.github.io/viagem/ | head -1 | sed 's/^/  /'
for d in $(ls -d */); do
  d=${d%/}
  [ "$d" = "archive" ] || [ "$d" = "scripts" ] || [ "$d" = "templates" ] || [ "$d" = "references" ] || [ "$d" = "skills" ] && continue
  echo "Viagem $d:  https://tsferraro.github.io/viagem/$d"
  curl -sI "https://tsferraro.github.io/viagem/$d/" | head -1 | sed 's/^/  /'
done
echo ""
echo "═══ ✅ Wrap-up completo ═══════════════════════════"
