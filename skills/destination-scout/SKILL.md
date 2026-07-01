---
name: destination-scout
description: Levantamento macro inicial de um destino turístico — o passo ANTES do roteiro detalhado. Entrega DOIS blocos nesta ordem fixa (1) MAPEAMENTO curado de atrações + restaurantes com veredito crítico 🟢🟡🔴, logística (distância da base, ingresso R$, reserva, horário) e clusterização geográfica; (2) HISTÓRIA & CURIOSIDADES em prosa corrida com gancho narrativo nas atrações. Use quando (1) usuário pede pesquisa/levantamento/panorama sobre um destino sem querer o roteiro dia-a-dia ainda - "pesquisa o que fazer em X", "traz recomendações de atrações e restaurantes em Y", "me dá um panorama de Z", "história e curiosidades de W"; (2) início do pipeline de viagem nova, como degrau 0 antes do esqueleto. SEMPRE começa fixando o BRIEFING INICIAL antes de pesquisar — dois inputs: (1) PERFIL DO VIAJANTE (família com criança · grupo de amigas · casal · sêniores · mochileiro) — o mesmo destino rende mapeamento diferente por perfil; (2) BASE/hospedagem — toda distância sai dali. Se algum não foi informado, pergunta antes de qualquer web_search. Entrega SEMPRE no chat primeiro; só DEPOIS pergunta se quer exportar Word/PDF (dá espaço a ajustes antes de converter). SEMPRE web_search antes de afirmar preço/distância/fato — NUNCA inventar · preços datados ("~R$50, jan/2026") · fontes citadas no fim. Honestidade crítica > diplomacia — marca turistada/superestimado/"pula sem culpa". Saída: chat sempre · Word (.docx) e PDF só sob demanda (scripts/md_to_docx.py + scripts/docx_to_pdf.py). NÃO sequencia múltiplos dias nem monta o app HTML (exceção: modo mini-plano opcional — um bloco/meia-diária com horários e âncora fixa, ex: "domingo de manhã + Notre-Dame 14h30") — é inventário curado que ALIMENTA o roteiro depois. Standalone funciona (pesquisa pra terceiros, sem virar app).
---

# Destination Scout

Skill (e standalone) que faz o **levantamento macro inicial** de um destino — inventário curado e crítico, antes de qualquer roteiro dia-a-dia.

## O que esta skill faz

Começa fixando o **briefing inicial** (perfil do viajante · base/hospedagem) e só então pesquisa. Entrega no chat e, só depois, oferece export. Retorna, **nesta ordem fixa**:

1. **MAPEAMENTO** · atrações + restaurantes curados, com veredito crítico, logística e clusters geográficos
2. **HISTÓRIA & CURIOSIDADES** · prosa corrida que dá contexto ao destino e ganchos às atrações

Saída: **chat sempre** · **Word (.docx) / PDF só quando pedido**.

## O que esta skill NÃO faz

- NÃO sequencia MÚLTIPLOS dias nem monta o app (isso é o roteiro — `build.py` + pipeline da roteiro-viagem). **Exceção: modo mini-plano** (abaixo) — pode entregar UM bloco/meia-diária com horários
- NÃO monta HTML/app
- NÃO inventa preço, distância, URL ou coordenada (regra herdada do CLAUDE.md)

Ela é o **degrau 0**: levantamento → valida com o Tobia → só então constrói roteiro. Por ser separada do roteiro, é reutilizável pra pesquisas avulsas (ex: pesquisa pra terceiros que nunca vira app).

## Quando triggera

- **Standalone**: "pesquisa o que fazer em X", "traz atrações e restaurantes de Y", "panorama de Z", "história e curiosidades de W"
- **Pipeline**: como Fase 0, antes do esqueleto da viagem nova

---

## PASSO 1 · Briefing inicial (SEMPRE antes de pesquisar)

