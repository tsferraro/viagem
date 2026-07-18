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

---

## 2026-07-01 · Passo 3.2 — Revisão arquitetural do gate (Opus) + endurecimento

**Contexto**: Tobia pediu revisão crítica do desenho do "portão de qualidade" (sem diplomacia). Diagnóstico do Opus achou **teatro de enforcement em 3 camadas**, verificado no código: (F1) o tier P0 nunca era emitido — nenhum `Finding(0,...)`; (F2) logo `aprovado = nota≥28 E P0=0` degenerava pra só `nota≥28`; (F3) nada em `scripts/` chamava o auditor — o "gate" só existia se uma sessão lembrasse. Baseline nos 5 roteiros reais: a régua a 28 carimbou 4 de 5 com 3-8 P1s não corrigidos.

**Decisões**:

| # | Decisão | Alternativa rejeitada | Motivo |
|---|---|---|---|
| 1 | **Régua 28 → 32** (roteiro) · 14 → 16 (scout · 80%) | Manter 28 | 28 carimbava roteiros com 3-8 P1s. A 32, só valencia (34) passa; os outros 4 iteram. Tobia pediu 32 explícito |
| 2 | **Emitir P0 de verdade**: card vazio (sem sobre+dicas+imperdivel) · link **oficial** 404 | Deixar P0 como texto aspiracional | Sem P0 real, o tier de bloqueio era código morto (F1/F2) |
| 3 | `coord_unverified` = **P1 forte, não P0** | P0 (bloqueia) | Bloquear re-deploy de miradouro estimado (2 das 5 viagens têm) treina bypass; a flag é honesta. Desconta ponto e empurra no loop |
| 4 | **Wire no `deploy.sh`**: `audit.py --deploy-gate` após validate | Hook do Claude Code · nada | deploy.sh é o funil por onde todo push passa. Enforcement real, não "se a sessão lembrar" (F3) |
| 5 | **Deploy bloqueia só em P0**; nota <32 = aviso. `VIAGEM_STRICT=1` endurece | Hard-block <32 no push | Heurística mole não deve brickar acesso da família; false-positive vira `--no-verify`. A régua de 32 vive no LOOP da sessão |
| 6 | **Nota em 2 metades**: Mecânico /20 (D2·D3·D4·D5·D9 · regex é autoridade) + Julgamento ⚖️ /20 (D1·D6·D7·D8·D10 · regex é piso · Claude confirma) | Um número /40 único | `sobre≥150 chars` mede comprimento, não storytelling. Separar impede confiar cego no proxy de escrita |
| 7 | **Fica em `skills/`** (não move pra `scripts/`) | Mover audit.py pra scripts/ (recomendação inicial do Opus) | Revertido à luz do objetivo do Tobia: skill consolida régua+runnable+guia de julgamento; mover quebra N cross-refs por ganho funcional zero. O framing "é linter" foi resolvido dando dentes + honestidade no report, não realocando |
| 8 | **Dedup**: `d9` para de re-checar `temaCurto` (dono = validate.py) | Manter check duplo | `temaCurto≤15` estava em validate.py E audit.py. Uma fonte de verdade pro estrutural |
| 9 | Honestidade no doc sobre "uma fonte de verdade" | Manter claim forte | Conceitos apontam pro mapping-rubric, mas thresholds viram regex no audit.py (redefinição lossy · sync manual). Documentado como é |

**Validação real** (5 roteiros + 1 scout, pós-mudança):

| Artefato | Nota | Metades | P0 | Aprovado (≥32/16) |
|---|---|---|---|---|
| valencia | 34/40 | mec 15 · julg 19 | 0 | ✅ |
| marais | 30/40 | mec 15 · julg 15 | 0 | ❌ itera |
| nyc | 29/40 | mec 11 · julg 18 | 0 | ❌ itera |
| corsica | 28/40 | mec 12 · julg 16 | 0 | ❌ itera |
| pais-sardenha | 28/40 | mec 11 · julg 17 | 0 | ❌ itera |
| notre-dame (scout) | 20/20 | — | 0 | ✅ |

