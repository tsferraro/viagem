#!/usr/bin/env bash
# wrap-up.sh — Protocolo de encerramento de sessão da skill roteiro-viagem
#
# Uso: scripts/wrap-up.sh [/path/repo]
#
# Roda ao final de qualquer sessão que mexeu em roteiros:
#   1. git status · mostra tudo modificado
#   2. validate.py em cada HTML modificado
#   3. regen-landing.py (segurança extra · deploy.sh já chama, mas reforça)
#   4. git commit + push (interativo)
#   5. curl HEAD nas URLs · confirma HTTP 200 + reporta ao Tobia

set -e

REPO_DIR="${1:-$HOME/repos/viagem}"
cd "$REPO_DIR"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VALIDATE_PY="$SCRIPT_DIR/validate.py"
REGEN_PY="$SCRIPT_DIR/regen-landing.py"

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

echo "═══ 3 · Regenerar landing (segurança extra) ══════"
python3 "$REGEN_PY" "$REPO_DIR"
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
echo "Landing:  https://tsferraro.github.io/viagem"
curl -sI https://tsferraro.github.io/viagem/ | head -1 | sed 's/^/  /'
for d in $(ls -d */); do
  d=${d%/}
  if [ "$d" = "archive" ] || [ "$d" = "scripts" ] || [ "$d" = "templates" ] || [ "$d" = "references" ] || [ "$d" = "skills" ]; then continue; fi
  echo "Viagem $d:  https://tsferraro.github.io/viagem/$d"
  curl -sI "https://tsferraro.github.io/viagem/$d/" | head -1 | sed 's/^/  /'
done
echo ""
echo "═══ ✅ Wrap-up completo ═══════════════════════════"
