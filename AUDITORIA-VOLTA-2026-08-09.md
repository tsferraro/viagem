# AUDITORIA DE VOLTA · 2026-08-09 · execução dos Lotes 1-5

Sessão auditora (a mesma de `AUDITORIA-RELATORIO-2026-08-08.md`) rodando o protocolo do
`HANDOFF-AUDITORIA-EXECUCAO.md` contra a `main` (`6105ded..2bc9b74`). Método: comandos de
aceite verbatim + ataques de forja num clone isolado + amostra factual do conteúdo alterado.

## Veredito: **APROVADO com 2 ressalvas operacionais** (nenhuma bloqueia; ambas fail-closed)

| Lote | Aceite | Resultado |
|---|---|---|
| 1 · ferramentas | `--json` parseável · self-diff com dívida (42=42 achados) · suite **27/27** · coord repetida bloqueia (exit 1, testado direto E na suite) · comentário 832-838 agora é honesto (diz o que o regex NÃO pega e por quê) · nota renomeada FORMA com "verdade é o FACTCHECK, não esta nota" | ✅ |
| 2 · factcheck-artefato | **4 forjas, 4 bloqueios**: artefato vazio (touch) · vereditos sem URL · data futura · ERRO sem "corrigido" — todos exit 1. Factcheck velho (07/Ago) + conteúdo commitado depois → bloqueia listando os 23 itens mudados. Bosa-falsa sem artefato → bloqueia. Gate ligado no deploy.sh (4d) | ✅ c/ ressalvas |
| 3 · padrões de prova | 5 classes presentes no source-credibility.md · schema unificado `{o,u,tier,data,prova[]}` no data-schema.md · fixture fonte-sem-tier dispara o aviso · cota "2 verificadas > 3 plausíveis" e regra da coord copiada-do-5º-decimal no CLAUDE.md (com a estatística certa: 5 derivadas erradas, copiadas 100%) | ✅ |
| 4 · conteúdo | grep 1553: **5 ocorrências** (a reescrita da historia[4] é fiel e bem construída — "os painéis da cidade contam... Bonifacio também caiu") · Loggia agora é o alpendre da cisterna · 500km no CLAUDE.md: **0** · Forte de Carlo ✓ · Baal Hammon ✓ · 25+2 estátuas ✓ · ~400 t/h ✓ · Sulci relativizado ✓ · dossiê ANOTADO sem apagar (§2.2/#4 e #10 marcados REFUTADO) · dívidas intocadas (67/49/36, último commit segue o baseline antigo) · audits sem P0 | ✅ |
| 5 · curadoria | skill coerente com a seção 6 · `fontes/registro.json`: 8 fontes, todas `candidata` · landing NÃO lista fontes/ como viagem · `pais-sardenha/DIARIO.md` existe · re-check pré-viagem documentado | ✅ |
| Regressão | validate + maps-audit + factcheck-gate: **exit 0 nas duas viagens em uso** | ✅ |

## Amostra factual do Lote 4 (auditoria da auditoria)

- **A executora refutou uma instrução MINHA — e estava certa.** O handoff mandava remover
  "quem parou o relógio foi Menotti" como sem-fonte; o cético dela achou a fonte (site do
  próprio Compendio + Wikipedia IT) e manteve com atribuição "segundo o próprio museu".
  **Confirmei independentemente**: a atribuição a Menotti existe nas fontes do museu. O erro
  era do MEU verificador da Fase 1 (declarou "não-encontrado" sem esgotar). Registro sem
  constrangimento: é o laço adversarial funcionando nos dois sentidos — inclusive contra o
  auditor. · O "mais visitado" foi rebaixado pra "um dos" com a ressalva explícita no texto ✓.
- Coords novas (dedup Tophet/MAB estendido pela executora a Piazza Garibaldi, Corso Umberto e
  Cala Grande-praia): todas plausíveis e citadas; **Cala Grande 41.23841, 9.14131 e Piazza
  Garibaldi 41.21286, 9.40661 são fonte-única** (diretórios) — geograficamente coerentes,
  risco baixo (rota vai por nome), ficam anotadas pro campo confirmar.
- Os 2 artefatos `FACTCHECK-2026-08-09.md` têm cara de pesquisa real: escopo declarado,
  limitações declaradas, um INCONCLUSIVO honesto (Plage de la Catena — fontes conflitantes,
  viagem já encerrada) em vez de veredito forçado.

## As 2 ressalvas (para a próxima sessão de manutenção · não bloqueiam nada hoje)

1. **Viagem NOVA bloqueia no gate 4d mesmo com factcheck honesto.** O frescor compara com o
   último commit do `data.json`; numa viagem nova ele nunca foi commitado → "anterior ao
   primeiro commit" → exit 1. Fail-closed (direção segura), mas vai travar o primeiro deploy
   da próxima viagem com mensagem confusa. Conserto barato: no gate, tratar "zero commits do
   data.json" + factcheck de hoje como o caso mesma-data (passa com ⚠), OU documentar no
   FACTCHECK-EXEC/deploy: "commite o data.json antes do primeiro deploy". Reproduzir:
   viagem nova não-commitada + factcheck válido → exit 1; após `git add+commit` → exit 0.
2. **`deploy.sh` falha-ABERTO se `factcheck-gate.py` sumir** ("⚠ pulando gate"). Pra gate de
   verdade, sumiço de script deveria bloquear (ou exigir `VIAGEM_SKIP_FCGATE=1` explícito).

Risco residual documentado e aceito: a **brecha-de-hoje** (edição sensível + factcheck datado
de hoje passam juntos, granularidade de dia) — confirmada no ataque A1b. É a troca declarada
por não exigir commit antes do gate; quem fecha é a auditoria recorrente e o campo.

## Estado do sistema após os 5 lotes

O que era protocolo de honra agora deixa rastro forjável-mas-detectável: artefato versionado
com veredito+fonte+data por item, gate de frescor por timestamp, fixture que documenta
executavelmente o que os gates NÃO cobrem, e nota rebatizada de FORMA. O ciclo
construtor→verificador→auditor rodou completo pela primeira vez — e produziu uma correção em
cada direção (executora corrigiu o auditor; auditor achou 2 furos operacionais da executora).
É este o regime de operação a manter.

---

# ADENDO · Auditoria de volta dos Lotes 6 e 7 (mesma data, rodadas posteriores)

## Lote 6 — APROVADO
6a reproduzido ao vivo no clone: viagem nova + factcheck de HOJE → exit 0 com ⚠ de
primeiro-deploy · factcheck de ontem → exit 1 com mensagem orientando. 6b: bloco fail-closed
no deploy com override `VIAGEM_SKIP_FCGATE=1`. Suite 29/29 (2 testes novos). A executora
anotou honestamente que os outros gates seguiam fail-open — virou o 7g.

## Lote 7 — APROVADO · todos os desvios endossados
Ataques da auditora (clone isolado):
- **7a-1 · o cenário original**: edit malicioso inline num card ⭐⭐⭐ do index.html →
  `sync-check` **bloqueia** (exit 1) apontando o campo. **7a-2**: edit inline na HISTORIA →
  bloqueia. **7a-3**: edit no cabeçalho → passa, e o gap é DECLARADO no script (linhas 32-37 +
  na própria mensagem de saída) — cobertura honesta, não fingida. Ordem dos gates correta
  (3b antes de tudo). Rebuild do marais: diff de exatamente 1 linha (ROTEIRO_SLUG), zero
  conteúdo perdido — conferido no commit.
- **7d**: `risco` intacto · `count_verdicts` só credita ⚠️ em doc que já usa 🏆/⏭️ (o desvio
  do "⚠️ cabeça d'água" foi a decisão certa — sem ela, levantamento sem crítica passaria no
  S2) · entrega antiga (roma-toscana) segue aceita.
- **7g**: fail-closed nos 2 gates restantes · `VIAGEM_SKIP_GATES` não alcança o fcgate
  (overrides separados, correto).
- **7f · a rede NÃO foi liberada — confirmado independentemente pela auditora** (curl na URL
  do Pages: 403 também nesta sessão). A mudança de política feita pelo Tobia não surtiu efeito
  no proxy — consistente com issues públicas de allowlist não aplicada no Claude Code web.
  O registro honesto (MEMORY re-testado e datado + FACTCHECK-EXEC exigindo declaração de
  nível página/snippet no artefato) é a resposta certa ao fato; nada a corrigir no repo.
- Suite 36/36 · sync-check verde nos 3 roteiros · commits 1-por-item como mandado.

## Errata aplicada pela auditora (item 5 do relato da executora — confirmado)
O CLAUDE.md documentava `deploy.sh` com 2 args; o script exige 3 (`"<msg>" "<subdir>"
"<slug>"`). Corrigido no bloco de exemplos do CLAUDE.md nesta rodada (verificado contra o
`Uso:` do próprio script). Era bug de doc pré-existente, fora do escopo do Lote 7 — a
executora fez certo em não tocar e reportar.

## Estado final do programa de auditoria (Lotes 1-7)
Fechados: nota-como-manchete · verificação sem rastro · gate 4d (com viagem nova) ·
fail-open em todos os gates · edit inline/burla do 4d · colisão de semáforos · fluxo sem
trilho · scout pulável em silêncio · schema de fontes sem tier · curadoria sem processo ·
laço de campo sem destino. Aberto e conhecido: rede do sandbox (403 — acionar suporte/testar
ambiente novo) · brecha-de-hoje do 4d (granularidade de dia, declarada) · cabeçalho fora do
sync-check (declarado) · itens ⭐⭐ só no re-check pré-viagem (declarado). Próximos gatilhos de
auditoria: primeira viagem nova no fluxo completo (roma-toscana set/2026) e os relatos de
campo dos pais.
