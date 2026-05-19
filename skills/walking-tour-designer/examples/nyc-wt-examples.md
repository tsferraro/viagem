# Walking Tours NYC · Exemplos Validados

6 walking tours do projeto NYC Jul/2026 com justificativa de cada · serve de reference pra calibragem.

---

## 1 · DUMBO · Industrial Past (descoberta pura · alto valor)

**Rubrica**:
- Bairro novo no roteiro: +2
- Distância 0.9km: +1
- 3 hidden gems (Eagle Warehouse, Empire Stores, Manhattan Bridge anchorage): +1
- Acessibilidade boa: 0
- **Total: +4 → ALTO**

**Card âncora**: Brooklyn Bridge Park · Pier 1

**Justificativa**: DUMBO entrou no roteiro só como "view de Manhattan" — WT enriquece com 100 anos de history industrial. Walkable c/ carrinho. Eagle Warehouse 1893 + Empire Stores 1869 = ângulo único.

```json
{
  "nome": "DUMBO · 🏭 Industrial Past",
  "descricao": "Old Fulton → Eagle Warehouse → Empire Stores → Jane's Carousel → Manhattan Bridge anchorage · ~40min",
  "stops": [
    {"n": 1, "nome": "Old Fulton Street (1814 ferry landing site)", "coord": {"lat": 40.7029, "lng": -73.9930}},
    {"n": 2, "nome": "Eagle Warehouse 1893 (28 Old Fulton St)", "coord": {"lat": 40.7028, "lng": -73.9924}},
    {"n": 3, "nome": "Empire Stores 1869 (53 Water St)", "coord": {"lat": 40.7037, "lng": -73.9907}},
    {"n": 4, "nome": "Jane's Carousel 1922 (Brooklyn Bridge Park)", "coord": {"lat": 40.7035, "lng": -73.9939}},
    {"n": 5, "nome": "Manhattan Bridge anchorage view (Adams St)", "coord": {"lat": 40.7040, "lng": -73.9897}},
    {"n": 6, "nome": "Pebble Beach (Plymouth St & Main St)", "coord": {"lat": 40.7034, "lng": -73.9920}}
  ]
}
```

---

## 2 · Greenwich Village · Híbrido Bohemian + Stonewall (alto valor · 2 partes)

**Rubrica**:
- Bairro só com 1 stop planejado (Washington Square Park): +1
- Distância parte 1: 1.1km, parte 2: 0.8km: +1
- Múltiplas hidden gems (Caffe Reggio, Christopher Park, Stonewall): +1
- 2 narrativas distintas: +1
- **Total: +4 → ALTO**

**Card âncora**: Washington Square Park

**Justificativa**: bairro denso, walkable, 2 ângulos não-sobrepostos (bohemian arts 1950s vs LGBTQ+ rights 1969).

```json
{
  "walkingTours": [
    {
      "nome": "Parte 1 · 🎭 Bohemian Trail",
      "descricao": "Caffe Reggio → Washington Square → ... · ~30min",
      "stops": [
        {"n": 1, "nome": "Caffe Reggio (119 MacDougal St)", "coord": {"lat": 40.7299, "lng": -74.0011}},
        {"n": 2, "nome": "Washington Square Arch (5th Ave entrance)", "coord": {"lat": 40.7311, "lng": -73.9978}},
        {"n": 3, "nome": "NYU Bobst Library (70 Washington Sq S)", "coord": {"lat": 40.7295, "lng": -73.9971}},
        {"n": 4, "nome": "Minetta Tavern 1937 (113 MacDougal)", "coord": {"lat": 40.7296, "lng": -74.0010}},
        {"n": 5, "nome": "Cherry Lane Theatre (38 Commerce St)", "coord": {"lat": 40.7314, "lng": -74.0049}},
        {"n": 6, "nome": "Marie's Crisis Cafe (59 Grove St)", "coord": {"lat": 40.7332, "lng": -74.0033}}
      ]
    },
    {
      "nome": "Parte 2 · 🏳️‍🌈 Stonewall & Legacy",
      "descricao": "Stonewall Inn → Christopher Park → ... · ~25min",
      "stops": [
        {"n": 1, "nome": "Stonewall Inn (53 Christopher St)", "coord": {"lat": 40.7340, "lng": -74.0024}},
        {"n": 2, "nome": "Christopher Park (Stonewall National Monument)", "coord": {"lat": 40.7338, "lng": -74.0020}},
        {"n": 3, "nome": "Julius Bar 1864 (159 W 10th St)", "coord": {"lat": 40.7345, "lng": -74.0028}},
        {"n": 4, "nome": "AIDS Memorial (St Vincent's Triangle)", "coord": {"lat": 40.7368, "lng": -74.0014}},
        {"n": 5, "nome": "Oscar Wilde Bookshop site (15 Christopher St)", "coord": {"lat": 40.7337, "lng": -74.0008}},
        {"n": 6, "nome": "LGBT Community Center (208 W 13th St)", "coord": {"lat": 40.7386, "lng": -74.0015}}
      ]
    }
  ]
}
```