- `--deploy-gate` testado: aprovado→exit0 · nota baixa sem P0→exit0+aviso · `VIAGEM_STRICT=1`→bloqueia · card vazio (fixture)→exit1 bloqueado.
- Insight do split: a metade MECÂNICA é onde estão os gaps reais e objetivos (nyc mec 11/20: coords <4 casas, custo sem data, TRANSIT_MAP) — a metade de julgamento inflava (18/20 = proxy de escrita, não qualidade real).

**Artefatos alterados**: `skills/critico-roteiro/audit.py` (P0, split, --deploy-gate, thresholds, dedup) · `scripts/deploy.sh` (gate wire) · `references/content-rubric.md` · `skills/critico-roteiro/SKILL.md` · `skills/destination-scout/SKILL.md` · `CLAUDE.md`.

---

## 2026-07-02 · Fase A — grader vira router (`--suggest`) + resolução da divergência

**Contexto**: o auditor diagnosticava e parava — nota + achados, sem dizer *o que fazer com eles*. Fase A do roadmap grader→router (plano revisado pela sessão-arquiteto, 6 correções incorporadas). Antes disso foi preciso resolver uma **divergência de branch** que estava mascarada.

**Divergência (achado, não decisão)**: a partir de `9275ca9`, `origin/main` ganhou 53 commits (conteúdo NYC/mapa/WT) enquanto a `main` local ganhou 2 (auditor com dentes) — sem push, porque o `guard-git-push.sh` da outra sessão trava. `git push` era rejeitado. Resolvido por **merge (não force-push)**: `audit.py` fez merge limpo, conflitaram 4 markdowns, resolvidos por **união** com os números novos (32/16) vencendo os antigos (28/14). Causa-raiz (o guard) fica com a sessão-arquiteto.

**Decisões**:

| # | Decisão | Alternativa rejeitada | Motivo |
|---|---|---|---|
| 1 | `station` + `hint` como **campos do `Finding`**, emitidos no `--json` | Só render no relatório | Machine-consumable: sub-agente despacha lendo JSON, sem parsear texto |
| 2 | Roteamento **por mensagem** (tabela `ROUTING`), não por call-site | Taggear os ~60 `F.append()` | Diff mínimo, auditores intactos, tabela legível num lugar só · zero risco pros 14 testes |
| 3 | Taxonomia das estações **herda** `MECHANICAL_DIMS`/`JUDGMENT_DIMS` | Criar eixo novo | O que dá pra perseguir é exatamente o que dá pra automatizar — alinhamento quase perfeito |
| 4 | **Guarda anti-Goodhart** codificada nos hints | Deixar implícito | "Subir a nota" só vale na metade mecânica. Nas ⚖️ o hint manda o que a PROSA precisa, nunca "faça X pra subir" |
| 5 | `_is_heavy` promovido a `is_heavy_card()` de módulo | Duplicar a heurística | UMA definição de "card âncora", dois usos: alerta de ritmo (D6) + peso na priorização |
| 6 | Densidade **por dia**, nunca nota por dia | Nota /40 diária | D9/D10 só existem no roteiro inteiro — nota diária seria incompleta ou enganosa |
| 7 | **Fase B extinta**, dobrada na A | Auto-patcher próprio | Com `temaCurto` fora (dono = validate.py), sobrava pouco. `hint` com patch colável resolve sem o risco de escrita automática |
| 8 | Ritmo continua **🤔 (nunca patch)** | Auto-sugerir corte | Decisão Tobia: "o peso do dia depende do público — quero enxergar as opções e decidir" |

**Validação**: 14/14 testes (rede do arquiteto) antes e depois · NYC 39/40 Excelente, 4 advertências de ritmo roteadas pra 🤔 · fixture `unverified_coord` exercitando as 4 estações + top-5 + heat map. Prova viva da guarda anti-Goodhart: card com `sobre` de **148 chars** (2 abaixo do piso) recebe hint *"NÃO encher linguiça pra bater char count"*.

**Próximo**: Fase C (estação de pesquisa · contrato anti-invenção no write-back) → Fase D (reescrita padrão-Marais, depende dos fatos da C).
