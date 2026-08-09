# Credibilidade de fontes · tiers + padrões de prova

Régua pra responder duas perguntas: **(1) essa fonte é boa pra ESTE tipo de afirmação?** e **(2) que evidência sustenta um veredito (🏆 imperdível / ⏭️ pula)?**

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
| **Veredito 🏆 imperdível** | as 3 condições abaixo |
| **Veredito 🔴 pula sem culpa** | crítica recorrente em T2/T3 independentes **OU** incompatibilidade objetiva com o perfil (463 degraus sem elevador não precisa de segunda fonte) |

### As 5 classes que mataram em campo (ago/2026 · R7 da auditoria) — padrão de prova próprio

Nenhuma delas tinha padrão nesta régua quando os erros aconteceram. Agora têm — e o FACTCHECK
cobra exatamente estes:

| Classe | Prova mínima | Caso que a criou |
|---|---|---|
| **Existência de lugar** | fonte que **NOMEIA** o lugar (tier por tipo) · 100% das paradas de WT e pontos de road trip, **nunca amostrado** (FACTCHECK.md §0) · existir não prova função nem posição — conferem separado | Loggia: "mirador sul" que não existe, em rota de dois avós |
| **Função de lugar** ("mirante", "restaurante", "praia de areia") | foto própria de **blog-campo** OU fonte local que descreva a função · portal/agregador **não decide** — nome real com função inventada é o modo de falha mais perigoso | Loggia (pórtico virou "mirante") · tonnara "séc. XIX" (era XVI) |
| **Posição / por-onde-anda** ("ao norte", "10min do desembarque", "no caminho de X") | **My Maps/GPX de blog-campo** OU mapa oficial de trilha · prosa de QUALQUER fonte não decide posição | Cala Lazarina "ao norte" (fica no sudoeste) |
| **Dia-de-fechamento × data do stop** | **2 diretórios concordantes OU site próprio** · divergiu → **telefone no card** + veredito "confirmar antes" | 9 casos na mesma classe: dossiê #12/14/15/16 + N1-N5 (Da Cesare almoço só domingo, Il Caminetto segunda…) |
| **Regra de acesso** (praia/sítio italiano) | busca de notícia **<12 meses OBRIGATÓRIA**: `<lugar> prenotazione OR numero chiuso OR ticket <ano>` — 12 meses bastam pro regime inteiro mudar | Golfo di Orosei: teto diário + QR desde 2025, card mandava "escolher na véspera" · Cala Coticcio · Caprera |

**Coordenada de item periférico** (praia, mirante, parada fora do centro): ou é **COPIADA de
fonte com o 5º decimal**, ou entra `coord_unverified: true`. **PROIBIDO derivar "perto de X"** —
na amostra da auditoria, as 5 coords derivadas estavam TODAS erradas (0,5-7,8km) e as copiadas
estavam 100% certas ao 5º decimal. Não existe meio-termo.

### As 3 condições do 🏆 imperdível

"Imperdível" **não é fato verificável — é veredito.** Nenhuma fonte conhece a família. O que se verifica é a evidência convergente:

1. **Convergência editorial**: ≥2-3 fontes **T2/T3 independentes** colocando o POI no topo por razões *substantivas* (o que ele tem de único), não "must-see" de manchete.
2. **Busca negativa rodada e sobrevivida**: pesquisar ativamente `<POI> superestimado / overrated / not worth it`. Se crítica credível existe, ela **entra no card** ("lindo porém lotado") mesmo mantendo o 🏆. *Dedupe: se a varredura de armadilhas do PASSO 2 já cobriu o POI, não repetir — obrigatória só pros 🏆-âncora que ela não cobriu (~3-5 por polo).*
3. **Fit ao perfil justificado por NÓS**: a fonte diz que o POI é excepcional; **quem diz que é imperdível *pra esta família* é a rubrica do elo mais restritivo** (`audience-profiles.md` + `mapping-rubric.md`). Coliseu: T2-unânime + 300m da base + elevador → 🏆. Museus Vaticanos: T2-unânimes + incompatíveis com carrinho+avó → ⏭️. **Mesma evidência, vereditos opostos — o perfil é a última instância e não se terceiriza.**

Sinais de T4 gameado (detector Rick Steves, já em `content-rubric.md` D8): só turistas/poucos locais, reviews todas na mesma semana ou no mesmo idioma, hype "must-see" sem substância, retail-heavy.

## Registro de proveniência

Na pesquisa (scout ou roteiro), **anotar a fonte na hora** — custa ~zero (a busca já achou a URL) e barateia todo fact-check futuro:

- **No levantamento `.md`**: a seção Fontes agrupa URLs; pra cards-âncora, indicar a fonte junto da afirmação crítica quando não-óbvio.
- **No `data.json`**: schema ÚNICO (unificado 2026-08-09 — havia 3 formatos divergentes):

```json
"fontes": [{
  "o": "SardegnaTurismo",            // quem é a fonte (órgão/guia/blog)
  "u": "https://...",                // URL
  "tier": "oficial",                 // oficial | editorial | campo | diretorio | crowd
  "data": "2026-08",                 // quando foi consultada (mês/ano ou AAAA-MM-DD)
  "prova": ["22 km²", "outono à primavera"]   // afirmações que ESTA fonte sustenta
}]
```

Mapeamento tier → camada: `oficial`=T1 · `editorial`=T2 · `campo`=T3 (blog com verificação de
campo) · `diretorio`=agregador de horários/diretório (oraridiapertura, sluurpy, Restaurant
Guru — útil pra fechamento×data, cego pro resto) · `crowd`=T4. T5 não tem tier: não entra.
O `audit.py` AVISA (P3) fonte sem `tier`/`data` em item novo — dados antigos seguem válidos.
`prova` é obrigatório onde há afirmação estruturada (superlativo/data/número/época — o
`check_claims_cobertos` cobra em ⭐⭐/⭐⭐⭐). Não burocratizar o resto: opções menores podem
herdar da seção Fontes do scout.

Afirmação **com proveniência T1 recente** registrada = verificada; o fact-check não re-caça (regra R1 do `FACTCHECK.md`).
