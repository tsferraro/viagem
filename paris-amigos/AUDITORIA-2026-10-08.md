# AUDITORIA externa · paris-amigos-out2026 · 2026-10-08

**Quem**: sessão auditora independente (não construiu o app) · Opus 5.5, esforço alto · 3 sub-agentes céticos de contexto limpo pra pesquisa.
**Objeto**: app no ar em `tsferraro.github.io/viagem/paris-amigos/` (deploy `6dfb10b`, rebuild de template em `7de5d84`), `paris-amigos/data.json` e o `FACTCHECK-2026-10-07.md` da construtora.
**Protocolo**: CLAUDE.md passo 11 + MEMORY "Auditoria adversarial" — amostra factual nova, conferência das correções, ataque aos gates, privacidade.

## Veredito

**O app é confiável pra usar a partir de amanhã.** Na amostra nova de 36 afirmações (peso em ⭐⭐⭐, `opcoes`, `aprofundar` e no que muda a ação no dia), **nenhum erro muda a sequência de um dia**: 2 ERRO de detalhe e 8 RISCO, todos corrigidos por texto. Taxa de erro da amostra: **2/36 (~6%)**, bem abaixo da taxa de base de 20-50% medida nas crises de ago/2026 — o factcheck de 07/10 fez o trabalho dele.

O ponto fraco não é o conteúdo, é a **régua de afirmações do `audit.py`**: ela não enxerga preço escrito "€36,70", ano depois de 2019, altura em cm nem horário "19:00", e não lê `nota` do dia, `legend_notes_html` nem `transit_map`. O único achado com cara de P1 de conteúdo (a nota do sábado mandando reservar Notre-Dame só no sábado) morava justamente numa `nota`.

| Frente | Resultado |
|---|---|
| 1 · Amostra factual nova | 36 afirmações · **26 OK · 2 ERRO · 8 RISCO · 0 INCONCLUSIVO** · 11 correções de texto → `FACTCHECK-2026-10-08.md` |
| 2 · Correções do FACTCHECK de 07/10 | **16/16 aplicadas** no `data.json` e no HTML (`sync-check` OK) |
| 3 · Ataque aos gates | **4 furos confirmados por mutação** (abaixo) · gates verdes no estado atual |
| 4 · Privacidade | sem nome nem endereço/coord da casa no app · **1 apelido** em handoff (tirado) e numa mensagem de commit (fica no histórico) |

## Achados

### P0 — nenhum

### P1

| # | Achado | Prova | Estado |
|---|---|---|---|
| P1-1 | **Nota do sábado contradizia o card de Notre-Dame**: a nota mandava "faça a reserva no próprio sábado de manhã"; o card (e o FAQ oficial) diz que as vagas abrem até 2 dias antes. Seguindo a nota, a família podia perder o horário da tarde de sábado | FAQ oficial de notredamedeparis.fr (snippet) + secretsofparis.com | **corrigido** · nota agora diz "tentem já na quinta e repitam na sexta" · **hoje é quinta: passar o recado** |
| P1-2 | **Régua de afirmações cega a 4 formatos** (`_claims_estruturados`, `audit.py`): preço com € antes do número (`€36,70` → zero afirmações; `36,70 €` → uma) · ano 2020-2099 (`DATA_HIST_RE` só pega `20[01][0-9]`: "fechado até 2027", "obras até 2028" passam) · `cm` não é unidade (altura mínima da Disney passa) · horário `HH:MM` | teste direto da função + mutações M2-M5 | **não corrigido** — decisão do Tobia (D1): fechar faz 3 viagens ativas ganharem P0 novo (paris-fds 3 · saint-germain 2 · paris-amigos 1, este um falso-positivo de vírgula colada ao `€3,`) |
| P1-3 | **`nota` do dia, `legend_notes_html`, `transit_map` e `cat` de transit ficam fora dos DOIS gates** (nem claim-a-claim no audit, nem projeção do factcheck-gate). É onde moram regra de reserva, preço de metrô, corrida de domingo, táxi de Orly | mutações M8 e M9: audit 0 P0/P1 e factcheck-gate não vê a mudança | **não corrigido** — entra na D1 |

### P2

