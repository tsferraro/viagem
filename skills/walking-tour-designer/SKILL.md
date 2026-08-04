---
name: walking-tour-designer
description: Projeta walking tours estruturados pra cidades — 4 a 16 stops com coordenadas validadas via web_search, particionado em 2 partes quando >8 stops. Use quando (1) invocada pela roteiro-viagem durante fluxo de roteiro, (2) usuário pede direto - "monta um walking tour pro Marais em Paris", "preciso de um tour caminhando por Shibuya", "rota a pé pelo Beco do Batman", "design walking tour Greenwich Village", "walking tour Alfama 2 partes histórico+gastronomia". Standalone funciona. Aplica RUBRICA DE VALOR explícita - alto valor (bairro NÃO está no roteiro principal · descoberta pura), médio (enriquece bairro já visitado · annotations), baixo (overlap com stops planejadas · só anotações). 4 tipos de tour - descoberta pura (6-8 stops bairro novo), annotations (5-6 stops ao longo de caminho planejado), híbrido temático (2 partes ~6 cada por tema, ex - Bohemian Trail + Stonewall em Greenwich Village), compacto (4-5 stops num quarteirão tipo DUMBO/Stone Street). SEMPRE web_search pra coordenadas · NUNCA inventar coords · marca coord_unverified - true se estimativa · mantém endereço entre parens no nome - "Caffe Reggio (119 MacDougal)" - pra busca Google Maps preservar info. Retorna array walkingTours pronto pra inserir em card-âncora + lista de dicas numeradas 1️⃣2️⃣3️⃣ + sugestão de card âncora com justificativa. NÃO retorna HTML · só estrutura de dados consumível pela roteiro-viagem ou pelo usuário.
---

# Walking Tour Designer

Sub-skill (e standalone) que projeta walking tours estruturados pra inserção em roteiros de viagem ou consumo direto.

## O que esta skill faz

Recebe um pedido (bairro + cidade + opcional: tema, composição, restrições) e retorna:

1. Array `walkingTours[]` pronto pra inserir em `card.walkingTours` da roteiro-viagem
2. Lista de `dicas` numeradas (1️⃣2️⃣3️⃣...) pra adicionar no card
3. Sugestão de card-âncora (qual stop existente abrigaria esse WT)
4. Justificativa explícita de **valor** (alto/médio/baixo)

## Quando triggera

- **Sub-skill**: invocada pela `roteiro-viagem` na Fase 6 do pipeline (após esqueleto validado, antes do build)
- **Standalone**: usuário pede direto "monta um walking tour pro Marais em Paris"

---

## Rubrica de valor (apresentar antes do conteúdo)

Pra cada candidato a walking tour, calcular nota:

| Critério | Pontos |
|---|---|
| Bairro NÃO está no roteiro principal | +2 (descoberta pura) |
| Bairro está mas só 1 atração planejada | +1 (enriquece) |
| Bairro já tem 3+ stops planejadas | -1 (overlap) |
| Distância total < 1.5km | +1 (walkable c/ criança) |
| Distância total > 3km | -1 (cansativo) |
| Possui 2+ hidden gems documentadas | +1 (vale o esforço) |
| Sem ângulo histórico/cultural único | -1 (genérico) |

Resultado:
- **Alto** (≥+2): proposta forte, recomendar implementar
- **Médio** (0 a +1): listar opcional, deixar usuário decidir
- **Baixo** (≤-1): mencionar mas desencorajar

Detalhes em `references/valor-rubrica.md`.

---

## 4 tipos de walking tour

| Tipo | Stops | Quando usar |
|---|---|---|
| **Descoberta pura** | 6-8 | Bairro novo, alta densidade walkable, sem overlap com roteiro |
| **Annotations** | 5-6 | Bairro já no roteiro · adiciona contexto histórico/cultural a paradas existentes |
| **Híbrido temático** | 2 partes × 6 | Bairro denso com 2 narrativas (ex: Bohemian + Stonewall em Greenwich Village) |
| **Compacto** | 4-5 | Quarteirão denso (DUMBO, Stone Street, Place des Vosges) |

Detalhes em `references/tipos-tour.md`.

---

## Estrutura de retorno (JSON)

