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
- **"Sem desvio" é critério, não detalhe.** Apareceu em três perguntas distintas — otimiza
  eficiência de estrada de forma consciente.
- **Pensa logística melhor que o roteiro.** A ideia de usar o carro no dia da mudança de base
  (Rondinara em 3/Ago) era superior às seis opções que eu havia levantado.
- **Verifica no chão e reporta rápido.** Dois erros pegos em campo em três dias. É a fonte
  mais confiável que este roteiro tem.

---

## Erros meus · padrão acumulado

Dois erros, mesma raiz: **descrever estabelecimentos a partir de busca, com confiança de
quem verificou.** A correção certa não é só o texto — é a régua. Proposta para a
`critico-roteiro`: exigir marcação quando a localização de um estabelecimento não foi
confirmada por fonte que a estabeleça explicitamente.

---

## Pendente de relato

Dias ainda sem entrada: 27, 29, 30, 31/Jul · 1, 2/Ago · e 4 a 8/Ago conforme acontecerem.
