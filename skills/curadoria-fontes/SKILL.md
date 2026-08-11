# curadoria-fontes · fontes com lastro de campo (R10 da auditoria 2026-08-08)

**Quando usar**: no degrau 0 de toda viagem nova (identificar candidatas do destino) · ao
processar relato de campo/DIARIO (gravar evento na fonte) · no wrap-up de toda viagem (balanço
das fontes) · quando alguém propõe citar uma fonte nova num card.

## 0 · Princípio

Lista de fontes é ESTOQUE que apodrece por gosto; curadoria é FLUXO lastreado em evento. O que
se versiona é o **registro por fonte** (o que ela afirmou → o que o campo confirmou/demoliu);
qualquer "lista de confiança" é uma *view* derivada do registro, recalculável e sempre
justificada. **Nenhuma fonte entra validada** — nem as achadas pela auditoria.

Contexto de origem: a decisão do Tobia (04/Ago) — ele não tem lista de blogs de confiança, e
isto não deve ser entregue como lista pronta, e sim como processo que roda em paralelo aos
próximos roteiros, acumulando fontes validadas por perfil.

## 1 · Peça central: `fontes/registro.json`

Uma entrada por fonte (domínio/autor), com:

```json
{
  "id": "twofortheworld",
  "dominio": "twofortheworld.com",
  "tipo": "blog-campo",            // blog-campo · portal-oficial · diretorio · editorial · crowd
  "perfis": ["road-trip"],          // familia-crianca · casal · walking-tour · road-trip
  "destinos": ["sardenha"],
  "sinais_presenca": ["mapa interativo Google da própria viagem de 2 sem, 4 bases"],
  "estado": "candidata",            // candidata → em-teste → validada → rebaixada
  "eventos": [
    {"data": "2026-08-08", "tipo": "entrada", "origem": "auditoria",
     "nota": "achada na busca de candidatas da auditoria; sinais só de snippet"}
  ]
}
```

**Estados movidos SÓ por evento** (nunca por gosto):
- `candidata` → `em-teste`: ≥1 recomendação dela **embarcou** num roteiro, com `fontes[].o`
  do card apontando pro `id` do registro.
- `em-teste` → `validada`: **≥2 confirmações de campo, 0 demolições**.
- qualquer → `rebaixada`: 1 demolição factual volta pra em-teste; **2 demolições tiram do jogo**.

Métrica derivável por fonte: `confirmadas/(confirmadas+demolidas)`, sempre com n.

## 2 · IDENTIFICAR (degrau 0 de cada viagem · 15-20min/destino)

Queries-padrão por perfil (2-4 candidatas por destino — é fichamento, não aprovação):

| Perfil | Queries |
|---|---|
| **walking tour** | `<bairro> self-guided walking tour blog map` · `<cidade> walking route "I walked"` · pulo do gato pro My Maps: `<destino> itinerary "google.com/maps/d"` (embed de My Maps tem URL própria; só quem montou mapa publica) |
| **road trip** | `<destino> road trip itinerary blog self-drive map` + variante no idioma local (`itinerario`, `carte`) — blogs locais versionam melhor estradas e obras |
| **família+criança** | `<destino> with toddler trip report stroller` — "carrinho" é o discriminador: quem descreve onde o carrinho NÃO passa esteve lá com um |
| **casal** | `<destino> couple trip report evening restaurants` |

## 3 · JULGAR "esteve lá" (checklist de 5min por candidata · exige ABRIR a página)

**Positivos (≥3 = forte)**: My Maps/GPX **próprio** da rota · fotos próprias com continuidade
(mesma pessoa/luz/estação) · data da visita declarada · narra **imprevisto ou custo pago**
("a estrada estava fechada", "paguei €X") · detalhe que não está em portal nenhum (o teste do
painel de Bonifacio) · atualização pós-publicação ("update 2025: o ferry mudou").

**Negativos (1 = descarta)**: prosa que ecoa portais (teste: 1 frase distintiva entre aspas no
Google — 3 sites = eco) · fotos stock · listicle sem rota · afiliado denso sem relato ·
**texto com cara de LLM** (fluente-genérico, zero número, zero data — o repo sabe exatamente
como é essa prosa: foi o que ele mesmo produziu).

## 4 · PRIORIZAR por tipo de afirmação (estende `references/source-credibility.md`)

| Tipo de afirmação | Quem decide | Quem NÃO decide |
|---|---|---|
| horário · preço · regra de acesso | oficial/estabelecimento, datado | blog (apodrece) |
| existência e FUNÇÃO de lugar | foto própria de blog-campo + 1 fonte local | portal, agregador |
| posição / por-onde-anda | My Maps de blog-campo · mapa oficial de trilha | prosa de qualquer fonte |
| veredito vale/não-vale | 2 blogs-campo convergentes de perfis ≠ | T1 (nunca diz "pula") |
| dia de fechamento | site próprio + 1 diretório; divergiu → telefone | 1 diretório sozinho |
| logística vivida (fila, sombra, carrinho) | blog-campo do MESMO perfil | todo o resto |

## 5 · GANHAR/PERDER confiança — o laço com o campo (a peça que faltava)

Pré-requisito único: quando a fonte for curada, `fontes[].o` do card usa o **id do registro**.
Daí o fluxo existente fecha sozinho:

1. Relato 📣/DIARIO confirma ou demole um item.
2. O processamento do relato (já é tarefa manual, por decisão registrada) ganha **uma linha a
   mais**: localizar o `fontes[].o` do item e **gravar o evento no registro da fonte** —
   `{"data", "tipo": "confirmacao"|"demolicao", "origem": "relato"|"DIARIO"|"factcheck",
   "item": "<card>", "nota": "<o que aconteceu>"}` — e mover o estado se o critério do §1 bateu.
3. No wrap-up de cada viagem (passo do protocolo de encerramento): **quais fontes embarcaram?
   alguma virou validada? alguma demoliu?** (~5min).

Custo marginal ~zero; sem isso, a curadoria é lista mantida por gosto — que é o que o Tobia
disse que não quer.

## Honestidade metodológica

Os sinais das 8 candidatas iniciais vêm de **snippets de busca** (WebFetch bloqueado no sandbox
da auditoria). O julgamento §3 completo exige abrir cada página: 5min/candidata na primeira
sessão desktop, ou o Tobia. Nenhuma pula etapa — isso não é fraqueza do processo, é o processo
existindo.
