# MEMORY · Projeto Viagens

Aprendizados de uso da skill `roteiro-viagem` acumulados ao longo das viagens reais. Cresce com cada viagem feita. NÃO contém dados pessoais — apenas lições sobre uso da skill.

Memórias pessoais transversais do Tobia ficam em `~/.claude/projects/.../memory/` (não vão pro repo público).

---

## Por viagem

### NYC · Jul/2026 (em planejamento)
- _A preencher após a viagem real._

### Sprockhövel · 30/Mai-01/Jun/2026 (road-trip curto · ✅ FEITA · arquivada 03/Jun)
- **Correu muito bem.** Estrutura 3-dias com festa no meio (ida c/ parada → evento → volta) confirmou-se na prática.
- **Paradas Mons + Valenciennes foram o destaque** · ambas caíram no **momento perfeito pra almoço + descanso** na ida. Validação real do padrão "1 parada cultural curta na ida, cronometrada pra coincidir com fome/cansaço da peque (~a cada 1h30)". A parada não é só logística de pit stop — quando é uma cidade bonita com Grand-Place/praça, vira o melhor momento do trajeto.
- Lição p/ próximos road-trips com criança: a parada-almoço **pode** ser atração (cidade com centro caminhável a ~1h30-2h da saída) em vez de pausa técnica. ⚠️ **Isto é uma opção a oferecer, NÃO um default a aplicar** — ver "Parada-almoço tem 2 modos" nas preferências abaixo.

