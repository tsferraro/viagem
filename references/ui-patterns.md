# UI Patterns · Itinerary Builder

Padrões de interface validados no NYC Jul/2026. Cada padrão tem o ESPÍRITO + o IMPLEMENT detail (regex/snippet) pra não perder lições.

---

## Soft re-render (lição #1)

**Espírito**: trocar dia NÃO deve refazer o rendering dos day-tabs. Só o conteúdo abaixo deles muda.

**Implement**:
- `render()` constrói TUDO (tabs + content) · só roda em troca de main-tab (guia ↔ mapa ↔ bairros)
- `renderInnerContent()` constrói SÓ o `#inner-content` · roda em troca de dia
- Event handler do day-tab faz toggle `.active` manual nos tabs + chama `renderInnerContent()` + `centerActiveTab()`

```js
function renderInnerContent() {
  const inner = document.getElementById('inner-content');
  if (state.view === 'guia')    inner.innerHTML = renderDay(DAYS[state.selIdx]);
  else if (state.view === 'mapa') inner.innerHTML = renderMap();
  bindCardHandlers();
}
```

**Benefício**: scroll horizontal dos day-tabs preservado · transição fluida.

---

## centerActiveTab (lição #2)

Após mudança de dia, scroll horizontal suave no container `.day-tabs` pra mantar o tab ativo visível:

```js
function centerActiveTab() {
  setTimeout(() => {
    const active = document.querySelector('.day-tab.active');
    if (active) active.scrollIntoView({
      behavior: 'smooth',
      inline: 'center',
      block: 'nearest'
    });
  }, 80);
}
```

`setTimeout 80ms` garante que DOM esteja atualizado antes do scroll.

---

## getMapsUrl · mantém endereço entre parens (lição #3)

**Espírito**: o NOME visível do stop pode ter endereço entre parens — "Apple (247 Bedford Ave)". Pra abrir no Google Maps, queremos buscar "Apple 247 Bedford Ave" (sem parens, mas com o endereço dentro).

**Implement**:
```js
function getMapsUrl(stop) {
  let queryName = stop.nome;
  // Para "opcoes": pega primeira alternativa (não o título genérico do grupo)
  if (stop.tipo === 'opcoes' && stop.opcoes?.length) {
    queryName = stop.opcoes[0].nome;
  }
  const clean = queryName
    .replace(/[()]/g, '')                          // remove SÓ os parens, mantém conteúdo
    .replace(/\s+/g, ' ')
    .trim();
  if (stop.coord) {
    return `https://www.google.com/maps/search/${encodeURIComponent(clean)}@${stop.coord.lat},${stop.coord.lng},17z`;
  }
  return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(clean)}`;
}
```

**Anti-padrão**: remover os parens E o conteúdo dentro deles (`stop.nome.replace(/\(.*?\)/g, '')`). Perde o endereço.

---

## getRouteUrl V1.3 · waypoints com coords puras

**Espírito**: walking route com múltiplos stops · Google Maps Directions API.

**V1.3 mudança**: waypoints são `lat,lng`, não nomes. Evita ambiguidade ("Apple Williamsburg" vs "Apple 5th Ave" — Google escolhia errado).

```js
function getRouteUrl(day) {
  const stops = day.stops.filter(s => s.tipo !== 'transit' && s.coord);
  if (!stops.length) return '#';
  if (stops.length === 1) return getMapsUrl(stops[0]);
  const coord = s => `${s.coord.lat},${s.coord.lng}`;
  const origin = coord(stops[0]);
  const dest = coord(stops[stops.length - 1]);
  const mid = stops.slice(1, -1).map(coord).join('|');
  let url = `https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${dest}&travelmode=walking`;
  if (mid) url += `&waypoints=${encodeURIComponent(mid)}`;
  return url;
}
```

---

## Card layout · expansível

```
┌─ Stop card (collapsed) ─────┐
│ ⏰ 11:30 · ☐ RESERVAR        │
│ 🚶 WALKING TOUR · 6 paradas  │
│ Nome do stop                 │
│ Categoria/endereço           │
└──────────────────────────────┘ ← click expande
↓
┌─ Stop card (expanded) ──────┐
│ [emoji grande]               │
│ Parágrafo "sobre"            │
│ ⭐ IMPERDÍVEL [highlight]    │
│ 💡 Dica 1                    │
│ 💡 Dica 2                    │
│ ⏱️ 45min · 💵 $30 · ♿ Ok    │
│ [🌐 official] [📰 review]    │
└──────────────────────────────┘
```

Toggle via `.stop-card.expanded` class + chevron `::after` rota 180°.

---

## Opcoes layout (3+ alternativas)

```
┌─ Opcoes block ──────────────┐
│ 🍽️ Almoço · Tribeca         │
├──────────────────────────────┤
│ 1️⃣ The Bagel Store           │
│    $5-9 · 15min a pé         │
│    Rainbow bagels icônicos   │
│ - - - - - - - - - - - - - -  │
│ 2️⃣ Bagel Pub                 │
│    $4-8 · 15min a pé         │
│ - - - - - - - - - - - - - -  │
│ 3️⃣ Eberle Bakery             │
│    $4-7 · 5min a pé          │
└──────────────────────────────┘
```

Dashed border · `background:#fafafa` · items separados por dashed divider.

---

## Transit collapsible

