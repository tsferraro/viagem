# Data Schema — `roteiro-viagem`

Schema completo dos objetos JS injetados no template `shell.html`.
Toda skill que gera roteiros DEVE respeitar este schema exato.

---

## 1. `DAYS` (array principal)

```javascript
const DAYS = [
  {
    date:        String,    // "Sex 3/Jul" · formato "DiaSem D/MesAbrev"
    tema:        String,    // "Williamsburg · 4th of July" · pode ter "·" como separador
    temaCurto:   String,    // "Williamsburg" · 3-15 chars · usado no day tab
    bairro:      String,    // "Manhattan — Midtown + Greenwich Village" · com emoji opcional
    grupo:       Boolean,   // true se família estendida está junta neste dia
    nota:        String,    // (opcional) descrição longa do dia, mostrada no banner
    cor:         String,    // "#7c3aed" · hex da cor principal do dia
    gradA:       String,    // "#5b21b6" · cor mais escura pro gradient banner
    gradB:       String,    // "#7c3aed" · cor mais clara pro gradient banner
    stops:       Array,     // ver seção 2 abaixo
  },
  // ... 11 dias para NYC, variável conforme destino
]
```

### Regras de cor
- Cada dia tem cor única
- Distribuir cores em HSL espaçadamente: `hue = (i / DAYS.length) * 360`
- Saturação 70%, lightness 50% pra `cor`
- gradA = lightness 30%, gradB = lightness 55%

### Regras de bairro
- Sempre começar com emoji (🌉 🗽 🎨 🏛️ 🏘️ etc.)
- Formato "Cidade — Bairro1 + Bairro2" se múltiplos
- Singular "Cidade — Bairro" se só um

---

## 2. `stops` (array dentro de DAYS)

Cada stop pertence a um de 3 tipos: `card`, `opcoes`, `transit`.

### 2.1 Stop tipo `card` (atração principal)

```javascript
{
  hora:           String,     // "11:00"
  emoji:          String,     // "🌳" · emoji único do stop
  periodo:        String,     // "manha" | "tarde" | "noite"
  tipo:           "card",
  nome:           String,     // "Brooklyn Bridge Park · Pier 1 + Pebble Beach"
  cat:            String,     // "Parque ribeirinho · vista Manhattan" (subtítulo)
  sobre:          String,     // (opcional) parágrafo descritivo · suporta **bold**
  imperdivel:     String,     // (opcional) "Se fizer só uma coisa, faça X"
  dicas:          Array,      // (opcional) array de strings · suporta **bold** + emojis
  duracao:        String,     // (opcional) "45min-1h" · range estimado
  custo:          String,     // (opcional) "Gratuito" | "$20-30" | "$8 família"
  acessibilidade: String,     // (opcional) "100% acessível" | "Escadas no acesso sul"
  risco:          String,     // "green" | "yellow" | "red" · default green
  coord:          Object,     // {lat: Number, lng: Number} · 4 casas decimais
  reserva:        String,     // (opcional) "reservado" | "pendente"
  walkingTours:   Array,      // (opcional) ver seção 4 abaixo
  fontes:         Array,      // (schema unificado 2026-08-09 · Lote 3 da auditoria)
                              // [{o: String,      // quem é a fonte (órgão/guia/blog)
                              //   u: String,      // URL
                              //   tier: String,   // "oficial"|"editorial"|"campo"|"diretorio"|"crowd"
                              //   data: String,   // quando consultada ("2026-08" ou "2026-08-09")
                              //   prova: Array}]  // afirmações que ESTA fonte sustenta (strings)
                              // Obrigatório em cards-ÂNCORA e afirmações de preço/horário;
                              // `prova` cobrado em ⭐⭐/⭐⭐⭐ (check_claims_cobertos).
                              // audit.py AVISA (P3) fonte sem tier/data em item novo.
                              // Régua + mapeamento de tiers: references/source-credibility.md
  poiCat:         String,     // (opcional · 2026-07-12 · mapa unificado) categoria do POI:
                              // "atracao" | "restaurante" | "cafe" | "padaria" | "loja" |
                              // "bar" | "parque" | "mercado" | "food-hall"
  valeAPena:      Number,     // (2026-07-12 · semântica confirmada no HANDOFF §4.1)
                              // RECOMPENSA PURA 0-3 (★) — valor intrínseco pro interesse
                              // agregado da composição da viagem, SEM desconto de esforço
                              // (escada/fila/multidão vivem SÓ em `risco`). 2 eixos
                              // independentes: 3★ pode coexistir com risco=red.
                              // 0 = "⏭️ pula sem culpa" (POI real de valor baixo, marcado
                              // de propósito) ≠ AUSENTE (= não-aplicável).
                              // Aplica a `card` e itens de `opcoes`; transit NUNCA tem.
                              // Render (fase 2): ★=tamanho do pino+selo · risco=anel de cor.
}
```

