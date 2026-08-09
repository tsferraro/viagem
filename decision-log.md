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

---

## 2026-07-02 · Fase C — estação de pesquisa (`--diff` + `RESEARCH.md`)

**Contexto**: a fila 🔎 do `--suggest` (Fase A) aponta o que pesquisar; faltava *executar* com disciplina anti-invenção. Ao entrar na C, um reframe de arquitetura mudou o que ela é.

**Reframe (decisão fundadora da fase)**: `audit.py` é um linter determinístico offline — fazer web_search e escrever fato no `data.json` é trabalho **agêntico**, molde de **protocolo** (como FACTCHECK/JUDGE), não de código. E o contrato anti-invenção **já é enforçado pela metade mecânica existente**: preço sem data → D3; coord chutada → D4; URL morta → D5 (`--check-links`); fato falso → FACTCHECK. Logo a Fase C não precisa de gate novo — precisa de (1) protocolo e (2) a trava de loop fechado.

**Decisões**:

| # | Decisão | Alternativa rejeitada | Motivo |
|---|---|---|---|
| 1 | Fase C = **`RESEARCH.md` (protocolo) + `--diff` (código)** | Um "robô de pesquisa" dentro do audit.py | Pesquisa é agêntica; linter é offline. Misturar violaria a arquitetura da própria skill |
| 2 | Contrato anti-invenção **reusa a metade mecânica**, não cria gate | Novo validador de write-back | D3/D4/D5 + FACTCHECK já cobrem forma+verdade. DRY, uma fonte de verdade |
| 3 | `--diff <antes>`: delta das 2 metades + veredito de regressão | Só re-rodar o audit e comparar na mão | A trava barata entre lotes; **mecânico não pode cair** (lá o número é verdade), julgamento pode oscilar mas é MOSTRADO (não escondido no agregado) |
| 4 | Regressão = mecânico caiu **OU** P0/P1 mecânico novo → exit 1 | Bloquear em qualquer queda de total | Julgamento é proxy; queda ⚖️ vira aviso, não bloqueio (senão o Goodhart inverte: trava melhora real de prosa que mexeu num proxy) |
| 5 | `audit_roteiro()` fatorado como função pura (sem prints) | Duplicar o loop das 10 dims | `--diff` roda o audit 2×; main() intacto → zero risco pros testes |
| 6 | `_finding_key` zera dígitos na identidade do achado | Casar msg exata | Contadores mudam ("1/1"→"2/3 cards") sem o achado ser "outro" — senão o diff vira ruído |
| 7 | Contrato: não confirmou = `[a confirmar]` / `coord_unverified`, **nunca** chute | "Quase certo" grava | É o ponto onde alucinação entra no doc que a família abre na rua. Honesto > completo |

**Validação**: suite 14→**20 checks** (3 de roteamento da Fase A + 3 do `--diff`: melhoria→exit 0, regressão→exit 1, `regressed` no JSON). NYC intacto. `--diff` provado nos dois sentidos (clean↔unverified).

**Próximo**: Fase D (reescrita padrão-Marais dos cards que a C municiou com fato) — usa `--diff` como trava a cada card reescrito.

---

## 2026-07-02 · `impeccable` marcada como vendorizada (fora do backlog de higiene)

`skills/impeccable/` é skill de terceiro (Apache 2.0, design/UI). No sweep do gate de design de skill dá 10/16 — mas **não é débito nosso**: editar é alterar código vendorizado, decisão de política, não higiene. Acordo com a sessão-arquiteto: ela exclui `impeccable` do sweep do lado do ecossistema; aqui fica o registro. Não tocar sem decisão explícita do Tobia.

---

## 2026-07-02 · Fase D — reescrita padrão-Marais (`REWRITE.md`) · ciclo grader→router FECHADO

**Contexto**: última fase do roadmap. A A roteia, a C municia com fato; a D transforma fato em prosa que encanta (padrão Marais). Fecha o ciclo "avaliar → consertar".

**Decisões**:

