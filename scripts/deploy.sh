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
#   SRC_HTML   : path do HTML novo (default: <repo>/<subdir>/index.html, o que o build.py
#                acabou de gerar · se não existir, $TMPDIR/build/index.html). Pode ser o
#                próprio <subdir>/index.html — aí não há cópia.
#   REPO_DIR   : path do repo (default: o repo ou worktree que contém este script)
#
# Publicação (2026-10-08): commita na branch ATUAL e empurra `HEAD:main`, só fast-forward.
# Funciona igual no checkout principal e num git worktree (branch claude/...). Antes,
# `git push origin main` num worktree empurrava o ref `main` local, parado: "Everything
# up-to-date" + "✅ Deploy completo" e nada no ar. Agora o ✅ só sai se origin/main, lido
# do remoto depois do push, for igual ao commit publicado.
#
# Regra (decisão 2026-05-19): TODA viagem vive em subpasta dedicada desde o nascimento.
# Root tem só landing (index.html com lista de viagens ativas).
# Arquivamento manual: skill move <subdir>/ pra archive/<slug>/ ao final da viagem.

set -e

COMMIT_MSG="$1"
SUBDIR="$2"
NEW_SLUG="$3"
SRC_HTML="$4"
REPO_DIR="$5"

if [ -z "$COMMIT_MSG" ] || [ -z "$SUBDIR" ] || [ -z "$NEW_SLUG" ]; then
  echo "Uso: deploy.sh \"<msg>\" \"<subdir>\" \"<slug>\" [<html>] [<repo>]"
  echo "Ex:  deploy.sh \"feat: corsica 13d\" \"corsica\" \"corsica-jul2026\""
  exit 2
fi

if [ "$SUBDIR" = "archive" ] || [ "$SUBDIR" = "scripts" ] || [ "$SUBDIR" = "templates" ] || [ "$SUBDIR" = "references" ] || [ "$SUBDIR" = "skills" ] || [ "$SUBDIR" = "entregas" ] || [ "$SUBDIR" = "fontes" ]; then
  echo "❌ SUBDIR '$SUBDIR' é reservado · use nome de viagem (nyc, corsica, etc)"
  exit 2
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VALIDATE_PY="$SCRIPT_DIR/validate.py"

# Repo: o default antigo (~/repos/viagem) não existe mais · o repo é o que contém o script.
[ -z "$REPO_DIR" ] && REPO_DIR="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || true)"
[ -z "$REPO_DIR" ] || [ ! -d "$REPO_DIR" ] && { echo "❌ Repo não encontrado: ${REPO_DIR:-(nenhum)}"; exit 2; }
REPO_DIR="$(cd "$REPO_DIR" && pwd)"

# HTML de entrada: default é o que já está na pasta da viagem (o build.py escreve lá).
if [ -z "$SRC_HTML" ]; then
  if [ -f "$REPO_DIR/$SUBDIR/index.html" ]; then
    SRC_HTML="$REPO_DIR/$SUBDIR/index.html"
  else
    SRC_HTML="${TMPDIR%/}/build/index.html"
    [ -z "$TMPDIR" ] && SRC_HTML="/tmp/build/index.html"
  fi
fi
[ ! -f "$SRC_HTML" ] && { echo "❌ HTML não encontrado: $SRC_HTML"; exit 2; }
# Absoluto ANTES do cd · senão um caminho relativo à pasta de quem chamou quebra.
SRC_HTML="$(cd "$(dirname "$SRC_HTML")" && pwd)/$(basename "$SRC_HTML")"

cd "$REPO_DIR"

# Pré-voo de git ANTES de mexer em qualquer arquivo: publicar = empurrar HEAD:main, então
# origin/main tem que estar contido em HEAD (fast-forward). Se o remoto andou, parar aqui.
CUR_BRANCH="$(git symbolic-ref --short -q HEAD || true)"
echo "→ Branch: ${CUR_BRANCH:-(HEAD destacado)} · publica com: git push origin HEAD:main"
if ! git fetch -q origin main; then
  echo "❌ git fetch origin main falhou (rede/credencial) · ABORTADO antes de mexer em arquivo"
  exit 1
fi
if ! git merge-base --is-ancestor origin/main HEAD; then
  echo "❌ origin/main tem commits que esta branch (${CUR_BRANCH:-HEAD}) não tem · ABORTADO"
  echo "   Publicar agora seria recusado (não é fast-forward) ou apagaria trabalho de outra sessão."
  echo "   Traga o remoto pra cá e rode o deploy de novo:"
  echo "     git merge origin/main"
  exit 1
fi