| # | Achado | Estado |
|---|---|---|
| P2-1 | **Funicular de Montmartre**: "com o mesmo bilhete do metrô" — desde jan/2025 o bilhete validado no metrô não serve pro funicular, é preciso validar outro (ERRO, 2 fontes) | **corrigido** |
| P2-2 | **Descartes "sob uma janela da 2ª capela"** — a lápide está na capela Saint-Benoît, deambulatório sul (ERRO de posição, guia da paróquia) | **corrigido** |
| P2-3 | **Frozen Ever After**: o card hesitava ("uma fonte diz 102 cm"); página oficial e dois guias dizem sem altura, os 102 cm são da Epcot | **corrigido** · afirma "sem altura mínima" |
| P2-4 | **Torre Eiffel "ingresso nominativo, levem documento de todos"** — nenhuma página oficial diz isso; o oficial só diz que a idade da tarifa criança pode ser comprovada | **corrigido** · pede só o documento do menino |
| P2-5 | **`aprofundar` em card ⭐⭐ fica fora do gate 4d** e no audit vira só P1 (o `--deploy-gate` deixa passar). É prosa histórica, como `historia[]`, que o gate trata como P0 sem olhar estrela. Caso real: o `aprofundar` da Pont Saint-Louis (⭐⭐) tinha o ERRO "1632" no factcheck de 07/10 | mutação M7 | **não corrigido** — D1 |
| P2-6 | **Item de `opcoes` ⭐⭐⭐ não passa pela régua claim-a-claim** (só pelo frescor do 4d). Pierre Hermé, Café de l'Homme e Freddy's → Prescription são ⭐⭐⭐ | mutação M6 | **não corrigido** — D1 |
| P2-7 | **Rebaixar ★3 → ★1 apaga toda a cobrança** de afirmação do card (fica fora da régua e do 4d). Não é furo de verdade se ninguém fizer de propósito, mas é a porta mais barata pra calar o gate | mutação M10b | registrado |
| P2-8 | **Privacidade**: o apelido de uma das viajantes aparecia em `handoffs/2026-10-07_app-paris-amigos.md` e aparece na mensagem do commit `1c31664` | handoff **corrigido** · commit **não reescrito** (reescrever histórico público do `main` é destrutivo; fica como dívida consciente) |

### P3

| # | Achado | Estado |
|---|---|---|
| P3-1 | Bateaux-Mouches: "em outubro, a cada 45 min até 16h" — o site oficial põe outubro nas duas temporadas; a saída das 16:30 existe nas duas | corrigido |
| P3-2 | Bouillon Racine (almoço): "12h-23h"; o oficial é 12h à meia-noite (o card da noite já dizia certo) | corrigido |
| P3-3 | Il Gelato del Marchese: nome com "2 rue de Condé" e busca do Maps por "rue des Quatre-Vents" (dois endereços circulam, mesma esquina) | corrigido · nome e busca unificados |
| P3-4 | Pont Saint-Louis "só pra pedestres": fechada a carros desde 2014, passa bicicleta | corrigido |
| P3-5 | LudoJardin: "horário de outubro a confirmar" → oficial abre 10h e fecha 1h antes do jardim (17h45 até 15/out) | corrigido |
| P3-6 | Carrossel do Luxembourg: preço "[a confirmar]" → ~€2 o giro (fonte secundária, abr/2026, ainda marcado a confirmar) | corrigido |
| P3-7 | Metrô: "não existe mais bilhete de papel" — a venda acabou em 05/11/2025, os antigos valem até 15/12/2026 | corrigido ("não se vende mais") |
| P3-8 | Disney: "a bilheteria não vende na hora" — vende, mais caro e sem garantia (ingresso já comprado, não muda nada) | corrigido |
| P3-9 | **Prova obsoleta**: 4 tokens de `prova` sustentavam afirmações já refutadas pelo factcheck de 07/10 (`grátis <5 anos`, `desde 2010`, `1840`, `A partir de €17`) — texto certo, prova errada | corrigido (tokens removidos) |
| P3-10 | Atelier des Lumières: uma dica diz "carrinho não entra", outra "há um espaço pra deixar, com vagas limitadas" | não mexido · eles vão sem carrinho |
| P3-11 | Domingo 11/out: L6 parada o dia todo, L11 e L13 até meio-dia; estação Saint-Michel (L4) fechada até 19/dez; RER com obras noturnas na semana. O roteiro não usa nenhuma dessas | registrado · Disney: reconferir horário do parque e obras do RER A no app na véspera |
| P3-12 | **Auto-observação**: pra zerar um P1 novo no card do Bateaux-Mouches eu acrescentei `temporada · verão · inverno` à prova. Os termos estão na fonte (o site tem dois quadros sazonais), mas o gesto é exatamente o que a régua premia: anexar token. Fica registrado pra quem auditar esta auditoria | registrado |

