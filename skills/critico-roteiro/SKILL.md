---
name: critico-roteiro
description: 'Portão de qualidade de CONTEÚDO dos roteiros e levantamentos. É o irmão do impeccable (que cuida do design) — aqui o eixo é conteúdo: escrita/storytelling, profundidade de card, logística e preços datados, coords, links vivos, adaptação ao público (família c/ criança), walking tours, honestidade ("pula sem culpa"), cobertura e arco/ritmo. Roda o script audit.py em DOIS modos — (1) ROTEIRO (data.json/index.html · 10 dimensões · /40) e (2) SCOUT (--scout · levantamento .md da destination-scout · 5 dimensões · /20). Use quando (1) vai ENTREGAR um roteiro ou levantamento e precisa passar pelo gate de qualidade (loop-até-excelente); (2) quer AVALIAR/MELHORAR conteúdo já feito; (3) roda embutido no pipeline da roteiro-viagem (passo 9b) e da destination-scout (antes do export). Retorna nota + achados P0-P3 + checklist manual + veredito de aprovação. Fonte de verdade do veredito/preço-datado/fontes é skills/destination-scout/references/mapping-rubric.md — esta skill VERIFICA essas regras, não as reescreve. Rubrica detalhada em references/content-rubric.md.'
---

# Crítico de Roteiro · portão de qualidade de conteúdo

Skill runnable que avalia (e ajuda a elevar) o **conteúdo**. Espelha o `impeccable` (design):

| Eixo | Régua (doc) | Skill runnable |
|---|---|---|
| **Design** | `references/design-rubric.md` | `skills/impeccable/` |
| **Conteúdo** | `references/content-rubric.md` | `skills/critico-roteiro/` (esta) |

## O que faz

Roda `audit.py` sobre um artefato de conteúdo e devolve **nota + achados P0-P3 + checklist manual + veredito**. É semi-automático: o script pega o automatizável de verdade (preço sem data, link 4xx, coord rasa, campo faltando, hype vazio, veredito ausente); o **checklist manual** cobre o que exige julgamento humano (a prosa encanta? o veredito está calibrado ao perfil?).

## Os 2 modos

```bash
# ROTEIRO · data.json (preferido) ou index.html · 10 dimensões · /40
python3 skills/critico-roteiro/audit.py <viagem>/data.json
python3 skills/critico-roteiro/audit.py <viagem>/data.json --check-links   # + HTTP nos links
python3 skills/critico-roteiro/audit.py <viagem>/index.html                # fallback sem data.json

# SCOUT · levantamento .md da destination-scout · 5 dimensões · /20
python3 skills/critico-roteiro/audit.py entregas/<slug>.md --scout             # macro (Fontes obrigatória)
python3 skills/critico-roteiro/audit.py entregas/<slug>.md --scout --terceiros # pra-terceiros (Fontes opcional)

# comum aos dois
--suggest       # PLANO DE CONSERTO: roteia cada achado + top-5 + patches prontos
--diff <antes>  # LOOP FECHADO: <depois>.json --diff <antes>.json · delta + regressão
--json          # saída machine-readable (inclui station/hint/half por achado)
--no-checklist  # omite checklist manual (CI)
```

Exit code: `0` aprovado · `1` não aprovado · `2` erro de input.

| Modo | Nota | Aprovação | Bandas |
|---|---|---|---|
| Roteiro | /40 (10 dim × 4) | **≥32** **E** P0=0 | 36-40 Excelente · 32-35 Bom · 28-31 Aceitável · <28 Ruim |
| Scout | /20 (5 dim × 4) | **≥16** **E** P0=0 | 18-20 Excelente · 16-17 Bom · 12-15 Aceitável · <12 Ruim |

Régua elevada de 28→32 em 2026-07-01 (a 28, 4 de 5 roteiros reais passavam com 3-8 P1s não corrigidos). Aspira-se **≥36**.

### A nota tem 2 metades (não misturar)

| Metade | Dims | Confiança | Como usar |
|---|---|---|---|
| **Mecânico** /20 | D2·D3·D4·D5·D9 | alta — regex checa o verificável | corrigir aqui primeiro (gaps objetivos: datas, coords, schema) |
| **Julgamento** ⚖️ /20 | D1·D6·D7·D8·D10 | baixa — regex é só piso | **Claude confirma no checklist**; não confiar no número |