TARGET_DIR="./$SUBDIR"
TARGET_HTML="$TARGET_DIR/index.html"
TARGET_SLUG="$TARGET_DIR/SLUG.txt"
mkdir -p "$TARGET_DIR"

echo "→ Subpasta: $SUBDIR · slug: $NEW_SLUG"

if [ "$SRC_HTML" -ef "$TARGET_HTML" ]; then
  echo "→ HTML de entrada já é $TARGET_HTML · sem cópia"
else
  cp "$SRC_HTML" "$TARGET_HTML"
fi
echo "$NEW_SLUG" > "$TARGET_SLUG"

# Gate de SCOUT (soft · Lote 7c · 2026-08-09): viagem NOVA que nasce sem levantamento macro.
# Córsega e Sardenha nasceram assim — pesquisa dia-a-dia, sem mapa do destino antes — e o
# resultado está na auditoria de 2026-08-08. Não bloqueia por default porque mini-roteiro e
# coletânea de cidade (marais) são casos legítimos sem scout. VIAGEM_STRICT=1 bloqueia.
# "Viagem nova" = subdir sem NENHUM commit no histórico (o cp acima ainda não foi commitado).
if [ -z "$(git log --oneline -1 -- "$SUBDIR" 2>/dev/null)" ]; then
  if ! ls entregas/"$NEW_SLUG"*.md >/dev/null 2>&1; then
    echo ""
    echo "⚠️  VIAGEM NOVA SEM LEVANTAMENTO SCOUT"
    echo "    Não existe entregas/${NEW_SLUG}*.md · esta viagem está indo pro ar sem o degrau 0"
    echo "    (skills/destination-scout: mapa do destino, vereditos e proveniência ANTES do"
    echo "    dia-a-dia). Córsega e Sardenha nasceram assim — o resultado está na auditoria de"
    echo "    2026-08-08. Legítimo pra mini-roteiro/coletânea; suspeito pra viagem de verdade."
    echo "    Pra transformar este aviso em bloqueio: VIAGEM_STRICT=1"
    echo ""
    if [ "$VIAGEM_STRICT" = "1" ]; then
      echo "❌ VIAGEM_STRICT=1 · viagem nova sem scout · ABORTADO"
      exit 1
    fi
  fi
fi

# Gate de SINCRONIA (Lote 7a · 2026-08-09): o index.html que vai pro ar veio MESMO do
# data.json? O edit inline no `const DAYS` (que o CLAUDE.md recomendava até hoje) fazia duas
# coisas ruins: dessincronizava o data.json (o próximo rebuild apaga em silêncio) e BURLAVA o
# gate 4d — o factcheck-gate projeta o conteúdo sensível a partir do data.json, então um edit
# só-no-HTML muda o que a família lê sem mexer na projeção. Roda ANTES dos outros gates
# porque é o que garante que os outros estão auditando o arquivo certo.
# Falha-FECHADO se o script sumir · override: VIAGEM_SKIP_GATES=1.
SYNC_PY="$SCRIPT_DIR/sync-check.py"
if [ -f "$SYNC_PY" ]; then
  echo "→ Gate de sincronia (data.json ↔ index.html)..."
  if ! python3 "$SYNC_PY" "$TARGET_DIR/data.json" "$TARGET_HTML" --quiet; then
    if [ "$VIAGEM_SKIP_GATES" = "1" ]; then
      echo "⚠️⚠️⚠️  VIAGEM_SKIP_GATES=1 · seguindo com HTML DESSINCRONIZADO do data.json ⚠️⚠️⚠️"
    else
      echo "❌ Gate de sincronia BLOQUEOU · rode build.py · ABORTADO"
      exit 1
    fi
  fi
elif [ "$VIAGEM_SKIP_GATES" = "1" ]; then
  echo "⚠️⚠️⚠️  sync-check.py NÃO ENCONTRADO · VIAGEM_SKIP_GATES=1 · PULANDO gate de sincronia ⚠️⚠️⚠️"
else
  echo "❌ sync-check.py não encontrado · gate de sincronia falha-FECHADO · ABORTADO"
  echo "   Override explícito (assumindo o risco): VIAGEM_SKIP_GATES=1 scripts/deploy.sh ..."
  exit 1
fi

# Validar (estrutural · bloqueia sempre que falhar)
echo "→ Validando (estrutura)..."
python3 "$VALIDATE_PY" "$TARGET_HTML" || { echo "❌ validate.py falhou · ABORTADO"; exit 1; }

