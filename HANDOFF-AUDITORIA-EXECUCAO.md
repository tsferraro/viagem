# HANDOFF · Execução das recomendações da auditoria (R3-R13 + N12-N16)

**Papéis** (decisão de arquitetura, não burocracia): a sessão que LÊ este handoff é a
**EXECUTORA**. Ela implementa e entrega. Quem verifica é a **sessão AUDITORA** (a que escreveu
`AUDITORIA-RELATORIO-2026-08-08.md`), numa rodada posterior, adversarialmente — inclusive
tentando burlar os gates novos. A executora NÃO se auto-aprova: entrega com os critérios de
aceite abaixo verdes e PARA. A causa-raiz nº 1 da crise foi verificação sem testemunha; este
fluxo é o antídoto. Não "melhore" nada fora do escopo de cada lote sem registrar no commit.

**Leitura obrigatória antes de começar**: `AUDITORIA-RELATORIO-2026-08-08.md` (seções 3, 4, 5)
+ `AUDITORIA-DOSSIE-2026-08-04.md`. O anexo `AUDITORIA-ANEXO-bosa-falsa.json` é o roteiro
sintético 100% falso que atravessou todos os gates — vira fixture no Lote 1.

**Regras de segurança** (valem em todos os lotes):
- `corsica/` e `pais-sardenha/` estão EM USO. Lote 4 é o único que toca conteúdo deles, e só
  no que está listado. `git pull origin main` antes de cada lote e antes de cada push.
- `<viagem>/.proveniencia-debt.json` SÓ ENCOLHE. Nunca regravar baseline com item novo.
- Cada lote = 1 commit (ou poucos) + push na main ao final do lote (repo serve da main).
- Se um critério de aceite não fechar, NÃO contorne o critério — registre o bloqueio no
  commit/entrega e siga pro próximo lote.

**Decisões do Tobia embutidas (defaults)** — executar assim, a menos que ele diga o contrário:
1. R3: a nota /40 passa a se chamar "forma" e sai da manchete das entregas (fica no rodapé).
2. R8: cota editorial vira "2 opções VERIFICADAS por refeição são suficientes; a 3ª é opcional
   e só entra verificada" (documentar no CLAUDE.md; não mexer em roteiros existentes).
3. R9: ledger NÃO será implementado. Só: campo `tier` + `data` no schema de `fontes`.

---

## LOTE 1 · Ferramentas + fixture + reframing (mecânico · 1 sessão)

**1a · R4 — bugs do `audit.py`** (paths/linhas na seção 1 do relatório e no código atual):
- Unificar as listas de auditores de `main()` e `audit_roteiro()` (UMA fonte de verdade; o
  comentário em ~2081 admite a duplicação). Consequência a corrigir junto: `--diff` deve
  passar `debt` a `check_proveniencia`/`check_claims_cobertos` (hoje 1346-47 sem debt vs
  2085-86 com — severidades infladas no diff).
- `--json`: NENHUMA linha fora do objeto JSON no stdout (a linha de dívida em ~2108-2110 vaza).
- D6 (~723-733): o loop `for day in [days[0], days[-1]]` tem `break` incondicional — o último
  dia nunca é examinado e o `else` dá +1 grátis. Corrigir e re-calibrar se a nota das fixtures
  mudar (atualizar fixtures com o motivo no commit, não afrouxar o check).
- Comentário ~812-814: AFIRMA que o regex cobre "mais ao sul" e "mirante" — não cobre. Corrigir
  o comentário para dizer o que o regex realmente pega e o que fica pro FACTCHECK (não tentar
  cobrir função/posição por regex — o relatório §3 explica por quê).
- `maps-audit.py`: novo check — **coordenada idêntica em stops distintos** do mesmo walking
  tour ou do mesmo dia (pega o caso Tophet/MAB, que passou invisível porque a rota vai por
  nome). Severidade: bloqueia como os outros checks do maps-audit.
- Bug documentado no MEMORY (L195): `coord_4dec` usa `str()` e lê `41.8440` como 3 casas —
  consertar via decimal/string bruta do JSON ou tolerância documentada.

