---
name: road-trip-designer
description: >
  Sub-skill do itinerary-builder pra estruturar dias de carro. Dado um dia com destinos definidos,
  retorna o array completo de stops enriquecido com info de estrada (roadType, parking, fuelAlert),
  pit stops pra criança (a cada 45-60min em trechos longos), ferry integrado, e rubrica de valor
  pra stops/desvios opcionais. Pode rodar standalone quando usuário pede "estrutura o dia de Bosa".
  Google Maps route já implícita via transport + baseCoord + baseName no nível do DAY.
---

# road-trip-designer

## O que esta skill faz

Retorna estrutura completa de um dia driving:

1. **Array `stops[]`** pronto pra inserir no DAY — transit com `roadType` + card com `parking`
2. **Rubrica de valor** pra cada stop/desvio opcional (alto/médio/baixo) antes de gerar JSON
3. **Pit stops** inseridos automaticamente se trecho >45min sem parada
4. **Campos DAY** obrigatórios: `transport`, `baseCoord`, `baseName`

Não retorna HTML — só dados. `itinerary-builder` cuida da renderização.

---

## Quando triggera

**Sub-skill** (chamada pelo `itinerary-builder`):
- Dia com deslocamento de carro >20km do hotel/base
- Múltiplos destinos com drives entre eles
- Ferry integrado no dia

**Standalone** (usuário pede diretamente):
- "Estrutura o dia de carro pra Bosa"
- "Como organizar o dia de Carloforte com o ferry?"
- "Quais paradas valem no caminho pra Bavella?"

---

## Rubrica de valor · stops e desvios opcionais

Apresentar esta rubrica ANTES de gerar JSON quando há stops opcionais no dia.

| Critério | Pontos |
|---|---|
| Desvio da rota principal <5min | +2 |
| Desvio 5–15min | +1 |
| Desvio >30min | -2 |
| Stop kid-friendly (espaço pra correr, sombra, WC) | +1 |
| Visão panorâmica do carro sem parada necessária | +1 |
| Dia já tem 3+ destinos principais | -1 |
| Stop requer booking/reserva adicional | -1 |
| Estrada de montanha (limita horário de volta) | -1 |

**Interpretação:**
- **Alto (≥+2)** → incluir no roteiro
- **Médio (0 a +1)** → opcional · perguntar se quer adicionar
- **Baixo (≤-1)** → omitir · citar em nota de texto se relevante

---

## 4 tipos de road trip day

| Tipo | Modelo | Uso | Exemplo real |
|---|---|---|---|
| **Hub & Spoke** | Base fixa → N destinos → volta base | Excursão diária sem troca de hotel | Sinis + Tharros + Putzu Idu from Càbras |
| **Linear** | Base A → B (pernoita diferente) | Transição entre bases | Porto Pollo → Bonifacio · ~1h30 |
| **Loop** | Sai da base → rota circular → volta | Drives panorâmicos, montanha | Col de Bavella · saída/chegada Porto Pollo |
| **Ferry-integrated** | Drive + ferry + drive (+ volta) | Ilhas, travessias | Maladroxia → Calasetta ferry → Carloforte |

Ver `references/tipos-road-trip.md` pra árvore de decisão completa.

---

## Campos obrigatórios no DAY

```json
{
  "transport": "driving",
  "baseCoord": {"lat": 39.9300, "lng": 8.5314},
  "baseName": "Càbras, Sardinia"
}
```

`baseName` deve ser legível pra Google Maps — nome de cidade ou localidade real, não coords brutas.
`getRouteUrl()` usa `baseName` como origin + destination e gera rota carro ida e volta da base.

---

## Estrutura de stops · campos de enriquecimento

### Transit (deslocamento de carro)

```json
{
  "hora": "08:30",
  "emoji": "🚗",
  "periodo": "manha",
  "tipo": "transit",
  "nome": "Càbras → Is Arutas",
  "cat": "~15min · SP6 direção San Giovanni di Sinis",
  "roadType": "costeira",
  "coord": {"lat": 39.9513, "lng": 8.3997}
}
```

