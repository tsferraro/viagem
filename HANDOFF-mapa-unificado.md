# HANDOFF · sessão-processos ↔ sessão-mapa · 2026-07-12

**De:** sessão-processos (Itália: scout Roma+Toscana+Florença · padrão-ouro · avaliação em camadas)
**Para:** sessão-mapa (fase1a/1b do mapa unificado: `poiCat` + `valeAPena` + coords de opções no NYC)
**Objetivo:** alinhar as duas frentes, dividir escopo pra não colidir, e colher confirmações. Coordenado pelo Tobia.

**Como responder:** preencha a seção **§4 Respostas** deste arquivo, commit + push na main. A sessão-processos puxa e segue.

---

## §1 · O que cada sessão já fez (estado na main, commit `e7928aa`)

**Sessão-processos (esta):**
- `entregas/roma-toscana-florenca-set2026.{md,pdf}` — levantamento macro Itália (19/20 no gate) · virou **exemplar-ouro de profundidade** (SKILL do scout §Padrão-ouro + content-rubric)
- **Avaliação em camadas** na `critico-roteiro`: `audit.py` (forma) → `FACTCHECK.md` (verdade · novo) → `JUDGE.md` (substância vs exemplar · novo) + gatilhos anti-desperdício no CLAUDE.md
- `references/source-credibility.md` (novo): tiers T1-T5 de fontes + padrões de prova (o que sustenta um 🟢)
- **Proveniência**: campo `fontes: [{url, tier}]` documentado no `data-schema.md`
- **Já documentei os SEUS campos** no `data-schema.md` (`poiCat` enum 9 valores + `valeAPena` 0-3) e **sincronizei a tabela do scout** (coluna "Recompensa ★" — a 1ª pesquisa já emite os 2 eixos que o app consome). **Confira em §4.1 se a semântica que escrevi bate com a sua intenção.**

**Sessão-mapa (você):**
- `c273e67` fase1a: `poiCat` + `valeAPena` em 30 cards + 39 opções do `nyc/data.json`
- `f42cecd` fase1b (parcial): `coord` por item de opção (7 de comida, via web_search)
- Fase 2 (render do mapa unificado) pendente

## §2 · Divisão de escopo (pra não se atrapalhar)

| Território | Dono | Arquivos |
|---|---|---|
| **Mapa unificado + render** | **sessão-mapa** | `templates/render-functions.js` · `templates/styles.css` · `templates/shell.html` · `nyc/data.json` · checks novos no `validate.py` pros seus enums (`poiCat`/`valeAPena`/coord-em-opcao) |
| **Processos/qualidade + Itália** | **sessão-processos** | `skills/*` (scout, critico-roteiro, protocolos) · `references/*` (rubricas, credibility) · `MEMORY.md` · `entregas/*` · futura fase 2 do roteiro Itália (subdir próprio) |
| **Compartilhados — tocar com cuidado** | ambos | `references/data-schema.md` (eu documento, você confirma/corrige semântica) · `CLAUDE.md` (seções distintas; sempre `git pull --rebase` antes de push) |

Regras de convivência: (a) **`git pull --rebase origin main` antes de todo push** (já colidimos 1× hoje — resolvido); (b) commits pequenos e frequentes; (c) mudança em arquivo do outro território = anunciar aqui no HANDOFF antes.

## §3 · Propostas de alinhamento (adotar nas suas fases seguintes)

1. **Proveniência nas coords/dados novos**: quando pesquisar coord/preço de POI na fase 1b/2, registre `fontes: [{url, tier}]` no card-âncora (régua: `references/source-credibility.md`). Custa zero na hora e poupa o FACTCHECK de re-caçar.
2. **Coords com 4 casas decimais** (regra do repo + audit D4): a fase1b tem pelo menos `Bernie's {lat: 40.73, lng: -73.9551}` com 2 casas — o audit vai acusar. Vale revisar as 7 e manter 4 casas nas próximas.
3. **Documente no `data-schema.md` o que criar de novo** (ex: `coord` em item de `opcoes` ainda não está lá — ver §4.2). Campo sem doc = sessão futura não sabe que existe (foi o que aconteceu com poiCat/valeAPena, já corrigi).
4. **Decomposição oficial**: `valeAPena` (recompensa ★) × `risco` (esforço/semáforo) = os 2 eixos; veredito 🟢🟡🔴 do scout = a síntese pro perfil. Já refleti isso no scout e no schema — o render deve tratar os 2 eixos como independentes (3★ pode coexistir com semáforo vermelho).

## §4 · Perguntas — RESPONDA AQUI

### 4.1 Semântica de `valeAPena` (documentei como 0-3)
- [ ] O **0 existe** de fato? O que significa (item sem valor próprio, ex: transit/logística) vs campo **ausente**?
- [ ] Aplica a stops `transit`? (assumi que não — confirmar)
- Resposta: _______________

### 4.2 `coord` em item de `opcoes`
- [ ] Vai virar **pino próprio no mapa** na fase 2? Todos os itens de opção terão coord, ou só os "3★"?
- [ ] Confirma que devo (eu, processos) documentar `coord` opcional em item de `opcoes` no data-schema, ou você documenta junto da fase 2?
- Resposta: _______________

### 4.3 Render da fase 2 (pra eu não desenhar por cima)
- [ ] Como ★ e semáforo aparecem no pino/popup/legenda? Filtros por `poiCat`?
- [ ] `validate.py`: você adiciona os checks dos enums novos (poiCat ∈ lista, valeAPena ∈ 0-3, coord 4 casas em opção)?
- Resposta: _______________

### 4.4 Aba "História & Curiosidades" (proposta do Tobia, apoiada pela sessão-processos)
Aba tipo coletânea-Marais (prosa por polo, sem mapa/stops), conteúdo vindo pronto do `.md` da destination-scout.
- [ ] **Quem faz?** Opção A: você embute na mesma mexida de template da fase 2 (1 mudança só). Opção B: sessão-processos faz DEPOIS da sua fase 2 mergeada. Preferência?
- Resposta: _______________

### 4.5 Escala do scout
Sincronizei a tabela do scout pra emitir "Recompensa ★ (0-3)" na primeira pesquisa. Algum ajuste na escala/semântica pra casar 100% com o render que você planeja?
- Resposta: _______________

---

*Depois de respondido e lido pelas duas sessões, este arquivo pode ser apagado ou movido pra `archive/` — não é doc permanente.*
