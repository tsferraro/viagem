# Exemplos Hub & Spoke · Sardenha · pais-sardenha-ago2026

3 exemplos reais calibrados do roteiro dos avós. Usar como referência de profundidade e formato.

---

## 1 · Dom 9/Ago · Sinis + Tharros + Putzu Idu

**Tipo**: Hub & Spoke · base Càbras · 3 destinos · todos <15min da base

### Rubrica de stops opcionais

Nenhum desvio opcional nesse dia — todos 3 destinos fazem parte do plano. Rubrica aplicada durante construção:

| Stop | Critério principal | Pontos | Decisão |
|---|---|---|---|
| Is Arutas (manhã inteira) | Principal do dia · obrigatório | — | ✅ incluir |
| Tharros (tarde) | On-route (15min da praia) · arqueológico único | +2 (on-route <5min da rota principal) | ✅ incluir |
| Putzu Idu (final de tarde) | On-route · opcional · kid-friendly (+1) · dia com 2 destinos já (+0) | +2 | ✅ opcional marcado nos dicas |

### Campos DAY

```json
{
  "transport": "driving",
  "baseCoord": {"lat": 39.9300, "lng": 8.5314},
  "baseName": "Càbras, Sardinia"
}
```

### Stops com enriquecimento

**Transit 1 — base → Is Arutas**:
```json
{
  "hora": "08:30",
  "emoji": "🚗",
  "periodo": "manha",
  "tipo": "transit",
  "nome": "Càbras → Is Arutas",
  "cat": "~15min · SP6 direção San Giovanni di Sinis",
  "roadType": "interior",
  "coord": {"lat": 39.9513, "lng": 8.3997}
}
```

**Card — Is Arutas**:
```json
{
  "hora": "09:00",
  "emoji": "🏖️",
  "periodo": "manha",
  "tipo": "card",
  "risco": "yellow",
  "nome": "Spiaggia di Is Arutas · areia de quartzo",
  "cat": "480m · grãos brancos/rosa de quartzo",
  "sobre": "Praia única no mundo: 'areia' feita de grãos de quartzo finos (rice grain), brancos e rosados. Parte do Marine Protected Area de Sinis. PROIBIDO levar quartzo embora (multas). Água cristalina, lagoa rasa.",
  "imperdivel": "Andar descalço · sensação única dos grãos · NÃO leva nenhuma na bolsa",
  "dicas": [
    "Parking €10/dia · enche às 10h em agosto · chegar 9h",
    "Chuveiros + WC públicos no parking",
    "Sombra escassa · leva guarda-sol"
  ],
  "duracao": "Manhã inteira",
  "custo": "€10 parking · €15-20 aluguel cadeira",
  "acessibilidade": "Trilha curta do parking · areia firme, fácil andar",
  "parking": "€10/dia · estacionamento principal 200m da praia · lotado 10h em agosto · WC e chuveiro no local",
  "coord": {"lat": 39.9513, "lng": 8.3997}
}
```

**Transit 2 — Is Arutas → Tharros**:
```json
{
  "hora": "12:30",
  "emoji": "🚗",
  "periodo": "tarde",
  "tipo": "transit",
  "nome": "Is Arutas → Tharros",
  "cat": "~15min · ponta da península Sinis",
  "roadType": "interior",
  "coord": {"lat": 39.8938, "lng": 8.4341}
}
```

**Card — Tharros** (nota: `coord_unverified: true` pois coord foi estimada):
```json
{
  "hora": "14:30",
  "emoji": "🏛️",
  "periodo": "tarde",
  "tipo": "card",
  "risco": "yellow",
  "nome": "Tharros · ruínas fenício-romanas no mar",
  "cat": "Sítio arqueológico em península no mar",
  "sobre": "Cidade fenícia-púnica fundada ~séc. VIII a.C., depois romana. Localizada em ponta extrema da península (Capo San Marco), com vista oceânica dos dois lados. Remanescentes: termas romanas, colunas de pé, Nuraghe Su Muru Mannu. Setting espetacular.",
  "imperdivel": "As colunas romanas com mar atrás · postal único da Sardenha",
  "dicas": [
    "Ticket combinado Tharros + Museo Civico Cabras = €10 (separados €6.50+€5)",
    "Tarde com luz dourada é melhor pra fotos",
    "Sem sombra · chapéu + água obrigatórios"
  ],
  "duracao": "1h30-2h",
  "custo": "€6.50 sozinho · €10 combinado",
  "acessibilidade": "Trilha de pedra · degraus em alguns pontos · sapato firme",
  "parking": "Estacionamento no sítio · €3-5 · 5min a pé da entrada",
  "coord": {"lat": 39.8938, "lng": 8.4341},
  "coord_unverified": true
}
```

