# Design Tokens · Itinerary Builder

Tokens visuais extraídos do gold standard (NYC Jul/2026). Devem ser preservados entre viagens — UX testada em campo.

---

## Type scale

| Tier | Tamanho | Peso | Letter-spacing | Uso |
|---|---|---|---|---|
| H1 | 22px | 700 | -0.3px | Título principal do app |
| H2 | 19px | 700 | -0.2px | Headers de seção |
| Card title | 16px | 700 | -0.2px | Nome do stop principal |
| Label | 14px | 600 | — | Nav, buttons, meta |
| Body | 14px | 400 | — | Conteúdo |
| Small | 12px | 600 | — | Meta, tabs, timestamps |
| Tiny | 10px | 700 | — | Badges, uppercase labels |

---

## Spacing grid (múltiplos de 4px)

```
Padding containers:  12px · 14px · 16px · 18px
Gaps flex:           4px · 6px · 8px · 10px · 14px
Margins blocks:      10px · 12px · 14px · 18px
Border-radius:       4px (button) · 8px (card) · 12px (container) · 50% (round)
```

---

## Paleta neutra (Tailwind base)

```
#f3f4f6  bg page
#fff     card bg
#fafafa  opcoes bg
#f9fafb  hover subtle
#e5e7eb  borders, dividers
#d1d5db  secondary borders
#9ca3af  placeholder, tertiary text
#6b7280  secondary text, labels
#374151  tertiary text
#111827  primary text · headlines
#0f172a  dark background · buttons
#1e293b  dark hover
```

---

## Paleta accent (cores por dia · HSL distribution)

Cada dia tem uma cor única, gerada via HSL spread: `hue = (i / n) * 360` onde `i` é o índice do dia e `n` o total. Cada dia ganha 3 variações:

```js
function generateDayColors(n) {
  return Array.from({length: n}, (_, i) => {
    const hue = Math.round((i / n) * 360);
    return {
      cor:   `hsl(${hue}, 70%, 50%)`,   // tab active, borda card
      gradA: `hsl(${hue}, 70%, 30%)`,   // gradient banner topo (dark)
      gradB: `hsl(${hue}, 70%, 55%)`,   // gradient banner fundo (light)
    };
  });
}
```

**Cores acentuadas (referência · podem ser substituídas pela HSL spread):**

```
red    #dc2626 (#991b1b dark, #7f1d1d darker)
orange #d97706 (#b45309 dark)
amber  #f59e0b (#92400e dark)
green  #10b981 (#047857 dark)
teal   #0d9488 (#0f766e dark, #134e4a darker)
blue   #3b82f6 (#1e40af dark)
purple #8b5cf6 (#6366f1 companion)
pink   #ec4899 (#be185d dark)
indigo #6366f1 (#4338ca dark)
```

**Cor especial pra walking tour flag**: gradient `#6366f1 → #8b5cf6` (linear 135°).

---

## CSS custom properties (inline no day-tab e card)

```css
--day-color: #dc2626;    /* cor única do dia */
--day-grad-a: #7f1d1d;   /* gradient topo */
--day-grad-b: #991b1b;   /* gradient fundo */
```

Aplicadas inline pelo `renderDay()`.

---

## Risk pills (3 níveis)

```css
.risk-green  { background:#d1fae5; color:#065f46; } /* 🟢 tranquilo */
.risk-yellow { background:#fef3c7; color:#92400e; } /* ⚠️ atenção */
.risk-red    { background:#fee2e2; color:#991b1b; } /* 🔴 alta atenção */
```

Critérios:
- **green**: sem ressalvas · família-friendly · clima previsível
- **yellow**: calor extremo, multidão, longa caminhada sem sombra, cobblestone, escadas evitáveis
- **red**: vias de tráfego pesado, área noturna duvidosa, escadas obrigatórias com carrinho, multidão extrema (fogos, eventos)

---

## Reserva badges (estado)

```css
.reserva-badge.pending { background:#fef3c7; color:#92400e; }  /* ☐ RESERVAR */
.reserva-badge.ok      { background:#d1fae5; color:#065f46; }  /* ☑ FEITO */
```

Toggle on click · persist em `localStorage[\`reserva-${stop.nome}\`]`.

---

## Mobile · safe-area

Padding extra pra notch/dynamic island do iPhone:

```css
body {
  padding-top:    env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
}
```

Viewport meta: `width=device-width, initial-scale=1.0, viewport-fit=cover, maximum-scale=1.0`.

---

## Popups Leaflet · contrast hack

Popups do mapa Leaflet têm CSS global que sobrescreve cores. Pra garantir link branco em fundo colorido, usar `!important`:

```css
.pp-link {
  color: #fff !important;
  text-decoration: none !important;
}
```

Justificado: popups são escopo isolado, `!important` não cascateia pro app.