Dois inputs recalibram TODO o levantamento. Fixe os dois **antes** de qualquer web_search — pesquisar com base/perfil errado obriga a refazer vereditos e distâncias. Se o usuário já informou algum no pedido, não repergunte; pergunte só o que falta. Use `AskUserQuestion` (ou, em chat puro, uma mensagem curta) — **não** um checklist burocrático.

| Input | Por que é crítico | Se não informado |
|---|---|---|
| **1. Perfil do viajante** | O mesmo destino rende mapeamento diferente por perfil (família c/ criança · amigos/amigas · casal · sêniores · mochileiro). Recalibra vereditos, tom, logística (carrinho? fôlego? balada?), orçamento e gastronomia. | "Pra quem é? família c/ criança pequena · grupo de amigos · casal · sêniores · mochileiro" |
| **2. Base / hospedagem** | TODA distância e logística é medida a partir da base. Sem ela, "15min" não significa nada. Pode ser bairro, hotel ou cidade-base de bate-volta. | "Onde vocês ficam hospedados (bairro/cidade)? distâncias saem dali" |

O **formato de output NÃO se pergunta agora** — entrega-se sempre no chat primeiro, e só depois (PASSO 5) pergunta-se Word/PDF, pra dar espaço a ajustes antes de exportar.

⚠️ Lição real (Chapada, 2026): pesquisa nasceu "família com filha 3a", virou "mãe + amigas". Mudou TODOS os vereditos. **Confirme o briefing antes de pesquisar** pra não refazer.

Detalhes e matriz de calibração por perfil: `references/audience-profiles.md`.

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