#### Convenções de conteúdo
- `nome` com paren content: "Caffe Reggio (119 MacDougal)" — endereço entre parens ajuda Google Maps search
- `dicas` pode incluir `1️⃣ 2️⃣ ...` pra numerar walking tour stops dentro do card
- `sobre` suporta **bold** com `**texto**` (renderizado como `<strong>` no HTML final)
- `risco`:
  - `green`: tranquilo (parques, museus pequenos)
  - `yellow`: atenção (multidão moderada, calor, distância)
  - `red`: alta atenção (multidão intensa como Times Square, lugares lotados em pico)

### 2.2 Stop tipo `opcoes` (3 alternativas)

```javascript
{
  hora:    String,
  emoji:   String,            // sempre 🍽️ pra almoço, 🛝 pra playgrounds, etc
  periodo: String,
  tipo:    "opcoes",
  nome:    String,            // "Almoço · Tribeca"
  cat:     String,            // "3 opções a 5-10 min do fim da ponte"
  coord:   Object,            // ponto central das opcoes (usado pro Maps URL via opcoes[0])
  opcoes:  Array,             // 2-4 alternativas:
}
```

Cada item em `opcoes`:
```javascript
{
  nome:  String,  // "Whole Foods Tribeca (270 Greenwich St)"
  desc:  String,  // 1-2 frases descritivas
  preco: String,  // "$" | "$$" | "$$$" | "$$$$"
  dist:  String,  // "10 min do ferry" | "no Chelsea Market"
  poiCat:    String,  // (opcional · 2026-07-12) mesma enum do card
  valeAPena: Number,  // (opcional · 2026-07-12) mesma semântica do card (HANDOFF §4.1)
  coord:     Object,  // (opcional · 2026-07-12 · HANDOFF §4.2) {lat, lng} 4 casas decimais,
                      // mesma semântica do coord de stop. Na fase 2 do mapa unificado,
                      // CADA item de opção vira pino próprio (não 1 pino de grupo).
                      // ⚠️ pinos de opção NÃO entram na rota do dia (getRouteUrl) —
                      // mesma família de bug dos cards 🔄 (anti-padrão #8).
}
```

#### Regras
- 2-4 opções (3 é o ideal)
- Primeira opção é a "recomendada" (vai pro Maps URL)
- Variar preço quando possível (1x $, 1x $$, 1x $$$)
- Sempre incluir distância relativa

### 2.3 Stop tipo `transit` (deslocamento)

```javascript
{
  hora:  String,
  emoji: String,             // 🚕 uber · 🚇 metro · ⛴️ ferry · 🚶 walking · 🚌 bus
  periodo: String,
  tipo:  "transit",
  nome:  String,             // "Uber Greenpoint → Battery Park"
  cat:   String,             // (opcional) "~30 min · entrada Whitehall Terminal"
  coord: Object,             // destino do transit
}
```

#### Regras
- `nome` formato "Modo Origem → Destino"
- Rotas detalhadas vêm de `TRANSIT_MAP[nome]` (ver seção 3)
- Se tem entry em TRANSIT_MAP, o stop vira colapsável automaticamente

---

## 3. `TRANSIT_MAP` (dicionário de rotas detalhadas)

```javascript
const TRANSIT_MAP = {
  "Uber Greenpoint → Battery Park": {
    ferry:  String,   // (opcional) "[ER] India St → Wall St/Pier 11 (~25 min) · $4.50"
    metro:  String,   // (opcional) "[G] Greenpoint Av → ... · ~35min · 1 transferência · $2.90"
    uber:   String,   // (opcional) "~30 min · ~$35"
  },
  // ... uma entry por par origem-destino
}
```