# Gate de CONTEÚDO (critico-roteiro · advisory): roda no HTML que vai pro ar.
# Bloqueia SÓ em P0 (erro objetivo: card vazio, link oficial morto). Nota < 32 vira
# aviso — a régua de 32 é enforçada no LOOP da sessão, não no push (heurística mole
# não deve brickar o acesso da família). VIAGEM_STRICT=1 endurece (bloqueia < 32).
#
# Falha-FECHADO se o script sumir (Lote 7g · mesmo padrão do 6b): gate que "pula" quando o
# script some não é gate, é sugestão. Override: VIAGEM_SKIP_GATES=1.
AUDIT_PY="$REPO_DIR/skills/critico-roteiro/audit.py"
if [ -f "$AUDIT_PY" ]; then
  echo "→ Gate de conteúdo (critico-roteiro)..."
  python3 "$AUDIT_PY" "$TARGET_HTML" --deploy-gate \
    || { echo "❌ Gate de conteúdo BLOQUEOU (P0 · erro objetivo) · ABORTADO"; exit 1; }
elif [ "$VIAGEM_SKIP_GATES" = "1" ]; then
  echo "⚠️⚠️⚠️  critico-roteiro/audit.py NÃO ENCONTRADO · VIAGEM_SKIP_GATES=1 · PULANDO gate de conteúdo (deploy SEM checagem de P0) ⚠️⚠️⚠️"
else
  echo "❌ critico-roteiro/audit.py não encontrado · gate de conteúdo falha-FECHADO · ABORTADO"
  echo "   Override explícito (assumindo o risco): VIAGEM_SKIP_GATES=1 scripts/deploy.sh ..."
  exit 1
fi

# Gate de MAPAS (maps-audit.py): monta as URLs do Google Maps como o app monta e bloqueia
# busca genérica / waypoint fantasma / ponto repetido. Existe porque validate e audit leem o
# DADO, e os bugs de ago/2026 (pino no mar, "Can't find that place") só existiam na URL final.
# Falha-FECHADO se o script sumir (Lote 7g) · override VIAGEM_SKIP_GATES=1.
MAPS_PY="$SCRIPT_DIR/maps-audit.py"
if [ -f "$MAPS_PY" ]; then
  echo "→ Gate de mapas (maps-audit)..."
  python3 "$MAPS_PY" "$TARGET_HTML" --quiet \
    || { echo "❌ Gate de mapas BLOQUEOU · corrija com mapsQuery/noMaps · ABORTADO"; exit 1; }
elif [ "$VIAGEM_SKIP_GATES" = "1" ]; then
  echo "⚠️⚠️⚠️  maps-audit.py NÃO ENCONTRADO · VIAGEM_SKIP_GATES=1 · PULANDO gate de mapas (deploy SEM checagem das URLs do Maps) ⚠️⚠️⚠️"
else
  echo "❌ maps-audit.py não encontrado · gate de mapas falha-FECHADO · ABORTADO"
  echo "   Override explícito (assumindo o risco): VIAGEM_SKIP_GATES=1 scripts/deploy.sh ..."
  exit 1
fi

# Gate de FACTCHECK (frescor+formato · R6 auditoria 2026-08-08): verificação sem artefato
# não conta. Bloqueia se não existe <viagem>/FACTCHECK-*.md, se o formato não tem vereditos
# por item com fonte, ou se conteúdo sensível (⭐⭐⭐/WT/historia) mudou depois do último
# factcheck. Cobra timestamp+estrutura (não gameable por substring); a VERDADE do factcheck
# é trabalho da sessão auditora. Ver skills/critico-roteiro/FACTCHECK-EXEC.md.
#
# Falha-FECHADO se o script sumir (refinamento 6b · auditoria de volta 2026-08-09): um gate
# que "pula" quando o script some não é gate, é sugestão — o mesmo "⚠ pulando" que os outros
# gates ainda usam foi a causa-raiz da crise (verificação sem testemunha). Override explícito
# e ruidoso pra quando o script precisa mesmo sumir por um instante: VIAGEM_SKIP_FCGATE=1.
FCGATE_PY="$SCRIPT_DIR/factcheck-gate.py"
if [ -f "$FCGATE_PY" ]; then
  echo "→ Gate de factcheck (frescor+formato)..."
  python3 "$FCGATE_PY" "$TARGET_DIR" --quiet \
    || { echo "❌ Gate de factcheck BLOQUEOU · rode o FACTCHECK-EXEC e versione o artefato · ABORTADO"; exit 1; }
elif [ "$VIAGEM_SKIP_FCGATE" = "1" ]; then
  echo "⚠️⚠️⚠️  factcheck-gate.py NÃO ENCONTRADO · VIAGEM_SKIP_FCGATE=1 · PULANDO gate de factcheck (deploy SEM verificação de frescor) ⚠️⚠️⚠️"
