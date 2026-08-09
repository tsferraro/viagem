# DOSSIÊ PARA AUDITORIA EXTERNA · o que deu errado nos roteiros (2026-08-04)

**Este documento foi escrito pelo agente que cometeu os erros.** Leia-o como depoimento do
auditado, não como diagnóstico neutro. Os **fatos** (§2) são verificáveis no repo e no histórico do
git; o **diagnóstico** (§5) e a **proposta** (§6) são hipóteses minhas e devem ser tratados como
material a contestar, não como conclusão.

O Tobia foi explícito: *"eu não confio"*. A auditoria deve chegar às próprias conclusões.

---

## 1. Contexto

- Repo `tsferraro/viagem` gera roteiros de viagem como app HTML single-file, servido por GitHub Pages.
- Público: Tobia, esposa e filha de 3 anos; e os pais dele (casal de 70+).
- Em uso REAL neste momento: `corsica/` (Tobia, 27/Jul→08/Ago) e `pais-sardenha/` (pais, 06→21/Ago).
- **Todos os erros abaixo foram encontrados EM CAMPO, pelo viajante, com o roteiro na mão.**
  Nenhum foi pego pelos gates automatizados do repo.

---

## 2. Inventário de erros (fatos)

### 2.1 Lugar que não existe — a categoria mais grave

| # | Erro | Realidade | Onde estava |
|---|---|---|---|
| 1 | `"Loggia · mirador sul (falésias)"` com prosa sobre o calcário mudando de branco a rosa por 40min | **O mirante não existe.** "Loggia" é o pórtico da Sainte-Marie-Majeure — parada 3 do mesmo tour. Nome real, função inventada | **Parada de walking tour** · virou rota no Google Maps que dois avós de 70 anos iam seguir no dia 7 |

Passou por `validate.py`, por `audit.py` **e por um FACTCHECK completo rodado na mesma manhã**.

### 2.2 Posição física errada

| # | Erro | Realidade |
|---|---|---|
| 2 | Cala Lazarina "ao norte da ilha, 10min do desembarque" | Fica no **sudoeste**; o desembarque é a leste |
| 3 | Coordenada fornecida como Cala Lazarina | Era da **Cala di Achiarinu** (praia vizinha). Conferida em DUAS fontes náuticas concordantes — que concordavam na posição e erravam no rótulo |
| 4 | Spiaggia La Bobba (Carloforte) | Coord ~**3 km** fora · ⚠️ **REFUTADO pela auditoria independente de 2026-08-08 (§2.7)**: a coord do roteiro (39.09611, 8.29472) bate ao 5º decimal com 2 fontes náuticas — estava CERTA. Este item do dossiê era ele próprio afirmação sem checagem |

### 2.3 Estabelecimento na cidade errada

| # | Erro | Realidade |
|---|---|---|
| 5 | **Le Lido** descrito como casual em Porto Pollo | Fica em **Propriano**, gastronômico desde 1932 · 9 ocorrências |
| 6 | **Auberge Coralli** no belvédère de Roccapina | Fica em outro ponto da N196; não serve café a quem passa |

### 2.4 Superlativo e exclusividade falsos

| # | Erro | Realidade |
|---|---|---|
| 7 | Pertusato "ponto mais ao sul da França metropolitana" | É o **segundo**; o extremo é o Capu Testagro |
| 8 | Pointe Saint-Antoine "ponto mais ao sul da Córsega" | Falso |
| 9 | "A Moby é o operador único" da rota Bonifacio–Santa Teresa | A **Ichnusa Lines** opera — foi por ela que a mãe do Tobia comprou. Eu havia acabado de *"corrigir"* o card removendo a Blu Navy, com base em agregadores |
| 10 | Stagno di Càbras: "maior população europeia de flamingos rosa" | A colônia é **Molentargius, em Cagliari**, a 500 km — e nem ela é a maior da Europa (é uma das três do Mediterrâneo ocidental) · ⚠️ o "**a 500 km**" foi **REFUTADO pela auditoria de 2026-08-08 (§2.7)**: são ~105km de carro (a Sardenha tem ~270km — 500 é geometricamente impossível). O resto do item permanece válido. O erro chegou a ser promovido a doutrina no CLAUDE.md; corrigido em 2026-08-09 |

### 2.5 Sazonalidade vendida errada

