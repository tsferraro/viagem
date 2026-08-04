# FACTCHECK · verificação adversarial de fatos (protocolo)

Camada 3 da avaliação de conteúdo. O `audit.py` (regex) mede **forma**; este protocolo mede **verdade** — a única coisa que o gate offline não enxerga. É executado pelo Claude (não é script): extrai afirmações verificáveis e tenta **refutá-las** contra fontes via web_search.

Régua de fontes: `references/source-credibility.md` (tiers + padrões de prova).

## Quando roda (gatilhos — NÃO rodar em edit pequeno)

| Situação | Escopo |
|---|---|
| **Viagem nova / entrega scout** | fact-check lean (regras abaixo) + **§4 completa**, 1× antes do deploy/export |
| **Aprofundamento de roteiro existente** | só as afirmações **novas/alteradas** na sessão |
| **Pré-viagem (1-2 semanas antes)** | modo re-check: SÓ fatos operacionais (preço/horário/reserva/dias de abertura) de TODOS os cards — pega informação que apodreceu |
| **Stop/estabelecimento novo ou renomeado** | **§4 no item tocado** — sempre, mesmo em edit pequeno |
| Edit pequeno (só texto de dica) | **não roda** — validate + audit + gate de mapas bastam |

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
5. **Relatório**: `fact-check: N confirmados · N desatualizados (corrigidos) · N [a confirmar]` — entra na entrega junto da nota do audit, com o placar da §4: `lugares conferidos · links vivos · atrativos re-checados`.

## 4 · Conferência de LUGAR, LINK e SITUAÇÃO (obrigatória em toda entrega)

Três verificações que o `audit.py` não faz e que, em ago/2026, foram a diferença entre um
roteiro com nota 37/40 e um roteiro que funcionava. Todas nasceram de erro real, em campo.

### 4a · O link do Maps leva ao lugar? (`scripts/maps-audit.py`)

**Primeiro rode a ferramenta** — ela monta as URLs exatamente como o app monta e pega o que é
mecânico. É gate de deploy, então não é opcional:

```bash
python3 scripts/build.py <viagem>/data.json <viagem>/index.html
python3 scripts/maps-audit.py <viagem>/index.html --urls
```

Ela bloqueia busca genérica, waypoint fantasma e ponto repetido. O que ela **não** sabe é se
`"Area Archeologica di Tharros"` existe — isso é o fact-check:

- Toda `mapsQuery` **nova** entra na amostra de claims, tipo `lugar`. Confirme por busca que o
  nome é o **nome canônico** do POI (o que o Google indexa), não uma tradução ou apelido.
- Casos reais que só a verificação pegou: *"Loggia · mirador sul"* não é POI (a loggia é da
  própria Sainte-Marie-Majeure; o mirador é **Falaises de Bonifacio**) · *"Necrópole púnica"* é
  **Villaggio Ipogeo** · *"Spiaggia di Tegge"* é **Punta Tegge** · a tonnara de Cala Sapone
  **não tem POI** (abandonada desde 1825) e o nome buscável é a praia.
- **`mapsQuery` não recebe `MAPS_REGION`** — confira você que ficou inequívoco. O roteiro dos
  pais tem um dia em Bonifacio (Córsega/França) com `maps_region: "Sardegna, Italia"`.
- **`mapsQuery` é OBRIGATÓRIO nas duas estruturas que montam rota**: parada de **walking tour**
  e ponto de **road trip** (dia `transport: "driving"` — o que a skill `road-trip-designer`
  gera). O `validate.py` bloqueia (`check_wt_maps_query`); dia comum só avisa. Sem ele a rota cai pra coordenada e o
  Maps mostra "Dropped pin"; funciona, e é inútil pra quem está dirigindo. Exigir o campo
  obriga a decidir o nome **ponto a ponto**, que é metade da verificação.
