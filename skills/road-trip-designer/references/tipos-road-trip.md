# Tipos de road trip day

## 1 · Hub & Spoke

**Modelo**: Base fixa → N destinos → volta base (mesma noite)

**Quando usar**:
- 2+ noites na mesma base
- Destinos a <1h30 da base (cada um)
- Família não precisa mudar de hotel

**Máximo recomendado**: 4 destinos principais por dia (senão fica pesado)

**Exemplo real**: Sinis (Dom 9/Ago) — base Càbras → Is Arutas (15min) → Tharros (15min) → Putzu Idu (15min) → Càbras

**JSON do DAY**:
```json
{
  "transport": "driving",
  "baseCoord": {"lat": 39.9300, "lng": 8.5314},
  "baseName": "Càbras, Sardinia"
}
```

**Anti-padrões**:
- Hub-spoke com base >1h30 de distância dos destinos → dia cansativo demais
- 5+ destinos num dia com filha pequena → cortar pra 3-4

---

## 2 · Linear

**Modelo**: Parte de Base A pela manhã → para em 1-2 pontos → pernoita em Base B

**Quando usar**:
- Mudança de hotel no dia
- Rota direcional (ex: norte→sul da ilha)
- 1-2 paradas max (não pode voltar pra ver mais)

**Exemplo real**: Porto Pollo → Bonifacio (7/Ago, Córsega) · 1h30 de carro · check-in novo hotel

**JSON do DAY**: Sem `baseCoord`/`baseName` (não há base de retorno). Ou usar base de chegada se quiser rota Maps.

**Anti-padrões**:
- Linear com >3 paradas — stresses o horário de check-in
- Não marcar a transição com risco amarelo se tem ferry obrigatório no dia

---

## 3 · Loop

**Modelo**: Sai da base → rota circular panorâmica → volta à mesma base

**Quando usar**:
- Estrada cênica que forma um circuito natural
- Destino de montanha ou interior sem backtracking
- Nenhum destino específico é o foco — o drive em si é a experiência

**Exemplo real**: Col de Bavella (1/Ago, Córsega) — base Porto Pollo → Bavella → Polischellu → volta Porto Pollo por rota diferente

**Diferença de hub-spoke**: No loop, a rota é não-linear e os pontos de parada são escolhidos ao longo do percurso, não "vai e volta da base". No hub-spoke, todos os destinos são spoke isolated que requerem backtrack.

**Anti-padrões**:
- Loop em estrada de montanha com late start — estradas de montanha pedem saída cedo (sol forte + congestionamento turístico)
- Loop sem rota alternativa definida se o percurso for de mão única ou inviável pra voltar

---

## 4 · Ferry-integrated

**Modelo**: Drive até porto → ferry → destino ilha/continente → atividades → ferry volta → drive base

**Quando usar**:
- Destino é uma ilha sem acesso de carro direto
- Travessia curta (<1h) que vale o investimento
- Ferry tem horário fixo → planeja o dia em torno dele

**Exemplos reais**:
- Carloforte (Sex 14/Ago): Maladroxia → Calasetta (25min) → ferry Calasetta→Carloforte (30min)
- La Maddalena (Qua 19/Ago): Santa Teresa → Palau (30min) → ferry Palau→La Maddalena (15min)

**Regra crítica**: Sempre marcar horário do ferry de VOLTA no último transit do dia. Ferry é o constraint que determina todo o resto.

**JSON ferry stop**:
```json
{
  "emoji": "⛴️",
  "tipo": "transit",
  "nome": "Ferry Calasetta → Carloforte",
  "cat": "~30min · Delcomar · €4-5 passageiro · €17 carro"
}
```

**Anti-padrões**:
- Deixar horário de volta do ferry ambíguo ("pega qualquer um") — em agosto ferries lotam
- Levar carro se ferry tem custo >€20 e destino é walkable — às vezes passageiro sem carro é melhor

---

## Árvore de decisão · qual tipo escolher?

```
Muda de hotel/base hoje?
├─ SIM → LINEAR
└─ NÃO
    ├─ Tem ferry no trajeto?
    │   └─ SIM → FERRY-INTEGRATED
    └─ NÃO
        ├─ A rota dos destinos forma um circuito natural?
        │   └─ SIM → LOOP (ex: estrada panorâmica circular)
        └─ NÃO → HUB & SPOKE (excursão com retorno à base)
```

---

## Tabela de risco por tipo

| Tipo | Risco padrão | Quando elevar pra RED |
|---|---|---|
| Hub & Spoke | 🟢 | >4 destinos principais |
| Linear | 🟡 | Ferry obrigatório + check-in forçado |
| Loop | 🟡 | Estrada de montanha + late start |
| Ferry-integrated | 🟡 | Agosto + ferry sem reserva = 🔴 |