**1b · R5 — fixture de conteúdo falso**: mover/copiar `AUDITORIA-ANEXO-bosa-falsa.json` para
`skills/critico-roteiro/tests/fixtures/` e adicionar teste que TRAVA o comportamento atual
documentado: "este arquivo 100% falso é APROVADO pelos gates" (assert nota ≥32 e P0=0). O
teste existe pra: (a) impedir comentário futuro de falsa cobertura; (b) quebrar de propósito
no dia em que alguém implementar um check que o pegue — aí o teste é atualizado com festa.

**1c · R3 — nota vira rodapé**: na saída do `audit.py`, renomear a linha final pra deixar
explícito: `★ FORMA: NN/40 (não mede verdade — ver FACTCHECK)`. No `CLAUDE.md`, pipeline
passo 10: trocar "reportar nota" por "reportar placar do factcheck (X confirmados / Y
corrigidos / Z inconclusivos) + nota de forma no rodapé".

**Aceite do Lote 1** (a auditora vai rodar exatamente isto):
```bash
python3 skills/critico-roteiro/audit.py pais-sardenha/data.json --json | python3 -c "import json,sys; json.load(sys.stdin)"  # sem erro
python3 skills/critico-roteiro/audit.py pais-sardenha/data.json --diff pais-sardenha/data.json  # self-diff: mesmas severidades do modo normal, exit 0
python3 skills/critico-roteiro/tests/run_tests.py    # verde, incluindo a fixture bosa-falsa
python3 scripts/maps-audit.py <fixture com coord repetida>  # exit 1
grep -n "mais ao sul" skills/critico-roteiro/audit.py  # comentário honesto
```

## LOTE 2 · R6 — verificação vira artefato (o coração · 1-2 sessões)

Implementar o FACTCHECK como **execução com rastro**, não protocolo de honra:
1. Novo modo em `skills/critico-roteiro/`: a sessão construtora dispara **sub-agentes céticos**
   (contexto limpo, sem o texto de justificativa do construtor) que verificam por estrato
   (restaurantes×dia · cards ⭐⭐⭐ · paradas de WT/coords · historia[] · logística) — o desenho
   é a Fase 1 do relatório, que custou ~130 buscas pra ~90 afirmações.
2. O resultado persiste em `<viagem>/FACTCHECK-<AAAA-MM-DD>.md`, versionado: item → veredito
   (OK/ERRO/RISCO/INCONCLUSIVO) → fonte(s) com URL → data. Erros viram correções ANTES do deploy.
3. `deploy.sh` ganha gate de FRESCOR (cobrável por timestamp, não por conteúdo — não é gameable
   por substring): bloqueia se (a) não existe `FACTCHECK-*.md` pra viagem, ou (b) o mtime/data
   do último factcheck é ANTERIOR ao último commit que alterou `sobre|imperdivel|dicas|opcoes|
   historia|coord` de item ⭐⭐⭐/WT no `data.json` (comparar via `git log -1 --format=%ct` do
   data.json vs data no nome do arquivo). Edit pequeno em item não-⭐⭐⭐ não bloqueia.
4. Documentar no `CLAUDE.md` (substitui a linha "FACTCHECK lean" do pipeline): quem escreveu
   NÃO roda o próprio factcheck no mesmo contexto — despacha sub-agentes ou pede sessão nova.

**Aceite do Lote 2**: a auditora vai (a) editar um card ⭐⭐⭐ num clone e confirmar que o
deploy BLOQUEIA sem factcheck novo; (b) tentar burlar o gate sem fazer verificação real (ex.:
tocar o arquivo de factcheck sem conteúdo) — o gate deve exigir pelo menos formato válido com
vereditos por item; (c) conferir que o FACTCHECK gerado numa viagem-teste lista fonte por item.

## LOTE 3 · R7/R9 — padrões de prova + schema de fontes (1 sessão)

- `references/source-credibility.md`: adicionar padrões de prova pras 5 classes que mataram
  (tabela na seção 5-R7 do relatório): existência · função de lugar · posição/por-onde-anda ·
  dia-de-fechamento×data (2 diretórios concordantes OU site próprio; divergiu → telefone no
  card) · regra de acesso (busca de notícia <12 meses obrigatória pra praia/sítio italiano).
- Coordenada: regra dura no `CLAUDE.md` — coord de item periférico é COPIADA de fonte com o 5º
  decimal ou entra `coord_unverified: true`. Proibido derivar "perto de X" (5 coords erradas
  na amostra da auditoria eram todas derivadas; as copiadas estavam 100% certas).
