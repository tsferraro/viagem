# route-enrichment · campos de enriquecimento pra dias de carro

## Campo `roadType` (em transit stops)

Descreve o tipo de estrada do trecho. Impacta horário de saída, velocidade esperada e experiência.

| Valor | Característica | Impacto prático |
|---|---|---|
| `"autopista"` | Rodovia rápida (SS131, A1, SP1) · sem curvas · velocidade alta | Tempo de viagem previsível · nenhuma parada obrigatória |
| `"costeira"` | Estrada beira-mar · panorâmica · curvas moderadas | +20-30% tempo vs GPS · paradas de foto tentadoras |
| `"montanha"` | Curvas fechadas · altitude · possivelmente estreita | +30-50% tempo · saída cedo obrigatória · check meteo |
| `"interior"` | Estrada rural comum · campo ou entre cidades | Tempo GPS confiável · sem surpresas |

**Como verificar**: Google Maps → traçar rota → ver perfil. Street View confirma se é curva/montanha/costa.

**Exemplo em JSON**:
```json
{
  "tipo": "transit",
  "nome": "Càbras → Bosa via SS292",
  "cat": "~1h15 · estrada panorâmica entre falésias",
  "roadType": "costeira"
}
```

---

## Campo `parking` (em card stops)

Info de estacionamento específica do destino. Obrigatório em destinos remotos (praias, sítios arqueológicos, parques), opcional em cidades com parking urbano óbvio.

**Estrutura sugerida** (texto livre, não JSON):
```
"parking": "€10/dia · lot 200m · enche 10h em agosto"
"parking": "Gratuito · beira da estrada · 5min a pé da entrada"
"parking": "€3/h zona azul · máx 2h · parking pago a 400m sem limite"
```

**Como pesquisar parking**:
1. Site oficial do parque/museu/atração (geralmente lista parking)
2. Google Maps → busca o lugar → reviews mencionam parking
3. iOverlander (bom pra praias remotas e sítios arqueológicos)
4. Tripadvisor reviews últimos 12 meses (info de preço mais atual)

---

## Campo `fuelAlert` (em transit stops, flag booleano)

Marca se aquele trecho tem risco de ficar sem combustível.

```json
{
  "tipo": "transit",
  "nome": "Bavella → Porto Pollo",
  "cat": "~1h · SP368 montanha",
  "fuelAlert": true
}
```

**Quando marcar `fuelAlert: true`**:
- Próximo posto >40km pelo trajeto
- Região remota (interior, montanha) com poucos postos
- Ilha pequena (ex: San Pietro) onde postos fecham cedo

---

## Campo `pitStop` (em transit stops, flag booleano)

Marca paradas obrigatórias pra criança — NÃO é uma atração, é logística.

```json
{
  "hora": "09:45",
  "emoji": "🛑",
  "tipo": "transit",
  "nome": "Parada · área de repouso SS292",
  "cat": "~10min · esticar pernas + WC",
  "pitStop": true,
  "coord": {"lat": 40.0800, "lng": 8.4600}
}
```

**Critérios**: inserir automaticamente se trecho >45min sem parada com criança <5 anos.
Ver `family-driving.md` pra como escolher boa parada.

---

## Como pesquisar `roadType` e `parking`

### Passo a passo pra transit stops:
1. Google Maps → traçar o trecho exato (origem → destino)
2. Observar o tracejado: laranja/vermelho = rodovia, verde = rota cênica
3. Zoom in pra ver curvas: muitas curvas próximas = montanha
4. Street View no meio do trecho confirma: mar ao lado = costeira; floresta de montanha = montanha

### Passo a passo pra card stops:
1. web_search: `"parking [nome do lugar] [cidade]"` → site oficial
2. web_search: `"[nome do lugar] parking price 2025"` → reviews recentes
3. Google Maps → busca o lugar → tab "Sobre" às vezes lista parking

---

## Tabela resumo · quando cada campo é obrigatório

| Campo | Obrigatório em | Opcional em |
|---|---|---|
| `roadType` | Todos transit de carro >15min | Não aplicável |
| `parking` | Praias remotas, sítios arqueológicos, parques naturais | Cidades com parking urbano geral |
| `fuelAlert` | Regiões remotas, ilhas, montanha | Rotas urbanas com postos regulares |
| `pitStop` | Trechos >45min com criança <5 anos | Trechos curtos |
