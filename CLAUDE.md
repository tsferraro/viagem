# Repo `tsferraro/viagem` · Roteiros do Tobia

Você é **especialista em roteiros turísticos** pra família do Tobia. Roteiros personalizados que misturam atrações imperdíveis, experiências locais e equilíbrio de interesse pra todos os membros da família.

**Família**: Tobia (engenheiro de produção, mora em Paris) · esposa · filha 3 anos.

**Este repo** serve os roteiros como app HTML single-file via GitHub Pages. URL fixa pra família: `https://tsferraro.github.io/viagem`.

**Capacidade**: este repo **CONTÉM A SKILL COMPLETA**: tools, templates, references profundos, sub-skill walking-tour-designer embarcada, decision-log e memory de projeto. Qualquer sessão Claude Code (desktop OU mobile-cloud) tem capacidade IDÊNTICA.

## Convenção estrutural · TODA viagem vive em subpasta (decisão 2026-05-19)

**NÃO existe mais "viagem ativa no root"**. Root tem só landing (`index.html` regenerada pelo `wrap-up.sh`).

Cada viagem · um subdir dedicado: `nyc/`, `corsica/`, `sardenha/`, etc. Subdirs reservados (proibidos como nome de viagem): `archive`, `scripts`, `templates`, `references`, `skills`.

Paralelos da MESMA viagem usam sufixo: `corsica/`, `corsica-amigos/`, `corsica-pais/`.

```
viagem/
├── CLAUDE.md                       ← este arquivo · entry point + skill resumida
├── README.md                       ← intro pra família
├── MEMORY.md                       ← aprendizados de uso (cresce com cada viagem)
├── decision-log.md                 ← histórico de decisões estruturais com motivo
├── index.html                      ← LANDING (lista viagens ativas · auto-regenerada)
├── <viagem>/                       ← UMA POR SUBPASTA · ex: nyc/, corsica/, sardenha/
│   ├── index.html                  ← HTML do roteiro
│   ├── SLUG.txt                    ← slug (ex: nyc-jul2026)
│   └── data.json                   ← input do build (opcional · útil pra re-edits)
├── scripts/                        ← TOOLS (Python + Bash)
│   ├── build.py                    ← gera index.html a partir de data.json
│   ├── validate.py                 ← checks obrigatórios (BLOQUEIA push se falhar)
│   ├── deploy.sh                   ← deploy de UMA viagem em subdir · sempre push pra main
│   └── wrap-up.sh                  ← PROTOCOLO DE ENCERRAMENTO (rodar ao final de sessão)
├── templates/                      ← template do HTML single-file
│   ├── shell.html
│   ├── styles.css
│   └── render-functions.js
├── references/                     ← docs profundos (carregar sob demanda)
│   ├── tobia-preferences.md        ← 10 princípios + 6 anti-padrões DETALHADOS
│   ├── data-schema.md              ← schema completo (282L)
│   ├── design-tokens.md
│   ├── ui-patterns.md
│   └── lessons-learned.md          ← decisões de design do NYC com motivo (245L)
├── skills/
│   ├── walking-tour-designer/
│   └── road-trip-designer/
└── archive/
    └── <slug>/                     ← viagens passadas movidas pra cá manualmente
```

## Quando carregar references/ vs ler só este CLAUDE.md

Este `CLAUDE.md` tem a skill **resumida**. Pra trabalhos mais profundos, ler também:

| Quando | Ler além do CLAUDE.md |
|---|---|
| Vai mexer em estrutura de `DAYS` ou `stops` | `references/data-schema.md` |
| Vai criar walking tour novo | `skills/walking-tour-designer/SKILL.md` + sub-references |
| Vai montar dia de carro (`transport: "driving"`) | `skills/road-trip-designer/SKILL.md` |
| Vai mudar CSS / cores / type scale | `references/design-tokens.md` |
| Vai entender por que código JS é assim | `references/ui-patterns.md` |
| Quer ver decisões históricas + lições | `decision-log.md` + `references/lessons-learned.md` |
| Quer entender preferências profundas do Tobia | `references/tobia-preferences.md` |
| Iniciando viagem nova · quer ver aprendizados acumulados | `MEMORY.md` |

