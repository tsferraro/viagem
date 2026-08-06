# HANDOFF · proposta: ledger de afirmações (o elo que falta entre pesquisa e escrita)

**Para**: sessão dedicada, a ser aberta pelo Tobia.
**Status**: PROPOSTA. Nada implementado. A sessão deve **discutir com o Tobia e obter aprovação
antes de escrever código** — ele pediu explicitamente que isto fosse decidido, não executado de
supetão.
**Origem**: sessão de 2026-08-04 (Tobia em viagem na Córsega, pegando erros em campo).

---

## 1. O problema, com evidência

Em 04/Ago o Tobia encontrou, de dentro do roteiro em uso, quatro erros da mesma família:

| Erro | Realidade |
|---|---|
| `"Loggia · mirador sul (falésias)"` — parada de walking tour com prosa sobre o calcário mudando de cor por 40min | **O mirante não existe.** "Loggia" é o pórtico da Sainte-Marie-Majeure, parada 3 do mesmo tour. Nome real, função inventada. Era rota que dois avós iam seguir no Maps |
| Cala Lazarina "ao norte da Lavezzi, 10min do desembarque" | Fica no **sudoeste**; a coord dada era da **Cala di Achiarinu** |
| "a Moby é o operador único" da rota Bonifacio–Santa Teresa | A **Ichnusa Lines** opera — e foi por ela que a mãe dele comprou |
| Stagno di Càbras: "maior população europeia de flamingos rosa", agosto como temporada | A colônia é **Molentargius, em Cagliari**, a 500km — e nem ela é a maior da Europa (é uma das três do Mediterrâneo ocidental). E o pico é **outono/inverno** |

**O padrão**: prosa confiante sobre geografia física e realidade comercial nunca vistas. E o
agravante — o card dos flamingos **tinha o campo `fontes` preenchido e passava no gate**, porque
alguém (esta sessão) anexou uma URL sem ler a fonte contra a frase.

---

## 2. O que JÁ existe no repo (não reconstruir)

O processo faseado **não está faltando** — está presente e foi pulado:

- `CLAUDE.md` · pipeline `mode create` em 10 passos
- `skills/destination-scout/SKILL.md` · explicitamente **"degrau 0"**: briefing → pesquisa →
  mapeamento → história → portão de qualidade → export
- `skills/critico-roteiro/` · `audit.py` (forma), `FACTCHECK.md` (verdade), `JUDGE.md` (substância)
- **REGRA ZERO** no `CLAUDE.md` (04/Ago): nada de memória, só fonte
- `FACTCHECK.md` **§0 EXISTÊNCIA** (04/Ago): 100% das paradas de WT e pontos de road trip, nunca amostra
- `audit.py` · `check_proveniencia()` e `check_claims_cobertos()` (04/Ago): cobra `fontes[].prova`
  claim-a-claim em 4 classes (superlativo · data histórica · número com unidade · época)
- Dívida congelada em `<viagem>/.proveniencia-debt.json` — **só encolhe**, `--baseline` recusa crescer

---

## 3. Por que ainda vaza — o diagnóstico

Duas constatações verificáveis hoje:

**(a) A fase é pulável sem consequência.** Não existe `entregas/sardenha*.md`. O roteiro dos pais
foi construído **sem o artefato de pesquisa**; os cards nasceram direto no `data.json`. A fase
existia no papel e ninguém a executou — e nada quebrou.

**(b) Mesmo executada, ela não vincula.** O artefato do scout é **prosa** (`.md` narrativo com
"Fontes" no fim). Prosa não responde à pergunta *"de onde veio esta frase?"*. Nada obriga o texto
do card a derivar dela. Quem escreve pode consultar o artefato ou a própria memória, e o resultado
sai idêntico na página.

Três peças são necessárias, e hoje falta a do meio:

| Peça | O que dá | Estado |
|---|---|---|
| **Ordem** (fases) | ler antes de escrever | existe · é pulável |
| **Material** (ledger) | o escritor só pode usar o que está lá | **NÃO EXISTE** |
| **Enforcement** (gate) | recusa afirmação sem origem | existe desde 04/Ago (`prova`) |

---

## 4. A proposta (a discutir, não a executar cegamente)

