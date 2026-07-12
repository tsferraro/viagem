# FACTCHECK · verificação adversarial de fatos (protocolo)

Camada 3 da avaliação de conteúdo. O `audit.py` (regex) mede **forma**; este protocolo mede **verdade** — a única coisa que o gate offline não enxerga. É executado pelo Claude (não é script): extrai afirmações verificáveis e tenta **refutá-las** contra fontes via web_search.

Régua de fontes: `references/source-credibility.md` (tiers + padrões de prova).

## Quando roda (gatilhos — NÃO rodar em edit pequeno)

| Situação | Escopo |
|---|---|
| **Viagem nova / entrega scout** | fact-check lean (regras abaixo), 1× antes do deploy/export |
| **Aprofundamento de roteiro existente** | só as afirmações **novas/alteradas** na sessão |
| **Pré-viagem (1-2 semanas antes)** | modo re-check: SÓ fatos operacionais (preço/horário/reserva/dias de abertura) de TODOS os cards — pega informação que apodreceu |
| Edit pequeno (trocar stop, dica) | **não roda** — validate + audit bastam |

## O que verifica — e o que NÃO (anti-desperdício)

**Verifica:**
1. **Fatos operacionais** (preço, horário, reserva, dias de fechamento) **sem proveniência T1** registrada
2. **Qualquer afirmação sem fonte registrada** que seja verificável (coords de POI, fato histórico com data/nome, "fecha às 14h de quinta")
3. **Amostra de ~20%** das afirmações COM proveniência (auditoria de honestidade — a fonte diz mesmo aquilo?)
4. **Vereditos 🟢-âncora**: a convergência exigida pelo padrão de prova existe? A busca negativa foi rodada?

**NÃO verifica (redundâncias cortadas):**
- **R1**: afirmação com proveniência **T1 recente** registrada na mesma sessão de pesquisa → já verificada. Não re-caçar o que o scout acabou de citar.
- **R2**: URLs vivas → é trabalho do `audit.py --check-links` (HTTP HEAD). Fact-check confere **conteúdo**, nunca status HTTP.
- Opinião/gosto ("mais cenário que comida") → não é fato; é território do JUDGE.

## Método

1. **Extrair claims** do `data.json` (ou `.md` do scout): lista de `{afirmação, tipo, fonte_registrada?, card}`. Tipos: `operacional` · `coord` · `histórico` · `veredito`.
2. **Aplicar filtros** acima → lista final (tipicamente 10-25 claims, não 50+).
3. **Fan-out de céticos**: sub-agentes em paralelo (~1 por lote de 5-8 claims), cada um com prompt adversarial: *"Tente REFUTAR cada afirmação via web_search na fonte do tier adequado (source-credibility.md). Prefira T1 pra operacional. Retorne por claim: CONFIRMADO (fonte+data) / DESATUALIZADO (valor novo+fonte) / NÃO ENCONTRADO."*
4. **Aplicar vereditos**:
   - `CONFIRMADO` → registrar proveniência se faltava
   - `DESATUALIZADO` → **P1**: corrigir o valor no card + datar
   - `NÃO ENCONTRADO` → marcar `[a confirmar]` no card (transparência > fingir precisão) — **nunca** manter número órfão
   - Fonte de tier errado pro tipo (preço citando blog quando existe T1) → achado, corrigir proveniência
5. **Relatório**: `fact-check: N confirmados · N desatualizados (corrigidos) · N [a confirmar]` — entra na entrega junto da nota do audit.

## Custo-alvo

Lean (com proveniência registrada na pesquisa): **~50-80k tokens** (1-2 sub-agentes). Se estiver passando disso, o problema é falta de proveniência na fase de pesquisa — corrigir lá, não inflar aqui. Modo pré-viagem: ~30-50k.