```json
{
  "valor": "alto",
  "justificativa": "Alfama não tem stop principal no esqueleto · bairro denso com 4 hidden gems documentadas · 1.2km total walkable c/ carrinho",
  "cardAncoraSugerido": "Miradouro da Senhora do Monte",
  "cardAncoraJustificativa": "Já é stop principal de manhã · WT começa imediatamente após o miradouro",
  "walkingTours": [
    {
      "nome": "Alfama · 🎵 Fado & Vista",
      "descricao": "Sé → Largo Chafariz → Beco do Carneiro → ... · ~50min",
      "stops": [
        {"n": 1, "nome": "Sé de Lisboa (Largo da Sé)", "coord": {"lat": 38.7099, "lng": -9.1334}},
        {"n": 2, "nome": "Largo do Chafariz de Dentro", "coord": {"lat": 38.7106, "lng": -9.1295}}
      ]
    }
  ],
  "dicas": [
    "1️⃣ Começar pela Sé pra pegar tram 28 de volta se cansar (5min)",
    "2️⃣ Beco do Carneiro tem 30 degraus íngremes — carrinho na mão",
    "3️⃣ Fado vadio às quintas no Tasca do Chico (Bairro Alto, não Alfama — confunde)"
  ]
}
```

---

## Regras de coordenadas (ESTRITO)

1. **SEMPRE web_search** antes de usar uma coord
2. **NUNCA inventar** baseado em "perto de X"
3. Se baseado em estimativa: marcar `coord_unverified: true` no metadata
4. Lat/lng com **4 casas decimais** (precisão ~10m)
5. Manter **endereço entre parens** no nome: `"Caffe Reggio (119 MacDougal)"` — ajuda Google Maps busca por nome+endereço
6. Range valido: `lat ∈ [-90, 90]`, `lng ∈ [-180, 180]`

Detalhes em `references/coord-validation.md`.

---

## Partition rule (>8 stops → 2 partes)

Walking tour com >8 stops cansa família com criança pequena. Particionar em 2 partes:
- Cada parte: ~6 stops
- Numeração reseta por parte (1-6 na parte 1, 1-6 na parte 2)
- Máx total: 16 stops (2 partes × 8)
- Nomes das partes: `"Parte 1 · 🎵 Tema A"`, `"Parte 2 · 🍷 Tema B"`

Se hibrido temático: cada parte tem tema próprio. Se descoberta pura: parte 1 = norte/manhã, parte 2 = sul/tarde.

---

## Anti-padrões obrigatórios

| Anti-padrão | Por quê |
|---|---|
| Retornar HTML | Skill retorna só estrutura · roteiro-viagem converte em HTML |
| Inventar coords | Mapa fica errado · família vai pro lugar errado |
| Mais de 16 stops num tour | Cansa criança · fragmentar em 2 viagens |
| Walking tour em bairro com 3+ stops já no roteiro | Overlap inútil · usar annotations |
| Stops sem endereço entre parens no nome | `getWalkingTourUrl()` usa o nome como query · sem endereço, Maps mostra "Com alfinete" · bug Sprockhövel 2026-05-23 |

---

## ✅ Checklist de conferência pós-build (OBRIGATÓRIO)

Após `build.py` rodar e ANTES de declarar walking tour pronto:

1. **Cada stop tem endereço entre parens no `nome`?** Ex: `"Beffroi de Mons (UNESCO · Rampe du Château)"` · sem isso, Google Maps mostra "Com alfinete" no lugar do nome (bug histórico Córsega 2026-05-19 + Sprockhövel 2026-05-23).
2. **`validate.py` passou no check `'WT URL usa nome (não coord)'`?** Feature-chave que garante `getWalkingTourUrl()` está na versão V1.5+ no HTML gerado.
3. **Walking tour findable**? Buscar pelo nome do tour no app deve trazer o card-âncora · `Search WT index` (feature-chave validate).
4. **Coord de cada stop validada via web_search?** Sem inventar perto de.
5. **Tour com >8 stops está partitionado?** validate alerta se >8 sem partition.