1. **`destination-scout` passa a emitir um LEDGER**, além da prosa: uma linha por afirmação, com
   `id`, texto da afirmação, fonte (órgão + URL), data da consulta e tier (`references/source-credibility.md`).
   A prosa continua — ela é o produto de leitura humana; o ledger é o produto de máquina.
2. **`prova` no card referencia o `id` da linha do ledger**, não uma string solta. Hoje
   `"prova": ["22 km²"]` é texto livre; passaria a ser `"prova": ["L-042"]` ou equivalente.
3. **`audit.py` recusa** (a) roteiro cujo slug não tem ledger correspondente e (b) `prova` que não
   resolve para uma linha existente. Com dispensa **explícita e registrada** para edit pequeno.
4. **A verificação continua fase separada e adversarial** (`FACTCHECK`). Não colapsar em "escrever
   ancorado" — quem escreve tem viés de confirmação sobre o próprio texto. Prova disso: o FACTCHECK
   rodou na Córsega na manhã de 04/Ago e **não pegou a Loggia**, porque §4a só olhava `mapsQuery`
   *nova* e a parada inventada não tinha `mapsQuery` nenhuma.

---

## 5. Perguntas de desenho que a sessão DEVE levar ao Tobia

Não decidir sozinha:

- **Onde o ledger vive?** `entregas/<slug>.ledger.json` · `<viagem>/ledger.json` · dentro do `.md`
  do scout como bloco estruturado? (afeta o fluxo de pesquisa avulsa pra terceiros, que hoje nunca
  vira app)
- **Migração**: os roteiros existentes (`corsica`, `pais-sardenha`, `marais`) têm ~116 itens de
  dívida somados e nenhum ledger. Gerar ledger retroativo? Ou ledger só para roteiro novo, com os
  antigos seguindo na dívida atual?
- **Granularidade**: uma linha por afirmação atômica, ou uma por fato-com-contexto? Atômica demais
  vira burocracia; grossa demais volta ao problema de hoje.
- **Custo**: a verificação de verdade mudou o veredito de ~1 em cada 5 itens em 04/Ago. Isso é
  caro. O ledger deve cobrir 100% ou só o que tem **consequência física** (paradas de tour, road
  trip, restaurante em dia específico)?
- **Priorização** — o Tobia propôs uma fase de priorização. O critério que emergiu do campo é
  **consequência física**, não importância: o que faz alguém andar, dirigir ou reservar num dia
  específico vem antes do que a pessoa só lê. Confirmar com ele.

---

## 6. Restrições duras

- ⛔ **Não zerar nem afrouxar a dívida.** `corsica/.proveniencia-debt.json` e
  `pais-sardenha/.proveniencia-debt.json` só encolhem. Se a mudança exigir re-freeze, isso é
  decisão do Tobia, não conveniência de implementação.
- ⛔ **Os dois roteiros estão EM USO em campo** (Tobia até 08/Ago, pais 06→21/Ago). Nenhuma mudança
  pode bloquear o deploy de uma correção urgente vinda do campo — foi por isso que o mecanismo de
  dívida existe.
- ⚠️ **Há outra sessão ativa no `pais-sardenha`** fechando dívida de proveniência. Ela depende do
  `audit.py`. Combine sequenciamento com o Tobia antes de mexer na régua.
- `git pull` antes de tocar em qualquer arquivo.

---

## 7. Como saber se funcionou

O teste não é "o gate passa". É:

1. Reconstrua o card do Stagno di Càbras como estava (com `fontes` colado e sem leitura) → o
   sistema tem que **recusar**.
2. Crie um card novo com um superlativo qualquer → tem que recusar até a afirmação resolver para
   uma linha de ledger.
3. Pule a fase de pesquisa e tente construir um roteiro → tem que **quebrar**, com mensagem clara.
   *Se pular a fase não quebra nada, a fase não existe* — é a lição central deste handoff.

---

## 8. Leitura obrigatória antes de propor qualquer coisa

- `CLAUDE.md` · REGRA ZERO e a seção "Anexar fonte NÃO é verificar"
- `skills/critico-roteiro/FACTCHECK.md` · §0 EXISTÊNCIA
- `skills/critico-roteiro/audit.py` · `check_proveniencia()` e `check_claims_cobertos()`
- `skills/destination-scout/SKILL.md` · PASSO 2 a 4b
- `decision-log.md` · entrada de 2026-08-04
- `corsica/DIARIO.md` · os erros de campo e o padrão deles