```
┌─ Transit (collapsed) ───── ▼
│ ⛴️ 22:30 NYC Ferry           │
│ India St → Pier 11 · ~15min  │
└──────────────────────────────┘ ← click expande
↓
┌─ Transit (expanded) ─────────
│ ⛴️ FERRY [East River] India St → Wall St · 15min · $4
│ 🚇 METRÔ [G] Greenpoint Av → ... · 35min · $2.90
│ 🚕 UBER ~$15-18 · 12min · backup
└──────────────────────────────
```

Chevron rota 180° em expanded. Background `#f3f4f6`. Só mostra rotas que existem em `TRANSIT_MAP`.

---

## Search hay strings

Build em runtime, busca via `.includes()`:

```js
let hay = `${s.nome} ${s.cat || ''} ${s.sobre || ''} ${d.bairro} ${d.tema}`;
if (s.walkingTours?.length > 0) {
  hay += ' walking tour ';
  s.walkingTours.forEach(t => {
    hay += t.nome + ' ' + (t.descricao || '') + ' ';
    t.stops.forEach(p => hay += p.nome + ' ');
  });
}
if (s.dicas) hay += ' ' + s.dicas.join(' ');
```

**Importante**: WT nomes + stops devem ir na hay, senão busca "walking tour" não funciona.

---

## Day-tab com cor única

```html
<button class="day-tab active" data-idx="0" style="--day-color:#dc2626">
  <span class="dt-date">Sex 3</span>
  Chegada
  <span class="dt-grupo">👥</span>  <!-- só se day.grupo === true -->
</button>
```

```css
.day-tab.active {
  background: var(--day-color, #0f172a);
  color: #fff;
  border-color: var(--day-color);
}
```

---

## Reserva checkbox interativo

```js
const isDone = localStorage.getItem(`reserva-${stop.nome}`) === 'done';
const badge = `<button class="reserva-badge ${isDone ? 'ok' : 'pending'}"
  data-reserva="${stop.nome.replace(/"/g, '&quot;')}" title="Clique pra alternar">
  ${isDone ? '☑ FEITO' : '☐ RESERVAR'}
</button>`;
```

**XSS protection**: `.replace(/"/g, '&quot;')` em `data-reserva` (nomes podem ter aspas).

**Bind handler** (em `bindCardHandlers()`):
```js
document.querySelectorAll('.reserva-badge').forEach(b => {
  b.addEventListener('click', e => {
    e.stopPropagation();
    const key = `reserva-${b.dataset.reserva}`;
    const isDone = localStorage.getItem(key) === 'done';
    localStorage.setItem(key, isDone ? 'pending' : 'done');
    b.classList.toggle('ok', !isDone);
    b.classList.toggle('pending', isDone);
    b.textContent = isDone ? '☐ RESERVAR' : '☑ FEITO';
  });
});
```

---

## Walking-tour-flag (visual)

```html
<div class="walking-tour-flag">
  🚶 WALKING TOUR · 1 parte · 6 paradas
</div>
```

```css
.walking-tour-flag {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 4px;
}
```

Sempre dentro do card-âncora · acima do nome do stop · clique no card expande WT inline.

---

## Popup contrast (Leaflet)

Popups Leaflet têm CSS isolado mas links levam estilo browser default (roxos). Use `!important`:

```css
.pp-link {
  color: #fff !important;
  text-decoration: none !important;
}
```

---

## Auto-abrir dia de hoje

```js
function getDefaultDayIdx() {
  const today = new Date().toISOString().split('T')[0];  // YYYY-MM-DD
  const dayIdx = DAYS.findIndex(d => parseDateString(d.date) === today);
  return dayIdx >= 0 ? dayIdx : 0;
}

const state = { view:'guia', selIdx: getDefaultDayIdx(), search:'', expandStop:null };
```

**Anti-padrão**: hardcode `selIdx: 1`. Em produção, durante a viagem, app abre no dia errado.

---

## localStorage keys (3 chaves)

| Key | Valor | Propósito |
|---|---|---|
| `roteiro_auth_v1` | `'1'` | Auth gate · auto-login |
| `reserva-${stop.nome}` | `'done'\|'pending'` | Checkbox de reserva |
| `legendRead` | `'1'\|'0'` | Footer legend collapsed? |

Todas envoltas em `try/catch` pra silenciar quota exceeded ou private mode.

## ★ do Resumo · a atração do dia sai do `valeAPena` (2026-08-04)

A linha `★` de cada dia, no Resumo (`renderOverview`, filtro `roteiro`), promete **a atração
principal do dia**. O código pegava `cards[0]` — o primeiro card do array, que é o mais cedo.

Isso quase nunca é a atração. Em 7 dos 16 dias do roteiro dos pais, o primeiro card era
logística: `Check-out + saída cedo`, `Café da manhã + check-out`, `Despedida do Tobia`. O Tobia
percebeu de imediato e perguntou o que a estrela significava — porque, olhando a tela, não
significava nada.

```js
// errado: primeiro do array
const main = cards.length ? cards[0].nome : '—';

// certo: eixo de recompensa, empate resolvido pela ordem (o mais cedo)
const main = cards.length
  ? cards.reduce((a,b)=>((b.valeAPena||0)>(a.valeAPena||0)?b:a)).nome
  : '—';
```

**A lição geral**: quando um rótulo promete *julgamento* ("a atração", "o destaque"), ele tem
que ler o campo de julgamento. `valeAPena` existe exatamente pra isso — usar posição no array
como proxy de importância é o mesmo erro de fingir o eixo com ⭐ digitada à mão na prosa.

`validate.py` guarda a assinatura na lista de features-chave (`★ do Resumo usa valeAPena`).