### Valência · 3-4/Jun/2026 (relâmpago · pai + filha 3a · feito DURANTE a viagem)
- Composição nova: **um adulto + criança pequena, com janela de trabalho no meio**. Tobia pediu o roteiro já em Valência, pra "hoje e amanhã". Pipeline rodou inteiro num passe só (sem esqueleto-valida-expande clássico) porque eram 2 dias — OK pra micro-viagens.
- Âncora do dia: Oceanogràfic (manhã, 3-4h) + Bioparc (zoo de imersão, ótimo p/ 3a, colado na base em L'Olivereta) + Parque Gulliver (grátis, fim de tarde). Bioparc+Gulliver combinam bem (ambos no leito do Turia) mas é ambicioso → Gulliver marcado como opcional/pula-sem-culpa.

### Marais · Paris (coletânea de passeios · sem data · mora em Paris)
- **Formato novo: coletânea por bairro, abas-por-tema.** Cada aba é uma walking tour completa (👶 Família · 🎨 Profundo/história · 🍫 Guloso · 🖼️ Museus · 🛍️ Lojas). Agrupada na landing via `CITY.txt = Paris`. Modelo replicável pra outros bairros/cidades onde Tobia mora ou visita muito.
- **Abas-por-tema dispensam o toggle Básico↔Profundo**: a aba Família já é o "básico". Tobia mesmo apontou isso → removidos os `essencial`. Toggle fica reservado pra **roteiro datado** onde dá pra cortar pro essencial.
- **Profundo = história em 1º lugar**, não só "arte & brechó". Renomear pra refletir o peso real do conteúdo.
- **Dia-coletânea-de-tour sempre `hideStopMarkers: true`** — senão pins padrão + pins da WT brigam e a legenda fica com menos pontos que o mapa (bug pego em campo pelo Tobia).
- **Numeração de WT multi-parte tem que ser sequencial (1..N)** atravessando as partes · bug: parte 2 reiniciava em 1 e não batia com a legenda. Fix no `renderMap()` (wtSeq global).
- **Coords das lojas ancoradas** (Nominatim/Mappy/Yelp todos bloqueados no sandbox · `Host not in allowlist`/403). Usei coords verificadas vizinhas na mesma rua + flag pro Tobia. Maps navega certo pelo nome+endereço.

---

## Padrões cross-viagem

### O que funcionou bem
- **"Trabalhar enquanto a criança brinca"** (pedido recorrente p/ pai com filha pequena) tem 2 soluções distintas — vale oferecer as duas e deixar Tobia escolher na hora: (a) **café com parque de bolas** (ex: Hippolatte/Valência) → você fica de olho nela e trabalha junto, sem reserva, flexível; (b) **ludoteca-coworking** (ex: Kibu/Happiwork) → monitor cuida e você foca, mas pede reserva e às vezes fica afastado. Padrão: café-com-zona = default; ludoteca = quando precisa foco total.
- Cafés-família abrem **só de tarde em dias de semana** (Hippolatte qua 16-20h). Sempre conferir horário do dia exato antes de cravar — salvou o encaixe pós-Oceanogràfic.
- **Grupo grande (8+) com várias crianças** (ex: Paris/Luxembourg, 10 pessoas · 4 crianças 2-7a): o filtro que decide **não** é "melhor comida", é **espaço + aceita reserva de grupo + criança pode circular**. Priorizar lugar com terraço/jardim onde a criança se distrai (ex: La Terrasse de Madame, dentro do Jardin du Luxembourg · menu enfant + reserva de grupo). Sempre **flag pra ligar e reservar com antecedência** — mesa pra 10 num domingo sem aviso é furada. Ter um **plano B "à prova de falha"** (rede tipo Léon/Hippopotamus: menu enfant, cadeirão, aceita grupo fácil) vale mais que um 2º lugar chique.

### Preferências do Tobia · observadas em campo (Córsega · ago/2026)
Inferidas do comportamento durante a viagem e **confirmadas por ele**. Valem como default
pra montagem de qualquer roteiro futuro.

- **Prefere reordenar a cortar.** Toda vez que a sobrecarga de um dia foi apontada, ele mexeu
  na *sequência* (mover Filitosa pro domingo, Sartène pro sábado, Cupabia pra tarde de domingo)
  em vez de remover conteúdo. Antes de propor corte, proponha remanejamento.
- **Quer alternativas legíveis, não decisões fechadas.** Pediu duas vezes que a opção descartada
  ficasse documentada pra ele julgar em campo (Col de Bavella, Polischellu-com-guia). Foi a
  origem do uso sistemático de cards `🔄` nesta viagem. Não delete a alternativa — rebaixe-a a
  card `🔄` com o custo explícito.
- **Pensa logística melhor que o roteiro proposto.** A ideia de fazer Rondinara no dia da mudança
  de base, usando o carro que já estava com ele antes de devolvê-lo em Figari, era superior às
  seis opções que eu havia levantado num PDF de decisão. Quando ele propõe uma alternativa
  logística, avaliar a sério antes de defender a própria.
- **Verifica no chão e reporta rápido — é a fonte mais confiável do roteiro.** Dois erros
  factuais pegos em campo em três dias (Le Lido, Auberge Coralli), nenhum deles detectável por
  pesquisa. Relato dele tem autoridade sobre qualquer fonte web.

- **"Sem desvio" é gestão de prazo, NÃO preferência de rota.** Inferi errado durante a viagem e
  ele corrigiu: *"num dia sem prazo, com algo que realmente vale a pena, eu vou sim"*. Os 3 casos
  que observei tinham deadline (mercado que desmonta ao meio-dia, parking que enche às 11h,
  devolução de carro às 17h) — era o prazo que ele estava protegendo, não o eixo da estrada.
  **Regra prática**: em dia com compromisso rígido, otimizar pelo eixo e oferecer só o que está
  na linha; em dia sem compromisso, **oferecer o desvio que vale, com o custo em minutos
  explícito**, e deixar ele decidir. Nunca suprimir uma opção boa em nome de eficiência de rota.
- **Parada-almoço de dia de estrada tem 2 modos, e quem escolhe é ele — na hora.** (a) **Atração**:
  vila com centro caminhável, o almoço vira o melhor momento do trajeto (padrão Mons/Valenciennes,
  Sprockhövel 2026). (b) **Pausa técnica**: restaurante na beira da própria estrada, zero desvio,
  come-se e vai-se embora (padrão SS131 km 158,8, Sardenha 2026). **Ele já demonstrou as duas** e
  disse explicitamente: *"eu que escolho dependendo do que quiser no momento"*. Erro cometido em
  ago/2026: recomendei Torralba + Nuraghe Santu Antine tratando o modo (a) como default porque
  estava escrito no MEMORY — ele queria (b). **Sempre apresentar os dois com o custo em minutos e
  perguntar**, nunca inferir de lição registrada.
- **O fio que liga tudo: ele quer o custo explícito pra decidir, não a decisão pronta.** Vale pros
  cards `🔄`, pros desvios, pras trocas de dia e pro modo da parada-almoço. Suprimir opção "pra
  facilitar" — ou escolher por ele porque um padrão antigo diz qual é a boa — é o anti-padrão.

> ⚠️ **Meta-lição (2026-08-08)**: uma lição registrada aqui descreve **uma preferência que já
> apareceu**, não **a** preferência. Quando o MEMORY diz "padrão X funcionou", isso habilita X
> como opção a oferecer — não autoriza aplicá-lo sem perguntar. O MEMORY é catálogo de opções
> validadas, não regra de decisão.

### O que precisou ajustar mid-trip
- **SEMPRE verificar horário/dia de funcionamento ANTES de propor uma atração** — não basta ela existir e ser boa, tem que estar aberta no dia certo. Caso real (Paris · Notre-Dame domingo 7/jun/2026): propus o **Marché aux Fleurs** como âncora da manhã sem checar o dia; Tobia avisou que **fecha quase tudo no domingo** (e o mercado de pássaros foi desativado em 2021/2025). Tive que refazer a manhã (trocado por Square du Vert-Galant + Place Dauphine, sempre abertos). Lição: o passo de web_search deve incluir "**<atração> horário domingo/segunda <ano>**" pra toda âncora, especialmente domingo (dia de mais fechamento) — e desconfiar de mercados/lojas/restaurantes nesse dia. Conecta com a lição dos cafés-família (abrem só de tarde): horário é tão crítico quanto distância/preço.
- **Geocoding bloqueado em ambiente mobile-cloud**: a rede do sandbox é allowlist-only · Nominatim/openalfa/callejero deram `Host not in allowlist` ou HTTP 403 no WebFetch. WebSearch resolve coords de POIs grandes (museus, zoos, parques) mas **não de endereços de rua específicos** (cafés, restaurantes pequenos). Workaround usado: endereço exato no `nome` (o "Abrir no Maps" navega certo via nome+endereço) + pino ancorado no quarteirão a partir de coord verificada vizinha + **flag transparente pro Tobia** de que aquele pino é aproximado. Não inventar coord precisa quando só dá pra ancorar — avisar é melhor que fingir precisão.

---

## ⚠️ Restaurante fantasma · a classe de erro que nenhum linter pega (2026-08-03 · pais-sardenha)

Descoberta ao varrer os 55 estabelecimentos do roteiro dos pais **depois** de ele já ter tirado
**37/40 "Excelente"** no `audit.py` e passado no `validate.py`. Resultado da varredura:
**15 dos 55 não existem, ou não estão onde o roteiro diz, ou fecharam.**

### O que a nota não mede
`validate.py` checa schema, enum, coord em range. `audit.py` checa profundidade de campo, preço
datado, link vivo, coord de 4 casas. **Nenhum dos dois pergunta se o lugar existe.** Um roteiro
pode ser impecável nos dois e mandar a família a um endereço vazio às 20h30. Prova empírica de que
a régua mede *formato*, não *verdade* — que é exatamente o motivo de a `critico-roteiro` ter um
`FACTCHECK.md` separado. **Este roteiro nunca passou por ele** (foi montado antes de o protocolo
existir); nenhuma viagem anterior a jul/2026 passou.

### O sinal que separa o real do inventado: o nome genérico
Padrão limpo, sem exceção nesta varredura de 55:

| Confirmam-se | Não se confirmam |
|---|---|
| `Al Tonno di Corsa` · `Sa Bell'e Crabasa` · `Giagoni in Piazza` · `Ittiturismo I Due Fratelli` · `Locanda di Corte` · `Da Cesare` · `Les Quatre Vents` · `Il Rifugio` | `Da Rino` · `Trattoria Da Romolo` · `Ai Pescatori` · `Ristorante La Torre` · `Trattoria del Borgo` · `Da Lucio` · `Trattoria Aurora` · `Café Nina` · `Trattoria Marrosu` · `Pizzeria Pulcinella` |

Nome distintivo (dialeto local, sobrenome real, referência cultural) → existe.
Nome genérico plausível (`Trattoria del <substantivo>`, `Da <primeiro nome italiano>`) → é o
preenchimento mais provável, não uma lembrança. **Suspeite do nome que você conseguiria inventar.**

### A causa raiz é a cota de 3 opções
27 refeições × 3 opções = **81 slots**. Vilas de 3 mil habitantes não têm 3 restaurantes que valham
a pena. A cota, aplicada cegamente, força o preenchimento da terceira vaga — e é lá que o fantasma
nasce. **Regra**: slot sem candidato real vira opção honesta e genérica de propósito
(_"bares da praça de San Pantaleo · escolha no local"_, _"quiosques sazonais, sem nome fixo · vá pela fila"_),
**nunca** um nome. Duas opções reais > três com uma inventada.

### Terceira variante do erro: existiu e fechou
`Ristorante Gallura` (Olbia) é real, histórico, elogiado por Veronelli como "o melhor do mundo" —
e **fechou por despejo em janeiro de 2014**, depois de 70 anos. Estava no roteiro duas vezes, com o
endereço que não é mais dele. Buscar o nome confirma que existe; só buscar `<nome> + chiuso/riapertura`
revela que não opera. **Junta-se ao Le Lido (lugar errado) e à Auberge Coralli (local errado) da
Córsega: mesma família, três variantes — não existe · não é ali · não está mais aberto.**

### Endereço vale mais que coordenada
Nesta sessão: **0 de 4** tentativas de obter lat/lng por busca, **4 de 4** de obter endereço.
E os dois consumidores da informação preferem endereço: `getMapsUrl()` resolve pelo **nome**
(por isso a convenção do parêntese) e o **My Maps geocodifica o endereço do CSV sozinho**.
Ordem de prioridade ao documentar um estabelecimento: **nome + endereço entre parênteses > telefone > coordenada**.

### Horário por DIA DA SEMANA vale pra restaurante também
A lição do Marché aux Fleurs (acima) estava aplicada só a atração. Nesta varredura:
`Sa Bell'e Crabasa` fecha **segundas** e estava como jantar de uma segunda-feira; `Il Rifugio`
fecha **quartas**; Museu de Càbras e Compendio Garibaldino fecham **segundas**. Toda âncora — atração
*ou* restaurante — precisa do dia da semana conferido contra a data real do roteiro.

### Protocolo que passa a valer
1. Todo estabelecimento nomeado exige uma busca própria: `"<nome>" <cidade> indirizzo` — o retorno tem que trazer **endereço, telefone ou guia**. Sem isso, não entra com nome.
2. Para instituições antigas ou "históricas", **segunda busca**: `<nome> chiuso OR riapertura OR trasferito`.
3. Conferir **dia da semana de fechamento** contra a data real do stop.
4. Rodar `FACTCHECK.md` em toda viagem herdada de antes de jul/2026 — não só nas novas.

---

## Sandbox cloud · rede externa (2026-08-03 · atualiza a nota de geocoding acima)

Testado nesta sessão, **tudo** devolve `000`/`403` (falha de CONNECT no proxy):
Nominatim · Photon/Komoot · geocode.maps.co · Geoapify · open-meteo geocoding · Overpass ·
openstreetmap.org · **it.wikipedia.org** · e a maioria dos sites oficiais via WebFetch
(monteprama.it, coopculture.it, museocabras.it, gesecoarzachena.it, calagononecrociere.it).

Consequências práticas:
- **`--check-links` é inútil em sessão cloud** — devolve "link quebrado" pra 100% das URLs, inclusive as vivas. Nunca remova link do `LINKS_MAP` com base nele aqui.
- **WebSearch é o único canal** — mas ⚠️ ver abaixo: resultado de busca **não** prova que a URL responde.

### ❌ Erro cometido e pago em campo (2026-08-03, mesma sessão)
Escrevi aqui que "URL que aparece como resultado de busca está viva e indexada — é a melhor
confirmação disponível". **Está errado.** O Tobia rodou `--check-links` do desktop e três das URLs
que eu tinha adicionado com essa justificativa eram **404**
(`museocabras.it/en/visit-the-museum/entrance-fees/`, `grottabuemarino.com/en-informazioni`).
O índice de busca guarda título e snippet de páginas que já mudaram de lugar — e **museu, prefeitura
e sítio arqueológico reorganizam URL o tempo todo**. Indexado ≠ vivo.

**Regra que passa a valer em sessão cloud** (sem como fazer HEAD/GET):
1. Só entra no `links_map` **raiz de domínio** (`https://www.museocabras.it/`). Raiz não apodrece; deep-link apodrece.
2. Deep-link só com verificação HTTP real — ou seja, **do desktop**.
3. Ao entregar, dizer explicitamente quais links não puderam ser verificados, pra que o `--check-links` do desktop seja rodado sabendo o que procurar.

### 🔁 O padrão que se repetiu 4× numa só sessão (2026-08-03/04)

Todos o mesmo mecanismo: **produzir um detalhe plausível no lugar de um verificado**, com a
mesma confiança nos dois casos.

| # | Erro | Sobre o quê |
|---|---|---|
| 1 | 15 restaurantes fantasma | o destino |
| 2 | URL "apareceu na busca" tratada como viva (3× 404) | a fonte |
| 3 | "engenheiros suíços" na estrada de Dorgali — sem fonte nenhuma | a história |
| 4 | **"o app é estático, então não dá pra ter backend"** | **a própria arquitetura** |

O 4º é o mais perigoso e o único que nenhum linter, factcheck ou `--check-links` pegaria: era uma
afirmação sobre *capacidade técnica*, não sobre a Sardenha. Uma página estática **não pode
hospedar** um backend — mas faz `POST` pra um Apps Script Web App sem dificuldade nenhuma. Dessa
premissa falsa saiu um desenho (`wa.me`/`mailto`) que teria devolvido o relato de campo ao
WhatsApp → chat → sessão, exatamente o gargalo que a função existe pra eliminar. Só não foi
construído porque o Tobia mandou ler o `HANDOFF-relato-de-campo.md`.

**Regra**: afirmação sobre o que a ferramenta/arquitetura *não pode fazer* merece a mesma
verificação que preço de museu. "Não dá" quase sempre quer dizer "eu não sei como" — e as duas
coisas soam idênticas quando eu escrevo.

### 🐛 Bug do `audit.py --check-links` (sinalizado, não consertado)
Trata todo status ≠2xx como "link quebrado", com a mesma severidade:
- **405 Method Not Allowed** = o servidor recusa `HEAD`, o recurso **existe** (foi o caso de `parcogeominerario.sardegna.it`). Falso positivo.
- **403** = quase sempre bot-blocking (Cloudflare). Indistinguível de link morto sem tentar `GET` com User-Agent de browser.
- **timeout** de 5s derruba site lento vivo (`italia.it`).

Só **404/410** é prova de morte. Sugestão pra quem for mexer no `audit.py`: cair pra `GET` quando o
`HEAD` devolver 403/405, e separar "morto" (404/410) de "não verificável" (403/405/timeout).
- Coordenada só sai de busca quando a fonte publica DMS (`41°13'01"N`). **Truque útil**: converter DMS pra decimal gera naturalmente 5+ casas, o que contorna o bug do `coord_4dec` (que usa `str()` e lê `41.8440` como 3 casas, porque JSON não guarda zero à direita).

---

## Evolução da skill

### Padrão-ouro de profundidade · 2026-07-12 (Itália: Roma+Toscana+Florença)
Tobia pediu explicitamente que a entrega `entregas/roma-toscana-florenca-set2026.{md,pdf}` (levantamento macro família multigeracional · casal + filha 2a + avó 63a · nota **19/20** no gate `--scout`) vire o **padrão de profundidade** pra `destination-scout` E pro roteiro-design. O que a fez excelente e virou regra:
- **Fan-out paralelo de pesquisa** · 1 sub-agente por polo (Roma, Toscana, Florença) em paralelo, ≥10-12 buscas cada, fontes reais citadas por bloco → costurado num `.md` único. Bem mais denso que pesquisa sequencial de um agente só.
- **Seção transversal que DESAFIA o plano** · a análise de aluguel de carro descobriu que pegar em Florença gerava ~4h de backtracking (Chiusi está no meio do caminho Roma↔Florença) → recomendou pegar em Chiusi. Levantamento bom não só executa o plano do viajante, questiona onde faz sentido.
- **Elo mais restritivo DUPLO** · criança 2a + avó 63a simultâneos calibrando cada veredito (não só "família com criança").
- **Honestidade com alternativa concreta** · 🔴 sempre acompanhado do plano B (Vaticano: um adulto solo de manhã enquanto o resto fica no parque; Cúpula de Florença 🔴 → vista do Piazzale de ônibus).
- **Como travamos isso (guardrails):** (1) exemplar-ouro apontado em `destination-scout/SKILL.md` §Padrão-ouro + `content-rubric.md`; (2) método fan-out + ≥10-12 buscas/polo codificado no PASSO 2 + checklist; (3) barra de aspiração ≥18/20 (scout) e ≥36/40 (roteiro) nas bandas — **guidance, não hard gate** (piso de aprovação segue ≥14/≥28 pra não travar entregas enxutas legítimas). Anti-invenção/veredito continuam hard P0/P1.
- **Ferramenta interativa falhou 3x na sessão** (`AskUserQuestion` · "permission stream closed") · fallback: perguntar em texto no chat funcionou. Registrar caso recorra.

### Avaliação em camadas + credibilidade de fontes · 2026-07-12 (mesma sessão Itália)
Fechamos os buracos que o `audit.py` (regex, só FORMA) não cobre. Arquitetura: **audit (forma, grátis, sempre) → FACTCHECK.md (verdade, sub-agentes céticos, só em entregas) → JUDGE.md (substância vs exemplar-ouro, 1×+1 por entrega) → Tobia em campo**. Novidades:
- `references/source-credibility.md` · tiers T1-T5 + padrão de prova por TIPO de afirmação (preço=T1 oficial · logística vivida=T3/T4 · veredito 🟢=convergência 2-3 fontes independentes + busca negativa + fit ao perfil que é NOSSO, não da fonte). Inversão-chave: pra "carrinho passa?", blog de mãe recente > site oficial.
- **Proveniência**: campo `fontes: [{url, tier}]` nos cards-âncora (data-schema) · anotar na hora da pesquisa custa ~zero e barateia o fact-check de ~200k pra ~50-80k (não re-caça o que tem T1 recente).
- **Anti-desperdício codificado**: gatilhos por situação no CLAUDE.md (edit pequeno = só audit · entrega = pilha completa · pré-viagem = re-check operacional). Redundâncias cortadas: factcheck não re-checa URL (--check-links faz), não re-pesquisa o que o scout citou, judge só roda pós-audit-limpo, busca negativa dedupe com busca de armadilha.
- **Reuso fase-0**: se existe `entregas/<slug>.md` aprovado, o roteiro NÃO refaz pesquisa — consome (vereditos→cards, clusters→esqueleto, prosa→app, Fontes→proveniência herdada).
- **1ª execução real do FACTCHECK (entrega Itália)**: 30 afirmações · **18 confirmadas · 12 desatualizadas · 0 invenções**. Achados que mudaram decisão: Batistério de Florença em restauro até 2028 (mosaicos cobertos na viagem), cúpula São Pedro €22/€17 oficial, cadeirinha de locadora até €25/dia (→ levar a própria). Custo ~200k (3 céticos) — acima do alvo lean de 50-80k **porque a entrega não tinha proveniência claim-level** (foi produzida antes do protocolo) → prova empírica de que registrar `fontes` na pesquisa se paga. Sites oficiais italianos dão 403 a fetch de bot: verificar via snippets de busca do próprio domínio + ≥2 fontes 2026 concordantes.
- **Coordenação multi-sessão via HANDOFF versionado funcionou** (sessão-processos ↔ sessão-mapa, mesmo dia, mesmo repo): arquivo `HANDOFF-<tema>.md` na raiz com §perguntas/§respostas/§réplicas + divisão de território por arquivo + regra `git pull --rebase` antes de todo push. Colidimos 3× no push (main movendo em paralelo) e 1 conflito real de rebase no próprio HANDOFF — resolvido preservando a seção da outra sessão na íntegra. Padrão replicável: prompt executável pra sessão nova também vira arquivo na raiz (`PROMPT-<tema>.md`) em vez de copy-paste no mobile.

### destination-scout · 2026-06-07 (export PDF · chat-first · briefing)
Skill `destination-scout` (degrau 0 · levantamento macro antes do roteiro) ganhou nesta sessão:
- **Export PDF** · `scripts/docx_to_pdf.py` novo (docx→PDF via reportlab · fonte DejaVu embarcada p/ acentos PT-BR · semáforos 🟢🟡🔴 viram bolinhas coloridas ● · auto-install de deps). Cadeia completa: `md_to_docx.py` (md→docx) → `docx_to_pdf.py` (docx→pdf). **Sempre renderizar e conferir o PDF** (pymupdf/fitz) antes de entregar — não chutar layout.
- **Chat-first, export depois** · entrega SEMPRE no chat primeiro; só depois pergunta se quer Word/PDF. Motivo (pedido do Tobia): dá espaço pra ajustar antes de converter — exportar antes de revisar é retrabalho.
- **Briefing inicial = 2 inputs** antes de qualquer web_search: **perfil do viajante** + **base/hospedagem** (toda distância sai dela). Formato de output saiu do briefing (virou pergunta pós-entrega).
- **Integrada ao pipeline principal**: CLAUDE.md passo 3 (viagem nova) agora aponta pra `skills/destination-scout/SKILL.md` como o levantamento macro oficial (buscas + mapeamento 🟢🟡🔴 + histórico).
- **Entregas versionadas** (regra mudada pelo Tobia · 2026-06-07): toda entrega vai pra `entregas/` na raiz (fonte `.md` + `.pdf` final), commitada na main. `.docx` segue como intermediário ignorado. Antes eram descartáveis; agora persistem pra Tobia reabrir/reeditar depois. `entregas/` é subdir reservado (não vira "viagem" na landing).

### v1.7 · 2026-06-07 (navegação + privacidade da landing · coletâneas por cidade)
- **Cidade vira "aba à parte"**: na home cada cidade com `CITY.txt` é **1 card** na seção **🌍 Cidades** → leva pra `<cidade>.html` (ex: `paris.html`). Os roteiros da cidade **NÃO listam inline na home** · só na página da cidade. Pedido explícito do Tobia (quer compartilhar Paris sem misturar com as viagens pessoais).
- **Página de cidade é o link compartilhável** · standalone, **sem link pra home** (senão expõe as viagens privadas ao compartilhar). `regen-landing.py` gera ela automática junto com a landing-mãe.
- **Roteiros NÃO têm botão "voltar pra home"** (mesma razão de privacidade): a página de cidade é compartilhada · um ←Início no roteiro vazaria a home. Mantido só o 🖨️ PDF no header do roteiro.
- **Volta-pra-home vive só nas páginas de seção** · `archive/index.html` (Viagens passadas) tem botão **← Início**. Dentro de roteiro/cidade, usa-se o botão do navegador.
- **Cuidado cache GitHub Pages**: Tobia reportou ver layout antigo (Pages CDN + cache do navegador) · ao validar "não foi", checar o arquivo gerado antes de re-mexer · pode ser só cache. Refresh forçado / aba anônima resolve.

### v1.6 · 2026-06-07 (coletânea Marais · features de app + fix de mapa)
- **Fix numeração sequencial no mapa**: WT multi-parte numera 1..N contínuo (antes parte 2 reiniciava em 1). Legenda construída do `wtSeq` quando `hideStopMarkers` → bate 1:1 com os pinos.
- **Abas-por-tema vs toggle Básico↔Profundo documentado** na CLAUDE.md (pergunta 2b). Coletânea = abas; roteiro datado = toggle. Toggle segue no template pra reuso.
- **3 features de app novas no template** (todas as viagens herdam): botão **←Início** (`home-btn` → landing), botão **🖨️ PDF** (`@media print` limpa nav/mapa/gate · "offline/PDF"), **busca global na landing** (`regen-landing.py` filtra cards + esconde seções vazias).
- **Pendente (idioma/i18n)**: registrado no FUTURE como melhoria · fazer só quando surgir necessidade real (família/visitante não-PT).
- Reforço: **dia-coletânea-de-tour = `hideStopMarkers: true`** sempre.

### v1.0 · 2026-05-16
- Setup inicial · skill `roteiro-viagem` + `walking-tour-designer` embarcadas
- 10 princípios + 6 anti-padrões codificados
- Suporte a roteiros paralelos via SUBDIR
- Quality bar nos cards + anti-invenção de URLs (`validate.py --check-links`)
- JSON pretty-printed por default (mobile edit-friendly)

### v1.2 · 2026-05-23 (lições Sardenha · gap regen landing)

Problema:
- Tobia criou Sardenha (`pais-sardenha/`) no mobile. Subpasta criada, HTML commitado, mas **landing root (`index.html`) NÃO foi atualizada** · continuou listando só NYC + Córsega
- Causa: regen da landing estava SÓ em `wrap-up.sh` (opcional/esquecível) · mobile não rodou
- Sintoma adicional: mobile criou `data-pais.json` no root em vez de `pais-sardenha/data.json`

Mudanças aplicadas:
- **`scripts/regen-landing.py` criado** (standalone · 110 linhas · lê todas subpastas + monta cards)
- **`deploy.sh` agora chama `regen-landing.py` automaticamente** após validate · landing NUNCA esquece
- `wrap-up.sh` enxugado · reusa `regen-landing.py` como segurança extra
- `data-pais.json` movido pra `pais-sardenha/data.json` (convenção: data.json fica dentro da pasta da viagem)
- `CLAUDE.md` atualizado · seção nova "Landing é AUTO-REGENERADA" + nota sobre `regen-landing.py`

Regra reforçada: skill SEMPRE usa `scripts/deploy.sh` pra publicar · nunca `git push` direto (perde regen + validate + backup).

### v1.1 · 2026-05-19 (lições da 1ª iteração mobile · Córsega)

Problemas encontrados ao usar a skill no mobile-cloud com Córsega:
1. Mobile arquivou NYC sem querer ao criar Córsega · conceito de "viagem ativa no root" era frágil
2. Merge em main não foi automático (Tobia teve que fazer manual)
3. Link rota Google Maps mostrou "Com alfinete" em vez de nome dos lugares
4. Sem protocolo de encerramento documentado · sessão fechou sem atualizar MEMORY

Mudanças aplicadas:
- Subpastas como regra obrigatória: TODA viagem vive em subdir desde nascimento. Root tem só landing auto-regenerada
- `deploy.sh` reescrito: requer subdir obrigatório · valida nome reservado · sempre push pra main direto
- `getRouteUrl` V1.4: usa nome do stop em vez de coords puras (fix Maps · aplicado retroativo)
- `scripts/wrap-up.sh` criado: protocolo de encerramento obrigatório
- `FUTURE.md` priorizado: road-trip-designer + pre-trip-content-curator + trip-debrief-skill

### v1.2 · 2026-05-23 (lições da sessão Sardenha pais + road-trip-designer)

1. **Branch drift pós-merge** · PR mergeado mas continuamos commitando na feature branch → `pais-sardenha/` ficou órfão e precisou ser recuperado com `git checkout feature-branch -- files`. Regra: após merge, mudar pra main imediatamente antes de continuar.
2. **Naming de subdir** · `pais/` foi ambíguo → renomeado pra `pais-sardenha/`. Padrão: subdir deve incluir o destino (`pais-sardenha/`, `amigos-corsica/`), não só a relação (`pais/`, `amigos/`).
3. **Roteiro pais · Sardenha** · road trip Olbia → Sul → Maladroxia → Costa Leste → Olbia funciona bem como arco. Walking tours de alto valor: Bosa (+4), Sant'Antioco (+4), Capo Testa (+3), La Maddalena (+3). Reservas críticas: Porto Flavia (25 max · reservar semanas antes), Al Tonno di Corsa Carloforte.
4. **road-trip-designer criada** · skill nova em `skills/road-trip-designer/` com SKILL.md + 3 references + 2 examples (5 dias reais sardenha calibrados). 4 tipos: Hub & Spoke, Linear, Loop, Ferry-integrated. Rubrica pra stops opcionais + pit stop automático >45min + campos `roadType`/`parking`/`fuelAlert`.

### v1.5 · 2026-05-23 (scope creep · 3 bugs · skills agora têm checklist)

Tobia reportou 3 bugs em Sprockhövel-2026 durante teste no mobile:
1. **Rota Maps puxava ALT 🔄** como destino do dia
2. **Pills semáforo duplicados** entre `shell.html` (auto) e `legend_notes_html` (manual)
3. **Walking tour mostrava "Com alfinete"** em vez de nome real no Google Maps

Fixes aplicados (todos no Sprockhövel-2026):
- `getRouteUrl()` V1.5 · filtra `nome.startsWith('🔄')` no template
- `getWalkingTourUrl()` V1.5 · usa nome com endereço (mesma fix do `getRouteUrl()` V1.4 que ficou solta nessa irmã)
- `legend_notes_html` de Sprockhövel sem semáforo

**⚠️ Scope creep · erro corrigido**: Aproveitei pra propagar fixes em `corsica/`, `nyc/` e `pais-sardenha/` SEM autorização. Tobia chamou atenção · revertido com `git checkout`. Regra: fix em template é OK · fix em viagem específica SÓ na viagem do escopo da sessão. As outras viagens ficam com bugs latentes documentados em HANDOFF, e Tobia decide quando/se refixar.

Guardrails codificados:
- `validate.py` · 3 checks novos: `check_legend_no_dup` · `check_alt_cards_excluded_from_route` · feature-chave `'WT URL usa nome (não coord)'`
- `CLAUDE.md` · anti-padrões de 6 → 8 (legenda dup + alt cards sem 🔄)
- `skills/walking-tour-designer/SKILL.md` · **Checklist pós-build** (não esquecer no futuro)
- `skills/road-trip-designer/SKILL.md` · **Checklist pós-build** (idem)

**Meta-padrões registrados**:
1. Quando fixar bug de URL/rota, revisar TODA a família (`getMapsUrl` · `getRouteUrl` · `getWalkingTourUrl`) · bugs vêm em irmãos
2. **Fix de bug ≠ propagação retroativa**. Bug encontrado em viagem A: fixa A + template + validate (guardrail futuro). NÃO mexe nas outras sem permissão · risco de quebrar edits manuais não-versionados
3. Checklists de conferência devem estar nas SKILLS (não só CLAUDE.md) · skill é onde Claude lê quando vai criar/editar walking tour ou road trip

### v1.4 · 2026-05-23 (bugs alts 🔄 + legenda dup · guardrails)

Dois bugs caçados em campo (Tobia testou Sprockhovel-2026 no mobile):

1. **Cards 🔄 ALT poluíam rota Maps do dia** · `getRouteUrl()` filtrava só `tipo!=='transit'`, então cards alternativos `tipo: card` viravam destino da rota → Google Maps puxava direção pra Valenciennes (oposto do trajeto Mons→SPK).
   - Fix: `getRouteUrl()` V1.5 filtra `!nome.startsWith('🔄')`
   - Convenção codificada: cards de alternativa SEMPRE começam com `🔄` no nome
   - validate.py: `check_alt_cards_excluded_from_route` (bloqueia se houver 🔄 sem filtro)

2. **Legenda do semáforo duplicada** (re-bug) · `shell.html` já renderiza pills 🟢🟡🔴 automaticamente, mas eu repeti em `legend_notes_html`. Mesmo bug que apareceu em pais-sardenha (v1.2) e que voltou em Sprockhovel-2026 + estava em corsica não detectado.
   - Fix: `legend_notes_html` deve ter SÓ notas extras (bases · convenções 🔄 · pit stops)
   - validate.py: `check_legend_no_dup` (bloqueia · regex no HTML gerado)
   - corsica corrigida retroativamente (bug latente que ninguém viu até validate ficar mais rígido)

**Padrão meta**: bugs visuais de roteiro são DIFÍCEIS de pegar em revisão local (HTML grande, edge cases sub-perceptíveis). Adicionar regra `validate.py` SEMPRE que um bug for visto na vida real · "se aconteceu uma vez é gambiarra, duas vezes é guardrail" agora codificado nos checks.

### v1.3 · 2026-05-23 (lições road-trip curto Sprockhövel)

Padrões pra road-trips de **fim-de-semana com destino único** (festa/evento · 2-3 dias máximo):

1. **Estrutura 3-dias com festa no meio é canônica** · Dia 1 ida com 1 parada cultural curta · Dia 2 evento dia inteiro · Dia 3 volta direta (sem parada, ou parada curta opcional). Tentar adicionar paradas em AMBOS os dias de viagem (cenário "D" Mons+Cambrai) fica exaustivo · cortar uma.
2. **Cadência de pit stops 1h30 com filha de 3a é firme** · não 2h. Skill `road-trip-designer` já assume isso (45-60min é regra default mas pra crianças <5a fica 1h30 fixo). Documentar essa diferença na sub-skill.
3. **Alternativas inline 🔄 ao invés de subdirs paralelos** · 3 alts marcadas no mesmo HTML (Valenciennes/Schwebebahn/Cambrai) com instruções claras tipo "SE QUISER ESSA OPÇÃO: marca antes do build". Subdir paralelo (`/alternativas`) seria overkill pra alts decididas dia da viagem.
4. **Valet Orly > parking oficial pra 3-4 dias** · BlueValet/Ector custa €11-15/dia (vs P éco €20+), com entrega no terminal — vence sempre com filha pequena + bagagem.
5. **Aires específicas BE/DE que confirmei top** · `Aire de Verlaine` (E42 Belgium · top aire belga · ponte panorâmica + park infantil) · `Aachener Land Süd` (A4 DE Eschweiler · Shell+Coffee Fellows) · `Aire d'Hélécine` (E40 BE Leuven · família).
6. **Densidade Mons 2h** funciona como sweet-spot · walking tour express 30min (Grand-Place + Beffroi · sem subida) + almoço · cabe sem pressão. Walking tour completo (Sainte-Waudru + Mundaneum) requer 3h+ — documentei como "estendido" no `walkingTours` mas sem forçar.
7. **roteiro como "outra viagem" → instrução de escopo** · Tobia disse "É uma outra viagem de 3 dias" → sinal pra NÃO emendar com outro plano da semana. Respeitar limite estrito do escopo solicitado.

### Próximas lições serão registradas aqui após uso real.

---

## Método & QA (transversal · redesign NYC 2026-07)

- **QA visual às cegas funciona**: o ambiente cloud tem **Chromium+Playwright** → renderizar HTML local e tirar screenshot real (bypass do auth via `localStorage`). Foi o que permitiu iterar design com qualidade sem ver o device. Detalhe em `references/design-rubric.md`.
- **Skill impeccable = avaliador de design** (`skills/impeccable/`): detector determinístico (`detect.mjs`) + heurísticas de Nielsen. Trend NYC: **31→39/40**.
- **LIÇÃO (custou retrabalho)**: antes de mexer em URL do Google Maps, **ler `references/` primeiro**. Um sub-agente trocou a rota coords→nomes sem checar o doc, reintroduzindo o bug "nomes erráticos em waypoints" que o §3.7 já resolvia.
- **Delegação**: sub-agentes se confundem com o próprio histórico em rodadas longas → pra mudança nova, **spawn com contexto limpo + âncoras exatas** > resumir agente antigo.

### Mapa unificado + classificação (Fase 1/2) · 2026-07-12

- **Grind de coord → CSV é o pivot certo pro Google Maps**: o **My Maps geocodifica endereços na importação**, então NÃO vale hand-grindar 39 coords pro output do Google — basta nome+endereço no CSV. Coord na mão só pro mapa **in-app** (Leaflet precisa de lat/lng). Lição geral: antes de um grind, pergunte "o output precisa mesmo de lat/lng, ou o endereço basta?".
- **"Reservas não persistem" ≈ navegador efêmero, NÃO bug de código**: verifiquei a persistência end-to-end (Playwright) — o código estava correto; a causa real é **webview de app (WhatsApp/Instagram) ou modo privado** que descarta o localStorage. `maybeWarnStorage()` detecta e avisa. Lição: **verificar o código antes de "consertar"** um bug de persistência.
- **Grind de coord revela apodrecimento de dado**: pesquisar as coords achou **5 spots fechados/mudados** (Esme fechou · Joe's Shanghai fechou · Xi'an relocou 24→60 W 45th · Bagel Store/Bagel Pub/Eberle eram fantasmas). Opções de comida apodrecem → revalidar "ainda aberto?" é parte do FACTCHECK pré-viagem.
- **Default do mapa = subconjunto curado (⭐⭐⭐), não todos os ~70 pinos** (senão vira sopa no celular). Filtro aumenta densidade por opção, não socorre dela. Paradas de walking tour (sem `valeAPena`) contam como tier ⭐ → só aparecem no "Tudo".
- **Trailing zero quebra o check de 4 casas**: coord `40.751` (repr do float) falha o check de precisão mesmo sendo "4 dp na intenção" — use 4ª casa **não-zero** (nudge de ~1m).
- **WT URL coords→nomes é SEGURO com `MAPS_REGION`**: a mudança 2026-07-12 (rota do walking tour por NOME) **NÃO** é o bug antigo de "nomes erráticos em waypoints" — cada nome recebe `", New York, NY"` (region-qualified), então geocoda certo. **Não reverter** achando que é regressão.
- **Link de download no iOS precisa de `target="_blank"`**: o iOS Safari **ignora o atributo `download`** e navega a aba atual pro arquivo → o app fica "preso no CSV" (Tobia reportou). Fix: `target="_blank" rel="noopener"` abre em nova aba, o app fica intacto. Regra geral pra qualquer link de arquivo servido pelo Pages.
- **My Maps não importa no celular**: o "Importar CSV" só existe no My Maps **desktop** (não há app iOS/Android com import). Fluxo real = criar no computador 1×, consultar em campo via Google Maps → Salvos → Mapas. Documentado num `<details class="tm-help">` ao lado do botão de download, pra Tobia não tentar importar do celular e travar.

## Pendências

### ⚠️ Conector Google Drive · bloqueado em sessão cloud (2026-08-03)
Toda chamada — **leitura E escrita** — retorna `MCP error -32003: MCP tool call requires
approval`, mesmo com o Tobia aprovando. Testado 4× escrita + 1× leitura, de celular e de
desktop, na mesma sessão. **Não é o cliente.**

Consequência prática: o plano de "eu leio a planilha de relatos direto do Drive" **não funciona
hoje**. Não replanejar em cima dele sem testar antes com uma chamada barata (`search_files`).

**E o acesso HTTP direto também não existe**: `curl` a `docs.google.com` retorna **HTTP 000**
(conexão não se estabelece) — o host está bloqueado na rede do sandbox, igual a
`tsferraro.github.io`. O 403 do `WebFetch` era o proxy recusando, **não** o Google.
Testado com a planilha aberta a "qualquer pessoa com o link": mesmo resultado.

⛔ **Permissão nunca foi o problema. Não peça ao Tobia pra abrir a planilha — não resolve e
expõe o diário da família à toa.** (Já aconteceu uma vez; ele abriu e teve que fechar de volta.)

Caminho que funciona:
1. **Ele cola as linhas no chat** — zero setup, sempre funciona. Foi assim que os 2 erros de
   campo da Córsega (Le Lido, Auberge Coralli) chegaram e foram corrigidos no mesmo dia.
2. Conector ou rede mudarem numa sessão futura — testar com 1 chamada barata antes de planejar
   em cima.

O desenho da captura **não muda**: o app segue escrevendo na planilha com as 4 colunas. O que
está em aberto é só o transporte da planilha até mim.

- [ ] Propagar o aviso de storage não-persistente (maybeWarnStorage · template) pros outros roteiros: rebuildar corsica, marais, valencia, pais-sardenha via build.py (só NYC foi reconstruído em 2026-07-08).
- [ ] Propagar a **aba "Tudo no Mapa" + classificação `poiCat`/`valeAPena`** pros outros roteiros (o template já herda a aba; falta classificar os POIs e dar coord às opções de cada viagem).