- Schema `fontes`: unificar os 3 formatos divergentes (source-credibility.md:61 ·
  data-schema.md:65 · formato real {o,u,prova}) num só: `{o, u, tier, data, prova[]}` com
  `tier ∈ {oficial, editorial, campo, diretorio, crowd}` · `audit.py` passa a AVISAR (P3)
  fonte sem tier/data em item novo — sem quebrar os dados existentes.
- R8 no `CLAUDE.md`: cota editorial "2 opções verificadas > 3 plausíveis".

**Aceite**: `grep` das 5 classes no source-credibility.md · fixture com fonte sem tier gera P3
· data-schema.md e source-credibility.md descrevem o MESMO formato.

## LOTE 4 · Conteúdo pendente (N12-N16 + R12 · 1 sessão · ÚNICO lote que toca roteiro em uso)

Fontes já apuradas na seção 2.4/2.7 do relatório — não re-pesquisar do zero, CONFERIR e aplicar:
- `corsica/data.json` historia[4]: (a) reescrever o trecho da "Loggia mirante" (a Loggia é o
  pórtico da Sainte-Marie — o §3 do próprio bloco já diz certo); (b) adicionar a queda de
  1553 (Dragut + esquadra francesa + Sampiero Corso; devolução a Gênova em 1559) — o título
  "resistiu cinco meses" precisa deixar de ser meia-verdade. Adicionar `fontes` ao bloco.
- `pais-sardenha` historia[]: "Carlos, o Forte"→"Forte de Carlo" · "o museu mais visitado"→
  "um dos mais visitados" · "nunca abandonada/2.800 anos ininterruptos"→ relativizar (houve
  despovoamento até o séc. XVIII) · remover "quem parou o relógio foi Menotti" (sem fonte) ·
  "26 estátuas"→ "25 estátuas remontadas (+2 em 2026; contagens variam com os novos achados)"
  — também no card do museu · "500 t/h"→"~400 t/h (fonte oficial do parque)" · tophet: Tanit
  E Baal Hammon.
- R12: `AUDITORIA-DOSSIE-2026-08-04.md` — anotar (não apagar; é registro histórico) que #4
  (La Bobba ~3km fora) e "500km" (§2.4) foram REFUTADOS pela auditoria; corrigir o "a 500km"
  no `CLAUDE.md` (seção do `prova`) pra "~100km". Registrar 1 linha no `decision-log.md`: o
  post-mortem também errou por afirmar sem checar.
- Rebuild + gates + deploy main (mesmo pipeline da rodada de correções urgentes).

**Aceite**: grep "1553" em corsica/data.json retorna ≥1 · grep "500km"/"500 km" no CLAUDE.md
retorna 0 · audit das 2 viagens sem P0 · dívidas intocadas ou menores.

## LOTE 5 · R10/R13/R11 — curadoria de fontes + laço de campo (1 sessão)

- Criar skill `skills/curadoria-fontes/SKILL.md` a partir da **seção 6 do relatório** (o
  desenho está pronto: registro por fonte, estados candidata→em-teste→validada→rebaixada
  movidos SÓ por evento, queries de identificação por perfil, checklist "esteve lá", tabela
  de priorização por tipo de afirmação).
- Criar `fontes/registro.json` com as 8 candidatas da seção 6.6, TODAS em estado `candidata`
  com o evento de entrada apontando pra auditoria. (`fontes/` não é subpasta de viagem — se o
  `regen-landing.py` a detectar como viagem, ajustar a detecção pra exigir `index.html`.)
- Ligar o laço: no `CLAUDE.md`, o roteamento de relato de campo ganha a linha "…e anote o
  evento no registro da fonte que originou o item confirmado/demolido". Wrap-up ganha o passo
  "quais fontes embarcaram/validaram/demoliram nesta viagem?".
- R13: criar `pais-sardenha/DIARIO.md` (esqueleto com os dias, como o da corsica).
- R11: registrar no `CLAUDE.md` o gatilho de re-check pré-viagem (7-10 dias antes, só
  operacional) — próxima aplicação real: roma-toscana set/2026, cujo scout tem 12 correções
  conhecidas e nunca aplicadas (`entregas/roma-toscana-*.FACTCHECK.md`).

**Aceite**: skill invocável e coerente com a seção 6 · registro.json parseável, 8 candidatas,
zero `validada` · landing NÃO lista "fontes" como viagem · DIARIO.md dos pais existe.