- **A outra metade é conferir cada um, um a um** — o campo estar preenchido não prova que o
  Google acha. Rode `maps-audit.py --urls`, percorra a lista e **marque cada query**:

  | Veredito | O que fazer |
  |---|---|
  | acha o lugar certo | segue |
  | acha outro lugar | corrigir a `mapsQuery` e re-conferir |
  | não acha nada | trocar pelo POI mais próximo que exista, ou `noMaps` |

  Derivar `mapsQuery` do nome em massa **não conta como conferência**: numa derivação
  automática de 39 paradas do Marais, duas saíram erradas (`Free'P'Star · friperies` virou
  `friperies`, e `5/7 rue de Fourcy` levou uma barra que quebra a URL `/dir/`). Automação
  propõe; a conferência item a item é que aprova.
- Abrir 2-3 URLs de rota no celular fecha a conta. Nada substitui isso.

### 4b · Os links do `links_map` respondem?

```bash
python3 skills/critico-roteiro/audit.py <viagem>/data.json --check-links
```

⚠️ **Em sessão cloud esse comando é inútil** — o proxy devolve 403 pra todo domínio e ele
reporta 100% dos links como quebrados. Rode do desktop, ou peça ao Tobia. Regras de leitura:

| Status | Significa |
|---|---|
| **404 / 410** | morto de verdade — remova ou substitua |
| **405** | o servidor recusa `HEAD`; o recurso **existe** |
| **403** | quase sempre bot-blocking (Cloudflare) |
| timeout | site lento, não morto |

E o erro que **eu** cometi: URL que aparece em resultado de busca **não** está provada viva —
o índice guarda página que já mudou de lugar. Museu e prefeitura reorganizam URL o tempo todo.
Sem verificação HTTP real, entra só o que já respondeu 2xx antes; na dúvida, não entra.

### 4c · O atrativo ainda funciona daquele jeito?

A classe de erro mais cara, porque o lugar **existe** e a busca confirma que existe. Três
variantes já vistas, todas em roteiros que passavam no linter:

| Variante | Caso real |
|---|---|
| Fechou | **Ristorante Gallura** (Olbia): despejo em jan/2014, depois de 70 anos. Estava no jantar da 1ª noite |
| Mudou a regra de acesso | **Cala Coticcio**: contingentada desde 2020, só com guia autorizado e reserva. O card mandava subir a trilha |
| Mudou preço/horário/canal | **Compendio Garibaldino**: €6→€8 e passou a exigir reserva por faixa · **Porto Flavia**: venda **só online**, fecha à meia-noite da véspera |

Protocolo mínimo por atrativo âncora e por todo estabelecimento nomeado:

1. `"<nome>" <cidade> indirizzo` — tem que voltar endereço, telefone ou guia. Sem isso, **não
   entra com nome**: vira opção genérica honesta (*"bares da praça · escolha no local"*).
2. Para instituição antiga ou "histórica", **segunda busca**: `<nome> chiuso OR riapertura OR
   trasferito`. Buscar só o nome confirma que existe, não que opera.
3. `<nome> orari <ano>` + **conferir o dia da semana contra a data real do stop**. Já pegou
   `Sa Bell'e Crabasa` (fecha segundas) marcado como jantar de uma segunda-feira.
4. Reserva/ingresso: **como se compra** (balcão? só online? fecha quando?) — não basta o preço.

**Sinal de alerta**: nome genérico plausível (`Trattoria del <substantivo>`, `Da <primeiro
nome>`). Numa varredura de 55 estabelecimentos, **todos** os 15 inexistentes eram desse tipo e
**nenhum** dos nomes distintivos falhou. Suspeite do nome que você conseguiria inventar.

## Custo-alvo

Lean (com proveniência registrada na pesquisa): **~50-80k tokens** (1-2 sub-agentes). Se estiver passando disso, o problema é falta de proveniência na fase de pesquisa — corrigir lá, não inflar aqui. Modo pré-viagem: ~30-50k.