#### Convenções
- Linha de metrô entre `[X]` (ex: `[G]`, `[L]`, `[E]`)
- Tempo de transit, número de transferências, preço
- Tom neutro (não anti-metro, usuário mora em Paris)
- Pelo menos 1 dos 3 modos sempre presente

---

## 4. `walkingTours` (array dentro de card)

```javascript
walkingTours: [
  {
    nome:       String,    // "Parte 1 · 🎶 Bohemian Trail (Folk + Comedy)"
    descricao:  String,    // "Washington Sq → MacDougal → Bleecker · ~40min"
    stops: [
      {
        n:     Number,     // 1, 2, 3... numeração sequencial DENTRO da parte
        nome:  String,     // "Caffe Reggio (119 MacDougal)" · com paren content
        coord: Object,     // {lat, lng}
      },
      // ... 4-8 stops por parte
    ]
  },
  // ... 1 ou 2 partes
]
```

#### Regras estruturais
- 1 parte se ≤ 8 stops
- 2 partes se > 8 stops (split por geografia + tema)
- Cada parte tem 4-8 stops (sweet spot: 6)
- Numeração `n` RESETA em cada parte (1-6 + 1-6)
- Total max 16 stops em 2 partes

#### Regras de nomenclatura
Padrão do nome:
- 1 parte: `"<Bairro> · <Emoji> <Subtítulo Temático>"`
- 2 partes: `"Parte 1 · <Emoji> <Subtítulo>"` + `"Parte 2 · <Emoji> <Subtítulo>"`

Exemplos:
- `"DUMBO · 🏭 Industrial Past"`
- `"Wall Street · 🏛️ História Americana"`
- `"Central Park · 🎨 Coração do Parque"`
- `"Parte 1 · 🎶 Bohemian Trail"`
- `"Parte 2 · 🌈 Stonewall + Hidden Gems"`

---

## 5. `LINKS_MAP` (referências por stop)

```javascript
const LINKS_MAP = {
  "Brooklyn Bridge Park · Pier 1 + Pebble Beach": [
    {type: "official", label: "Brooklyn Bridge Park",       url: "https://..."},
    {type: "review",   label: "Mommy Poppins (playgrounds)", url: "https://..."},
  ],
  // ... uma entry por card relevante
}
```

#### Regras
- Key = `nome` exato do card
- `type`: `"official"` (site da atração) ou `"review"` (terceiro confiável)
- 1 official + 0-2 reviews por entry
- Reviews preferidos: Time Out NY, Mommy Poppins (kid-friendly), Atlas Obscura (history), Eater (food), NY Times
- Nunca inventar URLs — sempre web_search prévio

---

## 5b. `HISTORIA` (opcional · 2026-07-12 · HANDOFF §4.4 · aba História & Curiosidades)

Prosa do bloco "História & Curiosidades" da `destination-scout`, embarcada no app como **aba(s) sem mapa e sem stops** (padrão coletânea Marais). Conteúdo produzido pela fase de scout/roteiro; render implementado pela fase 2.5 do mapa unificado.

```javascript
const HISTORIA = [
  {
    titulo:     String,  // "🏛️ Roma — três mil anos empilhados" · vira o nome da aba/seção
    prosa_html: String,  // parágrafos <p>...</p> com <strong>/<em> — HTML CRU (não markdown)
                         // vem pronto do bloco 2 do .md da destination-scout
  },
  // 1 entrada por polo (Itália = 3) · viagem de 1 cidade = 1 entrada
]
```

Regras:
- **Fonte única**: a prosa vem do `.md` aprovado em `entregas/` (regra de reuso fase-0 · scout SKILL) — não se reescreve no build.
- Prosa é conteúdo de "leitura de véspera/trem", não de campo — a aba NÃO carrega mapa, stops nem walkingTours.
- Deve imprimir bem no 🖨️ PDF (`@media print` trata como conteúdo corrido).
- Ausente/array vazio → aba não renderiza (retrocompatível com todas as viagens atuais).

## 6. Bairros canônicos (para `getBairroForCoord`)

Função em `render-functions.js` que mapeia coord pra bairro:

