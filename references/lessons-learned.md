# Lessons Learned — Roteiro NYC Jul 2026

Decisões tomadas durante a construção iterativa do app de roteiro NYC, com o motivo de cada uma.
Servir de referência pro arquiteto que vai destilar essas decisões na skill `itinerary-builder`.

---

## 1. ARQUITETURA & RENDERIZAÇÃO

### 1.1 Soft re-render no day switch (não rebuildar tabs)
**Decisão**: separar `render()` (full) de `renderInnerContent()` (só conteúdo do dia).  
**Motivo**: Switching de dia rebuildava 11 tabs + 10+ cards + rebindava 30+ event listeners → lag perceptível no swipe.  
**Implementação**: `renderInnerContent` só atualiza `#inner-content`. Click no day-tab toggla `.active` e chama `renderInnerContent` (não `render`).  
**Anti-padrão**: chamar `render()` em todo state change.

### 1.2 Event delegation com flag `__bound`
**Decisão**: prevenir bind duplicado via `if(c.__bound) return; c.__bound=true`.  
**Motivo**: re-renders parciais podiam re-bindar handlers → click disparava 2x.  
**Implementação**: cada handler verifica `__bound` antes de attach.

### 1.3 `centerActiveTab()` com setTimeout(80ms)
**Decisão**: scrollIntoView com `inline:'center'` após pequeno delay.  
**Motivo**: DOM precisa estabilizar antes do scroll calcular posições corretas.  
**Implementação**: chamada em todo state change que muda active tab.

### 1.4 Auto-abrir dia de hoje
**Decisão**: `getDefaultDayIdx()` no state init, NÃO hardcode `selIdx:1`.  
**Motivo**: durante a viagem, o app deve abrir no dia atual automaticamente.  
**Implementação**: parse `DAYS[i].date` ("Sex 3/Jul") → comparar com `new Date().toISOString().split('T')[0]`. Fallback: dia 0.

---

## 2. UX & DESIGN

### 2.1 Sticky nav com search + overview + main-tabs
**Decisão**: search bar + botão overview + 3 main-tabs sempre visíveis no topo.  
**Motivo**: navegação rápida sem scroll.  
**Implementação**: `position:sticky` com `top:0` + backdrop-blur.

### 2.2 Day tabs com fade gradient nas bordas
**Decisão**: pseudo-elementos `::before` (esquerda) e `::after` (direita) com gradient pra `#f3f4f6`.  
**Motivo**: indicar visualmente que tem mais tabs pra rolar.  
**Implementação**: `pointer-events:none` pra não bloquear scroll touch.

### 2.3 Cards colapsáveis (incluindo transit)
**Decisão**: todos cards/opcoes/transit-com-rotas começam colapsados, expandem on click.  
**Motivo**: roteiros longos viram parede de texto. Colapsado mostra essencial (hora, nome, cat).  
**Implementação**: classe `.expanded` toggla via JS. Transit só é colapsável se tiver rotas detalhadas.

### 2.4 Walking-tour-flag visível + indexado em busca
**Decisão**: badge "🚶 WALKING TOUR · X paradas" entre hora e título.  
**Motivo**: usuário pediu pra encontrar walking tours na busca + ver no card que tem tour.  
**Implementação**: 
- Renderiza `<div class="walking-tour-flag">` se card tem `walkingTours[]`
- Search hay inclui: "walking tour" + tour names + stop names
- Tag em resultados de busca

### 2.5 Risk pills (🟢 ⚠️ 🔴)
**Decisão**: cada card tem `risco: 'green'|'yellow'|'red'` traduzido em "tranquilo/atenção/alta atenção".  
**Motivo**: pra família com criança pequena, sinalizar lugares que exigem mais cuidado (lotação, multidão, escadas).  
**Implementação**: pill colorida no `.stop-cat`.

### 2.6 Reserva como checkbox interativo
**Decisão**: badge clicável `☐ RESERVAR` / `☑ FEITO` com localStorage persist.  
**Motivo**: tracking de reservas durante o planejamento.  
**Implementação**: `localStorage[\`reserva-${nome}\`]` = 'done'|'pending'. Default vem de `stop.reserva`.

### 2.7 Tema curto pros day tabs
**Decisão**: campo `temaCurto` (3-15 chars) pra day tabs, `tema` (longer) pro banner.  
**Motivo**: "Manhattan iconic em família" não cabia no tab — tabs adjacentes ficavam invisíveis.  
**Implementação**: tab usa `d.temaCurto || d.tema.split('·')[0].trim()`.