---

## LOTE 6 · Refinamentos da auditoria de volta (2026-08-09 · `AUDITORIA-VOLTA-2026-08-09.md`)

Os Lotes 1-5 foram APROVADOS. A auditoria de volta achou 2 ressalvas operacionais — ambas
fail-closed, nenhuma urgente, mas a nº 1 VAI travar o primeiro deploy da próxima viagem nova.

**6a · Gate 4d bloqueia viagem NOVA legítima.** Em `scripts/factcheck-gate.py`, o frescor
compara a projeção atual com a do último commit do `data.json` — que numa viagem nova nunca
existiu → "anterior ao primeiro commit" → exit 1 mesmo com factcheck honesto de hoje.
Conserto: quando `git rev-list` não devolve NENHUM commit pro `data.json` E `fc_date ==
date.today()`, tratar como o caso mesma-data (passa com ⚠ "viagem nova · primeiro deploy ·
confira que o factcheck cobre tudo"); se o factcheck NÃO é de hoje, continuar bloqueando, mas
com mensagem que diz o caminho ("viagem nova sem commit do data.json: rode o factcheck HOJE ou
commite o data.json antes do deploy"). Documentar o comportamento no bloco "O QUE BLOQUEIA" do
docstring e em `skills/critico-roteiro/FACTCHECK-EXEC.md`.
Reprodução (do ataque da auditora, num clone): viagem nova não-commitada + factcheck válido de
hoje → HOJE exit 1 (bug) · após `git add+commit` do data.json → exit 0.

**6b · `deploy.sh` falha-ABERTO se `factcheck-gate.py` sumir.** Hoje: "⚠ pulando gate".
Pra gate de verdade, ausência do script BLOQUEIA (exit 1), com override explícito e ruidoso:
`VIAGEM_SKIP_FCGATE=1` no env pula com aviso gritante. Aplicar o mesmo padrão aos outros
scripts de gate chamados pelo deploy (se algum tiver o mesmo `if [ -f ]`... senão, só o 4d).

**Aceite do Lote 6** (a auditora vai rodar):
```bash
# 6a — num clone: mkdir viagem-x + data.json válido NÃO commitado + FACTCHECK-<hoje>.md válido
python3 scripts/factcheck-gate.py viagem-x            # exit 0 com ⚠ de primeiro-deploy
# mesmo cenário com FACTCHECK de ontem                # exit 1 com mensagem orientando
python3 skills/critico-roteiro/tests/run_tests.py     # suite verde (adicionar fixture do caso)
# 6b — renomear factcheck-gate.py temporariamente e rodar deploy.sh em dry-run/clone: bloqueia
# com VIAGEM_SKIP_FCGATE=1: passa com aviso
```
Regra de sempre: 1 commit por item, push na main, nada fora do escopo, não se auto-aprovar.

---

## Protocolo de auditoria de volta (o que a AUDITORA vai fazer — transparência total)

1. Rodar todos os comandos de aceite acima, verbatim.
2. **Ataque aos gates novos**: tentar aprovar a fixture bosa-falsa no deploy com um
   FACTCHECK-*.md forjado (vazio, sem vereditos, com data adiantada) — o gate de frescor+formato
   deve recusar; tentar novamente o gaming por substring no `prova` — deve continuar passando
   no audit (isso é ESPERADO: regex não prova verdade) mas ser pego pelo factcheck-artefato.
3. Amostra de verificação factual nova (~15 itens) sobre qualquer conteúdo alterado no Lote 4.
4. Relatório curto: aceite por lote · o que quebrou · regressões.

**Como iniciar a execução** (Tobia): abrir sessão nova no repo e colar —
> Você é a sessão EXECUTORA do `HANDOFF-AUDITORIA-EXECUCAO.md` (raiz do repo). Leia-o
> inteiro, depois execute os lotes EM ORDEM (1→5), um commit por lote, push na main ao fim de
> cada um. Não se auto-aprove: pare quando os critérios de aceite estiverem verdes e liste o
> que ficou bloqueado. Não altere conteúdo de roteiro fora do Lote 4.

**Como iniciar a auditoria de volta** (Tobia, depois): sessão nova —
> Você é a sessão AUDITORA. Rode o "Protocolo de auditoria de volta" do
> `HANDOFF-AUDITORIA-EXECUCAO.md` contra o estado atual da main e reporte.
