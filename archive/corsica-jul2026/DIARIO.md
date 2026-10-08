# Diário de Campo · corsica-jul2026

Registro do que a família reportou **em campo** e do que cada coisa virou.

**Autoridade**: relato de campo ganha de qualquer fonte web. Se a busca diz X e o Tobia
viu Y, é Y. Sem discussão, sem "mas a fonte oficial diz".

**Fonte**: planilha `Diário de Campo · Roteiros do Tobia` (Google Drive) + mensagens no chat.
Controle de processamento é aqui — o Tobia nunca precisa marcar nada.

**Roteamento** (a mesma frase pode gerar as três coisas):

| Tipo | Destino | Vale pra |
|---|---|---|
| 🔴 Erro factual | `corsica/data.json` | Esta viagem + quem receber o link |
| 💡 Dica de campo | `dicas` do card | Quem reusar este roteiro |
| ❤️ Preferência da família | `MEMORY.md` · Padrões cross-viagem | Todas as viagens futuras |
| ⭐ Nota do dia | Aqui, só como contexto | Calibrar o arco |

⚠️ **Fronteira dura**: preferência da família **não entra no card**. "A filha cansa às 17h"
é verdade sobre eles, não sobre a Córsega — se vazar pro card, a versão que os amigos
receberem fica pior.

---

## Processados

### 2026-07-28 · Ter 28/Jul · Porto Pollo
**Relato**: "Não encontrei esse Le Lido em Porto Pollo. Ele fica em Propriano?"

| Tipo | Achado | Virou |
|---|---|---|
| 🔴 | Le Lido não existe em Porto Pollo — é em Propriano, 42 Av. Napoléon III, e é hotel-restaurante gastronômico desde 1932, não casual pé-na-areia | 9 ocorrências trocadas por L'Escale, L'Espace Porto Pollo, Les Sables Dorés e U San Petru · Le Lido remanejado pro jantar em Propriano · commit `fix: Le Lido é em Propriano` |
| 💡 | Supérette da vila (Spar) fecha ~13h-16h · não dá pra montar sanduíche no meio do dia | Aviso explícito no card de chegada |

**Classe do erro**: estabelecimento inventado ou mal localizado a partir de busca.
**Ação de classe**: varredura em TODAS as opções de restaurante do roteiro, não só a apontada.

---

### 2026-08-03 · Seg 3/Ago · estrada pra Roccapina
**Relato**: "Essa Pousada Coralli parece ser em outro ponto da estrada e não no Belvedere."

| Tipo | Achado | Virou |
|---|---|---|
| 🔴 | Auberge Coralli não fica no belvédère · é outro ponto da N196, do lado do mar, e marca a entrada da pista pra praia (~2,7km da areia) | Dica corrigida + telefone · commit `fix: Auberge Coralli não fica no belvédère` |
| 🔴 | Coralli não serve café da manhã a quem passa — restaurante só à noite, com reserva | Substituída pela Boulangerie Maniccia (Pianottoli-Caldarello, na N196) |

**Classe do erro**: eu afirmando que um estabelecimento fica "no local" sem verificação.
**Ação de classe**: toda menção a estabelecimento descrito como "no local" precisa de fonte
que confirme a localização, ou marcação explícita de que não foi verificado.

---

## Preferências observadas (candidatas ao MEMORY.md)

Nenhuma dessas foi dita — foram inferidas do comportamento ao longo da sessão.
**Confirmar com o Tobia antes de promover ao `MEMORY.md`.**

- **Prefere reordenar a cortar.** Toda vez que apontei sobrecarga de dia, ele mexeu na
  sequência em vez de remover conteúdo.
- **Quer alternativas legíveis, não decisões fechadas.** Pediu duas vezes (Bavella,
  Polischellu-com-guia) que a opção descartada ficasse documentada pra ele julgar em campo.
  Foi o que originou o uso sistemático de cards `🔄`.
- ~~**"Sem desvio" é critério de rota.**~~ ❌ **INFERÊNCIA ERRADA — corrigida pelo Tobia em
  2026-08-03**: *"num dia sem prazo com algo que realmente vale a pena eu vou sim"*. Era gestão de
  prazo, não preferência de eixo. Os 3 casos tinham deadline. Regra correta registrada no
  `MEMORY.md`.
