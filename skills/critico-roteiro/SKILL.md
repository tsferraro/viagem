---
name: critico-roteiro
description: Portão de qualidade de CONTEÚDO dos roteiros e levantamentos. É o irmão do impeccable (que cuida do design) — aqui o eixo é conteúdo: escrita/storytelling, profundidade de card, logística e preços datados, coords, links vivos, adaptação ao público (família c/ criança), walking tours, honestidade ("pula sem culpa"), cobertura e arco/ritmo. Roda o script audit.py em DOIS modos — (1) ROTEIRO (data.json/index.html · 10 dimensões · /40) e (2) SCOUT (--scout · levantamento .md da destination-scout · 5 dimensões · /20). Use quando (1) vai ENTREGAR um roteiro ou levantamento e precisa passar pelo gate de qualidade (loop-até-excelente); (2) quer AVALIAR/MELHORAR conteúdo já feito; (3) roda embutido no pipeline da roteiro-viagem (passo 9b) e da destination-scout (antes do export). Retorna nota + achados P0-P3 + checklist manual + veredito de aprovação. Fonte de verdade do veredito/preço-datado/fontes é skills/destination-scout/references/mapping-rubric.md — esta skill VERIFICA essas regras, não as reescreve. Rubrica detalhada em references/content-rubric.md.
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
--json          # saída machine-readable
--no-checklist  # omite checklist manual (CI)
```

Exit code: `0` aprovado · `1` não aprovado · `2` erro de input.

| Modo | Nota | Aprovação | Bandas |
|---|---|---|---|
| Roteiro | /40 (10 dim × 4) | ≥28 **E** P0=0 | 36-40 Excelente · 28-35 Bom · 20-27 Aceitável · <20 Ruim |
| Scout | /20 (5 dim × 4) | ≥14 **E** P0=0 | 18-20 Excelente · 14-17 Bom · 10-13 Aceitável · <10 Ruim |

O modo **scout** auto-detecta **mini-plano** (âncora fixa, sem tabela de veredito) vs **macro**: no mini-plano, veredito-por-atração vira N/A e Fontes fica opcional. `--terceiros` relaxa Fontes em qualquer levantamento (a lista de URLs fica no chat, não se manda pra mãe — decisão Tobia).

## Onde roda (loop-até-excelente)

| Pipeline | Onde entra |
|---|---|
| **roteiro-viagem** | passo 9b: build → validate → **audit** → corrige P1 → deploy |
| **destination-scout** | antes do PASSO 5 (export): rascunho .md → **audit --scout** → corrige → gera PDF |
| **standalone** | pra auditar/melhorar um roteiro ou levantamento já entregue |

`walking-tour-designer` e `road-trip-designer` **não** têm gate próprio — o output deles vira card do roteiro e é pego pela dimensão **D7 (Walking Tours)** do audit de roteiro.

## Regras da avaliação (herança do repo)

- **Honestidade > diplomacia**: a auditoria é real. Link morto → acusa. Card raso → nota baixa. Sem teatro.
- **Uma fonte de verdade**: veredito 🟢🟡🔴, preço datado e Fontes vêm da `mapping-rubric.md` da destination-scout. Esta skill VERIFICA, não redefine.
- **Alertas não viram cortes**: o alerta de ritmo (dias "pesados" pra criança) é **P3 advisory** — sinaliza pra o Tobia decidir e remanejar se achar válido; **nunca** corta stop automaticamente nem bloqueia entrega.
- **Falso-positivo é bug**: se um check acusa algo legítimo (ex: "perto" na etimologia de um nome, não numa distância), o check está errado e se corrige — não se ignora.

## As 10 dimensões (roteiro) · resumo

D1 Storytelling · D2 Profundidade de card · D3 Logística & precisão · D4 Coords · D5 Links · D6 Adaptação ao público · D7 Walking tours · D8 Honestidade & curadoria · D9 Cobertura & schema · D10 Arco & ritmo. Detalhe de cada uma (âncoras 0/2/4 + fonte) em `references/content-rubric.md`.

## As 5 dimensões (scout) · resumo

S1 Anti-invenção & preços (datados) · S2 Veredito 🟢🟡🔴 & honestidade · S3 Logística (km, não "perto") · S4 Fontes & verificação · S5 Estrutura & cobertura (ordem mapeamento→história, sabores-assinatura, clusters).

## Loop-até-excelente · como iterar

1. Roda o audit no artefato.
2. **P0 presente** → corrige (é bloqueio) → re-roda.
3. **nota < limiar ou P1 aberto** → corrige P1s no data.json / .md → re-roda.
4. **nota ≥ limiar e P0=0** → APROVADO · mostra a nota na entrega.
5. Máx ~3 rodadas automáticas; se não converge, o problema é de conteúdo (pesquisa/curadoria), não de formato — leva pro Tobia.
