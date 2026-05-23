# 🗺️ tsferraro/viagem

Repo dos roteiros de viagem da família Tobia. Servido via GitHub Pages.

## URLs

- **Landing** (lista de viagens ativas): https://tsferraro.github.io/viagem
- **Por viagem**: `https://tsferraro.github.io/viagem/<subdir>` (ex: `/nyc`, `/corsica`)
- **Arquivo**: https://tsferraro.github.io/viagem/archive

## Convenção

Toda viagem vive em subpasta dedicada · sem "viagem ativa no root":

- `nyc/` · Roteiro NYC Julho 2026
- `corsica/` · Roteiro Córsega Julho 2026
- `<futuras>/` · Próximas viagens
- `archive/<slug>/` · Viagens já realizadas

Subdirs reservados (não usar como nome de viagem): `archive`, `scripts`, `templates`, `references`, `skills`.

Para roteiros paralelos da MESMA viagem (família vs casal vs amigos): sufixo `corsica/`, `corsica-amigos/`, `corsica-pais/`.

## Para usar

Este repo carrega a skill `roteiro-viagem` completa (scripts + templates + references + sub-skills). Qualquer sessão Claude Code que clonar tem todas as ferramentas pra criar/atualizar viagens.

Ver `CLAUDE.md` pra documentação operacional completa.

## Protocolo

Ao final de toda sessão que mexer em roteiros: rodar `scripts/wrap-up.sh` (regenera landing, valida HTMLs, commita, push, reporta URLs).

## Privacidade

- Auth gate JS com senha custom por viagem (teatro contra acesso casual)
- `<meta name="robots" content="noindex,nofollow">` (não indexável)
- Repo público mas conteúdo protegido por senha simples
- Para privacidade real (Cloudflare Access magic-link), ver `FUTURE.md`