## Frente 2 · as 16 correções de 07/10

Todas no texto visível do `data.json` e do HTML: latão (não bronze) · obra do parvis × obra de trás da catedral · Luxembourg 7h45-18h45 · Flandrin 1842-43 · Atelier €19,50 e grátis só <3 · Flying Carpets sem altura · Orsay reserva "fortemente recomendada" · Breizh 10h-23h · Pierre Hermé 10h-20h/10h-19h · Iovine's 2015 · Monsieur Bleu 19h-02h · coord do carrossel · rota Square Barye → Sully-Morland (L7) · ponte de 1634 · Furstenberg 1699. Busca dos valores errados (`bronze`, `1632`, `1691`, `Cardinal Lemoine`…) no texto visível: zero. O que sobrava eram os 4 tokens de prova do P3-9.

Placar do factcheck de 07/10 bate com as linhas: 218 = 162 OK + 16 ERRO + 29 RISCO + 11 INCONCLUSIVO.

## Frente 3 · ataque aos gates (mutações numa cópia do `data.json`)

| Mutação | `audit.py` | `factcheck-gate` vê? |
|---|---|---|
| M1 · `aprofundar` ⭐⭐⭐ com data inventada (controle) | P0 ✅ | sim |
| M2 · preço `€99,90` em dica ⭐⭐⭐ | **nada** | sim |
| M3 · "exige 120 cm" na Disney | **nada** | sim |
| M4 · "fecha de vez em 2029" no `aprofundar` ⭐⭐⭐ | **nada** | sim |
| M5 · "13:00-15:00" em dica ⭐⭐⭐ | **nada** | sim |
| M6 · opção ⭐⭐⭐ com "a maior do mundo, fundada em 1890" | **nada** | sim |
| M7 · `aprofundar` ⭐⭐ com "1999, a maior da Europa" | P1 (deploy passa) | **não** |
| M8 · `nota` do dia com horário e preço inventados | **nada** | **não** |
| M9 · `transit_map` com afirmação inventada | **nada** | **não** |
| M10b · ★3 → ★1 + "de 1777, o maior de Paris" | **nada** | sim (só porque a chave sumiu) |

Leitura: com o 4d, as mutações em ⭐⭐⭐ ainda forçam um factcheck novo — o furo do M2-M6 é a régua claim-a-claim não apontar QUAL afirmação está sem prova. M7-M9 passam pelos dois gates sem ninguém ver.

Proposta de conserto (custo medido, nas viagens ativas de hoje):
1. `NUMERO_RE`: aceitar `€` antes do número e `cm`; tirar pontuação colada ao token
2. `DATA_HIST_RE`: `20[0-9]{2}` em vez de `20[01][0-9]`
3. `HH:MM` **não** entra (testado: vira falso-positivo nos horários do próprio roteiro)
4. Régua claim-a-claim também em `opcoes` ⭐⭐/⭐⭐⭐, `nota`, `transit_map`; `aprofundar` entra no 4d independente da estrela

Impacto de 1+2: paris-fds ganha 3 P0, saint-germain 2, paris-amigos 1 (falso-positivo `€3,`, some com o "tirar pontuação"). marais sem mudança.

## Frente 4 · privacidade

- `data.json`/`index.html`: sem nome de nenhum viajante, sem endereço nem coord da casa. "Casa" não tem pino (`noMaps` ou coord de estação/aeroporto). As únicas coords em Boulogne são de 2 restaurantes públicos.
- As estações L9 Marcel Sembat e L10 Boulogne Jean Jaurès aparecem (texto e URL de fonte): nível de bairro, não endereço. Aceitável.
- Apelido de uma viajante: ver P2-8.

## O que esta auditoria NÃO cobre

- Disney: nenhum horário pôde ser lido no site oficial (fila de espera pra robôs) — duas fontes independentes concordam; reconferir no app na véspera.
- 182 afirmações do factcheck de 07/10 não foram re-amostradas (de propósito: amostra nova).
- O re-check pré-viagem (R11, 7-10 dias antes) já não cabe: a viagem começa amanhã. Esta amostra cobre a maior parte do operacional.