### 3.1 · Resumo (3-4 linhas)
Big picture antes do detalhe (princípio #4 do repo). O que o destino É, pra esse perfil, e o nº1 imperdível. Use o título "Resumo" (PT-BR) — NÃO "TL;DR" (gíria, fica esquisito em guia pra família).

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

## PASSO 4b · Portão de qualidade (loop-até-excelente) · `critico-roteiro --scout`

Antes de considerar o levantamento pronto (e SEMPRE antes de exportar PDF), passe pelo **gate de conteúdo**. Salve o rascunho em `entregas/<slug>.md` e rode:

```bash
# macro (levantamento interno · Fontes obrigatória)
python3 skills/critico-roteiro/audit.py entregas/<slug>.md --scout
# pra-terceiros / mini-plano (Fontes opcional)
python3 skills/critico-roteiro/audit.py entregas/<slug>.md --scout --terceiros
```

Retorna nota **/20** + achados P0-P3. **Loop-até-excelente**:
1. **P0** presente → corrige (bloqueio) → re-roda.
2. **nota < 14 ou P1 aberto** → corrige no `.md` → re-roda (máx ~3 rodadas).
3. **nota ≥14 e P0=0** → aprovado · segue pro PASSO 5.

O que o gate pega (sem você caçar): preço sem data, veredito 🟢🟡🔴 ausente, "perto" vago em vez de km, sem armadilha sinalizada, restaurante sem sabor-assinatura, ordem mapeamento→história trocada, e — no macro — **seção Fontes ausente**. Régua completa: `references/content-rubric.md` §modo-scout. É o mesmo padrão de qualidade do roteiro, aplicado ao levantamento.

---

## PASSO 5 · Export Word/PDF (chat primeiro · só sob demanda)

**Entregue SEMPRE no chat primeiro.** Só depois da entrega — e depois de o usuário ter chance de pedir ajustes — pergunte se quer exportar:

> "Quer que eu gere um Word ou PDF disso, ou tá bom no chat?"

Exportar antes de o usuário revisar desperdiça trabalho (ajuste pós-export = reconverter tudo). Se ele já tiver pedido um formato explícito no início ("me manda em PDF"), ainda assim mostre o conteúdo no chat antes de rodar os scripts, pra ele validar.

**Toda entrega vive em `entregas/` (na raiz do repo) e é VERSIONADA** (decisão do Tobia, 2026-06-07). Salve ali a **fonte `.md`** + o **`.pdf` final**, com nome descritivo por destino (ex: `entregas/notre-dame-domingo-jun2026.{md,pdf}`). O `.docx` é só intermediário da conversão — não precisa versionar (o `.gitignore` ignora `.docx` em qualquer lugar; `entregas/**` libera o resto).

Fluxo de conversão: salve o levantamento em `entregas/<slug>.md`, converta pra docx (intermediário) e daí pra PDF:

```bash
python3 skills/destination-scout/scripts/md_to_docx.py entregas/<slug>.md /tmp/<slug>.docx
python3 skills/destination-scout/scripts/docx_to_pdf.py /tmp/<slug>.docx entregas/<slug>.pdf
```

- `md_to_docx.py` converte markdown (headings, tabelas, bullets, prosa, **negrito**/*itálico*) em `.docx`. Instala `python-docx` se faltar.
- `docx_to_pdf.py` renderiza o `.docx` em PDF com fonte DejaVu embarcada (acentos PT-BR), subtítulo cinza, tabelas com cabeçalho colorido. Os semáforos 🟢🟡🔴 viram **bolinhas coloridas** (●) e emojis decorativos que a fonte não cobre são removidos. Instala `reportlab`/`python-docx` se faltarem.
- Entregar o arquivo via SendUserFile. Se possível, **renderize e confira** o PDF antes de entregar (ex: `pip install pymupdf` + `fitz`) — não chute o layout.
- Depois de gerar: `git add entregas/<slug>.md entregas/<slug>.pdf` + commit + push (mesma main de sempre). Manter o `.md` fonte permite re-editar/regerar sem refazer do zero.

---

## Modo mini-plano (opcional · exceção ao "não sequencia dias")

Quando o usuário pede um plano pra **UM período específico** — meia-diária, uma âncora com horário (ex: "domingo de manhã + Notre-Dame 14h30") — a skill pode entregar um **mini-plano sequenciado**: 1 bloco curto (manhã OU tarde), roteiro linear com faixas de horário, terminando numa âncora fixa. NÃO confundir com o roteiro completo (multi-dia + app HTML).

Continua valendo TUDO: briefing (perfil + base) antes de pesquisar · ≥6 web_search · anti-invenção (preços datados, sem URL inventada, distâncias da base) · honestidade · chat-first + export sob demanda.

Estrutura do mini-plano:
1. **Âncora fixa no topo** — o compromisso e o horário (ex: "Notre-Dame 14:30 · estar na porta 14:15")
2. **Como chegar (da base)** — trajeto + aviso de logística real (carrinho/escada/baldeação)
3. **Sequência do bloco** com faixas de horário (ex: "Manhã ≈10h45-12h30")
4. **Almoço/parada** em tabela: opções + "distância até a âncora"

Quando NÃO usar: se é a viagem inteira → é o pipeline de roteiro (`build.py`). Exemplo trabalhado: um mini-plano de meia-diária em Paris (Notre-Dame domingo).

## Tom (herdado do CLAUDE.md)

PT-BR, casual, direto, consultor crítico. Tabelas pra comparação. NUNCA concordar por educação. Se é turistada/pulável, **dizer**. Honestidade > diplomacia.

## Checklist antes de entregar

- [ ] Briefing fixado ANTES de pesquisar: perfil · base/hospedagem
- [ ] Perfil refletido nos vereditos · distâncias medidas a partir da base
- [ ] Entregue no chat ANTES de perguntar sobre export
- [ ] ≥6 web_search feitas
- [ ] Todo preço datado · nenhuma URL inventada
- [ ] Bloco mapeamento ANTES do histórico
- [ ] Veredito 🟢🟡🔴 em cada atração
- [ ] Ao menos 1 armadilha de turista sinalizada (se existir)
- [ ] Resumo no topo (NÃO "TL;DR")
- [ ] Fontes citadas
- [ ] **Passou no gate `critico-roteiro --scout`** (nota ≥14/20 · P0=0) antes de exportar
- [ ] Word/PDF só se pedido (e PDF conferido visualmente antes de entregar)