---

## 3 · Williamsburg · Mural Trail (descoberta pura · médio valor)

**Rubrica**:
- Bairro com 1 stop planejado (Apple Williamsburg): +1
- Distância 1.4km: +1
- Hidden gems médios (murais sazonais): 0
- Sem narrativa única (vários murais): -1
- **Total: +1 → MÉDIO**

**Justificativa**: WT opcional · pode pular se preferir tempo livre no bairro.

---

## 4 · Stone Street · Dutch Roots (compacto · alto valor)

**Rubrica**:
- Bairro novo: +2
- Distância 0.3km (1 quarteirão): +1
- Hidden gems clássico (Adriaen Block plaque, Mill Lane): +1
- Acessibilidade boa: 0
- **Total: +4 → ALTO**

**Tipo**: Compacto (4 stops num quarteirão)

```json
{
  "nome": "Stone Street · ⚓ Dutch Roots",
  "descricao": "Adriaen Block plaque → Mill Lane → Stone Street tavern row · ~15min",
  "stops": [
    {"n": 1, "nome": "Adriaen Block plaque (Pearl St & Broad St)", "coord": {"lat": 40.7057, "lng": -74.0114}},
    {"n": 2, "nome": "Mill Lane (1660 oldest paved street)", "coord": {"lat": 40.7057, "lng": -74.0119}},
    {"n": 3, "nome": "Stone Street tavern row (32-55 Stone St)", "coord": {"lat": 40.7044, "lng": -74.0113}},
    {"n": 4, "nome": "Hanover Square (1637)", "coord": {"lat": 40.7048, "lng": -74.0103}}
  ]
}
```

---

## 5 · Times Square WT (baixo valor · desencorajado)

**Rubrica**:
- Bairro já com 3+ stops planejadas: -1
- Distância 0.5km: +1
- Sem hidden gems (turistada): 0
- Sem narrativa única: -1
- **Total: -1 → BAIXO**

**Decisão**: NÃO gerar. Apresentar rubrica + recomendar pulo.

> "Walking tour de baixo valor. Times Square já é stop principal · sem hidden gems · pula sem culpa."

---

## 6 · Upper East Side · Museum Mile Annotations (médio valor)

**Rubrica**:
- Bairro com 2 stops (Met + Guggenheim): +1
- Distância 1.0km: +1
- Annotations (Frick mansion 1914, Cooper-Hewitt 1902): +1
- Sem narrativa única (annotations dispersas): -1
- **Total: +2 → MÉDIO-ALTO**

**Tipo**: Annotations (5-6 stops contextuais entre Met e Guggenheim)

```json
{
  "nome": "Museum Mile · 🎨 Gilded Age Annotations",
  "descricao": "Frick Collection → Cooper-Hewitt → Jewish Museum → Guggenheim · ~35min",
  "stops": [
    {"n": 1, "nome": "Frick Collection (1 E 70th St, Henry Frick 1914 mansion)", "coord": {"lat": 40.7711, "lng": -73.9670}},
    {"n": 2, "nome": "Met Museum (1000 5th Ave, 1880 founded)", "coord": {"lat": 40.7794, "lng": -73.9632}},
    {"n": 3, "nome": "Goethe-Institut (30 Irving Pl)", "coord": {"lat": 40.7805, "lng": -73.9620}},
    {"n": 4, "nome": "Cooper-Hewitt (2 E 91st, Andrew Carnegie 1902 mansion)", "coord": {"lat": 40.7847, "lng": -73.9583}},
    {"n": 5, "nome": "Jewish Museum (1109 5th Ave, Felix Warburg 1908 mansion)", "coord": {"lat": 40.7853, "lng": -73.9577}},
    {"n": 6, "nome": "Guggenheim (1071 5th Ave, Frank Lloyd Wright 1959)", "coord": {"lat": 40.7830, "lng": -73.9590}}
  ]
}
```

---

## Calibragem

Use estes 6 exemplos pra calibrar:
- Quantos pontos de rubrica = nota X
- Quantos stops por tipo
- Quanto detalhe no campo `nome` (endereço entre parens)
- Justificativa adequada
