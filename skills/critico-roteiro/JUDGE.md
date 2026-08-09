# JUDGE · juiz qualitativo de profundidade (protocolo)

Camada 2 da avaliação de conteúdo. O `audit.py` mede forma (comprimento, campos, regex de fato); este protocolo mede **substância**: o conteúdo é interessante, bem curado e no nível do padrão-ouro? É executado pelo Claude via **sub-agente cético de contexto limpo** — quem escreve não julga.

Exemplar de referência: `entregas/roma-toscana-florenca-set2026.md` (ver `skills/destination-scout/SKILL.md` §Padrão-ouro de profundidade).

## Gatilho (anti-desperdício)

- Roda **1× por entrega** (viagem nova, entrega scout, aprofundamento) — nunca em edit pequeno.
- Roda **SÓ depois do audit limpo** (P0=0, P1=0, nota ≥ piso). Julgar card com `sobre` de 40 chars é pagar sub-agente pra descobrir o que o regex acha de graça.
- **Teto duro 1+1**: julga → corrige → re-julga 1× → **para**. Se o re-julgamento ainda reprovar, a decisão sobe pro Tobia — julgamento qualitativo não converge sozinho e loop infinito é desperdício puro.

## Método

1. **Amostrar**: os ~8-10 **cards-âncora** (não os 30) — os 🏆 principais de cada dia + qualquer card que o audit marcou como limítrofe.
2. **Spawn de sub-agente cético** (contexto limpo, sem o histórico de quem escreveu), com: os cards amostrados + 2-3 cards do exemplar-ouro como régua + este protocolo. Prompt-base: *"Você é crítico impiedoso de guias de viagem. Encontre os 3 cards mais fracos e diga por quê. Para CADA card responda:"*
   - **(a) Teste do jantar**: o `sobre` conta uma história que você repetiria num jantar, ou é Wikipédia resumida?
   - **(b) Teste do distraído**: o `imperdivel` aponta algo que o visitante perderia sem ele, ou é platitude?
   - **(c) Teste da decisão**: alguma dica/veredito deste card **muda uma decisão real** da família (horário, rota, pular, reservar), ou é filler?
   - **(d) Pareamento**: este card está no nível do card equivalente do exemplar (ex: Coliseu da entrega Itália)? `melhor | igual | pior` + por quê. *(Comparação pareada discrimina no topo, onde pontos de regex saturam.)*
   - **(e) Curadoria** (visão do conjunto): falta algum POI óbvio pro perfil? Sobra algum que um crítico cortaria? O 🏆 mais fraco está sustentado (convergência + busca negativa — `source-credibility.md`) ou é eco de listicle?
3. **Output do juiz**: lista de cards `pior` com o defeito específico e o **fix concreto** (não nota nova — o audit já numera; o juiz aponta ONDE e O QUÊ).
4. **Corrigir** os apontados → re-julgar só os corrigidos (1×) → registrar na entrega: `juiz: N/M âncoras no nível do exemplar · X corrigidos`.

## Custo-alvo

**~40-60k tokens por rodada** (1 sub-agente). Com o teto 1+1: máx ~120k por entrega.
