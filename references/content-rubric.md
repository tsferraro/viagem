# Rubrica de Conteúdo · avaliação de conteúdo dos roteiros

Régua **repetível** pra avaliar (e elevar) o conteúdo de qualquer roteiro. Complementa — não substitui — a rubrica de design (`references/design-rubric.md`). Nasceu do Passo 3 do projeto viagem (2026-07-01).

## Ferramenta: skill `critico-roteiro` (`skills/critico-roteiro/audit.py`)

Esta rubrica é a **régua**; a skill `critico-roteiro` é o **runnable** que a aplica (espelha `design-rubric.md` ↔ `impeccable`). Dois modos:

```bash
# ROTEIRO · 10 dimensões · /40
python3 skills/critico-roteiro/audit.py <viagem>/data.json              # audit completo
python3 skills/critico-roteiro/audit.py <viagem>/data.json --check-links # + verifica URLs HTTP
python3 skills/critico-roteiro/audit.py <viagem>/index.html             # fallback sem data.json

# SCOUT · levantamento .md da destination-scout · 5 dimensões · /20
python3 skills/critico-roteiro/audit.py entregas/<slug>.md --scout             # macro (Fontes obrigatória)
python3 skills/critico-roteiro/audit.py entregas/<slug>.md --scout --terceiros # pra-terceiros (Fontes opcional)

python3 skills/critico-roteiro/audit.py <arquivo> --json                # saída machine-readable
```

Retorna: **nota** por dimensão + achados P0-P3 + checklist manual + veredito de aprovação. Detalhes de invocação e modos: `skills/critico-roteiro/SKILL.md`.

---

## Relação com destination-scout

A `destination-scout` (skill em `skills/destination-scout/`) é o **degrau 0** — levantamento macro antes do roteiro. A rubrica de conteúdo é o **portão de qualidade** no final. Reutiliza vocabulário e conceitos da scout sem reescrever:

| Conceito na scout | Dimensão nesta rubrica | Reuso |
|---|---|---|
| `audience-profiles.md` · perfis × eixos | D6 Adaptação ao Público | Calibrar pelo elo mais restritivo; sempre perguntar idade |
| `mapping-rubric.md` · veredito 🟢🟡🔴 | D8 Honestidade (honestidade **na prosa**) | Recomendação (faça/depende/pula). ⚠️ **NÃO é o campo `risco`** — ver nota abaixo |
| `mapping-rubric.md` · logística obrigatória | D3 Logística & Precisão | Distância km, ingresso datado, reserva, horário, ⚠️ segurança |
| `prose-guide.md` · gancho, factual, sem floreio | D1 Storytelling & Escrita | Padrão-ouro Marais + guia que encanta pra gorjeta |
| Anti-invenção (preços datados, sem URL inventada) | D3, D5, D7 | Base dos checks automatizáveis do audit |
| Sabores-assinatura (gastronomia com identidade) | D8 Honestidade | Cards de restaurante com ingrediente local |

**Regra de ouro**: UMA fonte de verdade pra veredito/perfil/anti-invenção. Se um conceito precisar mudar, muda na skill-origem. Esta rubrica aponta pra lá.

> ⚠️ **`risco` (roteiro) ≠ veredito 🟢🟡🔴 (scout)** — escalas diferentes, não confundir:
> - **`risco`** do roteiro = **multidão/esforço** operacional (green=tranquilo · yellow=atenção · red=Times Square lotada). É um aviso de campo, não uma recomendação.
> - **veredito** da scout = **recomendação** (🟢 faça · 🟡 depende · 🔴 pula sem culpa).
> - Uma atração linda porém lotada é `risco=red` **mas** 🟢 *faça*. No roteiro o veredito 🔴 já foi "consumido" (o que não valia foi cortado na curadoria); o que sobra expressa honestidade **na prosa** (`sobre`/`dicas` com "pula sem culpa"), não num campo. Por isso **D8 audita honestidade no texto**, e usa a distribuição de `risco` só como proxy de "nem tudo é rosa" — não como se `risco` fosse o veredito.

