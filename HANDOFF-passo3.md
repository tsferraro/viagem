# HANDOFF · Passo 3 — Rubrica de Conteúdo + audit-content + loop-até-excelente

> **Como usar:** abra uma sessão nova no repo `tsferraro/viagem` e cole o bloco "PROMPT PRONTO" abaixo. Ele obriga a sessão a ler o necessário, se fundamentar em pesquisa externa, planejar e entregar um produto excelente.

Contexto: o **Passo 2 (design)** foi concluído — o design novo virou template (`references/design-rubric.md` documenta a avaliação de UI, nota 39/40). Falta o eixo **conteúdo**: escrita, adaptação ao público/objetivo, links vivos e complementares, walking tours, acessibilidade, logística. A impeccable **só cobre design** — conteúdo é uma rubrica separada.

---

## PROMPT PRONTO (copiar/colar na sessão nova)

Você é **especialista em roteiros turísticos** do repo `tsferraro/viagem` (família do Tobia — engenheiro em Paris, esposa, filha 3a). Sua missão é o **Passo 3**: criar a **avaliação de qualidade de CONTEÚDO** dos roteiros e transformá-la num **loop-até-excelente** dentro do pipeline de criação — que só entrega roteiro excelente, com tudo funcionando, e **imprime a nota final na entrega**.

Não improvise. Siga esta ordem e não pule etapas.

### FASE 0 · Leitura obrigatória (não escreva nada antes de ler tudo)
Leia integralmente e resuma pra si mesmo o que cada um estabelece sobre QUALIDADE DE CONTEÚDO:
- `CLAUDE.md` (seções: Quality bar · cards de atração; Walking tours · rubrica; Coordenadas · regra de ouro; Links externos · regra crítica; 10 princípios; 8 anti-padrões; Padrão-ouro de storytelling / coletânea Marais)
- `references/tobia-preferences.md` (10 princípios + 6 anti-padrões DETALHADOS)
- `references/lessons-learned.md` (decisões com motivo, inclusive §3 walking tours e §9 redesign)
- `references/data-schema.md` (schema completo — o que cada campo de card/opcoes/transit/walkingTour deve conter)
- `references/design-rubric.md` (como a rubrica-irmã de DESIGN foi estruturada — espelhe o formato e o rigor)
- `MEMORY.md` (aprendizados reais por viagem + método QA) e `decision-log.md`
- `skills/walking-tour-designer/SKILL.md` (+ sub-references) e `skills/road-trip-designer/SKILL.md`
- `scripts/validate.py` (já tem `--check-links`! entenda como funciona) e `scripts/build.py`
- Um roteiro real como referência de padrão-ouro: `nyc/data.json` (e a coletânea `marais/` como exemplo de modo "city")

### FASE 1 · Pesquisa externa (obrigatória — fundamente, não opine no vácuo)
Use WebSearch/deep-research. **Toda dimensão da rubrica deve citar ao menos uma fonte/best-practice.** Pesquise o **padrão-ouro** de:
- Como guias/roteiros profissionais são construídos e avaliados (ex.: critérios editoriais de Lonely Planet / Michelin / Rick Steves / DK Eyewitness; craft de free walking tour; jornalismo de viagem).
- Qualidade de informação turística: exatidão, atualidade, curadoria vs. cobertura, "signal vs. noise".
- UX/conteúdo de apps de itinerário (o que separa um roteiro que a pessoa realmente usa em campo de um que abandona).
- Acessibilidade familiar / viajar com criança pequena (fontes reconhecidas).
- Adaptação ao público e ao objetivo (family-friendly, ritmo, tempo real de deslocamento, honestidade sobre "turistada").
Sintetize os achados num pequeno "state of the art" com fontes, que vira a base da rubrica.

### FASE 2 · Plano (apresente ANTES de construir)
Apresente ao Tobia, em tabela, o plano: as **dimensões da rubrica** (com pontuação 0-4 cada, espelhando `design-rubric.md`), o que cada uma checa, o que dá pra **automatizar** vs. **julgar manualmente**, e como o **loop-até-excelente** vai funcionar (limiar de aprovação, o que bloqueia entrega, como a nota final é exibida). **Valide o plano com o Tobia antes de codar.** Uma pergunta por vez pra lacunas críticas.

