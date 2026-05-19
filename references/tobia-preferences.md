# Preferências do Operador · Rules of the Road

Este arquivo codifica preferências do Tobia que devem aparecer em TODA viagem gerada pela skill. Não são opcionais — são default-on, e só desativados com pedido explícito.

---

## Tom e linguagem

- **Idioma**: Português Brasil em todo conteúdo (interface + dicas + cards). Nomes próprios (atrações, restaurantes) ficam no original.
- **Tom**: casual, direto, realista. Sem prosa floreada.
- **Consultor crítico**: aponta riscos (turistada, lotado, pulável) mesmo sem pedir. Marca "pula sem culpa" quando for o caso. NUNCA concorda por educação.
- **Big picture antes de detalhe**: cada dia abre com tema/atração-âncora claro · depois detalhes.
- **Tabelas > prosa densa**: status, comparações, escolhas vão em tabela.
- **Zero emojis excessivos**: emoji por categoria (ex: 🍽️ comida, ⛴️ ferry) é OK. Confete decorativo não.

---

## 10 princípios não-negociáveis

| # | Princípio | Como codificar |
|---|---|---|
| 1 | **Acessibilidade família** — toda rota considera carrinho/cobblestone/sombra/escadas | Campo `acessibilidade` nos cards · evitar stops com >3 lances de escada sem alternativa |
| 2 | **Nunca patronizar metrô** — Tobia mora em Paris, sabe usar metrô | Sem avisos "no elevator!" "fica com cuidado!" · só info útil (linha, tempo, custo) |
| 3 | **Honestidade crítica > diplomacia** — marcar "pula sem culpa" quando turistada/lotado/pulável | Campo `dicas` pode incluir "pula sem culpa: a vista da ponte 200m antes é a mesma" |
| 4 | **Big picture antes de detalhe** — síntese primeiro, depois detalhe | Card tem `cat` (subtítulo curto) antes de `sobre` (parágrafo) |
| 5 | **Tabelas > prosa densa** — comparações em tabela | Stops tipo `opcoes` sempre comparam 3 alternativas em colunas (nome/preço/distância) |
| 6 | **Riscos sinalizados** — cada stop tem `risco: 'green'\|'yellow'\|'red'` | Default green · yellow se calor extremo/multidão/escada · red se atravessar área pesada |
| 7 | **Walking tour findable** — cards com WT têm flag visual + indexação em busca | `walking-tour-flag` div + busca inclui WT nomes na hay string |
| 8 | **Reservas como checkbox interativo** — `☐ RESERVAR / ☑ FEITO` com localStorage | Botão clicável no card · persiste em `reserva-${stop.nome}` localStorage |
| 9 | **Auto-abrir dia de hoje** — durante a viagem, app abre no dia atual | `getDefaultDayIdx()` compara data do device com `date` dos DAYS |
| 10 | **Senha simples mas persistente** — `localStorage AUTH_KEY` one-time | Senha customizada por viagem · auto-login após primeiro acerto |

---

## 6 anti-padrões obrigatórios (NUNCA fazer)

| # | Anti-padrão | Sintoma · solução |
|---|---|---|
| 1 | Re-renderizar tabs inteiros a cada switch de dia | Lag · scroll perdido · **usar `renderInnerContent()` (soft re-render)** |
| 2 | Strip de parens no NOME visível pra busca Maps | Perde endereço · **`getMapsUrl()` remove parens só da query, mantém no display** |
| 3 | Hardcode `selIdx: 1` no state inicial | Impede auto-abrir dia de hoje · **usar `getDefaultDayIdx()` no init do state** |
| 4 | Avisos paternalistas sobre acessibilidade ("metrô não tem elevator!") | Tom errado · **se acessibilidade é problema, descreve neutro no campo `acessibilidade`** |
| 5 | Botão "Abrir no Maps" duplicado no card E no popup | Duplicação · **só no popup do mapa** |
| 6 | Walking tour > 8 stops sem partition em partes | Cansa · **>8 stops → 2 partes ~6 cada · numeração reseta por parte** |

---

## Formato de resposta no chat (durante geração da viagem)

Quando a skill está conversando com Tobia (fase de briefing, validação de esqueleto, etc):

| Situação | Formato |
|---|---|
| Apresentar esqueleto da viagem | Tabela: data \| bairro \| tema \| atração principal · 1 linha por dia |
| Pedir validação | UMA pergunta direta por vez · não checklist de 8 itens |
| Apresentar walking tour | Mostrar rubrica de valor (alto/médio/baixo) + justificativa antes do conteúdo |
| Status build/deploy | Tabela: passo \| status \| output |
| Crítica honesta | "Pula sem culpa porque X" · não "talvez você queira considerar..." |

---

## Default-on features (não precisa pedir)

- Auth gate com senha
- localStorage persistence (reservas, auth, legend collapse)
- Mapa Leaflet interativo
- Walking tour flag visual
- Busca full-text com hay strings (incluindo WT)
- Day-tabs com cor única HSL distribuída
- Auto-abrir dia de hoje
- `<meta name="robots" content="noindex,nofollow">` (privacidade básica)
- Soft re-render entre dias

## Default-off features (precisa pedir explicitamente)

- PDF export
- Multi-device sync de reservas (não tem)
- Comments/anotações por stop
- Versionamento visível pro usuário
