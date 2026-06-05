---
name: destination-scout
description: Levantamento macro inicial de um destino turístico — o passo ANTES do roteiro detalhado. Entrega DOIS blocos nesta ordem fixa (1) MAPEAMENTO curado de atrações + restaurantes com veredito crítico 🟢🟡🔴, logística (distância da base, ingresso R$, reserva, horário) e clusterização geográfica; (2) HISTÓRIA & CURIOSIDADES em prosa corrida com gancho narrativo nas atrações. Use quando (1) usuário pede pesquisa/levantamento/panorama sobre um destino sem querer o roteiro dia-a-dia ainda - "pesquisa o que fazer em X", "traz recomendações de atrações e restaurantes em Y", "me dá um panorama de Z", "história e curiosidades de W"; (2) início do pipeline de viagem nova, como degrau 0 antes do esqueleto. SEMPRE calibra TUDO pelo PERFIL DO VIAJANTE (família com criança · grupo de amigas · casal · sêniores · mochileiro) — o mesmo destino rende mapeamento diferente por perfil. SEMPRE web_search antes de afirmar preço/distância/fato — NUNCA inventar · preços datados ("~R$50, jan/2026") · fontes citadas no fim. Honestidade crítica > diplomacia — marca turistada/superestimado/"pula sem culpa". Saída: chat sempre · Word (.docx) só sob demanda via scripts/md_to_docx.py. NÃO sequencia dias nem monta o app HTML — é inventário curado que ALIMENTA o roteiro depois. Standalone funciona (pesquisa pra terceiros, sem virar app).
---

# Destination Scout

Skill (e standalone) que faz o **levantamento macro inicial** de um destino — inventário curado e crítico, antes de qualquer roteiro dia-a-dia.

## O que esta skill faz

Recebe um destino + perfil do viajante e retorna, **nesta ordem fixa**:

1. **MAPEAMENTO** · atrações + restaurantes curados, com veredito crítico, logística e clusters geográficos
2. **HISTÓRIA & CURIOSIDADES** · prosa corrida que dá contexto ao destino e ganchos às atrações

Saída: **chat sempre** · **Word (.docx) só quando pedido**.

## O que esta skill NÃO faz

- NÃO sequencia dias (isso é o roteiro — `build.py` + pipeline da roteiro-viagem)
- NÃO monta HTML/app
- NÃO inventa preço, distância, URL ou coordenada (regra herdada do CLAUDE.md)

Ela é o **degrau 0**: levantamento → valida com o Tobia → só então constrói roteiro. Por ser separada do roteiro, é reutilizável pra pesquisas avulsas (ex: pesquisa pra terceiros que nunca vira app).

## Quando triggera

- **Standalone**: "pesquisa o que fazer em X", "traz atrações e restaurantes de Y", "panorama de Z", "história e curiosidades de W"
- **Pipeline**: como Fase 0, antes do esqueleto da viagem nova

---

## PASSO 1 · Perfil do viajante (SEMPRE primeiro)

O mesmo destino rende mapeamento **diferente** por perfil. Nunca pesquise antes de fixar isto. Se o usuário não informou, **pergunte UMA vez** (não checklist):

> "Pra quem é? (família com criança pequena · grupo de amigos/amigas · casal · sêniores · mochileiro/aventureiro) — isso muda bastante o que recomendo."

O perfil recalibra: **vereditos** (esforço aceitável), **tom**, **logística destacada** (carrinho? fôlego? balada? acessibilidade?), **orçamento**, **gastronomia** (romântico vs. boteco vs. kids-friendly).

Detalhes e matriz de calibração: `references/audience-profiles.md`.

⚠️ Lição real (Chapada, 2026): pesquisa nasceu "família com filha 3a", virou "mãe + amigas". Mudou TODOS os vereditos. **Confirme o perfil antes de pesquisar** pra não refazer.

---

## PASSO 2 · Web research (~6-10 buscas)

Obrigatório antes de escrever qualquer coisa. Buscar:

1. "o que fazer em <destino> atrações imperdíveis"
2. "<destino> melhores restaurantes onde comer <ano>"
3. "<destino> com <perfil>" (ex: "com crianças", "trilha leve sênior")
4. "<atração principal> ingresso valor distância reserva"
5. "<destino> história origem curiosidades"
6. "<destino> geologia/cultura/contexto" (o que for o ângulo único)
7. (cidade) "<destino> bairros onde se hospedar"
8. armadilhas: "<atração> superestimado vale a pena review"