```javascript
function getBairroForCoord(lat, lng) {
  if(lat>40.715 && lat<40.745 && lng>-73.97 && lng<-73.93) return '🏘️ Greenpoint / Williamsburg';
  if(lat>40.69 && lat<40.715 && lng>-74.00 && lng<-73.985) return '🌉 DUMBO / Brooklyn Bridge Park';
  if(lat>40.70 && lat<40.72 && lng>-74.02 && lng<-74.00) return '🗽 Lower Manhattan / Financial';
  if(lat>40.726 && lat<40.74 && lng>-74.01 && lng<-73.99) return '🎨 Greenwich Village / West Village';
  if(lat>40.74 && lat<40.76 && lng>-74.015 && lng<-73.99) return '🌿 Chelsea / Meatpacking / Hudson Yards';
  if(lat>40.75 && lat<40.77 && lng>-74.00 && lng<-73.97) return '🏢 Midtown';
  if(lat>40.77 && lat<40.81 && lng>-74.00 && lng<-73.94) return '🏛️ Upper West / East Side';
  return '🏙️ Outras áreas';
}
```

#### Pra outros destinos
A skill DEVE gerar uma função análoga com bairros do destino antes do build.
Web search prévio: "main neighborhoods <CIDADE>" + manual curation.

---

## 7. Cores por dia (HSL spread)

Geração de cores:

```javascript
function generateDayColors(n) {
  return Array.from({length: n}, (_, i) => {
    const hue = Math.round((i / n) * 360);
    return {
      cor:   `hsl(${hue}, 70%, 50%)`,
      gradA: `hsl(${hue}, 70%, 30%)`,
      gradB: `hsl(${hue}, 70%, 55%)`,
    };
  });
}
```

Para 11 dias: hues = 0°, 33°, 65°, 98°, 131°, 164°, 196°, 229°, 262°, 295°, 327°
- Vermelho · laranja · amarelo · verde · ciano · azul · índigo · violeta · magenta · rosa · vermelho-escuro

#### Conversão pra HEX (opcional)
Pode usar HSL direto no CSS, mas se quiser HEX:
```javascript
function hslToHex(h, s, l) {
  // ... implementação padrão
}
```

---

## 8. Validações que a skill DEVE rodar antes de commit

Ver `scripts/validate.py`. Resumo:

- ✓ Toda `coord` em range [-90,90] × [-180,180]
- ✓ Todo `stop.tipo` ∈ {card, opcoes, transit}
- ✓ Todo `reserva` ∈ {reservado, pendente} se presente
- ✓ Todo `risco` ∈ {green, yellow, red} se presente
- ✓ Todo `periodo` ∈ {manha, tarde, noite}
- ✓ TRANSIT_MAP keys batem com stops `tipo:'transit'` nomes
- ✓ LINKS_MAP keys batem com algum stop name
- ✓ walkingTours partes têm 4-8 stops cada
- ✓ Numeração `n` em walkingTours stops é sequencial e começa em 1
- ✓ Day cores não duplicadas
- ✓ Datas em sequência (sem gaps)
- ✓ `temaCurto` ≤ 15 chars
- ✓ Pelo menos 1 stop tipo `card` por dia

## `mapsQuery` · `noMaps` · `wt_labels` (2026-08-04)

Campos que controlam o que vai pro Google Maps. Ver `CLAUDE.md` §"o que vai pro Google Maps".

| Campo | Onde | Tipo | Efeito |
|---|---|---|---|
| `mapsQuery` | card · item de `opcoes` · parada de walking tour | String | **Manda esse texto e mais nada** pro Maps. Não recebe `MAPS_REGION` — escreva inequívoco (cidade e, se preciso, país). |
| `noMaps` | card · item de `opcoes` | Bool | Remove o link e **exclui o stop da rota do dia**. Pra check-in/out, despedida, "casa", picnic. |
| `wt_labels` | raiz do `data.json` | `"letters"` \| `"numbers"` | `letters` rotula as paradas como o Maps desenha: **○ A B C D** (a 1ª é origem, sem letra). Default `numbers`. |

Sem `mapsQuery`, o template limpa o nome: corta no `·` e **descarta o parêntese quando é
descrição**, mantendo quando parece endereço. `(Via Marconi 47)` fica · `(museu + vista)` sai.

**Rota do dia e de walking tour usam nomes só quando TODOS os pontos têm query utilizável** —
senão caem pra coordenada, que funciona mas o Maps rotula "Dropped pin". `maps-audit.py` mostra
qual dos dois cada rota está usando.