### 2.8 Senha persistente
**Decisão**: localStorage `AUTH_KEY='roteiro_auth_v1'`. Auto-login se já autenticou.  
**Motivo**: usuário pediu — toda visita ele tinha que redigitar.  
**Implementação**: check no `DOMContentLoaded`. NÃO no script inline do topo (DAYS pode não estar carregado).

### 2.9 Group dot (👥) nos dias com família estendida
**Decisão**: laranja `👥` no canto do day tab quando `d.grupo === true`.  
**Motivo**: distinguir dias só-casal vs dias com família estendida.

---

## 3. WALKING TOURS

### 3.1 Tipos de walking tour
Identificados 3 tipos:
- **Descoberta pura** (DUMBO, Wall St, Greenwich Village): bairro novo, alto valor
- **Annotations** (High Line): pontos curados ao longo de caminho já planejado
- **Híbrido temático**: bairro grande em 2+ partes por tema (GV: Bohemian + Stonewall)

### 3.2 Rubrica de valor explícita
Walking tour com **partition em partes** se > 8 stops. Ex: Greenwich Village = Parte 1 (6) + Parte 2 (6).

### 3.3 Visual diferenciado por parte no mapa
**Decisão**: Parte 1 marcadores cheios + dashArray '4,5'. Parte 2 contorno + dashArray '2,6'.  
**Motivo**: distinguir partes visualmente sem usar cores diferentes (mantém identidade do dia).

### 3.4 Coords sempre verificadas (web search)
**Anti-padrão observado**: Northern Dispensary 165 Waverly Pl (suposição) → usuário corrigiu pra 152.  
**Regra**: web_search antes de usar coord. Marcar `coord_unverified: true` se baseado em estimativa, prompta usuário.

### 3.5 Manter endereço entre parens no nome
**Decisão**: stop name = "Caffe Reggio (119 MacDougal)" — paren content fica.  
**Motivo**: ajuda Google Maps a buscar por nome+endereço junto. Sem o endereço, "Bob Dylan's apartment" sozinho não acharia nada.  
**Implementação**: `cleanForSearch` remove só os chars `()`, mantém conteúdo: `replace(/[()]/g,'').replace(/\s+/g,' ').trim()`.

### 3.6 Opcoes Maps URL usa primeira opção
**Decisão**: pra `tipo:'opcoes'`, `getMapsUrl` usa `opcoes[0].nome` (não o nome genérico).  
**Motivo**: "Café da manhã · Bagel" buscava genericamente → 3+ resultados. "Peter Pan Donut" busca específico.  
**Implementação**:  
```js
if(stop.tipo==='opcoes' && stop.opcoes?.length>0) {
  queryName = stop.opcoes[0].nome;
}
```

### 3.7 getRouteUrl formato V1.3 (coords puras, não nomes)
**Decisão**: `?api=1&origin=lat,lng&destination=lat,lng&waypoints=lat,lng|lat,lng&travelmode=walking`.  
**Motivo**: Google Maps trata nomes nos waypoints de forma errática. Coords puras são determinísticas.

### 3.8 Popup contrast forçado branco
**Decisão**: `.pp-link { color:#fff !important; text-decoration:none !important; text-shadow:0 1px 1px rgba(0,0,0,0.2) }`.  
**Motivo**: Leaflet sobrescrevia color do link → ficava azul sobre vermelho. Override com `!important` foi a única solução.

---

## 4. MAPA & GEOLOCAL

### 4.1 Polyline tracejada na cor do dia
**Decisão**: rota principal `dashArray:'6,8'` weight 3, walking tour `dashArray:'4,5'` weight 2.5.  
**Motivo**: distinguir hierarquia visual sem confundir.

### 4.2 fitBounds inclui sub-paradas de walking tour
**Decisão**: bounds calculado com `[...mainLatLngs, ...walkingTourLatLngs]`.  
**Motivo**: mapa precisa enquadrar TUDO, não só stops principais.

### 4.3 Bairros canônicos (não dinâmicos)
**Decisão**: 7 bairros hardcoded em `getBairroForCoord(lat,lng)` com ranges.  
**Motivo**: precisão > flexibilidade. Bairros NYC têm fronteiras conhecidas.  
**Anti-padrão**: depender de reverse geocoding (API rate limits, inconsistente).

---

## 5. CONTEÚDO & CURADORIA

