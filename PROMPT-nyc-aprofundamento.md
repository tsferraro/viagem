# PROMPT · Aprofundamento do roteiro NYC (executável por sessão nova)

> **Como usar (Tobia):** numa sessão nova do Claude Code neste repo, diga só: *"Lê e executa o `PROMPT-nyc-aprofundamento.md`"*. Depois de executado e mergeado, este arquivo pode ser apagado.
>
> **⚠️ Pré-condição de sequência (HANDOFF-mapa-unificado.md):** a **fase 2 do mapa unificado** (sessão-mapa, render de `poiCat`/`valeAPena`) edita `nyc/data.json` e `templates/`. **Confirme com o Tobia que a fase 2 já mergeou** antes de começar — se ainda não, pare e avise. Sempre `git pull --rebase origin main` antes de todo push.

---

## Missão

Aprofundar e elevar o roteiro `nyc/` do estado atual **34/40 (Bom)** no gate `critico-roteiro` para **Excelente (≥36, mirando 38-40)**, sem P0 e sem P1 — usando o padrão-ouro de profundidade e a avaliação em camadas do repo (2026-07-12).

**Perfil NYC:** família Tobia + esposa + filha ~3a · viagem Jul/2026 · calibrar pelo elo mais restritivo (criança pequena: carrinho, sombra, banheiro, soneca, 1 âncora/dia).

## PASSO 0 · Contexto (ler ANTES de mexer, nesta ordem)

1. `CLAUDE.md` — pipeline update, quality bar, 8 anti-padrões, **tabela de gatilhos da avaliação em camadas**
2. `skills/destination-scout/SKILL.md` §Padrão-ouro de profundidade — a barra a igualar
3. `references/content-rubric.md` — 10 dimensões /40 + barra de aspiração ≥36
4. `references/source-credibility.md` — tiers de fonte + o que prova um 🟢 imperdível
5. `skills/critico-roteiro/SKILL.md` + `FACTCHECK.md` + `JUDGE.md` — os 3 instrumentos
6. `references/data-schema.md` — atenção aos campos novos: `fontes` (proveniência), `poiCat`, `valeAPena` (0-3★, semântica no §2.1), `coord` em item de opções, `HISTORIA[]` (§5b)
7. `entregas/roma-toscana-florenca-set2026.md` — o EXEMPLAR: calibre o nível de sobre/imperdivel/dicas/honestidade por ele
8. `references/lessons-learned.md` + `references/tobia-preferences.md`
9. `nyc/data.json` + `nyc/index.html` — estado atual

## PASSO 1 · Baseline fresco

```bash
python3 skills/critico-roteiro/audit.py nyc/data.json
python3 skills/critico-roteiro/audit.py nyc/data.json --check-links
```
Anote nota por dimensão + TODOS os achados. (Referência de 2026-07-12: 34/40 · dimensões presas: D3 Logística 2/4 · D4 Coords 3/4 · D5 Links 3/4 · D8 Honestidade 3/4 · D9 Cobertura 3/4 — mas rode fresco, o data.json mudou com o mapa unificado.)

## PASSO 2 · Diagnóstico dirigido (alvos conhecidos do baseline de 2026-07-12)

- **D3**: custos pagos sem data → datar tudo "(jul/2026)"; "perto/próximo" vago em dicas de banheiro → referência concreta (andar/nome), não distância vaga.
- **D4**: coords com <4 casas (ex: Smorgasburg 40.722) → web_search e corrigir.
- **D5**: rodar `--check-links`; remover 4xx/5xx (sem link > link quebrado); official + 1 review nos cards-âncora.
- **D8**: distribuição de risco plausível; "pula sem culpa" onde couber; zero hipérbole em `imperdivel`.
- **D9**: dia "Sex 3/Jul" sem card → 1 card-âncora leve ou nota clara de chegada.

## PASSO 3 · Pesquisa profunda (a densidade vem daqui)

- Web_search REAL por card-âncora fraco (~10-12 buscas por dia/bairro reforçado). Se reforçar vários bairros: **fan-out paralelo** (1 sub-agente/bairro, retorna markdown + fontes).
- **Registrar proveniência na hora**: `fontes: [{url, tier}]` nos cards-âncora (tiers em `source-credibility.md`; preço/horário = T1 oficial).
- **Busca negativa** (`<POI> superestimado / not worth it`) pra todo 🟢-âncora ainda não coberto.
- NUNCA inventar preço/coord/URL — `[a confirmar]` quando não achar.

## PASSO 4 · Elevar cada card à quality bar (padrão Marais)

`sobre` ≥2 frases com FATO concreto (HTML cru `<strong>`, não markdown) · `imperdivel` = "o que observar" · `dicas` ≥2 com hora/preço/atalho · `duracao` range · `custo` datado "(jul/2026)" · `acessibilidade` concreta (P1 nos risco yellow/red) · coords 4 casas + endereço em parens · WT: partes 4-8 stops, dicas numeradas, ângulo único.
Cards novos: incluir `poiCat` + `valeAPena` (obrigatórios em card/opção — semântica: recompensa PURA 0-3★, sem desconto de esforço; esforço vive no `risco`). **Não reclassificar** os `valeAPena` existentes da sessão-mapa sem motivo achado na pesquisa.
**Opcional (validar com Tobia antes):** gerar `HISTORIA[]` (prosa história & curiosidades de NYC, schema §5b) — só se a fase 2.5 do render já estiver mergeada.

## PASSO 5 · Loop de qualidade em camadas (ordem obrigatória: barato → caro)

1. Edita `nyc/data.json` → `python3 scripts/build.py nyc/data.json nyc/index.html` → `python3 scripts/validate.py nyc/index.html` → `python3 skills/critico-roteiro/audit.py nyc/data.json`. Itera P1s até nota ≥36 e P0=0 (máx ~3 rodadas; se travar, reportar o porquê).
2. **FACTCHECK lean** (`skills/critico-roteiro/FACTCHECK.md`): só afirmações novas/alteradas + sem proveniência + amostra 20%. Não re-checar URL (o `--check-links` cobre).
3. **JUDGE 1×(+1)** (`skills/critico-roteiro/JUDGE.md`): só APÓS audit limpo · sub-agente cético de contexto limpo · amostra ~8-10 âncoras · pareamento com o exemplar Itália · teto 1 re-julgamento.

## PASSO 6 · QA visual

Chromium+Playwright disponíveis: renderizar `nyc/index.html` (bypass do gate via localStorage), screenshot, conferir cards/mapa/legenda no olho. Design a elevar? → `skills/impeccable/`.

## PASSO 7 · Publicar + encerrar

```bash
scripts/deploy.sh "content: aprofundar roteiro nyc (34→NN/40)" "<slug de nyc/SLUG.txt>"
```
→ **merge na main obrigatório** (Pages só serve main) → `scripts/wrap-up.sh` → perguntar ao Tobia se registra lição no `MEMORY.md`.
Na entrega, reportar: nota antes/depois por dimensão · resultado do FACTCHECK (N confirmados/corrigidos/[a confirmar]) · veredicto do JUDGE (N/M âncoras no nível do exemplar) · cards que mais mudaram.

## Regras invioláveis

- Anti-invenção absoluta (web_search sempre; `[a confirmar]` na dúvida).
- Escopo: **só NYC** + template/validate se for guardrail novo. NÃO propagar fix retroativo pra outras viagens sem autorização (MEMORY v1.5).
- Honestidade > diplomacia ("pula sem culpa" onde for turistada).
- `git pull --rebase origin main` antes de todo push (há outras sessões ativas no repo).