O relatório imprime as duas metades separadas (`mec 15/20 · julg⚖️ 19/20`). O regex não sabe se a prosa encanta — a metade ⚖️ existe pra apontar onde olhar, não pra dar veredito.

O modo **scout** auto-detecta **mini-plano** (âncora fixa, sem tabela de veredito) vs **macro**: no mini-plano, veredito-por-atração vira N/A e Fontes fica opcional. `--terceiros` relaxa Fontes em qualquer levantamento (a lista de URLs fica no chat, não se manda pra mãe — decisão Tobia).

## Os 3 instrumentos (2026-07-12 · avaliação em camadas)

O `audit.py` é o 1º de **três instrumentos** desta skill — cada um enxerga o que o outro não vê:

| Instrumento | Mede | Como | Quando |
|---|---|---|---|
| **`audit.py`** (regex) | **Forma** — raso, sem data, sem veredito, link morto | script offline, grátis | sempre (todo edit) |
| **`FACTCHECK.md`** (protocolo) | **Verdade** — preço/coord/fato confere na fonte? | sub-agentes céticos + web_search | entregas · pré-viagem (nunca em edit pequeno) |
| **`JUDGE.md`** (protocolo) | **Substância** — interessante? bem curado? nível do exemplar-ouro? | sub-agente cético de contexto limpo, comparação pareada c/ exemplar | 1× por entrega, só APÓS audit limpo · teto 1+1 |

Ordem obrigatória: **audit → factcheck → judge** (barato antes do caro; nunca julgar o que o regex já reprovaria). Régua de fontes dos dois protocolos: `references/source-credibility.md`.

Os 3 acima **avaliam**. Há mais **2 protocolos de conserto** — o que o `--suggest` despacha pra 🔎 e ✍️:

| Protocolo | Estação | Faz |
|---|---|---|
| **`RESEARCH.md`** | 🔎 | executa a fila de pesquisa com o contrato anti-invenção (preço datado · coord verificada ou `coord_unverified` · URL 2xx · senão `[a confirmar]`) |
| **`REWRITE.md`** | ✍️ | eleva a prosa ao padrão-ouro Marais (`sobre` conta história · `imperdivel` = o que observar · dicas parada-a-parada), grava direto |

Ciclo completo de conserto: **research → rewrite → `--diff` → factcheck → judge**. O `--diff` é a trava barata entre lotes (mecânico não pode cair); factcheck/judge rodam 1× na entrega.

## O que isto É (honestidade de framing)

É um **linter de conteúdo com camada de julgamento** — não uma IA que julga escrita. O `audit.py` é determinístico (irmão do `validate.py`, que é estrutural); a metade mecânica é autoridade, a metade ⚖️ é piso que o **Claude** confirma. Fica em `skills/` (não `scripts/`) porque consolida régua + runnable + guia de julgamento num lugar só, e roda de qualquer sessão (desktop/cloud) via `python3 skills/critico-roteiro/audit.py`.

**Tem suite de regressão própria** (`tests/run_tests.py` · 20 checks): o auditor testando a si mesmo. Rode sempre que mexer no `audit.py` — trava nota/severidade/roteamento/`--diff` contra drift de regex. Ver `tests/README.md`.

## Onde roda (loop-até-excelente + enforcement no deploy)

| Pipeline | Onde entra | Enforça? |
|---|---|---|
| **roteiro-viagem** | passo 9b: build → validate → **audit** → corrige P1 até ≥32 → deploy | loop (Claude) |
| **deploy.sh** | após validate: `audit.py --deploy-gate` no HTML que vai pro ar | **sim** — bloqueia em P0 (`VIAGEM_STRICT=1` bloqueia <32) |
| **destination-scout** | antes do PASSO 5 (export): rascunho .md → **audit --scout** → corrige → gera PDF | loop (Claude) |
| **standalone** | pra auditar/melhorar um roteiro ou levantamento já entregue | não |

**Dois níveis de enforcement, de propósito**: a régua de **32** vive no *loop da sessão* (Claude itera até bater); o **deploy** bloqueia só em **P0** (erro objetivo: card vazio, link oficial morto) — heurística mole não deve brickar o acesso da família ao roteiro. Quer barra máxima no push? `VIAGEM_STRICT=1`.

`walking-tour-designer` e `road-trip-designer` **não** têm gate próprio — o output deles vira card do roteiro e é pego pela dimensão **D7 (Walking Tours)** do audit de roteiro.

