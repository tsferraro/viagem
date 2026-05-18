#!/usr/bin/env bash
# deploy.sh — Deploy do roteiro pra tsferraro/viagem
#
# Uso:
#   deploy.sh "<commit-msg>" "<slug>" [/path/index.html] [/path/repo] [<subdir>]
#
# Args:
#   COMMIT_MSG : mensagem do commit
#   SLUG       : slug-da-viagem (ex: lisboa-ago2026)
#   SRC_HTML   : path do HTML novo (default: /tmp/build/index.html)
#   REPO_DIR   : path do repo clonado (default: ~/repos/viagem)
#   SUBDIR     : OPCIONAL · "" = roteiro principal · ex: "familia", "casal", "amigos" pra paralelo
#
# Workflow:
#   - Sem SUBDIR (principal):
#       1. Se slug atual ≠ novo: archive root em archive/<slug-atual>/
#       2. Substitui index.html raiz pelo novo
#       3. Atualiza SLUG.txt raiz
#   - Com SUBDIR (paralelo, ex: "familia"):
#       1. Cria/atualiza <SUBDIR>/index.html (sem mexer no raiz)
#       2. Atualiza <SUBDIR>/SLUG.txt
#       3. Não toca em archive (roteiros paralelos arquivam juntos quando o principal arquivar)
#   - Sempre:
#       - validate.py (BLOQUEIA se falhar)
#       - backup local em ~/.skill-backups/
#       - atualiza archive/index.html (índice navegável)
#       - git add · commit · push

set -e

COMMIT_MSG="$1"
NEW_SLUG="$2"
SRC_HTML="${3:-/tmp/build/index.html}"
REPO_DIR="${4:-$HOME/repos/viagem}"
SUBDIR="${5:-}"

if [ -z "$COMMIT_MSG" ] || [ -z "$NEW_SLUG" ]; then
  echo "Uso: deploy.sh \"<msg>\" \"<slug>\" [<html>] [<repo>] [<subdir>]"
  exit 2
fi

if [ ! -f "$SRC_HTML" ]; then
  echo "❌ HTML novo não encontrado: $SRC_HTML"
  exit 2
fi

if [ ! -d "$REPO_DIR" ]; then
  echo "❌ Repo não encontrado: $REPO_DIR"
  echo "   Rode antes: gh repo clone tsferraro/viagem $REPO_DIR"
  exit 2
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VALIDATE_PY="$SCRIPT_DIR/validate.py"
BACKUP_DIR="$HOME/.skill-backups"
mkdir -p "$BACKUP_DIR"

cd "$REPO_DIR"

# Target directory (root ou subdir)
if [ -n "$SUBDIR" ]; then
  TARGET_DIR="./$SUBDIR"
  TARGET_HTML="$TARGET_DIR/index.html"
  TARGET_SLUG_FILE="$TARGET_DIR/SLUG.txt"
  mkdir -p "$TARGET_DIR"
  echo "→ Modo PARALELO · subpasta: $SUBDIR"
else
  TARGET_DIR="."
  TARGET_HTML="./index.html"
  TARGET_SLUG_FILE="./SLUG.txt"
  echo "→ Modo PRINCIPAL · root"
fi

# --- 1. Detecta slug atual no target ---
CURRENT_SLUG=""
if [ -f "$TARGET_SLUG_FILE" ]; then
  CURRENT_SLUG=$(cat "$TARGET_SLUG_FILE" | tr -d '[:space:]')
fi

# --- 2. Archive (SÓ pro principal · paralelo não arquiva sozinho) ---
if [ -z "$SUBDIR" ] && [ -n "$CURRENT_SLUG" ] && [ "$CURRENT_SLUG" != "$NEW_SLUG" ] && [ -f "$TARGET_HTML" ]; then
  echo "→ Arquivando viagem anterior: $CURRENT_SLUG"
  mkdir -p "archive/$CURRENT_SLUG"
  cp "$TARGET_HTML" "archive/$CURRENT_SLUG/index.html"
  # Se havia subpastas paralelas, arquivar junto
  for sd in */; do
    name=$(basename "$sd")
    [ "$name" = "archive" ] && continue
    [ -f "$sd/index.html" ] || continue
    mkdir -p "archive/$CURRENT_SLUG/$name"
    cp "$sd/index.html" "archive/$CURRENT_SLUG/$name/index.html"
    rm -rf "$sd"
  done
fi

# --- 3. Substituir HTML target ---
cp "$SRC_HTML" "$TARGET_HTML"
echo "$NEW_SLUG" > "$TARGET_SLUG_FILE"
mkdir -p archive

# --- 4. Re-gerar archive/index.html (índice navegável) ---
{
  echo '<!DOCTYPE html>'
  echo '<html lang="pt-BR">'
  echo '<head>'
  echo '<meta charset="UTF-8">'
  echo '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
  echo '<meta name="robots" content="noindex,nofollow">'
  echo '<title>Arquivo de Viagens · Tobia</title>'
  echo '<style>body{font-family:-apple-system,sans-serif;max-width:600px;margin:40px auto;padding:0 20px;line-height:1.6;color:#111}h1{color:#111}ul{list-style:none;padding:0}li{padding:10px;border-bottom:1px solid #eee}a{color:#0f172a;text-decoration:none;font-weight:600}a:hover{color:#3b82f6}.meta{color:#6b7280;font-size:13px}.sub{font-size:13px;color:#6b7280;margin-left:8px}</style>'
  echo '</head><body>'
  echo '<h1>🗺️ Arquivo de Viagens</h1>'
  echo '<p class="meta">Roteiros das viagens passadas. Roteiro ativo: <a href="../">tsferraro.github.io/viagem</a></p>'
  echo '<ul>'
  for d in archive/*/; do
    [ -d "$d" ] || continue
    slug=$(basename "$d")
    # Lista paralelos se houver
    parallels=""
    for sd in "$d"/*/; do
      [ -d "$sd" ] || continue
      pname=$(basename "$sd")
      parallels="$parallels <span class=\"sub\">[<a href=\"$slug/$pname/\">$pname</a>]</span>"
    done
    echo "  <li><a href=\"$slug/\">$slug</a>$parallels</li>"
  done
  echo '</ul></body></html>'
} > archive/index.html

# --- 5. Validar ---
echo "→ Validando..."
if ! python3 "$VALIDATE_PY" "$TARGET_HTML"; then
  echo "❌ validate.py falhou · deploy ABORTADO"
  exit 1
fi

# --- 6. Backup local ---
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="viagem_${NEW_SLUG}${SUBDIR:+_$SUBDIR}_${TIMESTAMP}.html"
cp "$TARGET_HTML" "$BACKUP_DIR/$BACKUP_NAME"
echo "→ Backup: $BACKUP_DIR/$BACKUP_NAME"

# --- 7. Git commit + push ---
git add -A

if git diff --cached --quiet; then
  echo "ℹ️  Nada pra commitar — repo já está atualizado"
  exit 0
fi

git commit -m "$COMMIT_MSG"
git push origin main

echo ""
echo "✅ Deploy completo"
if [ -n "$SUBDIR" ]; then
  echo "   Live em: https://tsferraro.github.io/viagem/$SUBDIR"
else
  echo "   Live em: https://tsferraro.github.io/viagem"
fi
echo "   Arquivo: https://tsferraro.github.io/viagem/archive/"
