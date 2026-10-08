#!/usr/bin/env bash
# wrap-up.sh — Protocolo de encerramento de sessão da skill roteiro-viagem
#
# Uso: scripts/wrap-up.sh [/path/repo]
#   repo default: o repo ou worktree que contém este script
#
# Roda ao final de qualquer sessão que mexeu em roteiros:
#   1. git status + pré-voo (origin/main tem que estar contido em HEAD · senão PARA)
#   2. validate.py em cada HTML modificado
#   3. regen-landing.py (segurança extra · deploy.sh já chama, mas reforça)
#   4. git commit (interativo) na branch ATUAL + push HEAD:main + relê o remoto
#   5. curl HEAD nas URLs (a URL responde · NÃO prova versão nova · a prova é o passo 4)
#
# Publicação (2026-10-08 · mesmo padrão do deploy.sh, commit 4adefe5): funciona igual no
# checkout principal e num git worktree (branch claude/...). Antes, `git push origin main`
# num worktree empurrava o ref `main` local, parado: "Everything up-to-date", e o passo 5
# dava HTTP 200 com a versão VELHA no ar — confirmação falsa. E com "nada novo pra
# commitar" um commit local nunca publicado ficava pra trás. Agora o ✅ de publicação só
# sai se origin/main, relido do remoto depois do push, for igual ao HEAD.

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VALIDATE_PY="$SCRIPT_DIR/validate.py"
REGEN_PY="$SCRIPT_DIR/regen-landing.py"

# Repo: o default antigo (~/repos/viagem) não existe mais · o repo é o que contém o script.
REPO_DIR="${1:-$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || true)}"
[ -z "$REPO_DIR" ] || [ ! -d "$REPO_DIR" ] && { echo "❌ Repo não encontrado: ${REPO_DIR:-(nenhum)}"; exit 2; }
REPO_DIR="$(cd "$REPO_DIR" && pwd)"
cd "$REPO_DIR"

echo "═══ 1 · Git status + pré-voo ═════════════════════"
git status --short
# Pré-voo ANTES de mexer em arquivo (o passo 3 regenera a landing): publicar = empurrar
# HEAD:main, então origin/main tem que estar contido em HEAD (fast-forward).
CUR_BRANCH="$(git symbolic-ref --short -q HEAD || true)"
echo "→ Branch: ${CUR_BRANCH:-(HEAD destacado)} · publica com: git push origin HEAD:main"
if ! git fetch -q origin main; then
  echo "❌ git fetch origin main falhou (rede/credencial) · ABORTADO antes de mexer em arquivo"
  exit 1
fi
if ! git merge-base --is-ancestor origin/main HEAD; then
  echo "❌ origin/main tem commits que esta branch (${CUR_BRANCH:-HEAD}) não tem · ABORTADO"
  echo "   Publicar agora seria recusado (não é fast-forward) ou apagaria trabalho de outra sessão."
  echo "   Traga o remoto pra cá e rode o wrap-up de novo:"
  echo "     git merge origin/main"
  exit 1
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

echo "═══ 4 · Commit + publicar (HEAD:main) ═══════════"
git add -A
if git diff --cached --quiet; then
  echo "ℹ️  Nada novo pra commitar · conferindo se HEAD já está no ar"
else
  echo "Mudanças pendentes:"
  git diff --cached --name-only
  echo ""
  # `|| true`: sem terminal (stdin fechado/EOF) o read falha e o set -e matava o script aqui.
  read -r -p "Commit message (Enter usa default 'chore: wrap-up sessão'): " MSG || true
  MSG=${MSG:-"chore: wrap-up sessão"}
  git commit -m "$MSG"
fi
LOCAL_SHA="$(git rev-parse HEAD)"
REMOTE_BEFORE="$(git ls-remote origin refs/heads/main | cut -f1)"
if [ "$REMOTE_BEFORE" = "$LOCAL_SHA" ]; then
  echo "ℹ️  Nada a publicar · origin/main já está em ${LOCAL_SHA:0:7} (o que está no ar já é isto)"
  PUBLICADO="já estava no ar (${LOCAL_SHA:0:7})"
else
  if ! git push origin HEAD:main; then
    echo ""
    echo "❌ git push recusado · NADA foi publicado"
    echo "   Commit ${LOCAL_SHA:0:7} ficou só em ${CUR_BRANCH:-HEAD} (local)."
    echo "   Se o remoto andou no meio do wrap-up: git merge origin/main e rode de novo."
    exit 1
  fi
  # Prova: lê o remoto de novo. Só conta como publicado se origin/main AGORA é o HEAD.
  REMOTE_AFTER="$(git ls-remote origin refs/heads/main | cut -f1)"
  if [ "$REMOTE_AFTER" != "$LOCAL_SHA" ]; then
    echo ""
    echo "❌ Push terminou, mas origin/main = ${REMOTE_AFTER:-(ilegível)} ≠ ${LOCAL_SHA} · publicação NÃO confirmada"
    exit 1
  fi
  echo "✅ Publicado · origin/main ${REMOTE_BEFORE:0:7} → ${LOCAL_SHA:0:7}"
  PUBLICADO="${REMOTE_BEFORE:0:7} → ${LOCAL_SHA:0:7}"
fi

# Num worktree, o ref `main` local e o checkout principal ficam pra trás do que foi publicado.
# Avança o checkout principal só se ele estiver limpo e for fast-forward · senão, avisa.
if [ "$CUR_BRANCH" != "main" ]; then
  MAIN_WT="$(git worktree list --porcelain | awk '/^worktree /{p=substr($0,10)} /^branch refs\/heads\/main$/{print p; exit}')"
  if [ -n "$MAIN_WT" ]; then
    if [ -z "$(git -C "$MAIN_WT" status --porcelain --untracked-files=no)" ] \
       && git -C "$MAIN_WT" merge -q --ff-only origin/main 2>/dev/null; then
      echo "→ Checkout principal em ${LOCAL_SHA:0:7}: $MAIN_WT"
    else
      echo "⚠️  Checkout principal NÃO avançado (tem mudança local ou não é fast-forward): $MAIN_WT"
      echo "   O que está no ar está certo · só a cópia local ficou atrás. Lá: git merge --ff-only origin/main"
    fi
  elif git show-ref -q --verify refs/heads/main && git merge-base --is-ancestor main origin/main; then
    git branch -f main origin/main >/dev/null && echo "→ Ref main local avançado pra ${LOCAL_SHA:0:7}"
  fi
fi
echo ""

echo "═══ 5 · URLs ao vivo ══════════════════════════════"
echo "(HTTP 200 = a URL responde · NÃO prova que a versão nova já está servida — o Pages leva"
echo " ~1min pra rebuildar. A prova da publicação é o origin/main relido no passo 4.)"
echo "Landing:  https://tsferraro.github.io/viagem"
curl -sI https://tsferraro.github.io/viagem/ | head -1 | sed 's/^/  /'
for d in $(ls -d */); do
  d=${d%/}
  case "$d" in archive|scripts|templates|references|skills|entregas|fontes|handoffs) continue ;; esac
  echo "Viagem $d:  https://tsferraro.github.io/viagem/$d"
  curl -sI "https://tsferraro.github.io/viagem/$d/" | head -1 | sed 's/^/  /'
done
echo ""
echo "═══ ✅ Wrap-up completo · publicação: $PUBLICADO ═══"
