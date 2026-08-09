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
