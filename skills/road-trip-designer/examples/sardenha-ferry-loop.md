# Exemplos Ferry-Integrated · Sardenha · pais-sardenha-ago2026

2 exemplos reais de dias com ferry do roteiro dos avós.

---

## 1 · Sex 14/Ago · Carloforte · ferry Calasetta↔Carloforte

**Tipo**: Ferry-integrated · base Maladroxia · drive → porto → ferry → ilha → ferry → base

**Constraint principal**: Ferry Delcomar tem horários fixos (~6/dia cada sentido em agosto). O dia inteiro se organiza em torno do ferry de volta (~18h30).

### Campos DAY

```json
{
  "transport": "driving",
  "baseCoord": {"lat": 38.9989, "lng": 8.4489},
  "baseName": "Maladroxia, Sardinia"
}
```

### Estrutura completa de stops

**Transit 1 — Maladroxia → Calasetta (porto ferry)**:
```json
{
  "hora": "09:00",
  "emoji": "🚗",
  "periodo": "manha",
  "tipo": "transit",
  "nome": "Maladroxia → Calasetta (porto ferry)",
  "cat": "~25min · norte da ilha Sant'Antioco",
  "roadType": "interior",
  "coord": {"lat": 39.1078, "lng": 8.3686}
}
```

**Transit 2 — Ferry ida**:
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

**Card principal — Carloforte**:
```json
{
  "hora": "10:30",
  "emoji": "🏝️",
  "periodo": "manha",
  "tipo": "card",
  "risco": "green",
  "nome": "Carloforte · vila genovesa do atum",
  "cat": "Caruggi + Tonnara + culinária única",
  "parking": "Carro fica em Calasetta (estacionamento perto do porto, gratuito) · ferry de passageiro pra Carloforte",
  "coord": {"lat": 39.1451, "lng": 8.3073}
}
```

Nota sobre `parking`: o carro **fica em terra** em Calasetta. Carloforte é completamente walkable — levar carro custa €17 extra e não adiciona valor.

**Transit — Ferry volta**:
```json
{
  "hora": "18:30",
  "emoji": "⛴️",
  "periodo": "noite",
  "tipo": "transit",
  "nome": "Ferry Carloforte → Calasetta",
  "cat": "~30min · check horário Delcomar · próximo às 20h",
  "coord": {"lat": 39.1078, "lng": 8.3686}
}
```

**Transit — Calasetta → Maladroxia**:
```json
{
  "hora": "19:30",
  "emoji": "🚗",
  "periodo": "noite",
  "tipo": "transit",
  "nome": "Calasetta → Maladroxia",
  "cat": "~25min",
  "roadType": "interior",
  "coord": {"lat": 38.9989, "lng": 8.4489}
}
```

### Lições desse dia

- **Decisão carro vs passageiro**: Carloforte walkable → ferry passageiro (€4-5) em vez de carro (€17). Economia + menos logística. Carro fica em Calasetta com estacionamento gratuito.
- **Pit stop não necessário**: nenhum trecho >30min de carro (25min Maladroxia→Calasetta)
- **Horário de volta definido primeiro**: 18h30 → trabalha de trás pra frente → sai da praia 18h → almoço 13h-15h → manhã Walking tour caruggi
- **Reserva Al Tonno di Corsa**: Michelin recommend, reservar com 2-4 semanas de antecedência em agosto
- **risco verde**: ferry tem múltiplos horários por dia em agosto · sem risco alto

---

## 2 · Qua 19/Ago · La Maddalena · ferry Palau↔La Maddalena

**Tipo**: Ferry-integrated · base Santa Teresa di Gallura · drive → Palau → ferry → arquipélago → volta

**Diferença de Carloforte**: La Maddalena é maior (carro vale a pena) + arquipélago exige carro pra explorar Caprera.

### Campos DAY

```json
{
  "transport": "driving",
  "baseCoord": {"lat": 41.2389, "lng": 9.1907},
  "baseName": "Santa Teresa di Gallura, Sardinia"
}
```

### Estrutura de stops

**Transit 1 — Santa Teresa → Palau**:
```json
{
  "hora": "08:30",
  "emoji": "🚗",
  "periodo": "manha",
  "tipo": "transit",
  "nome": "Santa Teresa di Gallura → Palau",
  "cat": "~30min · SS133 costeira norte",
  "roadType": "costeira",
  "coord": {"lat": 41.1824, "lng": 9.3831}
}
```

**Transit 2 — Ferry ida com carro**:
```json
{
  "hora": "09:15",
  "emoji": "⛴️",
  "periodo": "manha",
  "tipo": "transit",
  "nome": "Ferry Palau → La Maddalena (com carro)",
  "cat": "~15min · Enermar/Delcomar · €4 passageiro · €12-15 carro · saídas ~cada 30min",
  "coord": {"lat": 41.2138, "lng": 9.4054}
}
```

**Card principal — La Maddalena + Caprera**:
```json
{
  "hora": "09:30",
  "emoji": "🏝️",
  "periodo": "manha",
  "tipo": "card",
  "risco": "green",
  "nome": "Arquipélago La Maddalena · praias + Caprera",
  "cat": "Ilha principal + Caprera (Garibaldi) via bridge",
  "parking": "Porto La Maddalena: €3-5/h · Caprera: estacionamento perto das praias gratuito ou €2-5",
  "coord": {"lat": 41.2138, "lng": 9.4054}
}
```

Nota sobre decisão carro: La Maddalena tem 3km de extensão + ponte pra Caprera — carro viabiliza ver praias remotas (Cala Coticcio) e Museo Garibaldi em Caprera.

**Transit — Ferry volta**:
```json
{
  "hora": "18:00",
  "emoji": "⛴️",
  "periodo": "tarde",
  "tipo": "transit",
  "nome": "Ferry La Maddalena → Palau",
  "cat": "~15min · saídas frequentes · último às ~22h",
  "coord": {"lat": 41.1824, "lng": 9.3831}
}
```

**Transit — Palau → Santa Teresa**:
```json
{
  "hora": "18:30",
  "emoji": "🚗",
  "periodo": "tarde",
  "tipo": "transit",
  "nome": "Palau → Santa Teresa di Gallura",
  "cat": "~30min",
  "roadType": "costeira",
  "coord": {"lat": 41.2389, "lng": 9.1907}
}
```

### Comparação das 2 decisões ferry

| | Carloforte | La Maddalena |
|---|---|---|
| **Carro no ferry?** | NÃO (walkable) | SIM (Caprera + praias remotas) |
| **Custo ferry** | €4-5 passageiro | €4 + €12-15 carro |
| **Ilha walkable?** | Sim (centro 30min a pé) | Não (Caprera = 8km) |
| **Duração travessia** | 30min | 15min |
| **Frequência ferry** | ~6/dia | ~cada 30min |
| **Risco horário** | Médio (6/dia) | Baixo (frequente) |

### Lições desse dia

- **Pit stop no caminho a Palau**: trecho 30min → abaixo do limiar de 45min → sem pit stop necessário
- **Caprera é o diferencial**: sem carro, fica só em La Maddalena centro (ok mas menor valor)
- **Último ferry é às ~22h** → risco muito baixo de perder o ferry de volta
- **Rubrica de parada**: não há stops opcionais no caminho Santa Teresa → Palau que valham desvio
