# RESEARCH · executar a fila 🔎 com contrato anti-invenção (protocolo)

Fase C do grader→router. O `audit.py --suggest` roteia achados pra estação 🔎 **pesquisar** — este protocolo diz como **executar** essa fila e escrever o fato de volta no `data.json` **sem inventar**. É executado pelo Claude (não é script): a pesquisa é agêntica; o que o código faz é *verificar* o resultado (metade mecânica + `--diff`).

> ⚠️ **Este é o ponto de maior risco do roadmap.** É aqui que um preço/coord/URL alucinado entra num documento que a família abre **no meio da rua**. O contrato abaixo é gate, não sugestão.

Régua de fontes: `references/source-credibility.md` (tiers T1-T5 + padrões de prova).

## Quando roda (gatilhos)

| Situação | Escopo |
|---|---|
| **Aprofundar roteiro** (subir nota, preencher gaps) | só os achados 🔎 do `--suggest` da sessão |
| **Viagem nova** | a fila 🔎 inteira do 1º audit, antes do FACTCHECK/JUDGE |
| **Pré-viagem** | só os 🔎 de fato operacional (preço/horário) — o resto não apodrece |
| Edit pequeno (1 dica, 1 stop) | **não roda** — conserta na mão, é mais barato |

## Entrada: a fila 🔎 machine-readable

```bash
python3 skills/critico-roteiro/audit.py <viagem>/data.json --suggest --json \
  | python3 -c "import json,sys; [print(f['stop'],'·',f['msg']) for f in json.load(sys.stdin)['findings'] if f['station']=='🔎']"
```

Cada achado 🔎 traz `stop` (qual card), `msg` (o gap) e `hint` (a busca a fazer + como gravar). Trabalha-se a fila priorizando pelo `--suggest` (top-5 cards · âncora antes de filler).

## O contrato anti-invenção (gate de escrita)

Todo valor pesquisado só entra no `data.json` se passar. **Sem exceção "quase certo".**

| Campo | Só grava se | Não confirmou → |
|---|---|---|
| **Preço** (`custo`) | tem fonte **E** data → grava com `(mês/ano)` | `[a confirmar]` |
| **Coord** (`coord`) | veio de web_search real, 4 casas | `coord_unverified: true` (NUNCA chuta "perto de X") |
| **URL** (`links_map`) | responde **2xx no momento da escrita** | omite a entrada (link ausente > link morto) |
| **Fato** (`sobre`/`dicas`) | fonte T1-T3 registrada | `[a confirmar]` no texto, não afirma |
| **Horário/reserva** | fonte oficial (site da atração) | `[a confirmar]` |

Princípio (herdado do CLAUDE.md · destination-scout): **preço sem data apodrece e vira armadilha silenciosa; coord chutada manda a família pro lugar errado.** O `[a confirmar]` explícito é honesto; o chute é o pecado.

## Método (por lote de ~5-8 cards)

1. **Pesquisa** — web_search por card (nome + o dado que falta). Anota o valor **e a URL da fonte e a data da consulta** (a proveniência é obrigatória, é o que o FACTCHECK vai auditar depois).
2. **Aplica o contrato** — cada valor passa pela tabela acima antes de virar linha no `data.json`. Não passou → `[a confirmar]` / `coord_unverified`.
3. **Write-back** — edita o `data.json` (nunca o HTML direto). Preserva o que já estava bom.
4. **Fecha o loop (obrigatório)**:
   ```bash
   python3 skills/critico-roteiro/audit.py <viagem>/data.json --diff <backup-antes>.json
   ```
   - **Mecânico não pode cair.** Se caiu, o lote quebrou algo objetivo → reverte e investiga.
   - `--diff` mostra resolvido / novo / intacto. "Novo" mecânico = efeito colateral a corrigir antes de seguir.
5. **Re-suggest** — roda `--suggest` de novo; a fila 🔎 deve ter encolhido. O que sobrou vai pro próximo lote (máx ~3 lotes; se não converge, o gap é de fonte, não de formato — leva pro Tobia).

## O que ENFORÇA o contrato (não é honra)

O contrato não depende de disciplina — é verificado por peças que já existem:

| Camada | Pega | Instrumento |
|---|---|---|
| **Forma** | preço sem `(mês/ano)`, coord sem flag, URL morta | `audit.py` metade mecânica (D3/D4/D5) + `--diff` |
| **Verdade** | o preço/coord/fato confere na fonte citada? | `FACTCHECK.md` (roda **depois** do lote) |
| **Substância** | a pesquisa melhorou o roteiro ou só encheu campo? | `JUDGE.md` (1× na entrega) |

Ordem: **research → --diff → factcheck → judge**. O `--diff` é a trava barata entre cada lote; o factcheck/judge rodam 1× no fim.

## Anti-Goodhart (a mesma guarda da Fase A)

A fila 🔎 existe pra **preencher gap real**, não pra subir número. Pesquisar a data de fundação de um card só pra o D1 achar um "ano de 4 dígitos" é otimizar o proxy. Se o fato não agrega à história que a família vai ouvir, **não pesquisa** — marca o card como "raso mas honesto" e segue. A metade ⚖️ se resolve com prosa boa, não com dado enfiado.