---

## Contexto de uso (o que define "excelente" AQUI)

Roteiro é usado **no campo, uma mão, no sol, com criança de 3 anos** — não é artigo de revista.

| Padrão-ouro | Barra concreta |
|---|---|
| Rick Steves "stubbornly selective" | Profundidade > cobertura. Dizer "pula sem culpa" é diferencial, não fraqueza |
| Free walking tour (ganhar gorjeta) | `sobre` conta história/curiosidade com fato concreto. `imperdivel` = o que o distraído perde |
| Prose-guide.md (Chapada) | Gancho de abertura, factual, sem floreio vazio ("paraíso indescritível" = zero informação) |
| Mapping-rubric.md (Chapada) | Veredito por perfil, distância em km, ingresso datado, ⚠️ segurança |
| Família com filha de 3a | Carrinho/escada/sombra/banheiro visíveis. Cadência 1h30 max. Elo mais restritivo calibra |

---

## 10 dimensões · 0-4 cada · /40 total

| # | Dimensão | O que checa | 4 (excelente) | 2 (aceitável) | 0 (ruim) | Auto? | Fonte |
|---|---|---|---|---|---|---|---|
| D1 | **Storytelling & Escrita** | `sobre` conta história c/ fato concreto; `imperdivel` = o que observar; dicas narram parada-a-parada; HTML cru (`<strong>`/`<em>`), zero floreio | Todo card-chave: ano/data/nome/lenda em `sobre`, imperdivel específico (não "incrível!"), WT dicas numeradas | Maioria ok, alguns sobre descritivos sem fato | Maioria genérica ou vazia | Proxy | prose-guide.md · padrão-ouro Marais |
| D2 | **Profundidade de Card** | Quality bar dos campos: `sobre` ≥100 chars, `imperdivel` ≥25 chars não-genérico, `dicas` ≥2 c/ hora/preço, `duracao` range, `custo` real, `acessibilidade` ≥20 chars | Avg ≥5/6 campos bem preenchidos | Avg 3/6 | Avg <2/6 | Sim | CLAUDE.md §quality bar · data-schema.md |
| D3 | **Logística & Precisão** | `custo` c/ data (mês/ano); TRANSIT_MAP cobrindo transit stops; sem "perto/próximo" vago; distância em km | TRANSIT_MAP ≥80% coberto; custo datado >70% pagos; zero "perto" | TRANSIT_MAP 40-70%; custo sem data em metade | TRANSIT_MAP <40%; tudo vago | Sim | mapping-rubric.md §logística obrigatória |
| D4 | **Coords & Precisão** | 4 casas decimais; range válido; endereço entre parens nos stops de WT; `coord_unverified` flaggado | Zero < 4 casas; WT stops c/ endereço em parens >70%; nenhum unverified sem flag | Alguns 3 casas; parens <50% dos WT stops | Coords inventadas ou <3 casas | Sim | CLAUDE.md §coords · walking-tour-designer SKILL |
| D5 | **Links & Verificação** | LINKS_MAP não-vazio; `type:official` presente; 0 broken (4xx/5xx); nenhuma URL inventada | LINKS_MAP preenchido c/ official + reviews; 0 broken | Alguns links ausentes em cards principais | LINKS_MAP vazio ou links 404 | Sim + `--check-links` | CLAUDE.md §links · validate.py --check-links |
| D6 | **Adaptação ao Público** | `acessibilidade` em cards risco yellow/red; sem avisos paternalistas (metrô, elevador); ≤6 cards/dia; dia de chegada/saída ≤3 cards | Acessibilidade em 100% dos risco yellow/red; zero paternalismo; ritmo saudável | Acessibilidade em 50-80% dos arriscados; 1-2 dias sobrecarregados | Acessibilidade ausente nos críticos; aviso patronizante; dias com 8+ cards | Parcial | audience-profiles.md · tobia-preferences.md §1+2 |
| D7 | **Walking Tours** | Partes com 4-8 stops; dicas numeradas 1️⃣2️⃣; WT stops c/ endereço em parens; partition se >8 stops; ângulo único por WT | Todas partes 4-8 stops; dicas numeradas em >50% dos WT cards; ≥50% stops c/ parens | Partes ok, sem numeração; parens parciais | Parte >8 sem partition; zero storytelling parada-a-parada | Parcial | CLAUDE.md §walking tours · walking-tour-designer SKILL |
| D8 | **Honestidade & Curadoria** | risco distribution (não tudo green); "pula sem culpa" onde existe fraco; armadilhas sinalizadas; zero hipérbole no `imperdivel` | <90% green; ao menos 1 "pula sem culpa"; zero "incrível/fantástico" no imperdivel | 90-99% green; crítica rara | 100% green; zero crítica; hipérbole em todo imperdivel | Parcial | mapping-rubric.md §veredito + §armadilhas · tobia-preferences §3 |
| D9 | **Cobertura & Schema** | Todos dias têm ≥1 card; temaCurto ≤15; `opcoes` 2-4 items c/ preço+dist; `nota` em dias complexos | 100% schema preenchido; temaCurto ≤15 em todos; opcoes bem formadas | Maioria ok, 1-2 gaps | Cards/dias missing; temaCurto longo; opcoes sem preço | Sim | data-schema.md · CLAUDE.md §schema |
| D10 | **Arco & Ritmo** | `tema` em todos dias; ordem manha→tarde→noite; ≤5 cards/dia família; big picture claro | Todos dias c/ tema; ordem temporal coerente; nenhum dia sobrecarregado | Maioria ok, ordem inconsistente em 1-2 dias | Dias sem tema; caos temporal; roteiro maratona | Parcial | lessons-learned §5 · tobia-preferences §4 |

