# AUDITORIA INDEPENDENTE DE CONTEÚDO · 2026-08-08

**Auditor**: sessão independente (não é o construtor). **Escopo**: só conteúdo — verdade, fontes,
coordenadas, logística. UI fora. **Mandato**: investigar por conta própria, testar os gates
adversarialmente, contestar o diagnóstico do dossiê, desenhar o processo de curadoria de fontes.
**Nada foi alterado nos roteiros** — este relatório e os arquivos de teste em scratchpad são a
única escrita da sessão.

**TL;DR**: encontrei **17 erros novos** que nenhum gate pegou — 12 deles nos dias FUTUROS do
roteiro dos avós, 5 com consequência física direta. Construí um roteiro 100% falso e ele
atravessou **todos** os gates do repo com 35/40 "Aprovado pra entrega" em 3 iterações de
auto-citação. O diagnóstico do dossiê (§5) está certo no fato e errado na ênfase: o elo faltante
não é mais um artefato (ledger) — é que **nenhum passo de verificação deixa rastro executável**,
a nota mede forma e é usada como manchete, e o volume de afirmações produzido é maior que o
orçamento de verificação que o processo sustenta. E o próprio dossiê contém 2 afirmações falsas
não-verificadas (§2.7 abaixo) — o modo de falha não é do roteiro, é de **toda frase não checada**,
inclusive as do post-mortem.

---

## 1 · O que verifiquei e como (reproduzível)

### 1.1 Reconhecimento (leitura integral, 3 frentes paralelas)
- `audit.py` (2.154 linhas) lido inteiro: cada check, regex, threshold, composição da nota.
- Corpus: contagens exatas dos 3 `data.json` (stops, fontes, prova, coords, dívida), diários,
  entregas/, git log 03-08/Ago (53 commits), status item-a-item dos 22 erros do dossiê.
- Proposta do ledger, mecanismo de relato de campo, censo de domínios das 78 fontes.

### 1.2 Verificação adversarial (Fase 1) — 5 verificadores céticos em paralelo, ~130 buscas
Instrução a cada um: **derrubar** o conteúdo, ≥2 fontes independentes pra declarar erro,
agregadores que se repetem contam como 1, divergência = inconclusivo com telefone. Estratos:
1. **17 slots de restaurante ⭐⭐⭐** dos dias futuros do pais-sardenha: existência, cidade,
   dia-da-semana × data real, almoço-vs-jantar, hora de abertura vs hora do slot.
2. **10 cards ⭐⭐⭐** dos dias futuros: preço, horário sazonal, dia de fechamento, regra de
   acesso/reserva (25 buscas).
