---
name: walking-tour-designer
description: Projeta walking tours estruturados pra cidades — 4 a 16 stops com coordenadas validadas via web_search, particionado em 2 partes quando >8 stops. Use quando (1) invocada pela itinerary-builder durante fluxo de roteiro, (2) usuário pede direto - "monta um walking tour pro Marais em Paris", "preciso de um tour caminhando por Shibuya", "rota a pé pelo Beco do Batman", "design walking tour Greenwich Village", "walking tour Alfama 2 partes histórico+gastronomia". Standalone funciona. Aplica RUBRICA DE VALOR explícita - alto valor (bairro NÃO está no roteiro principal · descoberta pura), médio (enriquece bairro já visitado · annotations), baixo (overlap com stops planejadas · só anotações). 4 tipos de tour - descoberta pura (6-8 stops bairro novo), annotations (5-6 stops ao longo de caminho planejado), híbrido temático (2 partes ~6 cada por tema, ex - Bohemian Trail + Stonewall em Greenwich Village), compacto (4-5 stops num quarteirão tipo DUMBO/Stone Street). SEMPRE web_search pra coordenadas · NUNCA inventar coords · marca coord_unverified - true se estimativa · mantém endereço entre parens no nome - "Caffe Reggio (119 MacDougal)" - pra busca Google Maps preservar info. Retorna array walkingTours pronto pra inserir em card-âncora + lista de dicas numeradas 1️⃣2️⃣3️⃣ + sugestão de card âncora com justificativa. NÃO retorna HTML · só estrutura de dados consumível pela itinerary-builder ou pelo usuário.
---

# Walking Tour Designer

Sub-skill (e standalone) que projeta walking tours estruturados pra inserção em roteiros de viagem ou consumo direto.

## O que esta skill faz

Recebe um pedido (bairro + cidade + opcional: tema, composição, restrições) e retorna:

1. Array `walkingTours[]` pronto pra inserir em `card.walkingTours` da itinerary-builder
2. Lista de `dicas` numeradas (1️⃣2️⃣3️⃣...) pra adicionar no card
3. Sugestão de card-âncora (qual stop existente abrigaria esse WT)
4. Justificativa explícita de **valor** (alto/médio/baixo)

## Quando triggera

- **Sub-skill**: invocada pela `itinerary-builder` na Fase 6 do pipeline (após esqueleto validado, antes do build)
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
| Retornar HTML | Skill retorna só estrutura · itinerary-builder converte em HTML |
| Inventar coords | Mapa fica errado · família vai pro lugar errado |
| Mais de 16 stops num tour | Cansa criança · fragmentar em 2 viagens |
| Walking tour em bairro com 3+ stops já no roteiro | Overlap inútil · usar annotations |
| Stops sem endereço no nome | Google Maps busca falha · perde dia |

---

## Comportamento do agente

1. **Apresentar rubrica primeiro**: antes do JSON, mostrar `valor` + `justificativa` em tabela
2. **Validar coords**: cada coord retornada deve ter sido web_searched · marcar `coord_unverified` se dúvida
3. **Standalone**: se invocada direto pelo usuário (sem itinerary-builder), retorna estrutura completa + adiciona seção "Como inserir no seu roteiro" com instruções
4. **Sub-skill**: se invocada pela itinerary-builder, retorna só o JSON

---

## Arquivos relacionados

- `references/valor-rubrica.md` — tabela completa de pontuação + interpretação
- `references/tipos-tour.md` — 4 tipos com exemplos
- `references/coord-validation.md` — regras estritas + parens + range checks
- `examples/nyc-wt-examples.md` — 6 walking tours validados do projeto NYC com justificativa de cada
