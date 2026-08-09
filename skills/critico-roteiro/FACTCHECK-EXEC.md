# FACTCHECK-EXEC · verificação com RASTRO (modo execução · R6 da auditoria 2026-08-08)

O `FACTCHECK.md` define **o que** verificar. Este arquivo define **como executar deixando
artefato** — porque a auditoria provou que protocolo de honra não é gate: dos 12 passos do
FACTCHECK/JUDGE, 10 não deixavam rastro nenhum, e *"rodei um factcheck completo"* era
indistinguível de não ter rodado — **inclusive para quem rodou**. A Loggia passou por um
"FACTCHECK completo" na manhã do dia em que foi desmentida em campo.

## Regra de papéis (não-negociável · CLAUDE.md pipeline 9c)

> **Quem escreveu NÃO verifica o que escreveu no mesmo contexto.** A sessão construtora
> DESPACHA sub-agentes céticos (contexto limpo — recebem os itens e as afirmações, NUNCA o
> texto de justificativa do construtor) ou pede uma sessão nova. A causa-raiz nº 1 da crise
> de ago/2026 foi verificação sem testemunha.

Prova de viabilidade: a auditoria de 2026-08-08 usou exatamente este desenho — 5 verificadores
céticos em paralelo, ~130 buscas pra ~90 afirmações — e achou 17 erros que "factchecks
completos" anteriores não acharam.

## Estratos (1 sub-agente por estrato · o desenho da Fase 1 do relatório)

| # | Estrato | O que cada item responde |
|---|---|---|
| 1 | **Restaurantes × dia** (todo slot de refeição ⭐⭐/⭐⭐⭐) | existe? · na cidade que o card diz? · **dia-da-semana × data real do stop** (fecha nesse dia?) · serve almoço/jantar no horário do slot? |
| 2 | **Cards ⭐⭐⭐** | preço · horário sazonal · dia de fechamento · **regra de acesso/reserva** (contingentamento, QR, canal — busca de notícia <12 meses pra praia/sítio italiano) |
| 3 | **Paradas de WT + pontos de road trip + coords** | §0 do FACTCHECK.md — existência 100%, nunca amostrada · função · posição · coord copiada de fonte (5º decimal) ou `coord_unverified` |
| 4 | **historia[]** | as afirmações mais específicas de cada polo (datas, números, superlativos, atribuições) |
| 5 | **Logística** | ferries (operador+preço+quem paga o quê) · tempos de estrada e obras · transit_map · aritmética do primeiro/último dia vs horário real de voo |

Prompt-molde do sub-agente (adversarial):

> Tente **REFUTAR** cada afirmação abaixo via busca. Regras: ≥2 fontes independentes pra
> declarar ERRO; agregadores que se ecoam contam como 1; divergência entre fontes = INCONCLUSIVO
> com "ligar antes" + telefone. Prefira T1 pro operacional (`references/source-credibility.md`).
> Retorne POR ITEM: veredito (OK / ERRO com valor certo / RISCO / INCONCLUSIVO) + fonte(s) com
> URL + data de hoje. Não recebeu justificativa do construtor de propósito — não confie em nada.

## O artefato · `<viagem>/FACTCHECK-<AAAA-MM-DD>.md` (versionado)

Formato EXIGIDO pelo gate (`scripts/factcheck-gate.py` — roda no `deploy.sh`):

```markdown
# FACTCHECK · <viagem> · <AAAA-MM-DD>

**Escopo**: <viagem nova completa | itens alterados na sessão X | re-check pré-viagem>
**Executor**: <N> sub-agentes céticos · contexto limpo · <sessão/data>

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| card:Sé de Lisboa | "claustro €5, fecha ter" | OK | https://... | 2026-08-09 |
| opcao:Da Cesare | "almoço seg 12:30" | ERRO → corrigido (almoço só dom) | https://maluentu.net/... | 2026-08-09 |
| wt:Cidadela:Loggia | "mirante sul existe" | INCONCLUSIVO — ligar +33... | — | 2026-08-09 |
```

Regras do formato:
- **Veredito ∈ {OK, ERRO, RISCO, INCONCLUSIVO}** — um item por linha de tabela.
- **OK/ERRO/RISCO exigem URL** na coluna Fonte(s). INCONCLUSIVO pode não ter (é o veredito
  honesto de "nenhuma fonte publica"), mas aí registra o telefone/próximo passo.
- **ERRO vira correção ANTES do deploy** e a linha ganha `→ corrigido` — o gate recusa ERRO
  sem essa marca (erro conhecido não embarcado é pior que erro desconhecido).
- A data no NOME do arquivo é a data da execução. Data futura = forjada, o gate recusa.

## O gate de frescor (`scripts/factcheck-gate.py` · gate 4d do deploy.sh)

Bloqueia o deploy se:
1. **Não existe** `FACTCHECK-*.md` na pasta da viagem;
2. O mais recente tem **formato inválido** (zero linhas de veredito · OK/ERRO/RISCO sem URL ·
   ERRO sem `→ corrigido` · data no nome futura);
3. O **conteúdo sensível mudou depois do factcheck**: a projeção sensível do `data.json`
   (cards ⭐⭐⭐: sobre/imperdivel/dicas/coord/mapsQuery · TODA parada de WT · opções ⭐⭐⭐ ·
   historia[]) difere entre a versão commitada na data do factcheck e a versão que vai pro ar
   — **e** o factcheck não é de hoje. Edit em item não-⭐⭐⭐ (fora de WT/historia) NÃO bloqueia.

O que o gate garante e o que não garante (honestidade de desenho): ele cobra **existência,
formato e frescor do trabalho** — coisas cobráveis por timestamp e estrutura, não gameables por
substring. Ele **não prova que a verificação foi honesta**: um factcheck forjado com URLs
plausíveis passa. Quem pega isso é a sessão AUDITORA (amostra adversarial) e o campo. A
granularidade é de DIA: edit sensível + factcheck do mesmo dia passam juntos — aceito, porque a
alternativa (timestamp por segundo) exigiria commit antes do gate e quebraria o fluxo do deploy.

## Custo e quando roda

Os gatilhos são os do `FACTCHECK.md` (não rodar em edit pequeno — o gate deixa passar edit
não-sensível sem factcheck novo). Custo medido na auditoria: ~130 buscas / ~90 afirmações num
roteiro de 16 dias. Viagem nova inteira será maior — medir na primeira aplicação (R11).