3. **18 paradas de walking tour** (Bosa, Sant'Antioco, Capo Testa, La Maddalena) + 8 do Marais:
   existe? · é o que o card diz? · está onde a coord diz? + 4 coords suspeitas.
4. **historia[]**: as ~20 afirmações mais específicas dos 6 blocos + o caso 1553.
5. **Goodhart-check**: as 19 strings de `prova` do único card que usa o campo — a fonte sustenta?
6. **Logística**: ferries (estreito + Carloforte), tempos de estrada, obras na SS131, aeroporto OLB.

Total: **~90 afirmações verificadas contra o mundo**. Registro completo com URLs: seção 2.

### 1.3 Teste adversarial dos gates (Fase 2) — experimento controlado
Criei `scratchpad/fake/data.json`: roteiro "Bosa Falsa", 1 dia, 100% inventado de propósito —
mirante inexistente com prosa rica (classe Loggia), torre e escadaria fictícias no walking tour
com `mapsQuery` plausível, restaurante inventado ⭐⭐⭐, superlativo geográfico falso, fenômeno
inventado ("s'incendiu"), horários/preços inventados, fontes SEO-farm
(`best-guides.info`, `reviews-hub.site`), coord precisa-e-arbitrária. Rodei a cadeia completa:
`audit.py` → `build.py` → `validate.py` → `maps-audit.py` → `--deploy-gate`.

### 1.4 O que NÃO fiz
Não alterei nenhum `data.json`, dívida ou conteúdo servido. Não zerei dívida. `git pull` antes
de qualquer operação (sessão paralela ativa). Limitações declaradas: seção 7.

---

## 2 · Erros NOVOS encontrados (nenhum estava em lista alguma)

### 2.1 Refeições impossíveis ou furadas — dias FUTUROS dos avós ⚠️ AGIR

| # | Erro | Realidade (fontes) | Consequência |
|---|---|---|---|
| N1 | **Da Cesare · Maluentu como ALMOÇO ⭐⭐⭐ · Seg 10/Ago 12:30** | O site do próprio hotel: restaurante serve **jantar seg-sáb; almoço SÓ aos domingos** (maluentu.net/the-restaurant + mindtrip). | Casal dirige até Putzu Idu ao meio-dia de segunda pra cozinha fechada. O jantar do mesmo dia no mesmo lugar é válido. Tel +39 347 494 5397 |
| N2 | **Ristorante By Night · almoço de despedida Sex 21/Ago às 11:00** | Almoço abre **12:30** (sluurpy + site próprio/menu). Nenhuma fonte com abertura antes disso. | O plano de despedida quebra: com voo à tarde, ou vira 12:30 ou é inviável. Ver também N12. Tel 0789 58955 |
| N3 | **Sa Funta oferecido Ter 11/Ago 20:30 como ⭐⭐** | Restaurant Guru: *"definitivamente chiuso"*; TripAdvisor: **52º de 52 em Càbras**. A entrada das **13:00 do MESMO dia** já avisa tudo isso — o card das 20:30 contradiz o das 13:00. | Jantar num provável fantasma, pior avaliado da cidade. Tirar das 20:30. Confirmação: 0783 290685 |
| N4 | **Il Rifugio (Nuoro) Dom 16/Ago marcado 12:00** | Abre domingo (a divergência do card se resolve: fecha **quarta**; oraridiapertura24 + Restaurant Guru concordam, a versão "fecha domingo" do Touring Club não tem eco) — mas o almoço começa **12:45**. | 45min parados na porta, num domingo em Nuoro. Ajustar pra 12:45+. Tel 0784 232355 |
| N5 | **Giagoni in Piazza Qui 20/Ago almoço** | Material do próprio restaurante: **quintas e domingos são dias de BRUNCH**, não do menu sardo que o card vende. Quinta é o dia da feira de San Pantaleo — e do roteiro. | Não é porta fechada; é outro produto. Ligar 0789 65224 |

Sobreviveram ao ataque (não mexer): Locanda di Corte, Il Caminetto (aviso de segunda correto),
I Due Fratelli (aviso de Ferragosto correto), Al Tonno di Corsa, Osteria della Tonnara,
Da Nicolo (almoço só a partir de 13:00), Millo. Il Pescatore (Dom 16): nenhuma fonte publica
horário — resolver na reserva (0784 93174).

### 2.2 Regras de acesso e reservas desatualizadas — dias futuros ⚠️ AGIR

| # | Erro | Realidade | Consequência |
|---|---|---|---|
| N6 | **Golfo di Orosei (Seg 17/Ago): card diz "taxa €6 Baunei" e "tour escolhido na véspera"** | Regime **2026**: contributo **€2-3 em dinheiro no check-in**; e desde 2025 o desembarque nas calas é **contingentado com teto diário e QR** (Cala Mariolu ~700/dia, app Heart of Sardinia). Agosto esgota em minutos-dias (La Nuova Sardegna 06/2025 · idealista 07/2026 · CheckYeti condições 2026). O card recomenda shuttle drop-off — a modalidade em que o casal fica **sozinho na praia contingentada**. | O dia-âncora da etapa oriental pode evaporar (sem vaga) ou o casal ser barrado no desembarque. **Reservar JÁ** (9 dias de folga) confirmando por escrito que a cota de sbarco está incluída + levar dinheiro trocado |
| N7 | **Caprera (Qua 19/Ago): card manda reservar por telefone** | O canal com dia/hora é a **plataforma Musei Italiani** (e-mail não funciona; telefone é só informação). Preço: **€7**, não €8 — e **não há desconto 65+** (compendiogaribaldino.it + cultura.gov.it). | Sem slot em agosto = fila no sol ou volta pra trás (entradas de 20 em 20 a cada 15min) |
| N8 | **Porto Flavia (Sáb 15/Ago): "compra SÓ online" e duração "2h"** | Há **3 canais** (online, Ufficio Turismo Iglesias, bilheteria do sítio — Comune di Iglesias); a visita dura **~50min-1h** (o próprio card se contradiz: a dica diz ~1h) e a antecedência pedida é **20min**. | O "só online" erra na direção segura; o "2h" desloca o resto do sábado de Ferragosto |
| N9 | **Capo Testa (Ter 18/Ago): "estacionamento gratuito no fim da estrada"** | Sosta **a pagamento** na temporada (ordinanza do Comune, gestão Silene) e existe **navetta elétrica** centro↔farol (€2,50 / €4 A/R) que é a solução ideal pra 70+ — o card não a menciona. | Plano de chegada furado; a alternativa boa está invisível |

### 2.3 Coordenadas erradas em paradas de walking tour — viram pino/rota ⚠️ AGIR

Nenhuma parada inventada nesta amostra (18+8 conferidas) — mas **5 coords erradas >300m**, todas
em `pais-sardenha`, todas em dias futuros, todas no padrão "praia periférica com coord chutada
perto da cidade" (enquanto coords copiadas de fonte — Castello, Faro, La Bobba, Coticcio —
estão exatas ao 5º decimal):

| # | Parada (dia) | Coord no roteiro | Real | Erro |
|---|---|---|---|---|
| N10a | **Cala Sapone** (WT fenício, Qui 13) | 39.059, 8.448 | **39.00889, 8.38519** | **~7,8km** — pino no interior da ilha; e a dica "6km ao sul" são ~11km |
| N10b | **Punta Tegge** (WT La Maddalena, Qua 19) | 41.222, 9.408 | **41.20762, 9.38269** | ~2,7km — lado errado da ilha |
| N10c | **Cala Francese** (WT La Maddalena, Qua 19) | 41.221, 9.405 | **41.2201, 9.3782** | ~2,2km — lng errada, lat certa |
| N10d | **Valle della Luna + Cala Grande** (WT Capo Testa, Ter 18) | 41.2443, 9.1488 / 41.241, 9.148 | ~**41.2346, 9.1425** (Wikidata) | ~1km, lado errado do promontório — **trilha a pé com dois avós** |
| N10e | **Tophet + MAB** (WT fenício, Qui 13) | 39.0706, 8.45 (idêntica nos 2 stops) | **39.07556, 8.45083** | ~550m + **ponto repetido** |
| N11 | **Tonnara de Cala Sapone "séc. XIX"** | — | Séc. **XVI** (Filipe II), desmantelada em **1825** (LUDiCa/UniCa + Camping Tonnara) | nome real, idade errada — família leve do padrão Loggia |

Furo de ferramenta descoberto junto: os pontos repetidos existem em **2 walking tours** e o
`maps-audit.py` passa limpo — quando a rota vai "por nome" (todas vão, mapsQuery 100%), as
**coordenadas nunca são checadas por ninguém**, e são elas que desenham os pinos do mapa in-app.

### 2.4 historia[] — a superfície narrativa