---

## Fundamentação externa (state of the art)

A rubrica não é achismo — cada dimensão-chave ancora numa best-practice **externa** reconhecida (não só nos docs internos do repo). O levantamento macro da `destination-scout` calibra pra família do Tobia; estas fontes dão a espinha editorial:

| Dimensão | Autoridade externa | Princípio importado |
|---|---|---|
| **D1 Storytelling** | Craft de travel writing · Rick Steves | *"Show, don't tell"* + especificidade (o detalhe concreto vence o genérico); *"anticipate what the traveler needs to know just before they realize they need to know it"* |
| **D2 Profundidade** | Rick Steves (depth > breadth) | *"If a place is covered, it's covered completely"* — profundidade > cobertura; ser **opinativo**, rankear por mérito |
| **D3 Logística** | Lonely Planet (on-the-ground) | **Recência**: pesquisa verificada nos últimos ~18 meses · preço/horário atuais · "inaccuracies quickly fixed" → preço datado não é capricho, é anti-apodrecimento |
| **D5 Links** | Lonely Planet · reviews | Filtrar por "mais recente"; link/preço velho engana tanto quanto link morto |
| **D6 Adaptação** | REI · consenso family-travel | **1-2 atividades _principais_/dia**; ancorar no viajante mais novo; janela da criança (~9h-12h e 16h-18h); pausa de ≥90min no meio |
| **D8 Honestidade** | Rick Steves · guias anti-turistada | *"Stubbornly selective"*; sinais de cilada: só turistas (poucos locais), retail-heavy, hype "must-see", reviews todas em inglês/na mesma semana |
| **D10 Arco & Ritmo** | Literatura de route-optimization | **Clustering geográfico**: agrupar por proximidade, minimizar backtracking cross-borough, coerência espacial por dia |

> Nota de recência (D3/D5): todo preço/horário carrega data de referência ("(mês/ano)") **e** se assume validade de ~18 meses (regra Lonely Planet). Levantamento/roteiro com preço sem data perde ponto em D3 — não por formato, mas porque a informação apodrece e vira armadilha silenciosa.

