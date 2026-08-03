# HANDOFF · Bugs do app reportados em campo (Córsega, ago/2026)

Reportados pelo Tobia **usando o app em viagem**. Todos confirmados no código.
Corrigir em `templates/render-functions.js` (beneficia todas as viagens) e **rebuildar
todos os `index.html`** — a correção não chega sozinha nos apps já gerados.

---

## 🔴 P0 · "New York, NY" hardcoded — quebra o app fora de NY

**Dois pontos**, os dois ignorando o global `MAPS_REGION` que já existe no template:

| Linha | Código | Efeito |
|---|---|---|
| ~315 | ``destStr+', New York, NY'`` em `renderTransit` | Botão **🚇 Transporte público** busca "Praia de Rondinara, New York, NY" |
| ~138 | ``clean+' New York'`` no fallback de `getMapsUrl` | Stops **sem coord** são buscados em Nova York |

**Fix**: trocar os dois por `MAPS_REGION` (com fallback pra string vazia se indefinido).
Foi o que o Tobia descreveu como *"alguns dão pau por erro de não colocar o local correto"*.

**Está quebrado agora, em produção, na Córsega.**

---

## 🔴 P1 · "Copiar endereço" copia o NOME, não o endereço

`renderTransit` linha ~314: `destAttr = destStr`, onde `destStr = dest || stop.nome` e `dest`
vem de `getNextDest()`, que devolve o **`nome`** do próximo stop.

Resultado: copia `"Praia de Rondinara · baía em concha"` — descrição em português, não endereço.
Colar isso em qualquer app de navegação não resolve nada.

**Fix (escolher um)**:
- (a) Novo campo opcional `endereco` no stop; o botão copia `endereco || nome`
- (b) Copiar a **coordenada** (`lat,lng`), que é universalmente colável e sempre correta
- (c) Renomear o botão para "Copiar destino" e assumir o nome

Recomendo **(b) como default + (a) quando houver endereço**: coord nunca falha e é o que
realmente se cola num GPS.

---

## 🟡 P1 · Rótulos de transporte hardcoded ("Uber")

`renderTransit` linha ~316: `<strong>🚕 Uber</strong>`. As chaves do `transit_map` são fixas
(`uber` / `metro` / `ferry`) e os rótulos, hardcoded.

Em viagem de **carro próprio** o campo foi preenchido com `"Carro próprio · ~40min"` e a tela
renderiza **"🚕 Uber Carro próprio · ~40min"**. Sem sentido.

Culpa dividida: o template por hardcodar rótulo, e eu por enfiar informação de carro numa chave
chamada `uber`.

**Fix**: schema de `transit_map` passa a aceitar lista de opções com rótulo próprio —
`[{modo:"carro", emoji:"🚗", label:"Carro próprio", texto:"~40min pela N196"}, …]`,
mantendo retrocompatibilidade com as 3 chaves antigas. Modos: `carro · uber · taxi · metro ·
onibus · ferry · trem · a-pe`.

---

## 🟡 P2 · Rota do dia perde pontos silenciosamente

`dirCoordUrl` (linha ~149): `MAXW=9` waypoints. Acima disso, **amostra** os intermediários por
interpolação e descarta o resto — sem avisar ninguém.

O limite é real (a URL API do Google Maps não aceita waypoints ilimitados), então o corte se
justifica; **o silêncio, não**. Foi o que o Tobia viu como *"alguns roteiros não vêm com todos
os pontos"*.

**Fix**: quando houver corte, mostrar aviso no botão ou ao lado
(*"rota com 9 de 13 pontos · Google Maps limita waypoints"*), e considerar partir em 2 links
(manhã / tarde) em vez de amostrar.

---

---

## 🔴 P0 · `getBairroForCoord` ignora o `BAIRROS_CONFIG` e usa caixas de NYC

`render-functions.js` linha ~604. A função tem **dez `if` com bounding boxes de bairros de Nova
York cravados** (Greenpoint, DUMBO, Midtown, Upper East Side…) e nunca lê o `BAIRROS_CONFIG`
que vem do `data.json`.

Consequência: na Córsega, **nenhuma** coordenada cai nas caixas de NY, então a aba de bairros
mostra tudo como `📍 Outros`. Os 9 bairros que foram cuidadosamente definidos no `data.json`
(Porto Pollo & Valinco, Sartène & Sul, Alta Rocca, Bonifacio Cidadela…) **não fazem
absolutamente nada**.

**Fix**: reescrever pra iterar `BAIRROS_CONFIG` (que já tem `latMin/latMax/lngMin/lngMax` e
`fallback:true`) e eliminar as caixas hardcoded.

Mesma raiz dos bugs de "New York": **valor da primeira viagem cristalizado no template**.

---

## Resíduos de NYC ainda no template (varredura feita)

```
render-functions.js:138   clean+' New York'                       → usar MAPS_REGION
render-functions.js:315   destStr+', New York, NY'                → usar MAPS_REGION
render-functions.js:604   getBairroForCoord()  10 caixas de NYC   → usar BAIRROS_CONFIG
render-functions.js:771   setView([40.75,-73.97],12)  fallback    → centrar no 1º POI da viagem
render-functions.js:836   setView([40.72,-73.95],12)  fallback    → idem
```

## Ação de classe

Os bugs 1 e 3 são o mesmo padrão: **valor específico de uma viagem (NYC) cristalizado no
template** durante a construção do primeiro roteiro. Antes de gerar a Sardenha, varrer o
template inteiro atrás de outros resíduos de NYC — `grep -n "New York\|NYC\|Manhattan\|Brooklyn"
templates/`.

## Ação pro `validate.py`

Adicionar check que **bloqueia** literal de cidade hardcoded fora de `MAPS_REGION` no HTML
gerado. Este é exatamente o tipo de erro que o validate existe pra pegar e não pegou.