### 5.1 Honestidade crítica sobre atrações
**Decisão**: dicas podem dizer "lotado de turista" ou "pula sem culpa" (ex: Magnolia Bakery).  
**Motivo**: usuário explicitamente pediu "consultor crítico, nunca concorde por educação" nas preferences.

### 5.2 Curiosidades históricas/culturais > facts genéricos
**Padrão**: cada stop tem 1-2 fatos não-óbvios.  
**Ex**: "Caffe Reggio · primeira cafeteria EUA a servir cappuccino (1927)" > "cafeteria popular".

### 5.3 Hidden gems sempre marcados
**Decisão**: prefixo 🔍 nos dicas + parada marcada como hidden gem.  
**Ex**: Patchin Place, AIDS Memorial, Northern Dispensary, 26th St viewing spur.

### 5.4 Imperdível separado de dicas
**Decisão**: campo `imperdivel` (uma linha) separado de `dicas[]` (lista).  
**Motivo**: o "se você só fizer uma coisa, faça X" merece destaque visual.

### 5.5 Dicas numeradas pra walking tour
**Decisão**: dicas usam `1️⃣ 2️⃣ ... 1️⃣1️⃣ 1️⃣2️⃣` (emoji-numbers).  
**Motivo**: replica visualmente o que aparece no mapa.

---

## 6. ANTI-PATTERNS OBSERVADOS

### 6.1 NÃO patronizar metrô
**Original**: avisos sobre "G train não tem elevador, panic!"  
**Correto**: usuário mora em Paris, sabe. Mencionar 1x no início (legenda), não em cada transit.

### 6.2 NÃO duplicar botão Maps
**Original**: botão "Abrir Maps" no card (Guia) E no popup (Mapa).  
**Correto**: só no popup. Card é content, mapa é geo.

### 6.3 NÃO inferir silenciosamente
**Original**: assumi que Northern Dispensary era 165 Waverly Pl.  
**Correto**: marcar como needs-verification + perguntar.

### 6.4 NÃO criar dia tabs com nome longo demais
**Original**: "Manhattan iconic em família" (27 chars).  
**Correto**: `temaCurto` com 3-15 chars.

### 6.5 NÃO usar tema genérico tipo "Dinossauros"
**Original**: tema "Dinossauros" pro dia AMNH.  
**Correto**: usar bairro ou atração principal ("AMNH · Museu de História Natural").

### 6.6 NÃO esconder reservas em rodapé separado
**Original**: caixa "⚠️ Reservas necessárias" no rodapé com lista.  
**Correto**: badge no próprio card (RESERVAR/FEITO), redundância é confusa.

### 6.7 NÃO esquecer de validar antes de commit
**Anti-padrão**: bugs JS que só aparecem em runtime.  
**Correto**: `node --check` em todo `<script>` antes de salvar.

---

## 7. INTERAÇÃO IDEAL

### 7.1 Big picture antes do detalhe
Sempre começar resposta com tabela/síntese, depois aprofundar.

### 7.2 Delta antes de version final em refactors
🟢 Adicionado · 🔵 Modificado · 🔴 Removido antes de mostrar código.

### 7.3 Tabelas > prosa densa
Pra status, comparações, planos, especificações.

### 7.4 Bold em palavras-chave
Não jogar palavras-chave aleatórias em bold. Só onde guia o olho do leitor.

### 7.5 Código sempre em bloco
Comandos, fórmulas, JSON, configs.

### 7.6 Não pedir desculpa por longas mudanças
Usuário valoriza ação > apologetic preamble.

### 7.7 Propor com nota de valor + esperar decisão
Pra features ambíguas (ex: High Line WT vale a pena?). Nunca decidir sozinho em pontos críticos.

---

## 8. DEPLOY & VERSIONING

### 8.1 Single-file HTML
**Decisão**: tudo em `index.html` (~131KB final).  
**Motivo**: GitHub Pages serve direto, zero build step, deploy = push.

### 8.2 Backups antes de mudanças grandes
**Padrão**: `cp index.html backups/index_$(date +%Y%m%d_%H%M%S).html`.

### 8.3 Mensagens de commit estruturadas
- `feat:` nova feature
- `fix:` bug fix
- `content:` enriquecimento de dados
- `refactor:` mudança estrutural sem nova feature
- `style:` só visual/CSS

### 8.4 Push direto pra main
**Decisão**: sem PR flow, sem branches.  
**Motivo**: usuário solo, GitHub Pages serve main, simplicidade > governance.