else
  echo "❌ factcheck-gate.py não encontrado · gate de factcheck falha-FECHADO · ABORTADO"
  echo "   Override explícito (assumindo o risco): VIAGEM_SKIP_FCGATE=1 scripts/deploy.sh ..."
  exit 1
fi

# Regenerar landing AUTOMATICAMENTE (lê todas subpastas atuais + monta cards)
# Decisão 2026-05-23: integrado ao deploy pra nunca esquecer · sessão Sardenha esqueceu rodar wrap-up
echo "→ Regenerando landing (index.html root)..."
python3 "$SCRIPT_DIR/regen-landing.py" "$REPO_DIR"

# Backup local · conveniência, não bloqueia: o sandbox do Claude Code nega escrita em
# ~/.skill-backups e o backup de verdade é o git.
TS=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="${VIAGEM_BACKUP_DIR:-$HOME/.skill-backups}"
BACKUP_FILE="$BACKUP_DIR/${SUBDIR}_${NEW_SLUG}_${TS}.html"
if mkdir -p "$BACKUP_DIR" 2>/dev/null && cp "$TARGET_HTML" "$BACKUP_FILE" 2>/dev/null; then
  echo "→ Backup: $BACKUP_FILE"
else
  echo "⚠️  Backup local não gravado em $BACKUP_DIR (sem permissão?) · seguindo · o git é o backup"
fi

# Git commit (na branch atual) + push HEAD:main (só fast-forward)
git add -A
if git diff --cached --quiet; then
  echo "ℹ️  Nada novo pra commitar · conferindo se HEAD já está no ar"
else
  git commit -m "$COMMIT_MSG"
fi
LOCAL_SHA="$(git rev-parse HEAD)"
REMOTE_BEFORE="$(git ls-remote origin refs/heads/main | cut -f1)"
if [ "$REMOTE_BEFORE" = "$LOCAL_SHA" ]; then
  echo ""
  echo "ℹ️  Nada a publicar · origin/main já está em ${LOCAL_SHA:0:7} (o que está no ar já é isto)"
  exit 0
fi

if ! git push origin HEAD:main; then
  echo ""
  echo "❌ git push recusado · NADA foi publicado"
  echo "   Commit ${LOCAL_SHA:0:7} ficou só em ${CUR_BRANCH:-HEAD} (local)."
  echo "   Se o remoto andou no meio do deploy: git merge origin/main e rode o deploy de novo."
  exit 1
fi

# Prova: lê o remoto de novo. O ✅ só sai se origin/main AGORA é o commit publicado.
REMOTE_AFTER="$(git ls-remote origin refs/heads/main | cut -f1)"
if [ "$REMOTE_AFTER" != "$LOCAL_SHA" ]; then
  echo ""
  echo "❌ Push terminou, mas origin/main = ${REMOTE_AFTER:-(ilegível)} ≠ ${LOCAL_SHA} · publicação NÃO confirmada"
  exit 1
fi

# Num worktree, o ref `main` local e o checkout principal ficam pra trás do que foi publicado.
# Avança o checkout principal só se ele estiver limpo e for fast-forward · senão, avisa.
if [ "$CUR_BRANCH" != "main" ]; then
  MAIN_WT="$(git worktree list --porcelain | awk '/^worktree /{p=substr($0,10)} /^branch refs\/heads\/main$/{print p; exit}')"
  if [ -n "$MAIN_WT" ]; then
    if [ -z "$(git -C "$MAIN_WT" status --porcelain --untracked-files=no)" ] \
       && git -C "$MAIN_WT" merge -q --ff-only origin/main 2>/dev/null; then
      echo "→ Checkout principal avançado pra ${LOCAL_SHA:0:7}: $MAIN_WT"
    else
      echo "⚠️  Checkout principal NÃO avançado (tem mudança local ou não é fast-forward): $MAIN_WT"
      echo "   O que está no ar está certo · só a cópia local ficou atrás. Lá: git merge --ff-only origin/main"
    fi
  elif git show-ref -q --verify refs/heads/main && git merge-base --is-ancestor main origin/main; then
    git branch -f main origin/main >/dev/null && echo "→ Ref main local avançado pra ${LOCAL_SHA:0:7}"
  fi
fi

echo ""
echo "✅ Deploy completo · origin/main ${REMOTE_BEFORE:0:7} → ${LOCAL_SHA:0:7}"
echo "   URL: https://tsferraro.github.io/viagem/$SUBDIR"
echo "   Landing: https://tsferraro.github.io/viagem (lista todas)"
