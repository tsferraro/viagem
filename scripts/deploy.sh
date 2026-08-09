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

if [ "$SUBDIR" = "archive" ] || [ "$SUBDIR" = "scripts" ] || [ "$SUBDIR" = "templates" ] || [ "$SUBDIR" = "references" ] || [ "$SUBDIR" = "skills" ] || [ "$SUBDIR" = "entregas" ] || [ "$SUBDIR" = "fontes" ]; then
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

# Validar (estrutural · bloqueia sempre que falhar)
echo "→ Validando (estrutura)..."
python3 "$VALIDATE_PY" "$TARGET_HTML" || { echo "❌ validate.py falhou · ABORTADO"; exit 1; }

# Gate de CONTEÚDO (critico-roteiro · advisory): roda no HTML que vai pro ar.
# Bloqueia SÓ em P0 (erro objetivo: card vazio, link oficial morto). Nota < 32 vira
# aviso — a régua de 32 é enforçada no LOOP da sessão, não no push (heurística mole
# não deve brickar o acesso da família). VIAGEM_STRICT=1 endurece (bloqueia < 32).
AUDIT_PY="$REPO_DIR/skills/critico-roteiro/audit.py"
if [ -f "$AUDIT_PY" ]; then
  echo "→ Gate de conteúdo (critico-roteiro)..."
  python3 "$AUDIT_PY" "$TARGET_HTML" --deploy-gate \
    || { echo "❌ Gate de conteúdo BLOQUEOU (P0 · erro objetivo) · ABORTADO"; exit 1; }
else
  echo "⚠️  critico-roteiro não encontrado · pulando gate de conteúdo"
fi

# Gate de MAPAS (maps-audit.py): monta as URLs do Google Maps como o app monta e bloqueia
# busca genérica / waypoint fantasma / ponto repetido. Existe porque validate e audit leem o
# DADO, e os bugs de ago/2026 (pino no mar, "Can't find that place") só existiam na URL final.
MAPS_PY="$SCRIPT_DIR/maps-audit.py"
if [ -f "$MAPS_PY" ]; then
  echo "→ Gate de mapas (maps-audit)..."
  python3 "$MAPS_PY" "$TARGET_HTML" --quiet \
    || { echo "❌ Gate de mapas BLOQUEOU · corrija com mapsQuery/noMaps · ABORTADO"; exit 1; }
else
  echo "⚠️  maps-audit.py não encontrado · pulando gate de mapas"
fi

# Gate de FACTCHECK (frescor+formato · R6 auditoria 2026-08-08): verificação sem artefato
# não conta. Bloqueia se não existe <viagem>/FACTCHECK-*.md, se o formato não tem vereditos
# por item com fonte, ou se conteúdo sensível (⭐⭐⭐/WT/historia) mudou depois do último
# factcheck. Cobra timestamp+estrutura (não gameable por substring); a VERDADE do factcheck
# é trabalho da sessão auditora. Ver skills/critico-roteiro/FACTCHECK-EXEC.md.
FCGATE_PY="$SCRIPT_DIR/factcheck-gate.py"
if [ -f "$FCGATE_PY" ]; then
  echo "→ Gate de factcheck (frescor+formato)..."
  python3 "$FCGATE_PY" "$TARGET_DIR" --quiet \
    || { echo "❌ Gate de factcheck BLOQUEOU · rode o FACTCHECK-EXEC e versione o artefato · ABORTADO"; exit 1; }
else
  echo "⚠️  factcheck-gate.py não encontrado · pulando gate de factcheck"
fi

# Regenerar landing AUTOMATICAMENTE (lê todas subpastas atuais + monta cards)
# Decisão 2026-05-23: integrado ao deploy pra nunca esquecer · sessão Sardenha esqueceu rodar wrap-up
echo "→ Regenerando landing (index.html root)..."
python3 "$SCRIPT_DIR/regen-landing.py" "$REPO_DIR"

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