| # | Erro | Realidade |
|---|---|---|
| 11 | Flamingos como atração de **agosto**, "permanentes o ano todo" | Concentração é **outono a primavera**. Em agosto há aves esparsas |

### 2.6 Dado operacional que muda o dia

| # | Erro | Impacto |
|---|---|---|
| 12 | **Il Caminetto** ⭐⭐⭐ no jantar de **segunda** 10/Ago | **Fecha às segundas.** O dia ficou sem jantar viável |
| 13 | **Sa Funta** ⭐⭐⭐ em 4 dias | **Pior avaliado de Càbras** (2/5, 52º de 52) + indício de fechamento definitivo |
| 14 | **Il Rifugio** ⭐⭐⭐ no almoço de **domingo** 16/Ago | Fontes divergem sobre domingo |
| 15 | **L'Archivolto** ⭐⭐⭐ como opção da cidadela | **Só serve JANTAR** (19h30-22h) — descoberto pelo Tobia procurando almoço |
| 16 | Mercado de Sartène na **sexta** | É **sábado** (corrigido por acaso, numa troca de dia pedida pelo Tobia) |
| 17 | Museu de Sartène €5 · Cidadela "Escalier €2,50, resto grátis" | €4 · e o Bastion custa €3,50 (existe Pass de €6,50) |
| 18 | "Navette €4 Figari→Bonifacio" | Tirado de agregador; as vans servem Porto-Vecchio |
| 19 | Cala Coticcio como trilha livre de 30-45min | **Contingentada desde 2020**: só com guia autorizado e reserva prévia |
| 20 | Gigantes de Mont'e Prama "~3000 a.C." | **Séc. IX-VIII a.C.** — erro de dois mil anos |
| 21 | Polischellu como banho livre | **Proibido sem guia** (arrêté de Quenza, €135/pessoa, idade mínima 8 anos) |

### 2.7 Narrativa incompleta a ponto de enganar

| # | Problema |
|---|---|
| 22 | O card do cerco de Bonifacio conta 1420 (a cidade resistiu 5 meses) e **omite 1553**, quando a cidade **foi tomada** após bombardeio e capitulou. O Tobia leu um painel no local e achou que o roteiro estava errado — o roteiro estava *incompleto de um jeito que soa épico* |

### 2.8 Bugs de app achados em campo

`"New York, NY"` hardcoded nas URLs do Maps · bairros de NYC hardcoded ignorando `BAIRROS_CONFIG` ·
"Copiar endereço" copiando o **nome** do stop · rótulo "🚕 Uber" em viagem de carro próprio · rota
truncando waypoints em silêncio · ★ do Resumo mostrando `cards[0]` (logística) em vez do de maior
recompensa · **72 de 73 opções na Córsega e 82 de 82 na Sardenha sem `coord`** — por isso restaurantes
não aparecem no mapa do dia nem na aba "Tudo no Mapa", que é justamente a tela para decidir onde
comer a partir de onde se está.

---

## 3. Por que os gates não pegaram (fatos)

- `validate.py` valida **estrutura**: sintaxe, enums, ranges de coordenada. Não sabe se um lugar existe.
- `audit.py` valida **forma**: campo presente, tamanho de texto, distribuição. Nota 37/40 num roteiro
  com lugar inventado dentro.
- `FACTCHECK.md` §4a mandava conferir *"toda `mapsQuery` **nova**"*. **A parada inventada não tinha
  `mapsQuery` nenhuma** — a ausência do campo a tornava invisível ao check.
- O `audit.py` passou a cobrar o campo `fontes`. Eu **anexei URLs a 11 cards sem ler as fontes contra
  a prosa**. A nota subiu; o card dos flamingos continuou falso. **Goodhart explícito.**
- Bugs na própria ferramenta, encontrados hoje: `main()` do `audit.py` duplicava a lista de auditores
  (check novo não rodava pelo CLI) · `--baseline` gravava a união com a dívida antiga (ela nunca
  encolhia) · o regex de superlativo exigia artigo, e "Maior população europeia" abre frase sem artigo
  — era exatamente por ali que o erro dos flamingos passava.

---

## 4. Estado atual (2026-08-04)

| | corsica | pais-sardenha | marais |
|---|---|---|---|
| Dívida de proveniência (itens sem fonte, congelados) | **67** | **49** | **36** |
| Opções sem `coord` | 72/73 | 82/82 | — |
| Nota do audit | 33-37/40 | 37/40 | reprova no validate |

