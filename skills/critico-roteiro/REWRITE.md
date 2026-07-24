# REWRITE · elevar a prosa ao padrão-ouro Marais (protocolo)

Fase D do grader→router. O `audit.py --suggest` roteia pra estação ✍️ **reescrever** os cards onde o **fato existe mas a escrita é fraca** (`sobre` raso, `imperdivel` genérico, `dicas` sem narrativa). Este protocolo diz como reescrever no padrão-ouro **Marais** — postura de guia de free walking tour que precisa **encantar pra ganhar a gorjeta**. É executado pelo Claude (não é script): reescrever bem é julgamento de escrita, não regex.

> **Grava direto** (decisão Tobia 2026-07-02): reescreve e salva no `data.json` sem pedir aprovação card-a-card — as redes automáticas seguram o objetivo; o Tobia pede ajuste se quiser. Travar a cada card mata o fluxo.

Régua de escrita: `references/content-rubric.md` D1 + o exemplar `marais/`.

## Quando roda (gatilhos)

| Situação | Escopo |
|---|---|
| **Depois da Fase C** | os cards que a pesquisa 🔎 acabou de municiar com fato → agora têm o quê contar, falta escrever |
| **Aprofundar roteiro** | os cards ✍️ do `--suggest` (fato já existe, prosa fraca) |
| **Card novo com fonte** | acabou de entrar com dado bom mas descrição de schema |
| Card já no padrão | **não mexe** — reescrever o que já encanta é risco sem ganho |

## O padrão Marais (as 3 regras de ouro)

| Campo | ❌ Raso (schema preenchido) | ✅ Marais (encanta pra gorjeta) |
|---|---|---|
| **`sobre`** | "Praça bonita e histórica, ótima pra passear." | **conta a história** com fato concreto (data, personagem, lenda, "por que isso existe"). HTML cru `<strong>`/`<em>`, **nunca** markdown `**` |
| **`imperdivel`** | "Imperdível!" / "Incrível!" | **o que OBSERVAR** — o detalhe que o distraído perde (a bala de canhão na fachada, o pavilhão mais alto, os Cavalos de Apolo) |
| **`dicas`** | "Vá cedo", "Leve a câmera" | **narram parada-a-parada** com hora/preço/atalho concreto; numa walking tour, guiam de pino em pino |

### Exemplo antes → depois
*(fatos ilustrativos — numa reescrita real vêm da Fase C com proveniência)*

**Antes** — `sobre`: `"Uma praça muito bonita e histórica de Paris, ótima para passear."` · `imperdivel`: `"Imperdível!"`

**Depois** — Place des Vosges (Marais):
```json
"sobre": "A <strong>praça mais antiga de Paris</strong>, inaugurada em <strong>1612</strong> como Place Royale. As 36 casas de tijolo rosa são idênticas de propósito — simetria era status. <strong>Victor Hugo</strong> morou no nº 6 (hoje museu, coleção gratuita) e escreveu ali parte de Os Miseráveis.",
"imperdivel": "Repare que o Pavilhão do Rei (sul) e o da Rainha (norte) são mais altos que as outras 34 casas — só a realeza podia furar a simetria.",
"dicas": [
  "Museu Victor Hugo (nº 6): grátis e quase sempre vazio — 30min tranquilos com a criança",
  "Os arcos dão sombra no verão e abrigo na chuva — volta natural pro carrinho",
  "Piquenique no gramado central é liberado; padaria na esquina da Rue de Birague"
]
```

## Método (por card · grava direto)

1. **Reúne o fato** — o que a Fase C trouxe (com proveniência) ou o que já estava no card. **Sem fato novo, não inventa** — ver anti-Goodhart abaixo.
2. **Reescreve** os 3 campos no padrão Marais. HTML cru. Mantém intacto o que o mecânico exige: **endereço entre parens no `nome`**, ano/data no `sobre` (o `<strong>1612</strong>` que o D1 procura já vem da história de verdade, não salpicado).
3. **Grava direto** no `data.json` (não no HTML). Preserva os outros campos.
4. **Fecha o loop (rede, não portão)**:
   ```bash
   python3 skills/critico-roteiro/audit.py <viagem>/data.json --diff <backup-antes>.json
   ```
   - **Regressão mecânica** (tirou sem querer o parens, o ano, quebrou schema) → exit 1 → **conserta antes de seguir**. Isso é objetivo, não gosto.
   - Julgamento subiu, mecânico estável → segue. O Tobia revê a prosa se quiser.
5. **JUDGE nos cards tocados** (1× no fim, não card-a-card) — a prosa ficou melhor de **verdade** ou só bateu o proxy? É o único juiz de substância; o `--diff` só garante que não regrediu a forma.

## Anti-Goodhart (a guarda que governa a fase)

O alvo é **a história**, não o número do D1. Perseguir "150 chars + um ano de 4 dígitos" é o modo de falha clássico:

- **Não encher linguiça** pra bater o comprimento. `sobre` de 90 chars com um fato bom > 200 chars de floreio.
- **Não salpicar data** só pro `FACT_RE` acender. O ano entra porque é parte da história que a família vai ouvir, ou não entra.
- **Sem fato, card fica "raso mas honesto"** — marca e segue. É melhor que inventar uma lenda pra ter o que escrever. Se dá pra encantar, encanta; se não dá, não finge.
- **"Paraíso indescritível" = zero informação.** Todo adjetivo sem fato atrás é candidato a corte.

## O que enforça (não é honra)

| Camada | Pega | Instrumento |
|---|---|---|
| **Forma HTML** | markdown cru (`**bold**`) em vez de `<strong>` | `validate.py` (bloqueia deploy) |
| **Não-regressão** | tirou parens/ano/schema sem querer | `audit.py --diff` (mecânico não pode cair) |
| **Substância** | a prosa melhorou ou só inflou o proxy? | `JUDGE.md` (nos cards tocados) |

Ordem do ciclo completo: **research (C) → rewrite (D) → --diff → factcheck → judge**. O `--diff` é a trava barata entre lotes; factcheck/judge rodam 1× na entrega.