Anti-padrão metodológico: declarar walking tour pronto sem abrir o botão "🚶 Walking Tour" no Maps mobile · esse é o jeito que Tobia descobre bug. Sempre conferir um botão do WT renderizado antes de fechar a sessão.

---

## ⚠️ Escopo · NÃO propagar fixes pra walking tours de viagens fora do scope

Quando achar bug em walking tour da viagem do escopo (ex: WT URL mostrando "Com alfinete"):
- ✅ Fix na viagem do escopo
- ✅ Fix no template (`templates/render-functions.js`)
- ✅ Guardrail no `validate.py`
- ❌ NUNCA rebuild de outras viagens "pra propagar fix" sem autorização explícita do Tobia

Rebuild de viagem antiga pode sobrescrever edits manuais que não estão no `data.json` (acontece quando Tobia edita HTML direto pra correção rápida em sessão anterior). Bug Sprockhövel 2026-05-23: rebuild de `pais-sardenha` desfez correção manual de legenda feita 6h antes em outra sessão.

Documentar pendência em `HANDOFF-PENDENTE.md` (root) e deixar Tobia decidir.

---

## Comportamento do agente

1. **Apresentar rubrica primeiro**: antes do JSON, mostrar `valor` + `justificativa` em tabela
2. **Validar coords**: cada coord retornada deve ter sido web_searched · marcar `coord_unverified` se dúvida
3. **Standalone**: se invocada direto pelo usuário (sem roteiro-viagem), retorna estrutura completa + adiciona seção "Como inserir no seu roteiro" com instruções
4. **Sub-skill**: se invocada pela roteiro-viagem, retorna só o JSON

---

## Arquivos relacionados

- `references/valor-rubrica.md` — tabela completa de pontuação + interpretação
- `references/tipos-tour.md` — 4 tipos com exemplos
- `references/coord-validation.md` — regras estritas + parens + range checks
- `examples/nyc-wt-examples.md` — 6 walking tours validados do projeto NYC com justificativa de cada

## `mapsQuery` obrigatório em toda parada (2026-08-04)

Bug pego em campo com print: a rota do walking tour de Bonifacio devolvia **"Can't seem to find
that place"**, porque `"Porte de Gênes (entrada principal)"` virava a busca `Porte de Gênes
entrada principal`. E o pino do card `"Walking tour Cidadela · com os avós"` abria o Maps **no
meio do mar** — nome de card descreve uma *atividade*, o Maps precisa de um *lugar*.

`validate.py` **bloqueia** parada de walking tour sem `mapsQuery` (`check_wt_maps_query`).

- **Uma `mapsQuery` por parada**, com o nome canônico do POI — o que o Google indexa, não a
  tradução nem o apelido. Casos que só a verificação pegou: *"Loggia · mirador sul"* não é POI
  (é **Falaises de Bonifacio**) · *"Necrópole púnica"* é **Villaggio Ipogeo** · *"Spiaggia di
  Tegge"* é **Punta Tegge**.
- **Não recebe `MAPS_REGION`** — escreva inequívoco. Um walking tour pode estar num roteiro de
  outra região (Bonifacio, na Córsega, dentro do roteiro da Sardenha).
- A rota só usa nomes quando **TODAS** as paradas têm `mapsQuery`; uma parada ruim mata a rota
  inteira, e o fallback por coordenada mostra "Dropped pin".
- O card-pai do tour normalmente precisa de `mapsQuery` próprio (`"Citadelle de Bonifacio"`).
- Conferir **uma a uma** (`critico-roteiro/FACTCHECK.md` §4a). Derivar em massa não conta: numa
  derivação de 39 paradas do Marais, duas saíram erradas.

### Rótulo das paradas: `wt_labels: "letters"`

Com esse campo no `data.json`, as paradas usam **o mesmo rótulo que o Google Maps desenha**: a
primeira é a origem (círculo, sem letra) e as seguintes são A, B, C. Cinco paradas viram
**`○ A B C D`**, não `A B C D E`. As dicas parada-a-parada devem usar os mesmos símbolos
(`○ Ⓐ Ⓑ Ⓒ Ⓓ`) pra que card e Maps se leiam lado a lado sem tradução mental.

Confira com `python3 scripts/maps-audit.py <viagem>/index.html --urls`.