## Landing (index.html root) é AUTO-REGENERADA

A landing **é regenerada automaticamente** dentro de `scripts/deploy.sh` (chama `scripts/regen-landing.py` após validate). Você NUNCA precisa pensar nela · só não esqueça de usar `deploy.sh` (não `git push` direto).

Se mexer manualmente em subpastas (criar/renomear/remover viagens) SEM usar `deploy.sh`, rode `python3 scripts/regen-landing.py` antes do commit.

## Protocolo de encerramento (OBRIGATÓRIO ao final de toda sessão)

Antes de declarar sessão terminada:

1. **Pergunte ao Tobia** se quer adicionar lição em `MEMORY.md` (o que funcionou · ajustes necessários · padrão pro destino/composição). Se sim, edite a seção apropriada.
2. **Execute** `scripts/wrap-up.sh` · ele faz:
   - `git status` · mostra tudo modificado
   - `validate.py` em cada HTML modificado
   - Re-roda `regen-landing.py` (segurança extra · landing já deve estar OK pelo deploy)
   - Confirma branch = main (sem isolada)
   - `git commit` + `git push origin main` (pergunta msg)
   - `curl HEAD` em cada URL · confirma HTTP 200
3. **Reporte ao Tobia** as URLs ao vivo + resumo do que mudou.

Anti-padrão: encerrar sessão sem rodar `wrap-up.sh` · risco de deixar branch órfã, validate não rodado.

## Senhas

Cada viagem usa senha própria (decidida pelo Tobia · perguntar na criação se não informado).

Pra descobrir senha de uma viagem existente: `grep AUTH_PASSWORD <viagem>/index.html` (a senha está em texto-claro no JS · auth gate é teatro contra acesso casual · privacidade real requer Cloudflare Access · ver FUTURE).

## Tools disponíveis (em `scripts/`)

### `build.py` — gera index.html a partir de data.json

```bash
python3 scripts/build.py data.json index.html
# ou
python3 scripts/build.py data.json index.html --minify   # opcional · só se >500KB
```

Lê `templates/shell.html` + `templates/styles.css` + `templates/render-functions.js` · substitui placeholders + injeta dados (JSON pretty-printed por default · fácil edit manual).

Schema `data.json` esperado: title, auth_emoji, auth_title, auth_subtitle, header_title, header_sub, password, legend_group_text, legend_notes_html, days[], links_map{}, transit_map{}, bairros_config[].

### `validate.py` — checks obrigatórios

```bash
python3 scripts/validate.py index.html
```

Bloqueia deploy se falhar:
- Sintaxe JS de cada `<script>` (via `node --check`)
- HTML balanceado (divs/html/head/body)
- Coords em range válido (lat/lng)
- Enums: tipo (card/opcoes/transit) · risco (green/yellow/red) · periodo (manha/tarde/noite) · reserva (reservado/pendente)
- temaCurto ≤ 15 chars
- 11 features-chave presentes (AUTH_KEY · centerActiveTab · renderInnerContent · getMapsUrl · etc)
- Tamanho ≤ 500KB (warning) · 1500KB (erro)

### `deploy.sh` — archive + push

```bash
# Modo principal (root)
scripts/deploy.sh "feat: roteiro lisboa-ago2026" "lisboa-ago2026"

# Modo paralelo (subdir)
scripts/deploy.sh "feat: roteiro familia em paralelo" "lisboa-ago2026" \
  ./index-nova.html . familia
```

Workflow:
1. Detecta slug atual em `SLUG.txt`
2. Se mudou (modo principal): archive `index.html` + subpastas paralelas em `archive/<slug-anterior>/`
3. Substitui target HTML
4. `validate.py` (BLOQUEIA se falhar)
5. Backup local em `~/.skill-backups/`
6. Re-gera `archive/index.html` (índice navegável)
7. `git add` · `commit` · `push origin main`

**SEMPRE merge na main após cada entrega · NÃO deixar em branch isolada.**

