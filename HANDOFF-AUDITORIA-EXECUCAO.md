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

## LOTE 7 · Fluxo com trilho + furos da 2ª rodada (aprovado pelo Tobia em 2026-08-09)

Contexto: o Lote 6 foi executado e ACEITO pela auditora. Esta rodada fecha os furos que a
auditora achou respondendo às perguntas de fluxo do Tobia + dá acabamento de UX ao pipeline.
Ordem interna: 7a primeiro (é o furo de segurança), depois 7g, depois o resto.

**7a · MATAR o edit inline no HTML + sync-check no deploy — o furo sério.**
O CLAUDE.md (pipeline ajuste, passo 3) manda editar "inline o `const DAYS`" pra mudanças
pequenas. Isso (i) dessincroniza `data.json`↔`index.html` (drift já documentado no
HANDOFF-PENDENTE) e (ii) **burla o gate 4d**: o `factcheck-gate` projeta o conteúdo sensível
do `data.json` — um edit inline muda o que a família LÊ sem mudar a projeção, e o gate passa.
Fazer: (1) CLAUDE.md: TODA mudança de conteúdo edita o `data.json` e roda `build.py`
(o build leva segundos; o "atalho" inline morre — registrar a decisão no decision-log com este
motivo); (2) `deploy.sh` ganha check de SINCRONIA antes dos gates: rebuild do `data.json` da
viagem em arquivo temporário e diff contra o HTML que vai pro ar — divergência = BLOQUEIA com
mensagem "index.html não veio do data.json · rode build.py" (se o build não for
byte-determinístico, comparar uma projeção estável — ex.: os blocos JSON extraídos — e
documentar o método no próprio script); (3) verificar os 3 roteiros atuais (corsica ·
pais-sardenha · marais): se algum `index.html` estiver dessincronizado do seu `data.json`,
REBUILD + validate + commit (conferindo antes, no diff, que o rebuild não perde nada que só
exista no HTML — se existir conteúdo órfão no HTML, ele volta pro data.json primeiro).

**7b · Fluxo vira TRILHO apresentado, não só documentação.**
CLAUDE.md ganha uma seção curta "Mapa de fases" (viagem nova: Pesquisa → Construção → Forma →
Verdade → Deploy → Campo) com 1 linha por fase: objetivo · o que a fase pede ao Tobia · o gate
que a fecha. E a instrução de conduta: **ao ENTRAR numa fase, a sessão anuncia** "fase X de Y
· objetivo · decisões que vou te pedir"; **ao SAIR, anuncia** o que fechou, o que ficou
pendente do Tobia e qual é a próxima fase. Sem burocratizar: é UMA seção enxuta + 2 frases de
conduta, não um formulário. As perguntas de briefing continuam uma-por-vez; a fase de pesquisa
inclui explicitamente o passo de curadoria de fontes (15-20min, skill `curadoria-fontes`).

**7c · Scout-gate soft no deploy de viagem nova.**
`deploy.sh`: quando o subdir da viagem é NOVO (primeiro deploy) e não existe
`entregas/<slug>*.md`, imprimir aviso duro ("viagem nova sem levantamento scout — Córsega e
Sardenha nasceram assim e o resultado está na auditoria de 2026-08-08"); `VIAGEM_STRICT=1`
bloqueia. Não bloquear por default: mini-roteiro/coletânea legítimos existem.

**7d · Fim da colisão de semáforos.**
O veredito do scout (🟢🟡🔴 = entra/talvez/pula) usa as MESMAS cores do `risco` do roteiro
(🟢🟡🔴 = atrito), significando outra coisa. Trocar o vocabulário do VEREDITO do scout para
**🏆 entra · ⚠️ talvez · ⏭️ pula** em `skills/destination-scout/SKILL.md`, no template de
entrega e nas referências do modo `--scout` (content-rubric). O `audit.py --scout` aceita os
DOIS vocabulários (entregas antigas não quebram). Roteiros/`risco` não mudam nada.

**7e · Duas linhas de doc que faltam.**
(1) FACTCHECK-EXEC.md + CLAUDE.md: deixar explícito que o frescor do gate 4d cobre
⭐⭐⭐/WT/historia — **itens ⭐⭐ são cobertos só pelo re-check pré-viagem (R11)**, escolha
deliberada de escopo. (2) CLAUDE.md, fim do pipeline: **cadência da auditoria externa = a cada
viagem nova entregue** (sessão auditora independente, não o construtor), além do re-check
pré-viagem.

**7f · Rede liberada: o factcheck sobe de nível.**
O Tobia liberou a política de rede do ambiente (2026-08-09). Fazer: (1) testar na própria
sessão: `WebFetch` numa página real (ex.: comune.bosa.or.it) e `curl -sI` na URL do Pages —
registrar o resultado; (2) se funcionou: atualizar a entrada "Sandbox cloud · rede externa" do
MEMORY.md (o fato mudou; anotar data e o que segue bloqueado, se algo seguir) e atualizar
FACTCHECK-EXEC.md: com rede, verificação é **nível-página** (abrir a fonte e ler contra a
afirmação) — snippet de busca vira fallback declarado, não padrão; `--check-links` volta a ser
viável em cloud (tirar a nota de "inútil em sessão cloud" onde estiver); (3) se NÃO funcionou
(issues conhecidas de allowlist não aplicada): registrar exatamente o que foi testado e o
erro, e avisar o Tobia na entrega — não fingir que abriu.

**7g · Fail-closed nos DOIS gates que sobraram.**
`deploy.sh` linhas ~71 e ~83: `critico-roteiro` e `maps-audit.py` ausentes ainda "pulam" o
gate. Aplicar o padrão do 6b: ausência = BLOQUEIA · override explícito `VIAGEM_SKIP_GATES=1`
(um só, ruidoso, cobrindo os dois — manter `VIAGEM_SKIP_FCGATE` como está).

**Aceite do Lote 7** (a auditora vai rodar):
```bash
# 7a — num clone: editar index.html inline (1 char em DAYS) → deploy BLOQUEIA por dessincronia;
#      editar data.json + build → passa · e os 3 roteiros atuais passam no sync-check
# 7b — grep "Mapa de fases" CLAUDE.md · seção existe, ≤30 linhas, com gates nomeados
# 7c — clone: subdir novo sem entregas/ → deploy avisa · VIAGEM_STRICT=1 → bloqueia
# 7d — grep "🟢" skills/destination-scout/SKILL.md → 0 no VEREDITO (risco não muda) ·
#      audit --scout numa entrega antiga (roma-toscana) continua passando
# 7e — greps das 2 linhas novas
# 7f — saída do teste de rede registrada na entrega + MEMORY/EXEC coerentes com o resultado
# 7g — clone: renomear maps-audit.py → deploy bloqueia · VIAGEM_SKIP_GATES=1 → passa gritando
python3 skills/critico-roteiro/tests/run_tests.py   # verde, com fixtures novas do 7a se couber
```
Regra de sempre: 1 commit por item, push na main ao final, aceites verdes, não se auto-aprovar,
e NENHUMA mudança de conteúdo de roteiro fora do rebuild do 7a-(3).

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