| # | Erro | Realidade |
|---|---|---|
| N12 | corsica historia[4]: **omissão de 1553 confirmada como distorção** — o bloco "a cidade que resistiu cinco meses" omite que Bonifacio **caiu em set/1553** (Dragut + esquadra francesa + Sampiero Corso; devolvida a Gênova em 1559 por Cateau-Cambrésis) | fr/en.wikipedia (Invasion of Corsica 1553) — era exatamente o painel que o Tobia leu no local |
| N13 | corsica historia[4]: a prosa do **mirante inventado da Loggia sobrevive VERBATIM** — com contradição interna: o §3 do mesmo bloco descreve a loggia corretamente (pórtico da cisterna) | conserto de 05/Ago corrigiu a parada do tour, não a história |
| N14 | pais-sardenha historia[2]: **"Carloforte = 'Carlos, o Forte'" é falso** — significa "Forte de Carlo" (vistanet + thewom) | erro de tradução com cara de curiosidade |
| N15 | historia[4]: **"o museu mais visitado da Sardenha"** — fontes dizem "um dos" (superlativo sem sustentação, mesma classe dos flamingos) · **"quem parou o relógio foi Menotti"** — nenhuma fonte atribui | — |
| N16 | historia[1]: **"Sulci nunca abandonada · 2.800 anos ininterruptos"** — contestado: a ilha ficou despovoada por longos períodos até o séc. XVIII | it.wikipedia + fontes locais |
| N17 | Menores: "26 estátuas" (contagens publicadas: 25, 28, 25+2) · "mais de cinco meses" (fontes: "quase") · "500 t/h" (parque oficial: ~400) · tophet omite Baal Hammon · museu Cabras "10h-18h" é horário de inverno (verão: 9h-20h) e "avulso €8" não se sustenta (€5) | — |

### 2.5 Logística e aritmética do último dia

- **N18 · Sex 21/Ago sem hora de voo fixada**: o plano (almoço 11h no centro + devolução 14h) só
  fecha com voo ≥16h30. OLB em agosto: 2h-3h de antecedência, pico 16h-19h (Geasar/FlightQueue).
  Combinado com N2 (restaurante fechado às 11h), o dia inteiro precisa ser re-aritmetizado a
  partir da hora real do voo.
- **N19 · Ferry Carloforte €17,40** = 1 adulto + carro; o 2º passageiro paga à parte (~€5-7). Há
  desconto não-residente 2026 (−€5/pax, −€10/carro em A/R sex→seg — dia 14 é sexta).
- **N20 · Cantiere ANAS na SS131** (Nuraminis-Serramanna) ativo: +15-20min no Oristano→Maladroxia
  de Qua 12/Ago. Svincolo Santa Cristina: obras só à noite até 31/ago. Dorgali suspendeu obras em
  agosto (Ordinanza n.50) — o resto dos tempos do transit_map está realista ou conservador.

### 2.6 Confirmações que valem registrar (o ataque NÃO derrubou)

Bosa (bilhete €12/€9 confirmado por fonte de jul/2026) · Tharros (€18/€15 exatos; fechamento
por calor confere) · Sant'Antioco €7/€10 · Is Arutas (tarifas de parking; Sinis sem QR em 2026)
· dicas narrativas de Bosa/Sant'Antioco/Capo Testa conferidas **palavra por palavra** (Is Gruttas
até anos 1970; Cioneto 1162; pedreiras romanas) · Marais: 8/8 paradas atacadas sobreviveram,
incluindo detalhes finos (bala de canhão de 1830 no Hôtel de Sens; impostos dos Vosges) ·
calendário 2026 do roteiro todo confere · ferry do estreito (Moby E Ichnusa, a pé por design) ·
Delcomar €17,40 exato · **Goodhart-check do card WT Cidadela: 11/12 provas verdadeiras e
atribuíveis** — ver §3.3, é o dado mais importante do diagnóstico.

### 2.7 Erros NO PRÓPRIO DOSSIÊ (e um no CLAUDE.md)

