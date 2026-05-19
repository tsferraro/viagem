#!/usr/bin/env bash
# deploy.sh — Deploy de roteiro pra subpasta em tsferraro/viagem
#
# Uso:
#   deploy.sh "<commit-msg>" "<subdir>" "<slug>" [/path/index.html] [/path/repo]
#
# Args:
#   COMMIT_MSG : mensagem do commit
#   SUBDIR     : subpasta da viagem (ex: nyc, corsica, sardenha, corsica-amigos)
#   SLUG       : slug-da-viagem (ex: nyc-jul2026)
#   SRC_HTML   : path do HTML novo (default: /tmp/build/index.html)
#   REPO_DIR   : path do repo clonado (default: ~/repos/viagem)
#
# Regra (decisão 2026-05-19): TODA viagem vive em subpasta dedicada desde o nascimento.
# Root tem só landing (index.html com lista de viagens ativas).
# Arquivamento manual: skill move <subdir>/ pra archive/<slug>/ ao final da viagem.

set -e

COMMIT_MSG="$1"
SUBDIR="$2"
NEW_SLUG="$3"
SRC_HTML="${4:-/tmp/build/index.html}"
REPO_DIR="${5:-$HOME/repos/viagem}"

if [ -z "$COMMIT_MSG" ] || [ -z "$SUBDIR" ] || [ -z "$NEW_SLUG" ]; then
  echo "Uso: deploy.sh \"<msg>\" \"<subdir>\" \"<slug>\" [<html>] [<repo>]"
  echo "Ex:  deploy.sh \"feat: corsica 13d\" \"corsica\" \"corsica-jul2026\""
  exit 2
fi

if [ "$SUBDIR" = "archive" ] || [ "$SUBDIR" = "scripts" ] || [ "$SUBDIR" = "templates" ] || [ "$SUBDIR" = "references" ] || [ "$SUBDIR" = "skills" ]; then
  echo "❌ SUBDIR '$SUBDIR' é reservado · use nome de viagem (nyc, corsica, etc)"
  exit 2
fi

[ ! -f "$SRC_HTML" ] && { echo "❌ HTML não encontrado: $SRC_HTML"; exit 2; }
[ ! -d "$REPO_DIR" ] && { echo "❌ Repo não encontrado: $REPO_DIR"; exit 2; }

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VALIDATE_PY="$SCRIPT_DIR/validate.py"
BACKUP_DIR="$HOME/.skill-backups"
mkdir -p "$BACKUP_DIR"

cd "$REPO_DIR"

TARGET_DIR="./$SUBDIR"
TARGET_HTML="$TARGET_DIR/index.html"
TARGET_SLUG="$TARGET_DIR/SLUG.txt"
mkdir -p "$TARGET_DIR"

echo "→ Subpasta: $SUBDIR · slug: $NEW_SLUG"

cp "$SRC_HTML" "$TARGET_HTML"
echo "$NEW_SLUG" > "$TARGET_SLUG"

# Validar
echo "→ Validando..."
python3 "$VALIDATE_PY" "$TARGET_HTML" || { echo "❌ validate.py falhou · ABORTADO"; exit 1; }

# Backup local
TS=$(date +%Y%m%d_%H%M%S)
cp "$TARGET_HTML" "$BACKUP_DIR/${SUBDIR}_${NEW_SLUG}_${TS}.html"
echo "→ Backup: $BACKUP_DIR/${SUBDIR}_${NEW_SLUG}_${TS}.html"

# Git commit + push (sempre em main)
git add -A
if git diff --cached --quiet; then
  echo "ℹ️  Nada pra commitar"; exit 0
fi
git commit -m "$COMMIT_MSG"
git push origin main

echo ""
echo "✅ Deploy completo"
echo "   URL: https://tsferraro.github.io/viagem/$SUBDIR"
echo "   Landing: https://tsferraro.github.io/viagem (lista todas)"