- **Pensa logística melhor que o roteiro.** A ideia de usar o carro no dia da mudança de base
  (Rondinara em 3/Ago) era superior às seis opções que eu havia levantado.
- **Verifica no chão e reporta rápido.** Dois erros pegos em campo em três dias. É a fonte
  mais confiável que este roteiro tem.

---

## FACTCHECK completo · 2026-08-04

Rodado o protocolo `skills/critico-roteiro/FACTCHECK.md` sobre os 13 dias. 117 afirmações
extraídas (101 operacionais · 11 históricas · 5 de contato); descontadas as já verificadas com
proveniência nesta sessão (Filitosa, Lavezzi, ferry, táxi Figari, Polischellu, Spin'a Cavallu,
Coralli, dia do mercado de Sartène), sobraram os dias 4-8/Ago e os números nunca conferidos.

**Placar: 3 confirmados · 3 corrigidos · 3 marcados `[a confirmar]`.**

| Afirmação | Veredito |
|---|---|
| Pertusato "ponto mais ao sul da França metropolitana" | ❌ é o **segundo** · o extremo é o **Capu Testagro**, a leste — reescrito |
| Pointe Saint-Antoine "ponto mais ao sul da Córsega" | ❌ falso · é uma ponta junto a Pertusato, com praia suspensa a 80m — reescrito |
| Museu de Sartène €5 | ❌ **€4 / €2,50 meia** · verão todos os dias 10h-18h · bilhete dá entrada em Levie por 2 meses |
| Cidadela "Escalier €2,50 · resto grátis" | ❌ o **Bastion custa €3,50** · existe **Pass Monuments €6,50** (€2 criança) pelos dois — economia de €2/pessoa, virou dica |
| Pertusato construído em 1844 | ✅ confirmado (altura da torre diverge entre fontes · número removido) |
| Lavezzi "reserva natural desde 1982" | ✅ confirmado (36 ha em 1982 · integrada em 1999 às Bouches de Bonifacio) |
| Tour de Capanella "séc. XVI" | ✅ confirmado e **enriquecido**: **1589**, série genovesa de 1530-1620 contra piratas berberes, alarme em cadeia de torre a torre |
| Parking Piantarella €5 | ⚠️ `[a confirmar]` · parking novo em obras pra 2026 · hoje tolera-se a beira da estrada, de graça |
| SPMB Circuito 1 €18,50-26 | ⚠️ `[a confirmar]` · fontes de 2026 vão de €18,50 a €50 · tel. 04 95 10 97 50 |
| Parking Rondinara €6 | ⚠️ `[a confirmar]` · €6 em 2025 com indício de €8 · há gratuito no alto, ~10min a pé |

**Padrão nos 3 erros de conteúdo**: todos eram *superlativos geográficos e preços* — as duas
categorias que mais apodrecem e que guias turísticos mais repetem sem checar. Superlativo copiado
("o mais X de Y") deve ser tratado como afirmação a provar, nunca como cor de prosa.

**Regra aplicada (FACTCHECK §4)**: número não confirmado nunca fica órfão. Os três viraram
`[a confirmar]` explícito no card, com a faixa e o telefone/alternativa gratuita — transparência
vale mais que precisão fingida.

---

## Erros meus · padrão acumulado

**Terceiro erro, de outra natureza (2026-08-03)**: inferi uma preferência ("sem desvio") a partir
de 3 observações que compartilhavam um confound (todas em manhãs com prazo). O confound eu tinha
identificado e escrito — mas listei a inferência junto das outras, como se tivesse o mesmo peso.
**Lição**: inferência de preferência com confound conhecido não deve ir pra mesma lista das
observadas limpas. Separar e perguntar ANTES de listar.

Dois erros de conteúdo, mesma raiz: **descrever estabelecimentos a partir de busca, com confiança de
quem verificou.** A correção certa não é só o texto — é a régua. Proposta para a
`critico-roteiro`: exigir marcação quando a localização de um estabelecimento não foi
confirmada por fonte que a estabeleça explicitamente.

---

## Pendente de relato

Dias ainda sem entrada: 27, 29, 30, 31/Jul · 1, 2/Ago · e 4 a 8/Ago conforme acontecerem.