Regras anti-invenção (do CLAUDE.md):
- **Preços datados**: "~R$50 (jan/2026)" — nunca preço sem data
- **Distância sempre da BASE informada**
- **NUNCA inventar URL** — só de web_search confirmado
- Se info não achada: marcar `[a confirmar]` em vez de chutar

---

## PASSO 3 · Bloco MAPEAMENTO

Estrutura de saída (markdown, pronto pra copiar):

### 3.1 · TL;DR (3-4 linhas)
Big picture antes do detalhe (princípio #4 do repo). O que o destino É, pra esse perfil, e o nº1 imperdível.

### 3.2 · Tabela "esforço × recompensa"
| Atração | Base p/ acesso | Esforço | Veredito |

Veredito = 🟢 (faça) · 🟡 (depende/avalie) · 🔴 (pula sem culpa). Calibrado pelo perfil. Rubrica em `references/mapping-rubric.md`.

### 3.3 · Atrações detalhadas
Por atração: o que é · distância da base · esforço/acesso · ingresso datado · reserva? · **veredito honesto** + ⚠️ alertas de segurança quando houver (ex: cabeça d'água).

### 3.4 · Restaurantes
Tabela: Lugar · O que é · Pra quê (calibrado: romântico/boteco/kids/grupo). Incluir **sabores-assinatura locais** (ingredientes endêmicos). Separar por núcleo geográfico (base vs. cidades vizinhas).

### 3.5 · Clusters geográficos
"O que combinar no mesmo dia" — agrupa por proximidade. Ponte natural pro roteiro futuro (NÃO é o roteiro, só o agrupamento).

### 3.6 · Dicas práticas + orçamento
Melhor época/clima · calçado/preparo · transporte · reservas antecipadas · **estimativa de custo/pessoa** (ingressos+guia+comida) · turismo de base comunitária quando aplicável.

### 3.7 · Armadilhas de turista (callout)
Honestidade > diplomacia. Cilada, fila inútil, "instagram vs. realidade", superestimado.

### 3.8 · Fontes
Lista de URLs usados (markdown links). Anti-invenção: só fontes reais consultadas.

---

## PASSO 4 · Bloco HISTÓRIA & CURIOSIDADES

Prosa corrida (NÃO bullets), 5-7 parágrafos. Estrutura narrativa em `references/prose-guide.md`. Resumo:

1. **Gancho** — o que torna o destino único (o "ângulo" — geologia, história, cultura)
2. **Origem do nome + história** — como o lugar surgiu
3. **Curiosidade/lenda** — o que rende boa história de mesa
4. **Atrações com suas micro-histórias** — tecer contexto em cada uma
5. **Gastronomia como identidade** — comida que conta a história do lugar
6. **Fecho** — por que a viagem vira "boa história pra contar na volta"

Mesmas regras anti-invenção. Fatos de web_search. Tom: envolvente mas factual, sem floreio vazio.

---

## PASSO 5 · Export Word (só sob demanda)

Quando o usuário pedir Word/.docx:

```bash
python3 skills/destination-scout/scripts/md_to_docx.py entrada.md "Saída.docx"
```

O script (`scripts/md_to_docx.py`) converte markdown (headings, tabelas, bullets, prosa) em `.docx` formatado. Instala `python-docx` se faltar. Entregar o arquivo via SendUserFile.

`.docx` é **descartável** (está no .gitignore) — é entregável regenerável, não versionado.

---

## Tom (herdado do CLAUDE.md)

PT-BR, casual, direto, consultor crítico. Tabelas pra comparação. NUNCA concordar por educação. Se é turistada/pulável, **dizer**. Honestidade > diplomacia.

## Checklist antes de entregar

- [ ] Perfil do viajante fixado e refletido nos vereditos
- [ ] ≥6 web_search feitas
- [ ] Todo preço datado · nenhuma URL inventada
- [ ] Bloco mapeamento ANTES do histórico
- [ ] Veredito 🟢🟡🔴 em cada atração
- [ ] Ao menos 1 armadilha de turista sinalizada (se existir)
- [ ] Fontes citadas
- [ ] Word só se pedido