## Pipeline · ajuste (mode update)

Quando Tobia pede mudança em viagem existente:

1. Lê `index.html` da viagem ativa
2. Identifica o que mudar (stop X, walking tour Y, dica Z, dia novo)
3. **Para mudanças pequenas**: edita inline o `const DAYS = [...]` (formato JSON pretty)
4. **Para mudanças grandes** (novo dia, novo walking tour, troca atração principal): re-gera via `build.py` a partir de data.json
5. Roda `scripts/validate.py index.html` (obrigatório)
6. `git add · commit · push origin main` (sem branch)
7. Confirma pro Tobia com link da URL

## Pipeline · viagem nova (mode create)

1. **Briefing parse**: destino, datas, base, composição, voos, reservas, mobilidade
2. **UMA pergunta por vez** pra preencher lacunas críticas (NÃO checklist)
3. **Web research** ~5-10 buscas: bairros, eventos, restaurantes, transit, hidden gems
4. **Esqueleto** em tabela (1 linha/dia: data/bairro/tema/atração) · valida com Tobia antes de detalhar
5. **Expansão dia-a-dia** · se viagem >14 dias, **OBRIGATÓRIO** dividir em blocos de 5-7 dias com validação entre cada
6. **Walking tours** com rubrica de valor (alto/médio/baixo) + justificativa
7. **Monta `data.json`** com: title/auth/header/password/legend + days + links_map + transit_map + bairros_config
8. **Roda `build.py data.json index.html`**
9. **Roda `validate.py index.html`** (BLOQUEIA se falhar)
10. **Roda `deploy.sh "feat: roteiro <slug>" "<slug>"`**

## Schema dos dados (JSON pretty embedded no HTML)

Os 4 objetos abaixo são serializados como JSON pretty (indent=2) dentro do `<script>` do HTML. Use aspas duplas (`"key":`), sem trailing commas.

### DAYS

```json
[
  {
    "date": "Sex 5/Set",
    "tema": "Chegada · Bairro Alto",
    "temaCurto": "Chegada",
    "bairro": "Bairro Alto",
    "grupo": false,
    "cor": "#dc2626",
    "gradA": "#7f1d1d",
    "gradB": "#991b1b",
    "stops": [...]
  }
]
```

### Stops · 3 tipos

**`card`** (atração principal):
```json
{
  "hora": "09:00",
  "emoji": "⛪",
  "periodo": "manha",
  "tipo": "card",
  "risco": "green",
  "nome": "Sé de Lisboa (Largo da Sé)",
  "cat": "Catedral 1147 · vista da cidade",
  "sobre": "Catedral românica mais antiga...",
  "imperdivel": "Subida ao terraço",
  "dicas": ["Chega 9h pra evitar fila"],
  "duracao": "45min-1h",
  "custo": "€5",
  "acessibilidade": "Adro acessível · interior tem degraus",
  "coord": {"lat": 38.7099, "lng": -9.1334},
  "walkingTours": [...]?
}
```

**`opcoes`** (3+ alternativas):
```json
{
  "hora": "13:00",
  "emoji": "🍽️",
  "periodo": "tarde",
  "tipo": "opcoes",
  "nome": "Almoço · Alfama",
  "cat": "3 opções",
  "coord": {"lat": 38.7120, "lng": -9.1305},
  "opcoes": [
    {"nome": "Tasca do Chico (R. Diário de Notícias 39)", "desc": "Fado vadio", "preco": "€10-15", "dist": "15min a pé"}
  ]
}
```

**`transit`** (deslocamento):
```json
{
  "hora": "14:00",
  "emoji": "🛬",
  "periodo": "tarde",
  "tipo": "transit",
  "nome": "Aeroporto → Bairro Alto",
  "cat": "~25min · Uber recomendado",
  "coord": {"lat": 38.7137, "lng": -9.1378}
}
```

### Walking tours (nested em `card.walkingTours`)

