# 4 Tipos de Walking Tour

## 1 · Descoberta pura

**Stops**: 6-8 (1 parte) OU 2 partes ~6 cada (se >8)

**Quando usar**: bairro **NÃO** está no roteiro principal · alta densidade walkable · sem overlap

**Exemplo (NYC)**: DUMBO · 6 stops com history industrial + Brooklyn Bridge Park

```json
{
  "nome": "DUMBO · 🏭 Industrial Past",
  "descricao": "Old Fulton → Eagle Warehouse → Empire Stores → ... · ~40min",
  "stops": [
    {"n": 1, "nome": "Old Fulton Street (1814 ferry landing)", "coord": {...}},
    {"n": 2, "nome": "Eagle Warehouse 1893 (28 Old Fulton)", "coord": {...}},
    {"n": 3, "nome": "Empire Stores 1869 (53 Water St)", "coord": {...}}
  ]
}
```

## 2 · Annotations

**Stops**: 5-6

**Quando usar**: bairro JÁ tem stops principais no roteiro · WT adiciona contexto histórico/cultural

**Exemplo**: bairro com 2 stops principais (museu + restaurante), WT adiciona 5 pontos de contexto entre eles

## 3 · Híbrido temático (2 partes)

**Stops**: 2 partes × 6 = 12 total

**Quando usar**: bairro denso com **2 narrativas distintas** (não-sequenciais)

**Exemplo (NYC Greenwich Village)**:

```json
{
  "walkingTours": [
    {
      "nome": "Parte 1 · 🎭 Bohemian Trail",
      "descricao": "Caffe Reggio → Washington Square Park → ... · ~30min",
      "stops": [...6 stops...]
    },
    {
      "nome": "Parte 2 · 🏳️‍🌈 Stonewall & Legacy",
      "descricao": "Stonewall Inn → Christopher Park → ... · ~25min",
      "stops": [...6 stops...]
    }
  ]
}
```

## 4 · Compacto

**Stops**: 4-5 (1 parte só)

**Quando usar**: quarteirão denso · não dá pra esticar

**Exemplo (NYC)**: Stone Street (Financial District) · 4 stops num quarteirão histórico

```json
{
  "nome": "Stone Street · ⚓ Dutch Roots",
  "descricao": "Adriaen Block plaque → Mill Lane → ... · ~15min",
  "stops": [...4 stops...]
}
```

## Decisão · qual tipo escolher

| Pergunta | Resposta | Tipo |
|---|---|---|
| Bairro está no roteiro principal? | NÃO + 6-8 stops cabem | **Descoberta pura** |
| Bairro está no roteiro? | SIM + 5-6 contextos válidos | **Annotations** |
| Bairro denso com 2 narrativas? | SIM | **Híbrido temático** |
| Quarteirão denso só? | SIM, 4-5 stops máx | **Compacto** |
| Bairro >8 stops num tipo só? | Sempre | **Particionar em 2 partes** |

## Anti-padrões

- 1 tour com 12 stops sem partition → ninguém aguenta com carrinho
- Annotations num bairro com só 1 stop principal → vira descoberta pura disfarçada
- Híbrido temático com 2 partes na sequência → na verdade é 1 tour longo · partition