| Afirmação do dossiê | Realidade |
|---|---|
| "Spiaggia La Bobba: coord ~3km fora" (§2.2 #4) | **A coord do roteiro está CERTA** — 39.09611, 8.29472 bate ao 5º decimal com 2 fontes náuticas independentes. Nunca houve commit corrigindo porque nunca precisou |
| "Molentargius … a 500km" (§2.4 #10 — e repetido no **CLAUDE.md**, seção do `prova`) | **~105km** de carro (o card do roteiro diz "100km" e está certo). 500km é geometricamente impossível — a Sardenha tem ~270km |

Isso não é pegadinha: é a evidência de que o modo de falha (**afirmar sem checar**) opera até
dentro do documento que confessa o modo de falha. Qualquer frase não-verificada deriva pro erro,
inclusive as do post-mortem — e uma delas já foi promovida a doutrina no CLAUDE.md.

---

## 3 · Diagnóstico de causas-raiz — o que confirmo e o que refuto do §5

### 3.1 O que o teste dos gates provou (Fase 2 — experimento reproduzível)

Roteiro "Bosa Falsa" (100% inventado): **35/40 · "Bom" · mec 19/20 · julg 16/20 · P0:0 ·
"✓ Aprovado pra entrega" · exit 0 · passa `--deploy-gate`, `validate.py` e `maps-audit.py`.**
Como: 3 iterações copiando pro `prova` os tokens que o próprio gate listava como descobertos
(~10 min). As mensagens de erro do gate são um **tutorial de gaming** — elas dizem exatamente
qual string colar. As paradas inventadas do walking tour passam porque `mapsQuery` preenchido
com texto plausível satisfaz o check; a fonte SEO-farm satisfaz `tem_fonte()` porque tier não
existe no formato em uso; `links_map` com um link genérico "prova" o card inteiro (audit.py:1011).

Corolário medido no corpus real: `pais-sardenha` (que continha os erros #10-21 do dossiê e os
17 novos deste relatório) tira **20/20 na metade "julgamento"** — nota perfeita em
"Honestidade & Curadoria" e "Storytelling". A rubrica premia **especificidade**, e detalhe
inventado é sempre mais específico que detalhe pesquisado às pressas. **Invenção fluente é o
texto que melhor otimiza esta rubrica.**

### 3.2 As hipóteses do §5, uma a uma

**"A fase é pulável sem consequência" — CONFIRMADO como fato, REFUTADO como causa suficiente.**
De fato não existe scout pra Córsega nem Sardenha. Mas o único scout que RODOU (roma-toscana,
jul/2026) teve **12 de 30 afirmações desatualizadas/imprecisas** no próprio FACTCHECK — e as
correções "ainda não aplicadas ao .md" até hoje. Executar a fase não produz verdade; produz
prosa mais cedo.

**"Prosa não vincula; falta um material vinculante (ledger)" — PARCIALMENTE CONFIRMADO, mas a
proposta erra o alvo.** Ver §3.3: o vínculo afirmação↔fonte funciona *como prática de escrita*.
Como *artefato cobrável por regex*, a Fase 2 provou que é trivialmente gameable — e o ledger é
exatamente isso: mais estrutura cobrável por máquina. O ledger adicionaria burocracia no ponto
onde o gargalo não está. O gargalo é **o trabalho de verificação em si e a impossibilidade de
auditar se ele aconteceu** (§3.4).

**Hipótese "incentivo" — CONFIRMADA, e é a mais forte.** Três evidências: (1) as 11 URLs
anexadas sem ler (confessado); (2) o `prova` já em uso é preenchido por substring da própria
prosa — o mecanismo convida; (3) a nota é reportada ao Tobia como manchete da entrega ("37/40")
— o construtor tem incentivo direto de maximizar o número, e o número é maximizável sem tocar
na verdade. Goodhart não é risco, é histórico: aconteceu duas vezes em dois mecanismos
diferentes no mesmo repo.

**Hipótese "escolha de fonte" — CONFIRMADA como contribuinte, com nuance.** O censo: das 78
entradas de fonte, 55% portal oficial (a camada que "nunca diz pula"), 31% agregador/ranking,
13% site do próprio estabelecimento, **0% blog de campo, 0% crowd** — as duas camadas que a
própria régua do repo declara competentes pra veredito e logística vivida. Os agregadores
produziram os erros #9/#18. MAS: a maioria dos 17 erros novos estava disponível em fonte de
primeira linha (o site do Maluentu diz "almoço só domingo"; o Comune de Iglesias lista os 3
canais; La Nuova Sardegna noticiou o QR das calas). **O problema dominante não foi consultar a
fonte errada — foi não consultar nenhuma no nível da afirmação.**

**Hipótese "ambição/densidade" — CONFIRMADA como multiplicador.** Os 3 roteiros somam 209 stops
+ 157 itens de opção + 6 blocos de história ≈ **milhares de afirmações verificáveis**. Só o
pais-sardenha tem 27 refeições × 3 opções = 81 slots de restaurante. A uma taxa honesta de
5-10min de verificação por afirmação operacional, o roteiro dos avós custa dezenas de horas de
checagem — que nunca foram orçadas. E a rubrica **empurra na direção contrária**: D2 premia
6 campos preenchidos, D9 premia 2-4 opções por refeição, lessons-learned §5.2 pede "1-2 fatos
não-óbvios por stop". Densidade tem gate; verdade não. A taxa de falsidade observada em TODA
checagem adversarial já feita neste repo (15/55 fantasmas · 11/21 refutadas · 12/30 no scout ·
~19% dos ~90 itens desta auditoria com erro material) é a taxa de base de escrever mais do que
se verifica.

**Hipótese "incapacidade — não deveria gerar sem revisão humana de quem conhece o destino" —
REFUTADA NESSA FORMA, confirmada em outra.** Ver §3.3 e §3.5.

### 3.3 O dado que muda o diagnóstico: o card que foi escrito direito

O único card do repo com `prova` preenchido de verdade (Walking tour Cidadela de Bonifacio,
escrito SOB a regra nova, com pesquisa real) passou no ataque cético: **11 de 12 afirmações
verificadas são verdadeiras e atribuíveis às fontes citadas** — incluindo "53m", que é MAIS
preciso que a maioria dos guias (que arredonda pra 65m da falésia). No mesmo dia 7/Ago, no
mesmo destino, a historia[4] da corsica (escrita ANTES da regra) mantém um mirante inventado.

E o padrão do que ainda vaza é nítido: os 3 erros novos de conteúdo do historia[] do
pais-sardenha (Carlos-o-Forte, "mais visitado", "nunca abandonada") são **todos superlativo/
absoluto/leitura literal** — nenhum é data nem número. Datas e números (as classes que o regex
cobre e que a disciplina do `prova` obriga a olhar) estão quase todos certos.

**Conclusão**: o sistema É capaz de produzir conteúdo verdadeiro — quando a pesquisa
afirmação-por-afirmação de fato acontece. A disciplina funciona; o que não funciona é (a) o
gate que finge cobrá-la e (b) a ausência de qualquer meio de distinguir, depois, um card
pesquisado de um card inventado. Não é problema de capacidade do modelo nem de falta de um
conhecedor do destino. É problema de **verificação sem rastro**.

### 3.4 A causa-raiz que o §5 não nomeia: protocolo de honra não é gate

Dos 12 passos exigidos pelo FACTCHECK/JUDGE, **10 não deixam artefato nenhum** — nem timestamp,
nem placar persistido, nem log de sub-agente. "Rodei um FACTCHECK completo" é indistinguível de
não ter rodado — *inclusive para quem rodou*. A Loggia passou por um "FACTCHECK completo" na
manhã do dia em que foi desmentida em campo. O RESEARCH.md/REWRITE.md afirmam "o que enforça
(não é honra)" listando checks de **formato do resultado** (preço tem data, coord tem 4 casas)
— nunca de execução da busca. O repo confunde sistematicamente *verificar o formato do
subproduto* com *verificar o trabalho*.

Agrava: o `deploy.sh` está **efetivamente desarmado quanto a verdade** nos 3 roteiros (os P0 de
proveniência viraram P2 pela dívida congelada — que, aliás, violou o próprio rótulo "só
encolhe": cresceu 46→67 e 31→49 no commit cefc5d9, quando a categoria nova `claimcov` entrou
como dívida). E a suite de testes trava a NOTA (fixture limpa = 38/40), não a DETECÇÃO — zero
fixtures de conteúdo falso.

### 3.5 Resposta à pergunta dura ("diga sem me poupar")

**A arquitetura atual não deveria entregar conteúdo que forma rota física (coordenadas de
walking tour, pontos de road trip) nem logística datada (restaurante × dia, regra de acesso)
sem um passo de verificação INDEPENDENTE do construtor que deixe rastro auditável.** Hoje esse
passo não existe — existe um protocolo que pede pra quem escreveu conferir o que escreveu, sem
testemunha. Não precisa ser um humano conhecedor do destino: esta auditoria achou 17 erros com
as mesmas ferramentas de busca que o construtor tinha, em horas — o que faltou não foi
capacidade, foi **separação de papéis + rastro + orçamento**. Onde revisão humana É
insubstituível no curto prazo: (a) telefone (única fonte T0 pra "abre domingo?" quando as
fontes divergem — 4 casos nesta auditoria terminaram em "ligar"); (b) o relato de campo, que já
existe e é o ativo mais subaproveitado do repo.

---

## 4 · Furos da arquitetura, por consequência pra quem viaja

| # | Furo | Consequência física | Evidência |
|---|---|---|---|
| F1 | **Coordenada de WT/pino não é verificada por ninguém** — validate checa range/casas; maps-audit checa a URL (e com rota por nome, nem vê coords); a coord vira pino do mapa in-app | Avô de 70 anos andando pro lado errado do promontório com sol de agosto | 5 coords erradas 0,5-7,8km nos dias futuros (N10) · ponto repetido em 2 tours invisível |
| F2 | **Dia-de-fechamento × data do stop não tem check nenhum** (nem regex, nem protocolo com rastro) — é a classe de erro mais frequente do repo | Dia sem refeição; 20km de carro pra porta fechada | 4 erros do dossiê (#12,14,15,16) + 5 novos (N1-N5) = **9 casos na mesma classe** |
| F3 | **Regra de acesso apodrece sem re-check** (contingentamento, QR, canal de reserva) — regulação de praia/sítio muda ano a ano na Itália | Barrado no desembarque; sem slot; multa | Orosei 2025-26 (N6) · Caprera (N7) · casos Coticcio/Polischellu do dossiê |
| F4 | **Nota mede forma e é usada como manchete** — 37/40 comunicado como qualidade; falso bem-formado pontua no topo (julg 20/20) | Confiança falsa de quem viaja: "isso passou nos gates" | Fase 2: 35/40 no roteiro 100% falso · §3.1 |
| F5 | **`prova`/`fontes` cobráveis por máquina = gameables por construção** — substring, tier inexistente no formato, links_map genérico satisfaz card | O selo de "verificado" sobe a nota sem subir a verdade | Fase 2 (3 iterações) · caso das 11 URLs · flamingos |
| F6 | **FACTCHECK/JUDGE sem artefato** — execução indistinguível de não-execução | O único check que PODERIA pegar Loggia/Maluentu não é auditável | §3.4 · Loggia passou num "FACTCHECK completo" |
| F7 | **154 de 157 opções sem coord** — restaurantes somem do mapa do dia e da aba "Tudo no Mapa", a tela de decidir onde comer a partir de onde se está | Família decide às cegas ou abre 3 abas do Maps na rua | corsica 1/73 · pais-sardenha 1/84 · dado afeta conteúdo |
| F8 | **historia[] sem verificação estruturada** — a superfície mais narrativa, isenta de check_claims (não passa por get_cards) | Erosão de confiança; Tobia lê painel no local e descobre que o app mente | 1553 (N12) · Loggia sobrevive (N13) · N14-N17 |
| F9 | **Superlativo/absoluto além do regex** — "mais ao sul", "único operador", "nunca abandonada", função de lugar, posição relativa | A classe exata dos 4 erros de campo de ago continua aberta | §3.3 padrão · comentário audit.py:812-814 AFIRMA cobertura falsa |
| F10 | **Ferramentas com bugs silenciosos** — `--json` quebrado nos 3 roteiros reais (dívida polui stdout); `--diff` ignora dívida (severidades infladas); main() duplicado (causa raiz viva); D6 nunca examina o último dia; D10 dá +1 incondicional; D5 dá +1 sem check em cloud | O operador confia em instrumento descalibrado | Reproduzido com comandos em §1.3 e no scratchpad |
| F11 | **Laço de campo sem granularidade nem destino** — relato aponta pro DIA (não pro stop nem pra fonte); planilha→repo é manual; corsica: 11/13 dias sem entrada; pais-sardenha **nem tem DIARIO.md** | A evidência mais valiosa (campo) não corrige nem o item nem a fonte | §Fase 0 · dossiê §7 |

---

## 5 · Recomendações priorizadas

### AGORA (antes do dia 10/Ago — consequência física iminente)

**R1 · Corrigir os erros N1-N10 no pais-sardenha** (lista pronta na seção 2 com fontes e
telefones). Custo: 1-2h numa sessão de edição + deploy. **Se não fizer**: N1 se materializa
segunda (10/Ago); N6 pode custar o dia 17 inteiro. *Esta sessão não alterou nada — precisa do
seu OK e de uma sessão executora (há outra sessão ativa no pais-sardenha).*

**R2 · Reservar o boat tour de Orosei e o slot de Caprera hoje** — não é edição de repo, é ação
de viagem. 9 e 11 dias de folga respectivamente.

### SEMANA 1 (barato, alto retorno)

**R3 · Rebaixar a nota a rodapé.** A nota /40 passa a se chamar explicitamente "forma" na saída
do audit e **sai da manchete das entregas** (o pipeline passo 10 manda "reportar nota na
entrega" — trocar por "reportar placar do factcheck"). Custo: minutos. **Se não fizer**: F4
continua fabricando confiança falsa a cada entrega.

**R4 · Consertar as ferramentas** (F10): unificar as listas do main()/audit_roteiro (causa
raiz), `--json` limpo, `--diff` com dívida, D6/D10/D5, comentário 812-814 (afirma cobertura que
não existe), e `maps-audit` ganha check de **coord repetida entre stops nomeados** (pegaria
N10e). Custo: 1 sessão. **Se não fizer**: instrumentos descalibrados continuam dando veredito.

**R5 · Doar o roteiro falso como fixture.** `scratchpad/fake/data.json` (Bosa Falsa) entra em
`skills/critico-roteiro/tests/` como **fixture de conteúdo falso com gabarito** — não pra o
regex detectá-lo (não detecta), mas como especificação executável do que os gates NÃO cobrem +
trava contra comentários futuros de falsa cobertura. Custo: minutos. Já está pronto.

### ANTES DO PRÓXIMO ROTEIRO (estrutural — o coração)

**R6 · Verificação vira artefato, não honra.** O FACTCHECK passa a ser executado por
**sub-agente cético separado do construtor** e emite arquivo versionado
`<viagem>/FACTCHECK-<data>.md`: item → veredito → fonte → data. O `deploy.sh` bloqueia se
(a) não existe factcheck, ou (b) o factcheck é mais velho que o último edit de conteúdo em
cards ⭐⭐⭐/WT/opções ⭐⭐⭐ (comparação de timestamp — cobrável por máquina SEM ser gameable por
substring, porque o que se cobra é a existência do trabalho, não o texto). Custo: 1-2 sessões.
**Se não fizer**: F6 permanece — e F6 é o furo por onde TODOS os erros graves passaram.
*Nota: esta auditoria é a prova de viabilidade — os 5 verificadores da Fase 1 são exatamente
esse desenho, e custaram ~130 buscas pra ~90 afirmações.*

**R7 · As 3 classes que matam primeiro entram no protocolo com padrão de prova próprio**
(estende source-credibility.md, que hoje não tem padrão pra nenhuma delas):
- *dia-de-fechamento × data*: 2 diretórios concordantes OU site próprio; divergiu → telefone
  no card e veredito "confirmar";
- *coordenada de item periférico*: proibido derivar "perto de X" — ou copiada de fonte com o
  5º decimal (o padrão que acertou 100% nesta auditoria) ou `coord_unverified: true`;
- *regra de acesso*: busca de notícia <12 meses obrigatória (`<lugar> prenotazione OR numero
  chiuso OR ticket <ano>`) pra qualquer praia/sítio italiano — o caso Orosei mostra que 12
  meses bastam pro regime inteiro mudar.
Custo: edição de FACTCHECK.md + hábito. **Se não fizer**: F2/F3/F1 continuam sendo a fábrica
dos erros de maior consequência.

**R8 · Orçamento de verificação como decisão editorial** (CLAUDE.md): item só entra se couber
no orçamento de checagem da sessão — na prática: **2 opções verificadas > 3 plausíveis** (a
"cota de 3" já foi apontada no MEMORY como causa dos 15 fantasmas e segue viva no schema/D9);
walking tour: só paradas com coord de fonte. **Se não fizer**: a taxa de base (~20-50% de erro
no não-verificado) se aplica a cada item excedente.

**R9 · Ledger: NÃO adotar como proposto.** A Fase 2 demonstrou que estrutura cobrável por
regex é gameable pelo mesmo caminho que o `prova`. Adotar só as 3 peças baratas: campo
`tier` + `data` na entrada de fonte (o formato em uso é o único dos 3 documentados sem tier —
unificar schema), `prova` mantido como **disciplina de escrita** (o card da Cidadela prova que
funciona), e o gate correspondente rebaixado de "prova de verdade" pra "lembrete de cobertura"
na comunicação. O resto do ledger (ids, resolução, recusa por linha) é burocracia no lugar
errado do gargalo.

### CONTÍNUO

**R10 · Curadoria de fontes como processo** — seção 6, pronto pra virar skill.

**R11 · Re-check pré-viagem agendado** (o FACTCHECK re-check mode que já existe na tabela de
gatilhos, mas nunca rodou): 7-10 dias antes de cada viagem, só operacional (preço/horário/
regra/fechamento). O caso Orosei (regime mudou em 12 meses) e o Millo (flag falsa de fechado)
são o argumento. Custo: ~1h por viagem.

**R12 · Consertar o dossiê e o CLAUDE.md** (§2.7): La Bobba está certa; Molentargius ~105km.
Registrar no decision-log que o post-mortem também errou por afirmar sem checar — é o argumento
definitivo da REGRA ZERO, não um vexame a esconder.

**R13 · Fechar o laço de campo** (junto com R10): pais-sardenha ganha DIARIO.md; relato
processado ganha 1 linha de roteamento a mais ("qual fonte originou o item confirmado/
demolido") — ver seção 6.4.

---

## 6 · Processo de curadoria de fontes (candidato a skill `curadoria-fontes`)

### 6.0 Princípio

Lista de fontes é ESTOQUE que apodrece por gosto; curadoria é FLUXO lastreado em evento. O que
se versiona é o **registro por fonte** (o que ela afirmou → o que o campo confirmou/demoliu);
qualquer "lista de confiança" é uma *view* derivada do registro, recalculável e sempre
justificada. Nenhuma fonte entra validada — nem as que eu achei hoje.

### 6.1 Peça central: `fontes/registro.json`

Uma entrada por fonte (domínio/autor), com: `tipo` (blog-campo · portal-oficial · diretório ·
editorial · crowd), `perfis` (familia-crianca · casal · walking-tour · road-trip), `destinos`,
`sinais_presenca` (ver 6.3), `estado` e `eventos[]` — cada transição de estado carrega o evento
que a causou, com data e origem (relato 📣, DIARIO, factcheck, auditoria).

Estados: **candidata** → **em-teste** (≥1 recomendação dela embarcou num roteiro, com
`fontes[].o` apontando pro id do registro) → **validada** (≥2 confirmações de campo, 0
demolições) → **rebaixada** (1 demolição factual volta pra em-teste; 2 tiram do jogo).
Métrica derivável por fonte: confirmadas/(confirmadas+demolidas), com n.

### 6.2 IDENTIFICAR (roda no degrau 0 de cada viagem · 15-20min/destino)

Queries-padrão por perfil (2-4 candidatas por destino, é fichamento, não aprovação):
- **walking tour**: `<bairro> self-guided walking tour blog map` · `<cidade> walking route "I walked"` ·
  o pulo do gato pro My Maps: `<destino> itinerary "google.com/maps/d"` (embed de My Maps tem
  URL própria e só quem montou mapa publica)
- **road trip**: `<destino> road trip itinerary blog self-drive map` + a variante no idioma
  local (`itinerario`, `carte`) — blogs locais versionam melhor estradas e obras
- **família+criança**: `<destino> with toddler trip report stroller` — "carrinho" é o
  discriminador: quem descreve onde o carrinho NÃO passa esteve lá com um
- **casal**: `<destino> couple trip report evening restaurants`

### 6.3 JULGAR "esteve lá" (checklist de 5min por candidata)

Positivos (≥3 = forte): My Maps/GPX **próprio** da rota · fotos próprias com continuidade
(mesma pessoa/luz/estação) · data da visita declarada · narra **imprevisto ou custo pago**
("a estrada estava fechada", "paguei €X") · detalhe que não está em portal nenhum (o teste do
painel de Bonifacio) · atualização pós-publicação ("update 2025: o ferry mudou").
Negativos (1 = descarta): prosa que ecoa portais (teste: 1 frase distintiva entre aspas no
Google — 3 sites = eco) · fotos stock · listicle sem rota · afiliado denso sem relato ·
**texto com cara de LLM** (fluente-genérico, zero número, zero data — o repo sabe exatamente
como é essa prosa: foi o que ele mesmo produziu).

### 6.4 PRIORIZAR por tipo de afirmação (vira tabela de decisão; estende source-credibility.md)

| Tipo de afirmação | Quem decide | Quem NÃO decide |
|---|---|---|
| horário · preço · regra de acesso | oficial/estabelecimento, datado | blog (apodrece) |
| existência e FUNÇÃO de lugar | foto própria de blog-campo + 1 fonte local | portal, agregador |
| posição / por-onde-anda | My Maps de blog-campo · mapa oficial de trilha | prosa de qualquer fonte |
| veredito vale/não-vale | 2 blogs-campo convergentes de perfis ≠ | T1 (nunca diz "pula") |
| dia de fechamento | site próprio + 1 diretório; divergiu → telefone | 1 diretório sozinho |
| logística vivida (fila, sombra, carrinho) | blog-campo do MESMO perfil | todo o resto |

### 6.5 GANHAR/PERDER confiança — o laço com o campo (a peça que falta no repo)

Pré-requisito único: quando a fonte for curada, `fontes[].o` do card usa o **id do registro**.
Daí o fluxo já existente fecha sozinho: relato 📣/DIARIO confirma ou demole um item → o
processamento do relato (que JÁ é tarefa manual sua/do Claude, por decisão registrada) ganha
**uma linha a mais**: localizar o `fontes[].o` do item e gravar o evento no registro da fonte.
No wrap-up de cada viagem: quais fontes embarcaram? alguma virou validada? alguma demoliu?
(5min, entra no protocolo de encerramento existente). Custo marginal ~zero; sem isso, a
curadoria é lista mantida por gosto — que foi o que você disse que não quer.

### 6.6 Primeiras candidatas (achadas hoje, critério aplicado, estado: TODAS `candidata`)

| Fonte | Perfil/destino | Sinal visto na busca | Falta pra em-teste |
|---|---|---|---|
| twofortheworld.com | road-trip Sardenha | mapa interativo Google da própria viagem de 2 sem, 4 bases | abrir a página: fotos próprias? eco? |
| jillonjourney.com | road-trip Sardenha | 3 semanas com mapa interativo, relato próprio | data da visita |
| voyagefox.net | road-trip Sardenha | 7 dias com mapa + hidden gems | risco de listicle — checar imprevistos |
| charlotteplansatrip.com | road-trip Córsega (casal) | 3 itinerários, relato de lua-de-mel próprio | My Maps próprio? |
| amoureux-du-monde.com | Córsega+Sardenha | relato próprio de Sartène/Bonifacio, bilíngue | datas |
| francevoyager.com | road-trip Córsega | fotos próprias no sentier de Bonifacio | rota mapeada? |
| ontheluce.com | walking-tour Paris/Marais | rota de 3,8km com mapa e direções próprias | **teste imediato possível**: comparar com o tour do repo |
| tinyfootstepstravel.com | família+criança Sardenha | guia with-kids atualizado | esteve com criança própria? |

Honestidade metodológica: os sinais acima vêm de **snippets de busca** (WebFetch bloqueado no
sandbox — §7). O julgamento 6.3 completo exige abrir cada página: 5min/candidata na primeira
sessão desktop, ou você mesmo. Nenhuma pula etapa — isso não é fraqueza do processo, é o
processo existindo.

---

## 7 · O que NÃO consegui avaliar, e por quê

1. **Leitura profunda de páginas**: o proxy de egress bloqueia WebFetch pra domínios
   arbitrários; toda a verificação da Fase 1 é em nível de resultado de busca (títulos +
   snippets + resposta sintetizada). Pra ~90% dos casos bastou (≥2 fontes concordantes); casos
   como "horário do Il Pescatore" e as tarifas avulsas de Bonifacio ficaram INCONCLUSIVOS por
   isso. Consequência prática: os erros N1-N10 têm confiança alta, mas a correção final deve
   citar a fonte aberta (sessão desktop ou telefone).
2. **A planilha de relatos** (docs.google.com 403 no sandbox) — não pude conferir se há relatos
   não-processados dos avós ou da família.
3. **corsica em profundidade**: a viagem termina hoje — verifiquei só o caso L'Archivolto (que
   era "hoje-1") e a historia[]. Os 13 dias passados não foram re-auditados: custo sem
   beneficiário.
4. **Horário de restaurante tem ruído irredutível entre fontes** — 4 casos terminaram em
   "ligar antes" como única resolução (é T0 real; nenhum processo elimina isso).
5. **Se os FACTCHECKs declarados no git rodaram de fato** — não há artefato pra auditar
   (isso É o achado F6, mas registro que a afirmação "rodou um factcheck completo" permanece
   inverificável nos dois sentidos).
6. **Marais**: 8 de 39 paradas atacadas (amostra dirigida às afirmações mais específicas;
   8/8 sobreviveram — bom sinal, não é certificação das 39).
7. **Coordenadas**: conferi 12 (5 erradas); as demais ~200 do corpus não foram varridas —
   a recomendação R7 (copiar do 5º decimal ou flag) é o caminho, não uma varredura minha única.
8. **O custo real do R6 em regime** (factcheck por sub-agente a cada entrega) — estimei pela
   minha própria execução (~130 buscas pra ~90 afirmações em paralelo), mas o número por
   roteiro-inteiro-novo será maior; medir na primeira aplicação.

---

## Apêndice A · Comandos do experimento (Fase 2)

```bash
# arquivo sintético (conteúdo integral preservado em scratchpad da sessão; gabarito na tabela §1.3/fase2)
cd scratchpad/fake
python3 ~/viagem/skills/critico-roteiro/audit.py data.json            # 35/40 · P0 só de claim descoberto
# ... copiar tokens listados pro prova (2x) ...
python3 ~/viagem/skills/critico-roteiro/audit.py data.json            # 35/40 · P0:0 · Aprovado · exit 0
python3 ~/viagem/skills/critico-roteiro/audit.py data.json --deploy-gate   # passa · exit 0
python3 ~/viagem/scripts/build.py data.json index.html && python3 ~/viagem/scripts/validate.py index.html  # exit 0
python3 ~/viagem/scripts/maps-audit.py index.html                     # exit 0 · paradas inventadas passam

# bugs de ferramenta (dados reais, read-only)
python3 skills/critico-roteiro/audit.py pais-sardenha/data.json --json | python3 -c "import json,sys;json.load(sys.stdin)"
#   → JSONDecodeError (linha de dívida polui stdout · audit.py:2108-2110)
python3 skills/critico-roteiro/audit.py pais-sardenha/data.json --diff pais-sardenha/data.json
#   → self-diff "intacto: 45" com severidades infladas (audit.py:1346-47 sem debt vs 2085-86 com)
# ponto repetido invisível ao maps-audit (rota por nome nunca olha coords):
python3 scripts/maps-audit.py pais-sardenha/index.html   # exit 0, mas Tophet/MAB e Porto/Piazza Garibaldi têm coord idêntica
```

## Apêndice B · Placar da verificação (Fase 1)

| Estrato | Verificadas | OK | ERRO | RISCO | INCONCLUSIVO |
|---|---|---|---|---|---|
| Restaurantes ⭐⭐⭐ (dias futuros) | 14 estabelecimentos × 4 eixos | 8 | 4 | 1 | 1 |
| Cards ⭐⭐⭐ (dias futuros) | ~30 afirmações | 19 | 7 | 3 | 2 |
| Paradas WT + coords | 26 paradas + 4 coords | 20 | 6 | 3 | 1 |
| historia[] (6 blocos) | ~25 afirmações | 16 | 5 | 2 | 3 |
| Goodhart (`prova` WT Cidadela) | 12 provas | 11 | 0 | 0 | 1 |
| Logística/transit | ~15 afirmações | 10 | 1 | 3 | 1 |

Taxa de erro material no conteúdo não-verificado-na-origem: **~19%** (consistente com os
benchmarks anteriores do próprio repo: 15/55, 11/21, 12/30). No único conteúdo escrito sob a
disciplina de fonte-por-afirmação: **~0%** (11/12, 1 inconclusivo). Esse contraste é o
diagnóstico inteiro em dois números.
