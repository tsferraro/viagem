# Coord Validation · Regras Estritas

## Regra de ouro

**NUNCA inventar coordenadas baseado em "perto de X"**. Sempre web_search ou marcar `coord_unverified: true`.

## Pipeline de validação

```
1. web_search "<nome do stop> <endereço se houver> <cidade>"
2. Extrair coord da página oficial OU de fonte confiável (Google Maps, Wikipedia)
3. Validar range:
   - lat ∈ [-90, 90]
   - lng ∈ [-180, 180]
4. Validar plausibilidade:
   - coord faz sentido pro bairro/cidade?
   - distância pra outros stops do tour é coerente?
5. Se confiança alta: salvar com 4 casas decimais
6. Se baseado em estimativa: marcar metadata
```

## Schema de coord

### Simples (default)

```json
{
  "coord": { "lat": 38.7099, "lng": -9.1334 }
}
```

### Com metadata (se unverified ou source explícito)

```json
{
  "coord": {
    "lat": 38.7099,
    "lng": -9.1334,
    "metadata": {
      "verified": true,
      "source": "web_search",
      "date_checked": "2026-08-05"
    }
  }
}
```

`source` pode ser:
- `"web_search"` — extraído de busca oficial
- `"google_maps"` — coord copiada do Google Maps direto
- `"user_provided"` — usuário forneceu
- `"estimated"` — chute baseado em descrição (sinaliza unverified)

## Marker `coord_unverified`

Se a coord é estimativa (não passou pelo web_search ou fonte não-oficial):

```json
{
  "coord": {
    "lat": 38.71,
    "lng": -9.13,
    "metadata": { "verified": false, "source": "estimated" }
  }
}
```

A skill itinerary-builder vai destacar essas coords no validate.py pra usuário corrigir.

## Parens no nome (lição crítica)

Manter endereço entre parens no campo `nome`:

```json
{ "n": 1, "nome": "Caffe Reggio (119 MacDougal)", "coord": {...} }
```

Por quê:
- `getMapsUrl()` na itinerary-builder remove SÓ os parens da query (mantém conteúdo): `"Caffe Reggio 119 MacDougal"` → Google Maps acha
- Usuário vê endereço no display
- Backup pra caso coord esteja ligeiramente errada

**Anti-padrão**: `"nome": "Caffe Reggio"` (sem endereço) · Maps confunde com outras lojas com mesmo nome

## Precisão recomendada

- 4 casas decimais (~10m precision)
- 5+ casas só se for ponto crítico (entrada exata de prédio)
- 3 casas = ~100m (aceitável pra bairro grande, ruim pra stop específico)

## Plausibilidade

Antes de salvar, checar:
- Coord do stop 1 e stop 2 do tour estão a menos de 500m entre si?
- Coord está dentro do bairro pretendido (visual no Google Maps)?
- Se WT total tem 6 stops, distância acumulada está em ~1-2km?

## Range checks (no validate.py do itinerary-builder)

```python
for lat_str, lng_str in coords:
    lat, lng = float(lat_str), float(lng_str)
    if not (-90 <= lat <= 90):
        err(f"lat {lat} fora de [-90, 90]")
    if not (-180 <= lng <= 180):
        err(f"lng {lng} fora de [-180, 180]")
```

`validate.py` bloqueia deploy se coord inválida.

## Erros comuns a evitar

| Erro | Sintoma | Fix |
|---|---|---|
| Lat e lng trocados | Stop fica no meio do oceano | Sempre web_search confirma |
| Sinal trocado (-/+) | Stop fica no hemisfério errado | Range check pega |
| Coord do café com nome similar em outra cidade | Stop no lugar errado | Endereço entre parens evita |
| Precisão 1-2 casas | Stop a 1km do real | Mínimo 4 casas |