## `--suggest` · o grader vira router

Sem isto o audit diagnostica e **para**. Com `--suggest`, cada achado é despachado pra uma das **4 estações de conserto** — e a taxonomia **herda** o split mecânico/⚖️, não inventa outro eixo:

| Estação | Quando | Vem no `hint` |
|---|---|---|
| 🔧 **Corrigir** | conserto determinístico | o patch pronto pra colar |
| 🔎 **Pesquisar** | falta um fato externo (preço, coord, URL, história) | a busca a fazer + como gravar → executa via `RESEARCH.md` |
| ✍️ **Reescrever** | o fato existe, falta a escrita | o que a prosa precisa ter → executa via `REWRITE.md` |
| 🤔 **Você decide** | julgamento do Tobia (ritmo, "isso é fraco?") | **nunca** vira patch |

Também imprime **top-5 cards** (severidade × peso do card: âncora vale 2, filler 1) e **densidade por dia** — triagem pra saber onde atacar. A densidade **não é nota por dia**: D9/D10 só existem no roteiro inteiro, então nota diária seria incompleta ou enganosa.

⚠️ **Guarda anti-Goodhart** (governa os hints): perseguir o número só é alvo legítimo na metade **mecânica**, onde o regex é autoridade. Nas dims ⚖️ o número é proxy — inflar `sobre` até 150 chars ou salpicar um ano de 4 dígitos sobe a nota sem melhorar o roteiro. Por isso nenhum hint de dim ⚖️ manda "faça X pra subir a nota"; manda o que a prosa precisa ter, e quem valida é o checklist.

No `--json`, cada achado carrega `station`, `hint` e `half` — um sub-agente despacha lendo JSON, sem parsear texto.

## Regras da avaliação (herança do repo)

- **Honestidade > diplomacia**: a auditoria é real. Link morto → acusa. Card raso → nota baixa. Sem teatro.
- **Uma fonte de verdade**: veredito 🏆⚠️⏭️ (🟢🟡🔴 nas entregas até 2026-08-09 · o audit aceita os dois), preço datado e Fontes vêm da `mapping-rubric.md` da destination-scout. Esta skill VERIFICA, não redefine.
- **Alertas não viram cortes**: o alerta de ritmo (dias "pesados" pra criança) é **P3 advisory** — sinaliza pra o Tobia decidir e remanejar se achar válido; **nunca** corta stop automaticamente nem bloqueia entrega.
- **Falso-positivo é bug**: se um check acusa algo legítimo (ex: "perto" na etimologia de um nome, não numa distância), o check está errado e se corrige — não se ignora.

## As 10 dimensões (roteiro) · resumo

D1 Storytelling · D2 Profundidade de card · D3 Logística & precisão · D4 Coords · D5 Links · D6 Adaptação ao público · D7 Walking tours · D8 Honestidade & curadoria · D9 Cobertura & schema · D10 Arco & ritmo. Detalhe de cada uma (âncoras 0/2/4 + fonte) em `references/content-rubric.md`.

## As 5 dimensões (scout) · resumo

S1 Anti-invenção & preços (datados) · S2 Veredito 🏆⚠️⏭️ & honestidade · S3 Logística (km, não "perto") · S4 Fontes & verificação · S5 Estrutura & cobertura (ordem mapeamento→história, sabores-assinatura, clusters).

## Loop-até-excelente · como iterar

1. Roda o audit no artefato.
2. **P0 presente** → corrige (é bloqueio objetivo) → re-roda.
3. **nota < limiar (32 roteiro / 16 scout) ou P1 aberto** → corrige, priorizando:
   - **a) metade mecânica primeiro** (D2·D3·D4·D5·D9): gaps objetivos e baratos — preço sem data, coord <4 casas, TRANSIT_MAP incompleto, campo faltando. É onde o número é confiável e o ganho é rápido.
   - **b) metade ⚖️ julgamento** (D1·D6·D7·D8·D10): abre o artefato e o checklist manual e **decide** — a prosa encanta? o veredito calibra pro perfil? Não persegue o número do regex; persegue a qualidade real.
4. **nota ≥ limiar e P0=0** → APROVADO · confirma as dims ⚖️ no checklist · mostra a nota (com as 2 metades) na entrega.
5. Máx ~3 rodadas automáticas; se não converge, o problema é de conteúdo (pesquisa/curadoria), não de formato — leva pro Tobia.