| # | Decisão | Alternativa rejeitada | Motivo |
|---|---|---|---|
| 1 | Fase D = **protocolo puro** (`REWRITE.md`), zero código novo | Um "reescritor" no audit.py | Reescrever bem é julgamento de escrita, não regex. E o enforcement JÁ existe todo (ver #2) |
| 2 | Enforcement **reusa 3 redes que já existem** | Gate de reescrita novo | markdown cru → `validate.py`; regressão mecânica → `--diff`; substância → `JUDGE.md`. Nada a construir |
| 3 | **Grava direto** no data.json, sem portão de aprovação card-a-card | Diff-pra-aprovar a cada card | Decisão Tobia: "escreve direto pra me facilitar; se eu quiser ajuste, peço — senão trava demais". Redes automáticas seguram o objetivo |
| 4 | Anti-Goodhart é a guarda central da fase | Mirar o número do D1 | "sobre de 90 chars com 1 fato bom > 200 de floreio"; sem fato → "raso mas honesto", não inventa lenda |
| 5 | RESEARCH + REWRITE = **2 protocolos de conserto** (par das 3 de avaliação) | Instrumento solto | Taxonomia limpa: audit/factcheck/judge avaliam; research/rewrite consertam; `--suggest` despacha 🔎→RESEARCH, ✍️→REWRITE |

**Validação (prova end-to-end do ciclo)**: fixture com prosa de 1 card destruída → `--suggest` marca ✍️ + top-5 âncora (10 pts) → reescrita Marais → `--diff`: **mecânico 18→18 (±0), julgamento 19→20 (+1)**, 2 achados ✍️ resolvidos, zero regressão, exit 0. É a prova viva do anti-Goodhart: melhora real de prosa aparece no **julgamento**, sem tocar (nem inflar) o mecânico. Suite 20/20.

**Roadmap grader→router FECHADO**: A (`--suggest`) · C (`--diff` + RESEARCH) · D (REWRITE) entregues. B extinta. O audit deixou de ser só grader — diagnostica, roteia, e cada estação tem seu protocolo de conserto com loop fechado.

---

## 2026-08-03 · `pais-sardenha/` fica com o nome errado, de propósito

**Contexto**: a convenção do `CLAUDE.md` pra roteiros paralelos da mesma viagem é
`<viagem>-<sufixo>` — logo, o roteiro dos pais deveria estar em `sardenha-pais/`, não em
`pais-sardenha/`. A pasta foi criada antes da convenção existir.

**Decisão**: **não renomear**. A URL `tsferraro.github.io/viagem/pais-sardenha` já está com os
pais, a viagem começa em 06/Ago (três dias depois desta sessão) e renomear quebraria o link
com o roteiro em uso — sem contar o `localStorage` das reservas e dos "feitos", que é
chaveado por página.

**Alternativas rejeitadas**:

| Alternativa | Por que não |
|---|---|
| Renomear pra `sardenha-pais/` | Quebra o link já compartilhado, três dias antes da viagem |
| Renomear + redirect HTML em `pais-sardenha/` | Duas pastas pra mesma viagem, pior que o problema |

**Ação pra próxima viagem**: quando `sardenha/` (o roteiro da família, 16-23/Ago) for criado
em outra sessão, ele nasce com o nome certo. Se um dia o `pais-sardenha/` for arquivado,
arquiva como `sardenha-pais` e o débito morre com ele.

---

## 2026-08-03 · `validate.py` passa a bloquear região hardcoded em URL do Maps

**Contexto**: o bug do `', New York, NY'` cravado em `renderTransit` e do `' New York'` no
fallback de `getMapsUrl` (HANDOFF-bugs-app-ago2026.md) foi reportado **em campo, na Córsega**,
e passou pelo `validate.py` sem ser detectado. O próprio handoff pedia o check.

**Decisão**: novo `check_no_hardcoded_region()` no `validate.py`. Varre **só as linhas que
montam URL de Maps** (`google.com/maps` ou `encodeURIComponent`), ignora as que já usam
`MAPS_REGION`/`regionSuffix()`, e **bloqueia** (erro, não aviso) qualquer literal com cara de
sufixo geográfico — `', New York, NY'`, `' Sardegna'`. A prosa dos `DAYS` fica livre pra citar
qualquer cidade: um roteiro de NYC não vira falso-positivo.

**Duas armadilhas encontradas escrevendo o check** (ambas viraram teste):
1. O strip de comentário `//` comia a própria URL a partir do `https://`. Fix: `(?<!:)//`.
2. A classe de caracteres do sufixo não aceitava vírgula, então `', New York, NY'` — a forma
   exata do bug real — não casava. Fix: vírgula na classe.

**MAPS_REGION ausente é aviso, não erro**: builds anteriores a ago/2026 (marais, nyc-lab-*)
não têm o global. Bloquear travaria uma correção de dica num roteiro antigo por um motivo que
não é o da correção.

---

## 2026-08-04 · O que vai pro Google Maps deixa de ser o nome do card

**Contexto**: Tobia mandou 4 prints do app em campo. Dois mostravam falha dura: o pino do card
`"Walking tour Cidadela · com os avós"` abria o Google Maps **no meio do mar**, e a rota do
walking tour de Bonifacio devolvia **"Can't seem to find that place"**. A causa aparecia no
próprio print: o campo de busca dizia `Porte de Gênes entrada principal`.

O código só apagava os **parênteses** e mandava o conteúdo junto. Isso fazia sentido quando o
parêntese era endereço (`(119 MacDougal)` — a convenção documentada), mas as paradas de walking
tour usam parêntese para **descrição** (`(museu + vista)`, `(cemitério ritual)`, `(info point)`).
Nunca ninguém tinha aberto o link em campo.

**Decisão**: três camadas — `mapsQuery` (explícito, manda em tudo) → `noMaps` (não é lugar) →
limpeza automática (corta no `·`, descarta parêntese descritivo, mantém o que parece endereço).

**A decisão não-óbvia**: a **rota de walking tour passa a usar coordenadas por padrão**, e só usa
nomes quando *todas* as paradas têm `mapsQuery`. Antes era o contrário — tentava nomes e caía pra
coordenada só se faltasse nome. Uma única parada ruim derrubava a rota inteira. Legibilidade da
URL é bonito; rota que abre é obrigatório.

| Alternativa rejeitada | Por quê |
|---|---|
| Melhorar só a limpeza automática | Nenhuma regex transforma "Walking tour Cidadela" num lugar |
| Preencher `mapsQuery` em toda parada de toda WT | Trabalho grande e frágil; a rota por coordenada já resolve hoje, sem risco |
| Deixar o nome sujo e confiar no Google | O print prova que não funciona |

**Guardrail**: `check_maps_query()` no `validate.py` bloqueia card cujo nome viraria busca sem
sentido (lista fechada de prefixos de atividade: walking tour, check-in/out, despedida, chegada…).

**Junto**: chip `☐ Reservas` mostrava `0/0` quando o roteiro não tinha nenhuma reserva —
`reservasComplete` exigia `totalReservas>0`. Agora some nos dois extremos (nenhuma e todas feitas).
E os filtros da aba "Tudo no Mapa" trocaram preto/branco por **azul** no selecionado: no print do
Tobia era impossível dizer o que estava ativo, e no tema escuro o "selecionado" ficava branco
igual ao fundo. `📍 Onde estou` saiu do azul pra não empatar com estado de seleção.

---

## 2026-08-04 (2) · Rota por nome + paradas rotuladas como o Google Maps

Sequência do fix anterior, a partir de mais um print em campo: a rota do walking tour **abria**
(11 min, traçado certo pela cidadela), mas os cinco pontos eram **"Dropped pin"**. Tobia: *"é mto
melhor navegar pelo nome certo do lugar do que pelas coordenadas"*. Certo — coordenada era o piso
seguro, não o alvo.

**Decisão**: preencher `mapsQuery` nas **28 paradas** de walking tour dos dois roteiros, com nomes
canônicos verificados por busca um a um. As 6 rotas passam a usar nomes.

Achados da verificação (nenhum foi chutado):

| Parada | Nome que o Maps acha |
|---|---|
| "Loggia · mirador sul" | a loggia é da própria Sainte-Marie-Majeure; o mirador é **Falaises de Bonifacio** |
| "Necrópole púnica subterrânea" | **Villaggio Ipogeo** (Touring Club: "Necropoli Punica-Villaggio Ipogeo") |
| "Tonnara ruins · Cala Sapone" | **Cala Sapone** (a tonnara está abandonada desde 1825, sem POI próprio) |
| "Spiaggia di Tegge" | **Punta Tegge** |
| "Sa Costa" | **Quartiere Sa Costa** |
| "Lungofiume Temo" | **Ponte Vecchio, Bosa** (é onde o passeio começa) |

**Bug que a verificação evitou**: o walking tour de Bonifacio está no roteiro **da Sardenha**, cujo
`maps_region` é `"Sardegna, Italia"`. Anexar a região mandaria procurar `Porte de Gênes, Bonifacio,
Sardegna, Italia` — ilha errada, país errado. Decisão: **`mapsQuery` nunca recebe `MAPS_REGION`**;
quem escreve deixa inequívoco (`"Porte de Gênes, Bonifacio, Corse, France"`).

## Rótulo das paradas: ○ A B C, não A B C D

Pedido antigo do Tobia (vinha do NYC): os pontos do card deviam usar as letras do Google Maps.
A função `wtLabel` já existia — **desligada e com o mapeamento errado**: fazia `1→A`.

O Maps rotula a **origem** com um círculo sem letra, e só as paradas seguintes com A, B, C. Cinco
paradas são `○ A B C D`. O código antigo produziria `A B C D E`, deslocando tudo em uma casa —
pior que não ter letra nenhuma, porque parece certo e só falha na hora de conferir no chão.

Ligado via `"wt_labels": "letters"` (default segue `"numbers"`). Vale pinos, legenda, popup e as
dicas parada-a-parada, que foram reetiquetadas (27 dicas nos dois roteiros).

**Resíduo achado no caminho**: o popup do pino de walking tour ainda usava `cleanForSearch` — a
limpeza velha, que mantinha `(museu + vista)` na busca. Migrado pra `mapsQueryOf` e a função morta
removida. A feature-chave `'getMapsUrl mantém parens'` do `validate.py` guardava justamente o
comportamento bugado; trocada por três checks da política nova.

## 2026-08-04 · REGRA ZERO: nada de memória · proveniência vira gate mecânico

**Decisão do Tobia, em campo**: *"Só escreva e recomenda atrações a partir de fontes reconhecidas
e confiáveis, nunca da sua 'memória'. O FACTCHECK tem que verificar tudo, não dá pra fazer um
walking tour falso e nem pra passar no factcheck."*

**O que motivou**: o card `"Loggia · mirador sul (falésias)"` do tour da cidadela de Bonifacio
descrevia um mirante **inexistente**, com prosa sobre o calcário mudando de cor por 40 minutos.
"Loggia" é real — é o pórtico da Sainte-Marie-Majeure, parada 3 do mesmo tour. Nome real, função
inventada. Era **parada de walking tour**: virou rota no Maps pros avós. Passou por `validate.py`,
`audit.py` e um FACTCHECK completo rodado no mesmo dia.

Mais três do mesmo tipo no mesmo dia, todos pegos em campo: Cala Lazarina dada como "norte" da
Lavezzi (é sudoeste) · coordenada dada como Lazarina era da Cala di Achiarinu · Ichnusa Lines
declarada inexistente na rota Bonifacio–Santa Teresa (opera, e a mãe do Tobia comprou por ela).

**Diagnóstico da causa**: não foi falta de pesquisa. Foi **texto de fonte e texto de memória
saírem com a mesma cara**. Sem marca de proveniência, nem o autor distingue os dois na revisão
seguinte. A prova: a lição sobre superlativos foi escrita no `corsica/DIARIO.md` de manhã e o
mesmo erro se repetiu seis horas depois. **Regra em prosa não segura — tem que ser mecânica.**

**Por que o FACTCHECK não pegou**: a §4a mandava conferir "toda `mapsQuery` **nova**". A parada
inventada **não tinha `mapsQuery` nenhuma**, e a ausência do campo a tornava invisível ao check.
Um lugar que ninguém consegue nomear pro Maps é o candidato nº 1 a não existir, e era tratado
como "nada a verificar".

**O que mudou (3 camadas)**:
1. `CLAUDE.md` · **REGRA ZERO** — tabela do que exige fonte (posição, função, exclusividade) e o
   que fazer quando não se acha (`[a confirmar]`, `coord_unverified`, ou não criar a parada).
2. `skills/critico-roteiro/FACTCHECK.md` · **§0 EXISTÊNCIA** — roda antes de tudo, cobre 100% das
   paradas de WT e pontos de road trip, **nunca amostra**. Três perguntas por lugar: existe? é o
   que o card diz que é? está onde o card diz? Veredito `NÃO ENCONTRADO` → **remover a parada**.
3. `skills/critico-roteiro/audit.py` · `check_proveniencia()` — card ⭐⭐⭐ sem `fontes` nem
   `links_map` é **P0** · ⭐⭐ é P1 · parada de WT sem `mapsQuery` é **P0**. Testado: injetar uma
   parada inventada faz o `--deploy-gate` sair com exit 1.

**Bug de tooling descoberto no caminho**: `main()` do `audit.py` duplicava a lista de auditores de
`audit_roteiro()` — check novo registrado numa não rodava na outra. Duas fontes de verdade.
Contornado registrando nos dois, com comentário; unificar as listas fica pendente.

**Efeito imediato**: `pais-sardenha` passou a ter **2 P0** (cards ⭐⭐⭐ sem proveniência) e não
passa mais no gate até receber fontes. É o comportamento desejado.

## 2026-08-09 · O post-mortem também errou por afirmar sem checar (R12 da auditoria)

A auditoria independente de 2026-08-08 refutou **duas afirmações do próprio dossiê de erros**
(`AUDITORIA-DOSSIE-2026-08-04.md` §2.2 #4 e §2.4 #10): a coord de La Bobba estava CERTA (nunca
precisou de conserto), e o "Molentargius a 500km" são ~105km — e esse 500 já tinha sido copiado
pro CLAUDE.md como doutrina. Anotado no dossiê (sem apagar: é registro histórico), corrigido no
CLAUDE.md. É o argumento definitivo da REGRA ZERO: **toda frase não-verificada deriva pro erro,
inclusive as do documento que confessa o modo de falha**.

## 2026-08-09 · Edit inline no HTML morre · `data.json` é a única entrada (Lote 7a)

**O que muda**: o `CLAUDE.md` (pipeline de ajuste, passo 3) mandava, "pra mudança pequena",
editar inline o `const DAYS` dentro do `index.html`. Passa a valer o contrário: **TODA mudança
de conteúdo — do typo ao dia novo — edita o `data.json` e roda `build.py`**. O `index.html` é
saída, nunca entrada. `scripts/sync-check.py` vira gate 3b do `deploy.sh` e bloqueia o que não
bater.

**Motivo 1 (conhecido)**: drift. O `data.json` deixava de ser a fonte de verdade e o próximo
rebuild apagava em silêncio o que só existia no HTML — drift já registrado no HANDOFF-PENDENTE,
e o `marais/index.html` estava dessincronizado (ROTEIRO_SLUG velho) quando o gate entrou.

**Motivo 2 (o grave · achado da 2ª rodada da auditoria)**: o edit inline **burlava o gate 4d**.
O `factcheck-gate.py` projeta o conteúdo sensível (⭐⭐⭐ · paradas de WT · `historia[]`) a partir
do **`data.json`**. Editar só o HTML muda o que a família lê sem mexer na projeção: o gate de
frescor não enxerga mudança nenhuma e o deploy passa sem factcheck novo. O atalho que economizava
segundos de `build.py` era uma porta dos fundos no gate mais caro de construir.

**Alternativa rejeitada**: manter o atalho e ensinar o gate 4d a projetar também o HTML. Custa
um segundo parser do artefato de saída pra preservar um atalho que economiza segundos — e
deixaria o drift de pé.

**Método do gate (documentado no próprio script)**: compara a **projeção de dados** dos dois
arquivos (consts `DAYS · LINKS_MAP · TRANSIT_MAP · BAIRROS_CONFIG · HISTORIA · EXTRAS` +
escalares como `AUTH_PASSWORD · MAPS_REGION · ROTEIRO_SLUG`), não os bytes — assim mexer em
`templates/` não vira falso bloqueio. Fica **fora** do escopo: cabeçalho/auth (viram markup) e
a verdade do conteúdo (é FACTCHECK).