`roadType` enum: `"autopista"` · `"costeira"` · `"montanha"` · `"interior"` — ver referência.

### Transit (ferry)

```json
{
  "hora": "09:45",
  "emoji": "⛴️",
  "periodo": "manha",
  "tipo": "transit",
  "nome": "Ferry Calasetta → Carloforte",
  "cat": "~30min · Delcomar · €4-5 passageiro · €17 carro",
  "coord": {"lat": 39.1451, "lng": 8.3073}
}
```

Ferry sempre com: operador, duração, custo passageiro + custo carro (se aplicável).

### Card (atração no destino)

```json
{
  "hora": "09:00",
  "emoji": "🏖️",
  "periodo": "manha",
  "tipo": "card",
  "risco": "yellow",
  "nome": "Spiaggia di Is Arutas · areia de quartzo",
  "cat": "480m · grãos de quartzo únicos no mundo",
  "sobre": "...",
  "imperdivel": "...",
  "dicas": ["Parking €10 · enche às 10h · chegar 9h", "..."],
  "duracao": "Manhã inteira",
  "custo": "€10 parking · €15-20 aluguel cadeira",
  "acessibilidade": "Trilha curta do parking · areia firme",
  "parking": "€10/dia · lot 200m · enche 10h em agosto · chuveiros no local",
  "coord": {"lat": 39.9513, "lng": 8.3997}
}
```

`parking` é campo específico de road-trip — separado de `dicas` — com preço, distância e horário crítico.

### Pit stop (parada obrigatória pra criança em trechos >45min)

```json
{
  "hora": "09:45",
  "emoji": "🛑",
  "periodo": "manha",
  "tipo": "transit",
  "nome": "Parada · área de repouso SS292",
  "cat": "~10min · esticar pernas + WC",
  "pitStop": true,
  "coord": {"lat": 40.0800, "lng": 8.4600}
}
```

Inserir automaticamente em trechos >45min sem parada. Não perguntar — é regra de ouro família.
Ver `references/family-driving.md` pra critérios de boa parada.

---

## Anti-padrões

1. **Pit stop desnecessário** em trecho <30min — poluição visual, desnecessário
2. **>5 destinos num hub-spoke** — dia fica pesado; máximo 4 paradas principais
3. **`parking` vazio** em destinos remotos/arqueológicos — info de parking é crítica nesses casos
4. **Desvio >30min com dia lotado** — jamais incluir se dia já tem 3+ destinos
5. **`roadType` inventado** — verificar no Google Maps (street view ou Maps label) antes de definir
6. **Ferry sem horário/operador** — deixa família sem info crítica pra programar retorno

---

## Comportamento do agente

### Sub-skill (chamada pelo itinerary-builder)

1. Identificar tipo de day: hub-spoke / linear / loop / ferry-integrated
2. Calcular duração total dos trechos → verificar necessidade de pit stop (>45min sem parada)
3. Apresentar rubrica pra CADA stop opcional antes de gerar JSON
4. Preencher `roadType` com web_search ou Maps knowledge pra cada transit
5. Pesquisar `parking` pra cada card stop remoto (parque, praia, sítio arqueológico)
6. Marcar `coord_unverified: true` onde coords são incertas
7. Retornar JSON pronto pra inserção

### Standalone

Mesmos passos + seção "Como inserir no roteiro":
- Qual campo do DAY recebe o array de stops
- Quais campos de `transport`/`baseCoord`/`baseName` adicionar no nível do DAY

---

## Arquivos relacionados

- `references/tipos-road-trip.md` — 4 tipos em detalhe + árvore de decisão
- `references/route-enrichment.md` — todos campos opcionais com schema + guia de pesquisa
- `references/family-driving.md` — regras pit stop, sombra, horário pra criança pequena
- `examples/sardenha-hub-spoke.md` — 3 dias reais hub-spoke calibrados
- `examples/sardenha-ferry-loop.md` — 2 dias reais com ferry integrado