**A dívida está congelada de propósito** (`<viagem>/.proveniencia-debt.json`), para não bloquear o
deploy de correções urgentes vindas do campo. Item novo é P0/P1 cheio; `--baseline` recusa crescer.

**Leitura honesta desses números**: mais de 150 afirmações nos roteiros em uso **nunca foram
verificadas contra fonte**. A nota 37/40 mede forma, não verdade.

---

## 5. Meu diagnóstico — HIPÓTESE, a contestar

Ofereço porque foi pedido, e sinalizo que sou parte interessada:

1. O processo faseado **já existe** no repo (`destination-scout` como degrau 0; pipeline `mode create`
   em 10 passos) e **foi pulado**: não existe `entregas/sardenha*.md`. Os cards nasceram direto no
   `data.json`.
2. Mesmo executada, a fase **não vincula**: o artefato do scout é prosa, e prosa não responde
   *"de onde veio esta frase?"*.
3. O elo faltante seria um **material vinculante** entre pesquisa e escrita, não mais uma fase.

**Onde eu posso estar errado, e a auditoria deve testar**: talvez o problema não seja de artefato mas
de *incentivo* (nunca houve custo em pular); ou de *fonte* (usei portais de turismo genéricos quando
existem fontes de campo melhores); ou de *ambição* (roteiros densos demais para o nível de verificação
sustentável); ou simplesmente de *capacidade* — talvez este tipo de conteúdo não deva ser gerado sem
revisão humana de um conhecedor do destino.

## 6. Minha proposta — HIPÓTESE, a contestar

Ledger de afirmações emitido pelo scout; `prova` no card referenciando o id da linha; `audit.py`
recusando roteiro sem ledger. Detalhes em `HANDOFF-ledger-proveniencia.md`.

**Não adote sem avaliar.** Foi escrita por quem errou, logo depois de errar, e não passou por
contraditório.

---

## 7. Um ângulo que eu NÃO explorei e o Tobia levantou

As fontes que usei foram sobretudo **portais oficiais de turismo** (SardegnaTurismo, Offices de
Tourisme) e **agregadores**. Elas são boas para existência, horário e preço — e foram justamente os
agregadores que produziram os erros #9 (operador único) e #18 (navette).

O Tobia apontou uma classe de fonte que eu ignorei: **blogs de viagem com verificação de campo**, que
publicam **My Maps montados com os pontos e as ruas a percorrer**, testados pelo próprio autor. Para
walking tour e road trip — onde o que importa é *por onde se anda*, não o horário do museu — essa
fonte pode ser superior a qualquer portal oficial.

Nenhuma parte do repo hoje distingue, prioriza ou cataloga esse tipo de fonte.

**Decisão do Tobia (04/Ago)**: ele não tem hoje uma lista de blogs de confiança — tentou lembrar e
nenhum se destacou. Então isto **não deve ser entregue como lista pronta**, e sim como **processo
(ou skill) de curadoria progressiva**, que roda em paralelo à construção dos próximos roteiros e vai
acumulando fontes validadas por perfil de viagem.

Observação para quem desenhar isso: o repo já tem o mecanismo de feedback que fecha o ciclo — a
**caixa 📣 de relato de campo** e os `DIARIO.md`. Quando uma recomendação é confirmada ou demolida em
campo, isso é evidência sobre **a fonte que a originou**, não só sobre o item. Uma curadoria com esse
laço tem lastro; uma lista mantida por gosto, não.

---

## 8. Onde olhar no repo

```
CLAUDE.md                          entry point · REGRA ZERO · quality bar
skills/destination-scout/SKILL.md  degrau 0 · pesquisa
skills/critico-roteiro/            audit.py · FACTCHECK.md · JUDGE.md
references/source-credibility.md   régua de tiers de fonte (curta · candidata a revisão)
scripts/validate.py                gate estrutural
scripts/maps-audit.py              gate de URLs do Maps
corsica/DIARIO.md                  relatos de campo e os erros, com data
decision-log.md                    decisões estruturais, 2026-08-04
HANDOFF-ledger-proveniencia.md     minha proposta (contestável)
<viagem>/.proveniencia-debt.json   dívida congelada
git log --since="2026-08-03"       toda a cronologia dos consertos de hoje
```