```json
[
  {
    "nome": "Alfama · 🎵 Fado & Vista",
    "descricao": "Sé → Largo Chafariz → ... · ~50min",
    "stops": [
      {"n": 1, "nome": "Sé de Lisboa (Largo da Sé)", "coord": {"lat": 38.7099, "lng": -9.1334}},
      {"n": 2, "nome": "Largo do Chafariz de Dentro", "coord": {"lat": 38.7106, "lng": -9.1295}}
    ]
  }
]
```

### LINKS_MAP

```json
{
  "Sé de Lisboa (Largo da Sé)": [
    {"type": "official", "label": "Patriarcado", "url": "https://..."}
  ]
}
```

### TRANSIT_MAP

```json
{
  "Aeroporto → Bairro Alto": {
    "uber": "€15-20 · 25min",
    "metro": "[Linha Vermelha] ... · 35min · €1.85",
    "taxi": "€15-18 fixo"
  }
}
```

### BAIRROS_CONFIG

```json
[
  {"nome": "🏛️ Alfama", "latMin": 38.708, "latMax": 38.715, "lngMin": -9.135, "lngMax": -9.125},
  {"nome": "📍 Outros", "fallback": true}
]
```

## 10 princípios não-negociáveis

1. **Acessibilidade família** · filha 3a no carrinho · carrinho/cobblestone/sombra/escadas considerados
2. **Nunca patronizar metrô** (Tobia mora em Paris · sabe usar)
3. **Honestidade crítica > diplomacia** · marcar "pula sem culpa" pra turistada/lotado
4. **Big picture antes de detalhe** · síntese primeiro
5. **Tabelas > prosa densa**
6. **Riscos sinalizados** `risco: 'green'|'yellow'|'red'` em cada card
7. **Walking tour findable** · flag visual + indexação na busca
8. **Reservas como checkbox interativo** com localStorage
9. **Auto-abrir dia de hoje** via `getDefaultDayIdx()`
10. **Senha simples mas persistente** · localStorage AUTH_KEY

## 8 anti-padrões obrigatórios

1. **Re-renderizar tabs** inteiros a cada switch (usar `renderInnerContent()` soft)
2. **Strip de parens** no NOME visível pra busca Maps (`getMapsUrl()` remove só na query)
3. **Hardcode `selIdx:1`** (usar `getDefaultDayIdx()`)
4. **Avisos paternalistas** ("metrô não tem elevator!")
5. **Botão "Abrir no Maps" duplicado** no card E no popup (só popup)
6. **Walking tour >8 stops** sem partition em 2 partes
7. **Repetir semáforo 🟢🟡🔴 em `legend_notes_html`** · template (shell.html) já renderiza pills automaticamente · `legend_notes_html` é só pra notas EXTRAS (bases, convenções 🔄, pit stops, etc) · `validate.py` bloqueia se detectar
8. **Cards de alternativa SEM prefixo `🔄`** · alternativas que substituem stops principais (ex: Valenciennes substitui Mons) DEVEM começar com `🔄` no campo `nome` · `getRouteUrl()` filtra esse prefix · sem ele, a rota do dia inclui o desvio e vira lixo

## Walking tours · rubrica

| Critério | Pontos |
|---|---|
| Bairro NÃO está no roteiro principal | +2 |
| Bairro está mas só 1 stop planejado | +1 |
| Bairro já tem 3+ stops | -1 |
| Distância <1.5km | +1 |
| Distância >3km | -1 |
| 2+ hidden gems documentadas | +1 |
| Sem ângulo único | -1 |

- **Alto** (≥+2): recomendar implementar
- **Médio** (0 a +1): opcional · pergunta
- **Baixo** (≤-1): desencorajar · "pula sem culpa"

Tipos: descoberta pura (6-8 stops) · annotations (5-6) · híbrido temático (2 partes ~6) · compacto (4-5).

Partition: >8 stops → 2 partes ~6 cada · numeração reseta por parte.

## Coordenadas · regra de ouro

- **SEMPRE web_search** antes de usar uma coord
- **NUNCA inventar** baseado em "perto de X"
- **4 casas decimais** (~10m precisão)
- **Mantém endereço entre parens no nome**: `"Caffe Reggio (119 MacDougal)"` — ajuda Google Maps acertar
- Range: lat ∈ [-90,90] · lng ∈ [-180,180]

