# Rubrica de Design · avaliação de interface dos roteiros

Régua **repetível** pra avaliar (e elevar) o design/UI de qualquer roteiro. Complementa — não substitui — a rubrica de conteúdo (escrita, links, walking tours). Nasceu do redesign NYC (2026-07-01), avaliado com a skill **impeccable**.

## Ferramenta: skill `impeccable` (embarcada no repo)

Vive em `skills/impeccable/` (Apache 2.0). É runnable pra ajustar/gerar design ou reavaliar um roteiro.

| Uso | Como |
|---|---|
| Avaliar UI (nota + achados) | `node skills/impeccable/scripts/detect.mjs --json <arquivo.html>` (detector determinístico · 0 = limpo) + review heurístico manual (ver §critérios) |
| Ler os critérios profundos | `skills/impeccable/reference/product.md` (register de app/tool) + `critique.md` (heurísticas + carga cognitiva + personas) |
| Comandos (craft/critique/polish/…) | `skills/impeccable/SKILL.md` |

**Register correto pros roteiros = `product`** (o design SERVE a tarefa de campo; não é o produto). Barra: *familiaridade merecida · a ferramenta desaparece na tarefa*.

## Pipeline de QA visual (essencial · descoberto no redesign NYC)

O ambiente tem **Chromium + Playwright** → dá pra **renderizar o HTML local e tirar screenshot real**, mesmo "às cegas". Isso é o que permitiu iterar design com qualidade.

```bash
# helper (bypassa o auth gate via localStorage; viewport mobile 390px)
GROOT=$(npm root -g) node <helper>/shot.js "<abs .html>" "<out>.png" mobile
```
Depois `Read` o PNG. Pra estados (card expandido, tab, feito) → clonar o helper e `page.click(...)` antes do shot. **Iterar ≥3 rodadas: render → screenshot → ver → ajustar.** (O Leaflet/CDN é bloqueado offline → aba Mapa renderiza em branco no screenshot; ignorar.)

## Contexto de uso (o que define "excelente" AQUI)

Roteiro é usado **no campo, uma mão, no sol, com criança de 3 anos** — não é dashboard de mesa.

| Critério | Padrão |
|---|---|
| Legibilidade no sol | Contraste real (≥4.5:1 corpo · ≥3:1 grande · placeholder 4.5:1). Cinza-claro "elegante" = ilegível |
| Uma mão | Ação principal no alcance do polegar (**bottom bar**) · alvos ≥44px |
| Scan em 2s | "onde estou / o que é agora / quanto custa / é longe" sem expandir |
| Offline | Essencial (horário, endereço, dica) não depende de rede |
| Criança 3a 1ª classe | Carrinho/escada/sombra/banheiro visíveis |

## Heurísticas de Nielsen (0-4 · honesto · 4 = genuinamente excelente)

Maioria das interfaces reais tira 20-32/40. Bandas: 36-40 Excellent · 28-35 Good · 20-27 Aceitável · <20 Ruim.

| # | Heurística | O que checar no roteiro |
|---|---|---|
| 1 | Status do sistema | dia de hoje auto-aberto · "AGORA" em tempo real · reserva/feito mudam à vista |
| 2 | Mundo real | manhã/tarde/noite · €/$ · "15min a pé" · sem jargão |
| 3 | Controle & liberdade | desfazer (↺) · fechar/colapsar óbvio · nada prende |
| 4 | Consistência | mesmo card/botão/ícone em toda tela |
| 5 | Prevenção de erro | ações reversíveis · smart defaults · link nunca erra o lugar |
| 6 | Reconhecer > lembrar | 1ª parada acima da dobra · "A fazer" mostra o que falta |
| 7 | Flexibilidade | busca · date-strip · filtros · atalhos que não atrapalham o novato |
| 8 | Estético/minimal | cada elemento ganha o pixel · sem decoração que não informa |
| 9 | Recuperação de erro | empty states que ensinam · mensagens em linguagem simples |
| 10 | Ajuda | legenda/avisos contextuais · hint de 1º uso no momento certo |

## Bans absolutos de IA (match-and-refuse · o detector pega vários)

1. **Side-stripe** (`border-left/right` >1px colorido decorativo) → fundo tint + ícone, ou **função** (ex: o check "feito" na borda vira toggle → deixa de ser decoração)
2. **Hero-metric** (número grande + label + stats + gradiente = clichê SaaS) → status compacto/acionável
3. **Gradient text** (`background-clip:text`) · **Glassmorphism decorativo** · **grids de card idênticos**
4. **Eyebrow uppercase** em toda seção · **markers numerados 01/02/03** como scaffolding
5. **Colored glow on dark** (box-shadow colorido em fundo escuro) → sombra neutra
6. **Animar propriedades de layout** (width/height/max-height) → `transform`/`grid-template-rows`

## Registro · redesign NYC (2026-07-01)

- Trend impeccable (heurística): **Bold 31 → Evolução 33 → Híbrido v1 36 → v2/v3 38/40**. Detector: **0 antipadrões**.
- Vencedor = **Híbrido** (bottom bar · topbar Resumo+Lupa · status compacto data-real + stats acionáveis · check "feito" → "Feitas hoje" · AGORA tempo real · Resumo Roteiro/A-fazer/Feito · rotas por coord [V1.3] · transporte com copiar-endereço + transporte-público · walking tour em cor distinta).
- Sandboxes de comparação: `nyc-lab-bold/`, `nyc-lab-evo/`, `nyc-lab-hibrido/` (reservados na landing).

## Modos de template (2 · separados)

- **Viagem datada**: date-strip · "X/11 dias" · AGORA · stats de viagem.
- **Coletânea de cidade** (Paris/Marais · sem datas · abas-por-tema): **sem** date-strip/stats/AGORA · mantém tabs/cards/feito. Aplicar o design "a todos" respeita esse modo.
