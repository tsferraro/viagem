# Credibilidade de fontes · tiers + padrões de prova

Régua pra responder duas perguntas: **(1) essa fonte é boa pra ESTE tipo de afirmação?** e **(2) que evidência sustenta um veredito (🟢 imperdível / 🔴 pula)?**

Princípio central: **credibilidade não é absoluta, é relativa ao tipo de afirmação.** A fonte perfeita pra "quanto custa o ingresso" (site oficial) é péssima pra "vale a pena" (nunca vai dizer "pula"). Fonte boa é fonte **cuja posição lhe dá acesso àquela verdade específica**.

Usada em 3 lugares:
1. **`destination-scout` PASSO 2** — na pesquisa, escolher fonte pelo tier certo e **registrar a proveniência** (url + tier)
2. **`skills/critico-roteiro/FACTCHECK.md`** — o fact-check checa (a) se a fonte confirma a afirmação E (b) se o tier é adequado ao tipo de afirmação
3. **`skills/critico-roteiro/JUDGE.md`** — o juiz avalia se um `imperdivel` está sustentado por convergência ou é eco de listicle

---

## Os 5 tiers

| Tier | Quem é | Autoridade pra quê | Cego/viciado em quê |
|---|---|---|---|
| **T1 · Oficial/primária** (`official`) | site da atração, ticketing oficial (ex: `colosseo.it`, `duomo.firenze.it`), órgão de turismo, operadora de transporte | **Fatos operacionais**: preço, horário, reserva, regras, acessibilidade declarada | **Nunca diz "pula"** — o incentivo é vender. Inútil pra veredito. Acessibilidade declarada ≠ vivida |
| **T2 · Editorial com reputação em jogo** (`editorial`) | Rick Steves, Lonely Planet, Michelin, imprensa de qualidade, The Infatuation | **Vereditos e curadoria** — são pagos pra ter opinião e erram com custo reputacional | Podem estar desatualizados; viés "clássico/canônico" |
| **T3 · Nicho/local com perfil** (`local`) | blogs especializados no lugar ou no perfil (ex: Romewise, MamaLovesItaly, TheTuscanMom) | **Logística vivida**: carrinho passa? fila às 9h? banheiro? sombra? — e vereditos calibrados a um perfil | Amostra de 1; qualidade varia; frequentemente monetizado por afiliado |
| **T4 · Multidão agregada** (`crowd`) | notas Google/TripAdvisor, fóruns de viajantes | **Sinal de consenso e de armadilha** (volume de "lotado", "não vale", menções a "stroller") | Gameável; bolha turística; nota média diz pouco |
| **T5 · SEO-farm / slop** | listicle "25 things to do" sem autor, prosa genérica, afiliado por parágrafo, conteúdo gerado em massa | **Nada** — não citar como fonte | É onde nasce fato inventado que se propaga entre listicles |

**Inversão contraintuitiva (decorar):** pra *preço*, T1 > T3. Pra *"o carrinho passa no Fórum?"*, blog de mãe recente (T3) e reviews mencionando "stroller" (T4) valem **MAIS** que o site oficial, que declara "acessível" por obrigação legal. Pra logística vivida, a multidão vence a autoridade.

## Filtro de incentivo (3 perguntas antes do tier)

1. **A fonte ganha se você for?** (afiliado GetYourGuide/tickets, post patrocinado, é o próprio estabelecimento) → desconta o entusiasmo proporcionalmente.
2. **Tem autor com nome e histórico?** Sem autor identificável = tratar como T5 até prova em contrário.
3. **É independente ou eco?** Listicles se copiam: 5 fontes repetindo o mesmo fato com as mesmas palavras = **1 fonte**. Independência real = detalhes diferentes, autores diferentes, datas diferentes.

## Recência

Regra dos ~18 meses (Lonely Planet, já em `content-rubric.md`): fonte T2 de 2019 **perde** pra T3 de 2026 em qualquer fato operacional. Preço/horário sempre com data de referência "(mês/ano)". Em POI que mudou recentemente (reforma, novo ticketing, restauro), só fonte pós-mudança conta.

## Padrões de prova por tipo de afirmação

| Tipo de afirmação | Prova mínima |
|---|---|
| **Preço / horário / reserva** | 1× **T1** (oficial), datado "(mês/ano)". Sem T1 encontrável → `[a confirmar]` — nunca promover T3/T5 a fonte de preço |
| **Logística vivida** (carrinho, fila real, sombra, banheiro) | 1-2× **T3/T4 recentes** (é onde essa verdade mora) |
| **Fato histórico / lenda** | **T2** ou fonte de referência; lenda sempre apresentada *como* lenda ("dizem que...") |
| **Veredito 🟢 imperdível** | as 3 condições abaixo |
| **Veredito 🔴 pula sem culpa** | crítica recorrente em T2/T3 independentes **OU** incompatibilidade objetiva com o perfil (463 degraus sem elevador não precisa de segunda fonte) |

### As 3 condições do 🟢 imperdível

"Imperdível" **não é fato verificável — é veredito.** Nenhuma fonte conhece a família. O que se verifica é a evidência convergente:

1. **Convergência editorial**: ≥2-3 fontes **T2/T3 independentes** colocando o POI no topo por razões *substantivas* (o que ele tem de único), não "must-see" de manchete.
2. **Busca negativa rodada e sobrevivida**: pesquisar ativamente `<POI> superestimado / overrated / not worth it`. Se crítica credível existe, ela **entra no card** ("lindo porém lotado") mesmo mantendo o 🟢. *Dedupe: se a varredura de armadilhas do PASSO 2 já cobriu o POI, não repetir — obrigatória só pros 🟢-âncora que ela não cobriu (~3-5 por polo).*
3. **Fit ao perfil justificado por NÓS**: a fonte diz que o POI é excepcional; **quem diz que é imperdível *pra esta família* é a rubrica do elo mais restritivo** (`audience-profiles.md` + `mapping-rubric.md`). Coliseu: T2-unânime + 300m da base + elevador → 🟢. Museus Vaticanos: T2-unânimes + incompatíveis com carrinho+avó → 🔴. **Mesma evidência, vereditos opostos — o perfil é a última instância e não se terceiriza.**

Sinais de T4 gameado (detector Rick Steves, já em `content-rubric.md` D8): só turistas/poucos locais, reviews todas na mesma semana ou no mesmo idioma, hype "must-see" sem substância, retail-heavy.

## Registro de proveniência

Na pesquisa (scout ou roteiro), **anotar a fonte na hora** — custa ~zero (a busca já achou a URL) e barateia todo fact-check futuro:

- **No levantamento `.md`**: a seção Fontes agrupa URLs; pra cards-âncora, indicar a fonte junto da afirmação crítica quando não-óbvio.
- **No `data.json`** (cards-âncora): campo opcional `fontes: [{"url": "...", "tier": "official|editorial|local|crowd"}]` — ver `data-schema.md`. Não burocratizar: obrigatório só nos cards-âncora e em afirmações de preço/horário; opções de restaurante e stops menores podem herdar da seção Fontes do scout.

Afirmação **com proveniência T1 recente** registrada = verificada; o fact-check não re-caça (regra R1 do `FACTCHECK.md`).