### Lições desse dia
- `coord_unverified` aplicado em Tharros → verificar antes da viagem (ligar OT Oristano)
- Putzu Idu tratado como opcional dentro dos `dicas` de Tharros — não forçou um 4º card
- Pit stop não necessário: nenhum trecho >30min

---

## 2 · Seg 10/Ago · Bosa · 1h15 de estrada costeira

**Tipo**: Hub & Spoke · base Càbras · 1 destino principal + opção praia no retorno

### Rubrica de stops opcionais

| Stop | Critério | Pontos | Decisão |
|---|---|---|---|
| Estrada SS292 en route | Costeira panorâmica · "o drive é a experiência" · on-route | +2 | ✅ mencionar em cat do transit |
| Bosa Marina (praia, 3km sul) | Desvio <5min de Bosa (+2) · kid-friendly (+1) · mas dia já tem walking tour long (-1) | +2 | ✅ opcional · card com "pular sem culpa" |

### Campos DAY

```json
{
  "transport": "driving",
  "baseCoord": {"lat": 39.9300, "lng": 8.5314},
  "baseName": "Càbras, Sardinia"
}
```

### Stops chave

**Transit — Càbras → Bosa**:
```json
{
  "hora": "08:30",
  "emoji": "🚗",
  "periodo": "manha",
  "tipo": "transit",
  "nome": "Càbras → Bosa via SS292 costeira",
  "cat": "~1h15 · estrada panorâmica entre falésias · uma das melhores da Sardenha",
  "roadType": "costeira"
}
```

Nota: a estrada SS292 é tão boa que vale menção explícita no `cat` do transit — o drive em si é parte do programa.

**Pit stop** (trecho 1h15 → obrigatório com criança 3a):
```json
{
  "hora": "09:15",
  "emoji": "🛑",
  "periodo": "manha",
  "tipo": "transit",
  "nome": "Parada · SS292 km ~40",
  "cat": "~10min · mirador costeiro + esticar pernas",
  "pitStop": true,
  "coord": {"lat": 40.0800, "lng": 8.4600}
}
```

**Card — Bosa** (com walking tour encaixado):
```json
{
  "parking": "€2-3/h zona azul centro · estacionar perto do Lungofiume · cidade velha só a pé"
}
```

### Lições desse dia
- Pit stop obrigatório: trecho 1h15 → inserir parada ~45min
- Walking tour (Bosa Medieval) encaixado dentro do card principal — não precisa day separado
- Bosa Marina marcada como opcional com "pular sem culpa" explícito nos dicas — evita frustração se cansados

---

## 3 · Sáb 15/Ago · Porto Flavia + Cala Domestica

**Tipo**: Hub & Spoke · base Maladroxia · 2 destinos · 1h15 pra chegar

### Rubrica de stops opcionais

| Stop | Critério | Pontos | Decisão |
|---|---|---|---|
| Porto Flavia | Principal · reserva obrigatória · 2h tour | — | ✅ obrigatório |
| Cala Domestica | On-route voltando (desvio +5min) · pra almoço e banho | +2 | ✅ incluir |
| Pan di Zucchero (só de longe, do penhasco) | Vista do tour de Porto Flavia · sem desvio | +2 | ✅ mencionar em imperdivel |

### Atenção especial: booking obrigatório

Porto Flavia tem max 25 pessoas por tour. Reservar em `portoflaviatours.it` com semanas de antecedência em agosto. **Marcar na seção de reservas pendentes do roteiro.**

### Transit Maladroxia → Porto Flavia (estrada mista):
```json
{
  "hora": "08:00",
  "emoji": "🚗",
  "periodo": "manha",
  "tipo": "transit",
  "nome": "Maladroxia → Porto Flavia",
  "cat": "~1h15 · SP83 via Iglesias e Buggerru",
  "roadType": "interior"
}
```

**Pit stop** (1h15 → obrigatório):
```json
{
  "hora": "08:45",
  "emoji": "🛑",
  "periodo": "manha",
  "tipo": "transit",
  "nome": "Parada · Iglesias centro",
  "cat": "~10min · café + WC · cidade histórica espanhola",
  "pitStop": true,
  "coord": {"lat": 39.3143, "lng": 8.5357}
}
```

**Card Porto Flavia**:
```json
{
  "parking": "Estacionamento no local · gratuito · 2min a pé da entrada do tour"
}
```

### Lições desse dia
- Saída às 08h obrigatória — tour às 09:30 com margem 30min
- Pit stop em Iglesias vira parada de valor duplo: logística + vista rápida de cidade histórica
- Cala Domestica após Porto Flavia é sequência natural (mesma estrada, 15min)
