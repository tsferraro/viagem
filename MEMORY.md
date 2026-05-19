# MEMORY · Projeto Viagens

Aprendizados de uso da skill `itinerary-builder` acumulados ao longo das viagens reais. Cresce com cada viagem feita. NÃO contém dados pessoais — apenas lições sobre uso da skill.

Memórias pessoais transversais do Tobia ficam em `~/.claude/projects/.../memory/` (não vão pro repo público).

---

## Por viagem

### NYC · Jul/2026 (em planejamento)
- _A preencher após a viagem real._

---

## Padrões cross-viagem

### O que funcionou bem
- _A registrar conforme viagens acontecerem._

### O que precisou ajustar mid-trip
- _A registrar conforme viagens acontecerem._

---

## Evolução da skill

### v1.0 · 2026-05-16
- Setup inicial · skill `itinerary-builder` + `walking-tour-designer` embarcadas
- 10 princípios + 6 anti-padrões codificados
- Suporte a roteiros paralelos via SUBDIR
- Quality bar nos cards + anti-invenção de URLs (`validate.py --check-links`)
- JSON pretty-printed por default (mobile edit-friendly)

### v1.1 · 2026-05-19 (lições da 1ª iteração mobile · Córsega)

Problemas encontrados ao usar a skill no mobile-cloud com Córsega:
1. Mobile arquivou NYC sem querer ao criar Córsega · conceito de "viagem ativa no root" era frágil
2. Merge em main não foi automático (Tobia teve que fazer manual)
3. Link rota Google Maps mostrou "Com alfinete" em vez de nome dos lugares
4. Sem protocolo de encerramento documentado · sessão fechou sem atualizar MEMORY

Mudanças aplicadas:
- Subpastas como regra obrigatória: TODA viagem vive em subdir desde nascimento. Root tem só landing auto-regenerada
- `deploy.sh` reescrito: requer subdir obrigatório · valida nome reservado · sempre push pra main direto
- `getRouteUrl` V1.4: usa nome do stop em vez de coords puras (fix Maps · aplicado retroativo)
- `scripts/wrap-up.sh` criado: protocolo de encerramento obrigatório
- `FUTURE.md` priorizado: road-trip-designer + pre-trip-content-curator + trip-debrief-skill

### Próximas lições serão registradas aqui após uso real.