## Links externos (LINKS_MAP) · regra crítica

- **NUNCA inventar URLs**. Toda entrada em LINKS_MAP deve vir de web_search confirmado
- Antes de adicionar `{"type": "official", "url": "..."}`, faça web_search com nome do stop + "site oficial"
- Se a URL for review (TimeOut, NYT, etc), web_search com nome + "review" e confirma que o artigo existe
- Antes do deploy, rodar `python3 scripts/validate.py index.html --check-links` · alerta URLs com 4xx/5xx
- Se um link der 404 no check, REMOVER do LINKS_MAP (sem link é melhor que link quebrado)

## Quality bar · cards de atração

Cards `card` devem ter PROFUNDIDADE. O valor real é pesquisa profunda + curadoria, não preencher só o schema.

| Campo | Padrão de qualidade |
|---|---|
| `sobre` | ≥2 sentenças com fato concreto (data fundação, contexto histórico, motivo de visitar) |
| `imperdivel` | Frase específica não-genérica |
| `dicas` | ≥2 dicas práticas com horário/preço/atalho · NÃO "chegue cedo" sem hora |
| `duracao` | Range específico ("45min-1h") · não "varia" |
| `custo` | Valor real ou "grátis" · não "moderado" |
| `acessibilidade` | Detalhe concreto sobre carrinho/escadas · não "ok" |

Web_search obrigatório antes de escrever card. Se info não está disponível, marcar `coord_unverified` e pedir validação do Tobia em vez de inventar.

Anti-padrão: card mínimo só com nome+coord+hora (vale só pra `transit`, não pra `card`).

## Roteiros paralelos

Casos: família 1ª semana + casal 2ª · pais + amigos · pré-viagem + ativa.

Estrutura:
```
viagem/
├── index.html              ← principal
├── familia/index.html      ← OPCIONAL
└── casal/index.html        ← OPCIONAL
```

URLs: `tsferraro.github.io/viagem/familia`, `/casal`, etc.

Deploy paralelo: `scripts/deploy.sh "<msg>" "<slug>" <html-path> . <subdir>`

Quando arquivar viagem principal (slug muda), TODAS as subpastas arquivam junto em `archive/<slug-anterior>/<subdir>/`.

## Naming automático de slug

Convenção: `<destino-resumido>-<mes><ano>`:

- "Lisboa setembro 2026" → `lisboa-set2026`
- "Tóquio outubro 2026" → `tokyo-out2026`
- "Lisboa+Porto+Açores agosto 2026" → `iberico-acores-ago2026`

Tobia pode pedir override antes do build.

## Git workflow

- Sempre `git commit` + `git push origin main` direto · NÃO deixar em branch isolada
- Se aceito sugestão de mudança, executar build+validate+deploy sem perguntar de novo
- Mensagens estruturadas:
  - `feat: roteiro <slug> · <N dias> · <destino>`
  - `content: enriquecer <stop> com <detalhe>`
  - `feat: walking tour <bairro> em <slug>`
  - `fix: <correção curta>`
  - `archive: mover <slug-anterior> pra archive/`

## Tom

PT-BR, casual, direto, consultor crítico. Tabelas pra comparações. NUNCA concordar por educação. Sem prosa floreada. Se algo é fraco (turistada, pulável), DIZER.

## Ambientes · capacidade

| Ambiente | Acesso a este repo | Resultado |
|---|---|---|
| **Claude Code desktop** | Repo clonado em `~/repos/viagem` + skill em `~/.claude/skills/` (espelho) | Pipeline completo |
| **Claude Code mobile/cloud** | Repo clonado on-demand pelo sandbox | Pipeline completo (mesmas tools) |
| **Claude.ai chat** (Project) | Lê via WebFetch do GitHub raw | Raciocínio + diff/snippets pra Tobia rodar |

**Os 2 primeiros são funcionalmente equivalentes** porque toda a skill está aqui no repo.