**Fontes**: [Rick Steves — Travel Philosophy](https://www.ricksteves.com/press-room/ricks-travel-philosophy) · [What Makes a Good Guidebook](https://blog.ricksteves.com/cameron/2023/02/good-guidebook) · [Lonely Planet — accuracy](https://support.lonelyplanet.com/hc/en-us/articles/218157937-General-guidebook-information) · [Show, Don't Tell (Reedsy)](https://reedsy.com/blog/show-dont-tell/) · [REI — Traveling with Kids](https://www.rei.com/learn/expert-advice/traveling-with-kids.html) · [Pacing trips with kids](https://noplacelikeanywhere.com/how-can-i-help/planning/how-to-pace-your-trips-with-kids-to-avoid-fatigue-and-burnout/) · [Avoiding tourist traps](https://www.atlasroadtravel.com/blog/how-to-avoid-tourist-traps) · [Route optimization best practices](https://zeorouteplanner.com/route-optimization-best-practices-cut-travel-time-by-30/)

---

## Severidade dos achados

| Nível | Significado | Exemplo |
|---|---|---|
| **P0** | Bloqueia deploy | Coord inventada sem flag; URL 404 em link oficial; card tipo=card completamente vazio (sem sobre + dicas + imperdivel) |
| **P1** | Corrigir antes de entregar | `sobre` < 50 chars; `imperdivel` genérico ("incrível!"); `acessibilidade` ausente em risco yellow/red; WT parte >8 stops sem partition |
| **P2** | Recomendado · não bloqueia | `custo` sem data de referência; só 1 dica; TRANSIT_MAP incompleto; link review ausente em card principal |
| **P3** | Sugestão · opcional | Links não checados via HTTP; `nota` ausente; temaCurto poderia ser mais específico; WT sem dicas numeradas |

---

## Bandas de pontuação

| Nota | Banda | Ação no loop |
|---|---|---|
| 36-40 | **Excelente** | Entrega automática |
| 28-35 | **Bom** | Entrega se sem P0s e sem P1s abertos |
| 20-27 | **Aceitável** | Iterar: corrigir P1s até ≥28 |
| <20 | **Ruim** | Refazer seções afetadas |

**Aprovação automática**: nota ≥28 E P0=0. **Barra de aspiração (padrão-ouro, decisão Tobia 2026-07-12): mira Excelente ≥36/40** — ≥28 é o piso que libera deploy, não o alvo. A profundidade do roteiro herda a do levantamento: um scout raso gera roteiro raso. Se o levantamento foi feito no padrão-ouro (ver `skills/destination-scout/SKILL.md` §Padrão-ouro de profundidade), os cards do roteiro já nascem com `sobre` factual, `imperdivel` = "o que observar", dicas com hora/preço e vereditos calibrados — que é o que puxa a nota de "Bom" pra "Excelente".

---

## Loop-até-excelente

```
build.py data.json index.html               ← gera HTML
validate.py index.html                      ← checks estruturais (P0 técnico)
critico-roteiro/audit.py data.json          ← checks de conteúdo (P0-P3 + nota /40)
        ↓
  P0 presente? → Claude lê achados → corrige data.json → re-build → re-audit
                 (máx 3 rodadas automáticas)
        ↓ sem P0
  nota < 28 ou P1 aberto?
    → Claude corrige P1s no data.json → re-build → re-audit
        ↓
  nota ≥ 28 e sem P0 → APROVADO
        ↓
deploy.sh → exibe na entrega:
  ✓ Estrutura:  validate.py  0 erros
  ★ Conteúdo:   34/40 · Bom  |  P0: 0  P1: 0  P2: 2  P3: 1
  URL: https://tsferraro.github.io/viagem/<slug>/
```

---

## Checklist manual (dimensões de julgamento humano)

O audit gera este checklist automaticamente nas dimensões que não são 100% automatizáveis:

| Dimensão | O que verificar manualmente |
|---|---|
| **D1 Storytelling** | `sobre` conta história/curiosidade (data, personagem, lenda) OU é só descrição? `imperdivel` = o que observar vs. platitude? Dicas de WT narram parada-a-parada? |
| **D6 Adaptação** | Ritmo de criança 3a respeitado (sombra, banheiro, colo)? Elo mais restritivo calibra vereditos? Atrações família têm kids-friendly destacado? |
| **D7 Walking Tours** | Ângulo único por WT (não genérico "conheça o bairro")? Rubrica de valor justificada antes do tour? Storytelling parada-a-parada presente? |
| **D8 Honestidade** | Atrações fracas/turistadas marcadas com "pula sem culpa"? Armadilhas sinalizadas (fila inútil, foto enganosa)? Todo card tem info que o viajante usa (não filler)? |
| **D10 Arco** | Big picture de cada dia claro no tema/nota? Sequência geográfica eficiente (sem backtrack)? Roteiro como um todo tem ritmo saudável? |

---

## Modo scout · auditoria do levantamento `.md` (/20)

A mesma skill (`--scout`) audita os levantamentos da `destination-scout` — outro formato (prosa + tabelas), **mesmos princípios** (mapping-rubric). 5 dimensões × 4 = **/20**:

| # | Dimensão | 4 (excelente) | 0 (ruim) |
|---|---|---|---|
| S1 | **Anti-invenção & Preços** | Todo preço datado "(mês/ano)" | Maioria dos preços sem data |
| S2 | **Veredito & Honestidade** | 🟢🟡🔴 por atração + armadilha sinalizada + zero hype | Nenhum veredito (vira folder de agência) |
| S3 | **Logística & Precisão** | Distância em km/min (não "perto") + ingresso/reserva/horário | Tudo vago |
| S4 | **Fontes & Verificação** | Seção Fontes presente | Sem Fontes **no macro** (opcional em pra-terceiros/mini) |
| S5 | **Estrutura & Cobertura** | Resumo no topo · mapeamento antes de história · sabores-assinatura · clusters | Ordem trocada, sem sabores, sem clusters |

- Bandas: 18-20 Excelente · 14-17 Bom · 10-13 Aceitável · <10 Ruim. **Aprovação: ≥14 E P0=0.**
- **Barra de aspiração (padrão-ouro, decisão Tobia 2026-07-12):** aprovar em ≥14 é o *piso* (não travar entregas enxutas legítimas — pra-terceiros, mini-plano). Mas o **alvo de toda entrega macro é Excelente ≥18/20** — a profundidade da entrega `entregas/roma-toscana-florenca-set2026.md` (19/20) é a referência concreta a igualar (ver `skills/destination-scout/SKILL.md` §Padrão-ouro de profundidade). Não desistir em "Bom" quando dá pra chegar em "Excelente".
- Auto-detecta **mini-plano** (âncora fixa, sem tabela de veredito): veredito-por-atração vira N/A, Fontes opcional.
- `--terceiros`: relaxa Fontes (lista de URLs fica no chat, não se manda pra terceiros — decisão Tobia).

---

## Pipeline completo (os degraus + os 2 loops)

```
destination-scout (curadoria macro do destino)
    ↓ rascunho .md
  [LOOP SCOUT] critico-roteiro --scout → nota /20 → corrige → PDF export
    ↓ inventário curado + vereditos + história (aprovado)
roteiro-viagem pipeline (build.py + validate.py)
    ↓ HTML single-file validado
  [LOOP ROTEIRO] critico-roteiro → nota /40 → corrige P1 → aprovado
    ↓
deploy.sh → GitHub Pages ao vivo
```

O audit verifica se o artefato **honrou os padrões da scout**: veredito por atração, preços datados, distâncias em km, público calibrado, Fontes citadas (quando macro).
