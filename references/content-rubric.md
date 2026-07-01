# Rubrica de Conteúdo · avaliação de conteúdo dos roteiros

Régua **repetível** pra avaliar (e elevar) o conteúdo de qualquer roteiro. Complementa — não substitui — a rubrica de design (`references/design-rubric.md`). Nasceu do Passo 3 do projeto viagem (2026-07-01).

## Ferramenta: scripts/audit-content.py

```bash
python3 scripts/audit-content.py <viagem>/data.json              # audit completo
python3 scripts/audit-content.py <viagem>/data.json --check-links # + verifica URLs HTTP
python3 scripts/audit-content.py <viagem>/index.html             # fallback sem data.json
python3 scripts/audit-content.py <viagem>/data.json --json       # saída JSON (machine-readable)
```

Retorna: **nota /40** por dimensão + achados P0-P3 + checklist manual + veredicto de aprovação.

---

## Relação com destination-scout

A `destination-scout` (skill em `skills/destination-scout/`) é o **degrau 0** — levantamento macro antes do roteiro. A rubrica de conteúdo é o **portão de qualidade** no final. Reutiliza vocabulário e conceitos da scout sem reescrever:

| Conceito na scout | Dimensão nesta rubrica | Reuso |
|---|---|---|
| `audience-profiles.md` · perfis × eixos | D6 Adaptação ao Público | Calibrar pelo elo mais restritivo; sempre perguntar idade |
| `mapping-rubric.md` · veredito 🟢🟡🔴 | D8 Honestidade · campo `risco` | **Mesma escala** · não criar nova |
| `mapping-rubric.md` · logística obrigatória | D3 Logística & Precisão | Distância km, ingresso datado, reserva, horário, ⚠️ segurança |
| `prose-guide.md` · gancho, factual, sem floreio | D1 Storytelling & Escrita | Padrão-ouro Marais + guia que encanta pra gorjeta |
| Anti-invenção (preços datados, sem URL inventada) | D3, D5, D7 | Base dos checks automatizáveis do audit |
| Sabores-assinatura (gastronomia com identidade) | D8 Honestidade | Cards de restaurante com ingrediente local |

**Regra de ouro**: UMA fonte de verdade pra veredito/perfil/anti-invenção. Se um conceito precisar mudar, muda na skill-origem. Esta rubrica aponta pra lá.

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

**Aprovação automática**: nota ≥28 E P0=0. Claude aspira ≥32 antes de desistir.

---

## Loop-até-excelente

```
build.py data.json index.html          ← gera HTML
validate.py index.html                 ← checks estruturais (P0 técnico)
audit-content.py data.json             ← checks de conteúdo (P0-P3 + nota /40)
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

## Pipeline completo (os 3 degraus)

```
destination-scout (curadoria macro do destino)
    ↓ inventário curado + vereditos + história
roteiro-viagem pipeline (build.py + validate.py)
    ↓ HTML single-file validado
audit-content.py (portão de qualidade)
    ↓ nota /40 + P0-P3 + aprovação
deploy.sh → GitHub Pages ao vivo
```

O audit pode verificar se o roteiro **honrou os padrões da scout**: veredito por atração, preços datados, distâncias em km, público calibrado.
