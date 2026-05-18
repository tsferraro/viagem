# 🗺️ tsferraro/viagem

Repo dos roteiros de viagem da família Tobia. Servido via GitHub Pages.

## URLs

- **Viagem ativa**: https://tsferraro.github.io/viagem
- **Arquivo de viagens passadas**: https://tsferraro.github.io/viagem/archive

## Estrutura

- `index.html` · viagem ativa
- `<subdir>/index.html` · roteiros paralelos (família, casal, etc)
- `archive/<slug>/` · viagens arquivadas
- `scripts/` · ferramentas de build/validate/deploy
- `templates/` · template do HTML single-file

## Para usar

Este repo carrega a skill `itinerary-builder` completa. Qualquer sessão Claude Code que clonar tem todas as ferramentas pra criar/atualizar viagens.

Ver `CLAUDE.md` pra documentação operacional completa.

## Privacidade

- Auth gate JS com senha custom por viagem
- `<meta name="robots" content="noindex,nofollow">` (não indexável)
- Repo público mas conteúdo protegido por senha (família memoriza)
- Para privacidade real (Cloudflare Access magic-link), ver FUTURE.md da skill