### FASE 3 · Entrega (produto excelente, testado)
1. `references/content-rubric.md` — a rubrica repetível. Dimensões sugeridas (refine com a pesquisa): **Escrita & storytelling** (padrão Marais: guia que encanta pra ganhar a gorjeta) · **Adaptação ao público/objetivo** (família, criança 3a, ritmo, "não patronizar metrô") · **Profundidade & curadoria** (quality bar de cards: sobre ≥2 frases com fato, imperdível específico, dicas com hora/preço, duração/custo/acessibilidade reais) · **Links** (oficiais/reviews confirmados, vivos, e **complementares de suporte/recomendação**) · **Walking tours** (rubrica de valor alto/médio/baixo + storytelling parada-a-parada) · **Acessibilidade/família** · **Logística & transporte** (tempos reais, modos, honestidade) · **Coords/precisão** (web_search, 4 casas, sem invenção) · **Honestidade** ("pula sem culpa"). Cada dimensão: 0-4 + o que é 4 vs 2 vs 0 + fonte.
2. `scripts/audit-content.py` — audit **semi-automático** que roda sobre um `data.json` (ou o HTML) e retorna uma **nota + achados P0-P3**. Automatize o automatizável de verdade (não fake): links 4xx/5xx (reaproveite/estenda o `--check-links`), presença/profundidade dos campos de card, coords ausentes/suspeitas, WT sem ângulo/valor, temaCurto, densidade de "signal". Para o que exige julgamento (qualidade da escrita, adaptação), gere um checklist estruturado + (opcional) um passo com sub-agente avaliador. Imprima **nota final /N + banda** ao terminar.
3. **Loop-até-excelente**: integre ao pipeline de criação (documente em `CLAUDE.md` na seção de pipeline e/ou `deploy.sh`/`wrap-up.sh`): ao final da criação, roda o `audit-content.py`; se abaixo do limiar → itera (corrige os P0/P1) e re-roda; só entrega quando **excelente**, e mostra a nota final pro Tobia junto do link.
4. Rode o audit no `nyc/data.json` como prova real (mostre a nota + achados). Corrija falsos-positivos.
5. Registre no `decision-log.md` + atualize `CLAUDE.md` (aponte `references/content-rubric.md` + `audit-content.py` na tabela de references e no pipeline).

### Granularidade da avaliação (decisão do Tobia)
Avaliar em **dois níveis**, e a nota final é agregada COM breakdown por dia visível:
- **Por dia/parada** (localiza o problema): profundidade/curadoria de card, links vivos, valor do walking tour, coords. O loop-até-excelente ataca primeiro o dia de menor nota.
- **Roteiro inteiro** (1x): arco/equilíbrio entre dias, adaptação ao público/objetivo, ritmo pra criança 3a, honestidade geral.
- **Nota final** = agregada (média ponderada), mas **sempre mostrar o placar por dia** — só-agregado esconde dia fraco; só-por-dia não dá manchete.

### Regras
- **Honestidade > diplomacia** (tom PT-BR, consultor crítico). A auditoria tem que ser **real** — se um link está morto, ela acusa; se um card é raso, ela pontua baixo. Nada de teatro.
- App é self-contained; não quebre o pipeline existente (build/validate/regen-landing/deploy).
- Fundamente cada critério numa best-practice citada (Fase 1). Sem "achismo".
- Entregue um produto **excelente e testado**, não um rascunho. Itere até ficar impecável.
- Ao final, rode `scripts/wrap-up.sh` (protocolo de encerramento) e reporte URLs + nota.

---

### Pontos de qualidade já existentes no repo (a rubrica DEVE incorporar)
- **Quality bar de card** (CLAUDE.md): `sobre` ≥2 frases com fato concreto · `imperdivel` específico · `dicas` ≥2 com hora/preço/atalho · `duracao` range · `custo` real · `acessibilidade` concreta. Anti-padrão: card mínimo só nome+coord.
- **Rubrica de walking tour**: pontua bairro fora do roteiro (+2), <1.5km (+1), 2+ hidden gems (+1), sem ângulo único (-1)… → alto/médio/baixo. Partition >8 stops.
- **Storytelling padrão-ouro (Marais)**: postura de guia de free walking tour; `sobre` conta história/curiosidade (data, personagem, lenda); `imperdivel` = "o que observar" (o detalhe que o distraído perde); narrar parada-a-parada nas `dicas`; HTML cru (`<strong>`/`<em>`), não markdown.
- **Coords · regra de ouro**: sempre web_search antes; nunca inventar; 4 casas; endereço entre parens no nome.
- **Links · regra crítica**: nunca inventar URL; confirmar via web_search; `validate.py --check-links` antes do deploy; link 404 → remover ("sem link é melhor que link quebrado"). Processo pra evento: buscar o **endereço** do evento; sem ponto confiável → **não colocar o ponto** (`noMaps`).
- **10 princípios / 8 anti-padrões** (acessibilidade família; não patronizar metrô; honestidade > diplomacia; big picture antes de detalhe; riscos sinalizados; etc.).
- **Adaptação ao público**: família com filha 3a (carrinho/sombra/escada/banheiro/ritmo), Tobia mora em Paris (metrô sem paternalismo), honestidade sobre turistada.
- **Ideia do Tobia (loop-até-excelente)**: o audit vive DENTRO da criação; só entrega roteiro excelente com tudo funcionando; **nota final exibida na entrega**.
