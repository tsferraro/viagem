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
| 1 | Redesign **híbrido** vira o novo padrão | Bold puro (31/40 · hero-metric banido) · Evolução (33/40 · seguro mas menos uau) | Híbrido 39/40 · bottom-bar+status do Bold + segurança da Evolução |
| 2 | Skill impeccable salva em `skills/impeccable/` | Manter fora do repo | Runnable pra reavaliar/gerar design · mesma lógica "skill completa no repo" |
| 3 | 2 templates **separados** (datada vs coletânea-cidade) | 1 template com flags | Menos conditional spaghetti · coletânea não tem datas/AGORA/stats |
| 4 | Rota do Maps por **coordenadas** (reafirma V1.3) | Nomes nos waypoints | Nome vago/evento cai no lugar errado ("Fogos Macy's"→loja) · doc §3.7 já mandava coords |
| 5 | `noMaps:true` p/ stops sem ponto público | Deixar link errado | "Sem ponto se não confiável" · omite link em vez de enganar |

**Validação**: detector impeccable 0 antipadrões · validate.py 0 erros · testado no device do Tobia (rota a-pé, RESERVADO, transporte). Registro completo em `references/design-rubric.md`.

---

## 2026-07-01 · Passo 3 — Rubrica de Conteúdo + audit-content.py + loop-até-excelente

**Contexto**: Rubrica de design (Passo 2) entregue a 39/40. Próximo passo: rubrica de CONTEÚDO — escrita, links, coords, logística — que o validate.py estrutural não cobre.

**Decisões**:

| # | Decisão | Alternativas rejeitadas | Motivo |
|---|---|---|---|
| 1 | Rubrica de conteúdo REFERENCIA destination-scout sem duplicar | Reescrever vocabário de veredito/perfil/anti-invenção | Uma fonte de verdade pra cada conceito; mudança na scout propaga automaticamente |
| 2 | 10 dimensões × 4pts = /40 · mesma escala da design-rubric | Escala diferente (0-3, 0-5) | Coerência com rubrica-irmã; Tobia já conhece a banda de referência |
| 3 | Limiar de aprovação automática: nota ≥28 E P0=0 · Claude aspira ≥32 | 24 (muito permissivo) · 32 obrigatório (rígido demais) | 28 = banda "Bom"; P0=0 garante que não há bloqueio crítico; 32 é aspiracional não obrigatório |
| 4 | `audit-content.py` aceita tanto `data.json` quanto `index.html` | Só data.json | Retrocompatibilidade: roteiros sem data.json (editados manualmente) também auditáveis |
| 5 | D7 (Walking Tours) retorna 4/4 (N/A) se viagem não tem WT | Penalizar roteiros sem WT | Um roteiro de só 2 dias sem WT não é pior por isso — não deve perder nota |
| 6 | Preços livres de data sem penalidade; gratuito sem data = correto | Exigir data até em gratuitos | "Gratuito" não vence com o tempo; data só importa em preços pagos (mapping-rubric §anti-invenção) |
| 7 | Loop-até-excelente: máx 3 iterações automáticas · parar e perguntar ao Tobia se falhar | Loop infinito | Evita ciclo de auto-correção sem convergência; após 3 tentativas, o problema é de conteúdo, não de formato |
| 8 | destination-scout = "degrau 0" explícito no pipeline | Scout como opcional | Ordem formal: scout → build → validate → audit → deploy; cada degrau tem portão de qualidade |

**Artefatos criados**:
- `references/content-rubric.md` — rubrica de 10 dimensões com relação destination-scout + pipeline loop-até-excelente
- `scripts/audit-content.py` — script ~500L (suporta .json e .html · exits 0/1/2 · --check-links opcional) · **movido pra `skills/critico-roteiro/audit.py` no Passo 3.1**
- CLAUDE.md atualizado: tabela references + tools section + pipelines create e update

---

## 2026-07-01 · Passo 3.1 — Auditor vira skill `critico-roteiro` + modo scout + FASE 1 completada

**Contexto**: revisão do Passo 3 com o Opus (a pedido do Tobia) + complemento de outra sessão que revisou as entregas da `destination-scout`. Três gatilhos: (1) o auditor deveria ser skill própria, invocável de todo lugar; (2) a FASE 1 (pesquisa externa) foi indevidamente pulada no Sonnet; (3) achado de fork na rubrica.

**Decisões**:

| # | Decisão | Alternativa rejeitada | Motivo |
|---|---|---|---|
| 1 | Auditor vira **skill `critico-roteiro`** (`skills/critico-roteiro/audit.py` + SKILL.md) | Manter script solto em `scripts/` | Simetria com `impeccable` (design): régua em `references/`, runnable em `skills/`. Roda como gate dentro das outras skills E standalone |
| 2 | Nome `critico-roteiro` (escolha do Tobia) | `critico-conteudo` (sugestão Claude · mais preciso pois audita scout tb) | Decisão do Tobia; rename é trivial se quiser depois |
| 3 | Modo **`--scout`** audita `.md` da destination-scout (5 dim · /20) | Segundo script separado | UMA ferramenta, helpers compartilhados, sem forkar as regras da `mapping-rubric` |
| 4 | `--terceiros` relaxa seção **Fontes** (opcional pra-terceiros/mini-plano) | Fontes sempre obrigatória | Complemento Tobia: lista de URLs fica no chat, não se manda pra mãe. Auto-detecta mini-plano pela estrutura |
| 5 | **Loop-até-excelente na destination-scout** (PASSO 4b · gate antes do export) | Só checklist manual | Scout precisava de portão real; pega preço sem data + sem Fontes (furos do Chapada-Guia) |
| 6 | Alerta de **pacing = P3 advisory**, nunca corta nem bloqueia | Baixar nota/sugerir corte | Tobia: "o peso do dia depende do público e da dinâmica familiar — quero enxergar as opções e decidir" |
| 7 | Corrigido **fork `risco` ≠ veredito 🟢🟡🔴** na content-rubric | Manter "mesma escala" (errado) | `risco`=multidão/esforço; veredito=recomendação. Escalas diferentes. D8 audita honestidade **na prosa**, não no campo `risco` |
| 8 | **FASE 1 completada**: fundamentação externa por dimensão (Rick Steves, Lonely Planet, ciência de pacing infantil, route-optimization) | Ancorar só na destination-scout (in-house) | Citar só docs internos é circular; a rubrica ganhou espinha editorial externa |
| 9 | `walking-tour`/`road-trip` **sem gate próprio** | Loop em todas as 4 skills | Output deles vira card do roteiro → já auditado por D7 no gate do roteiro (evita redundância) |

**Validação real**:
- Roteiro NYC: **29/40 · Bom · Aprovado** (P0=0) · pacing agora emite 5 alertas P3 não-bloqueantes
- Notre-Dame (mini-plano): **20/20 · Excelente** (falso-positivo "perto" da etimologia corrigido — check de distância escopado só ao bloco de logística)
- Fixture macro sintético (padrão Chapada-Guia): **11/20 · Aceitável · NÃO aprovado** — pegou preço sem data (P1) + sem Fontes (P1), exatamente os furos que a revisão manual apontou

**Follow-up sugerido** (não feito): transformar `design-rubric.md` num `critico-design` nativo, simétrico a este, com `impeccable` como ferramenta externa que ele chama.
