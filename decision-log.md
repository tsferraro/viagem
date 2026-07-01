# Decision Log · Itinerary Builder

Decisões estruturais tomadas durante criação da skill. Cada entry: data · contexto · decisão · alternativas rejeitadas · validação.

---

## 2026-05-16 · Skill criada (versão inicial)

**Contexto**: Tobia concluiu projeto iterativo (~15 turnos · NYC Jul/2026 · HTML 131KB validado em campo) e pediu "replicar o PROCESSO" via skill.

**Decisões consolidadas (validadas com Tobia)**:

| # | Decisão | Alternativas rejeitadas | Motivo |
|---|---|---|---|
| 1 | Skill em `~/.claude/skills/` global | Plugin separado · pasta projeto | Uso pessoal recorrente · acesso de qualquer cwd |
| 2 | Repo `tsferraro/viagem` dedicado com archive interno | `tobia-personal` com symlink · 1 repo/viagem | Symlinks Jekyll instável · slug aleatório quebra UX família · modular 1 repo = 1 propósito |
| 3 | Scope faseado: skills funcionais + evals.json + dry-run · sem optimization de description ainda | Full skill-creator workflow upfront | Otimização sem dados reais é caro · sessão 2 pós-uso |
| 4 | WT designer standalone + sub-skill | Só sub-skill | Tobia pode pedir WT direto |
| 5 | Privacidade: opção A (URL pública + auth JS + noindex) | Cloudflare Access | Risco baixo · MVP rápido · Cloudflare documentado em FUTURE.md |

**Decisões internas Claude (com marker "sugestão · validar" no plano)**:

| # | Decisão | Motivo |
|---|---|---|
| A | `coord.metadata.verified` nested · não flag raiz | Permite estender com source/precision sem migration |
| B | Bairros via web_search + curation manual | Reverse-geocoding adiciona dependência sem ganho |
| C | LINKS_MAP só pra cards relevantes · não obrigatório | Forçar gera entries vazias |
| D | Templates: shell.html com placeholders Python + styles.css + render-functions.js separados | Simplicidade · debug fácil · sem Jinja runtime dep |

**Mitigações pra viagens longas (25+ dias) codificadas**:
- validate.py limites elevados: warning 250KB · erro 400KB
- SKILL.md fase 5 obriga blocos de 5-7 dias pra >14 dias
- Strategy "etapas" via campo `etapa` no DAYS (Lisboa/Porto/Açores)
- Compressão JSON minificada em build.py

---

## Decisões pendentes (sinalizar quando rodar pela 1ª vez)

- [ ] **Cadência incremental**: testar em campo se >14 dias realmente degrada qualidade (hipótese). Confirmar pós-Agosto 2026.
- [ ] **BAIRROS_CONFIG**: validar se ranges lat/lng curados manualmente são "good enough" ou se vale Nominatim/reverse-geocoding.
- [ ] **archive/index.html UX**: índice navegável de viagens passadas é útil ou pollui? Confirmar com família.
- [ ] **Senha por viagem**: cada viagem nova ganha senha custom ("jujuba" → "fado" → "tsuru") ou senha fixa pra família memorizar?

---

## Mudanças in-flight (durante criação · 2026-05-16)

| Mudança | Origem | Status |
|---|---|---|
| `getBairroForCoord` reescrito pra dinâmico via `BAIRROS_CONFIG` | Hardcode NYC quebrava em outras cidades | Done |
| validate.py com `MAX_SIZE_WARN/ERR` configuráveis | Viagens 25d precisam | Done |
| `meta noindex` adicionado no shell.html | Privacidade básica sem custo | Done |
| `BAIRROS_CONFIG_JSON` placeholder no shell.html | Suporte ao novo `getBairroForCoord` | Done |
| validate.py regex aceita JS literal E JSON (`"key":` vs `key:`) | DAYS injetado como JSON minificado · regex original esperava JS object literal | Done · dry-run Lisboa 9 coords detectadas |

## Pós-dry-run · 2026-05-16 (questões do Tobia)

| Pergunta | Resposta | Ação |
|---|---|---|
| Skill funciona pra qualquer roteiro? | Sim · 25d foi exemplo · cadência incremental ativa só pra >14d | Confirmado · sem mudança |
| Acesso mobile (Claude.ai app)? | **DESCOBERTA**: existe Claude Code mobile-cloud · acessa GitHub direto · roda em sandbox sem skills locais. Solução elegante: `CLAUDE.md` no root do repo `tsferraro/viagem` · lido automaticamente por qualquer sessão Claude Code | Criado `REPO_CLAUDE_MD.md` com conteúdo pronto pra colar no repo |
| Auto-commit no fluxo? | Já codificado · skill executa deploy.sh sem perguntar após validate.py passar | Reforçado no SKILL.md |
| Nomenclatura GitHub/URLs? | Skill gera slug automático (`<destino>-<mes><ano>`) · Tobia NÃO renomeia · pode override se quiser | Documentado na seção "Naming automático" do SKILL.md |
| Subpastas pra 2+ roteiros paralelos? | Adicionado suporte SUBDIR no deploy.sh · estrutura `familia/`, `casal/`, `amigos/`, `extra/` | deploy.sh atualizado · SKILL.md atualizado · paralelos arquivam junto |
| Mobile pode ter mesma capacidade do desktop? (Opção A escolhida) | Sim · embarcar `scripts/` + `templates/` DENTRO do repo `tsferraro/viagem` · mobile-cloud clona e roda os scripts no sandbox dele | Criado `~/.skill-backups/repo-template/` self-contained (CLAUDE.md + README + scripts + templates) · validate.py limites elevados pra 500KB/1500KB · build.py default pretty-printed (removido minify default · `--minify` opcional só pra emergência) · SKILL.md desktop aponta source-of-truth = repo |

---

## 2026-07-01 · Redesign de interface + skill impeccable embarcada

**Contexto**: Tobia pediu teste de melhoria de design do roteiro NYC. Rodada a skill **impeccable** (design/UI · Apache 2.0) como avaliador. 3 variantes em sandbox (`nyc-lab-bold/`, `-evo/`, `-hibrido/`).

**Decisões**:

| # | Decisão | Alternativas rejeitadas | Motivo |
|---|---|---|---|
| 1 | Redesign **híbrido** vira o novo padrão | Bold puro (31/40 · hero-metric banido) · Evolução (33/40 · seguro mas menos uau) | Híbrido 38/40 · bottom-bar+status do Bold + segurança da Evolução |
| 2 | Skill impeccable salva em `skills/impeccable/` | Manter fora do repo | Runnable pra reavaliar/gerar design · mesma lógica "skill completa no repo" |
| 3 | 2 templates **separados** (datada vs coletânea-cidade) | 1 template com flags | Menos conditional spaghetti · coletânea não tem datas/AGORA/stats |
| 4 | Rota do Maps por **coordenadas** (reafirma V1.3) | Nomes nos waypoints | Nome vago/evento cai no lugar errado ("Fogos Macy's"→loja) · doc §3.7 já mandava coords |
| 5 | `noMaps:true` p/ stops sem ponto público | Deixar link errado | "Sem ponto se não confiável" · omite link em vez de enganar |

**Validação**: detector impeccable 0 antipadrões · validate.py 0 erros · testado no device do Tobia (rota a-pé, RESERVADO, transporte). Registro completo em `references/design-rubric.md`.
