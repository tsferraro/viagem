---
status: consumido
de: sessão "Roteiro de viagem Paris" (local_a7da077a · 06-07/10/2026 · pré-roteiro aprovado)
para: sessão nova · construir o app paris-amigos-out2026
---

# Sessão · app do roteiro paris-amigos-out2026 (no ar antes da chegada)

modo: onda
modelo/esforço: Opus 5.5 · alto — construção de app a partir de roteiro aprovado, com gates e factcheck
1ª ação: get_session (self) — confira modelo e esforço; fora do pedido, diga em 1 linha e siga
subagentes: Sonnet 5.5 (montar blocos do data.json a partir das fontes já levantadas) · Opus 5.5 (FACTCHECK cético, contexto limpo — quem escreve não confere a si mesmo, CLAUDE.md passo 9c)
orçamento de agentes: até 8
onde roda: local
gerador do que a sessão publica: `scripts/build.py` + `scripts/deploy.sh` do repo (já existem, versionados no repo)
canal de decisão: chat — sem Mesa ativa
componentes a reusar: template do repo (`templates/`), estrutura de pool do `paris-fds`, coletânea `marais/`, scripts de gate em `scripts/`
recarga (§ 10a.0): `CLAUDE.md` do repo (pipeline, schema, gates, REGRA ZERO) · este handoff · `entregas/paris-amigos-out2026.ROTEIRO-PROPOSTO.md` · `MEMORY.md` (seções "Paris · dicas de campo" e a regra das 18:30) · `git log -10`
paradas P0: só os 4 do GLOBAL § 10a-bis
definição de pronto: `https://tsferraro.github.io/viagem/paris-amigos/` responde HTTP 200, abre com a senha `paris2026`, e o `deploy.sh` passou os 5 gates (sync-check · validate · audit `--deploy-gate` · maps-audit · factcheck-gate) · placar do factcheck na entrega

**Prazo**: no ar até **qui 8/out 22h**. Prazo duro: **sex 9/out 18h** (eles pousam em Orly às 19:55).

## 👁 Visível ao Tobia
Nada pendente de merge: o roteiro aprovado está no `main` (commit `d23d0b9`) e o PDF v4 já foi enviado a ele.

## O pedido, literal
> *"Aprovado! Vamos construir este roteiro no app!"* (Tobia, 07/10)

1. Construir o app datado `paris-amigos-out2026` com os 7 dias do roteiro v4.
2. Abas de bairro: *"Só a Família de cada um, mas pode ter apenas o resumo como no PDF com todas as paradas dos outros roteiros além da Família."*
3. Profundidade: *"Dias enxutos, bairros com história, mas deixe o profundo dos passeios em complementos com expande/recolhe, recolhidos caso ela queira mais infos"*.
4. (As páginas de bairro no `paris.html` são a **outra** frente: handoff `2026-10-07_coletaneas-bairros-paris.md`. Não fazer aqui.)

## Fontes canônicas (seguir literal · REGRA ZERO)
| # | Fonte | O que buscar |
|---|---|---|
| 1 | `entregas/paris-amigos-out2026.ROTEIRO-PROPOSTO.md` | **o roteiro aprovado**: dias, horários, detalhes, avisos, "Antes de vir", anexo de bairros |
| 2 | `entregas/paris-bairros-out2026.md` | levantamento completo dos 5 bairros: **cada parada com fonte (URL + tier)**, horários, preços datados, ganchos de história, onde comer, alertas de out/2026 |
| 3 | `entregas/paris-amigos-out2026.SAIDA-SEGUNDA.md` | as 8 opções da noite das duas (segunda), com fontes |
| 4 | `entregas/paris-amigos-out2026.PREROTEIRO.md` §Fontes | fontes operacionais: Orsay, Orangerie, Bateaux-Mouches, Disney, Orly, metrô, eventos |
| 5 | `paris-fds/data.json` | **molde de estrutura**: dias datados + abas de pool sem data (`date: "🌳"`) · card do Atelier des Lumières (fontes já provadas) · aba 🐠 Trocadéro pra reaproveitar |
| 6 | `marais/` | coletânea Família já pronta: a aba de bairro aponta pra ela, não copia |
| 7 | `references/data-schema.md` · `skills/critico-roteiro/FACTCHECK-EXEC.md` | schema e protocolo do factcheck com rastro |

## Decisões já tomadas (NÃO redecidir)
| # | Decisão | Quem · quando |
|---|---|---|
| 1 | Roteiro v4 aprovado como está: sex chegada · **sáb** manhã em casa → Notre-Dame → Île Saint-Louis → Square Barye → Bateaux-Mouches 16:30 · **dom** Luxembourg + Saint-Germain · **seg** Orangerie → Tuileries → Atelier des Lumières (Van Gogh, último dia) → preparar a Disney → noite das duas · **ter** Disney Adventure World · **qua** Orsay → Deyrolle → Torre Eiffel · qui voo 6:30 | Tobia "Aprovado!" 07/10 |
| 2 | **Em casa até 18:30, no máximo 19:00**, todo dia (crianças) | Tobia 06/10 |
| 3 | Disney: sair do parque ~17:15 | aprovado com o roteiro |
| 4 | Senha **`paris2026`** · slug **`paris-amigos-out2026`** | Tobia 07/10 |
| 5 | Abas de bairro = **só a 👶 Família** de cada bairro (Saint-Germain/Luxembourg · Quartier Latin · Cité + Saint-Louis · Louvre/Tuileries · Montmartre) **+ resumo dos outros percursos** (trajeto · tempo · melhor dia, como no anexo do PDF) · Marais = link pra coletânea `marais/` · Trocadéro = reaproveitar a aba do paris-fds | Tobia 07/10 |
| 6 | Dias enxutos (logística + horário) · abas de bairro com história · **o aprofundamento vai em bloco expande/recolhe, recolhido por padrão** | Tobia 07/10 |
| 7 | Card da segunda à noite "🍷 Noite só de vocês duas" com as **8 opções**, ⭐ em Café de l'Homme e Freddy's → Prescription | Tobia 07/10 (D11) |
| 8 | Ajustes de campo da esposa do Tobia (07/10): táxi em Orly, não Uber · **sem Berthillon** como parada · Bateaux-Mouches: "a gente compra" (anfitriões) · bloco "Preparar a Disney" na segunda 16:30 · Grande Galerie de l'Évolution destacada no percurso Família do Quartier Latin | Tobia 07/10 |
| 9 | Pônei fora · Montmartre fora dos dias (🔄 alternativa na segunda + aba de bairro) | Kel/Tobia 06/10 |
| 10 | Ingresso da Disney já comprado pra terça: não mexer | Tobia 06/10 |

## Envelope de autonomia
| Campo | Valor |
|---|---|
| (a) orçamento | agentes: até 8 · semanal: até 6 pontos · teto que fecha: 85% → estaciona, fecha e entrega |
| (b) N4 pré-aprovados, por nome | `templates/render-functions.js` + `templates/styles.css` (+ `scripts/validate.py` se precisar): **campo opcional novo** pra aprofundamento recolhido. Hoje `sobre` é renderizado dentro de `<p>` (render-functions.js ~l.429), então um bloco `details` do HTML dentro dele quebra o HTML. O campo tem de ser **aditivo**: viagem sem o campo renderiza igual. Prova: `validate.py` + `sync-check.py` verdes em `marais`, `paris-fds`, `corsica`, `pais-sardenha` depois da mudança |
| (c) pode sair para fora sozinho | `deploy.sh` desta viagem (push no `main` → GitHub Pages), **só com os 5 gates verdes** |
| (d) portão reprovado | entrega com selo 🔴 · nada sai para fora · `VIAGEM_SKIP_*` **proibido** sem o Tobia |

## Paradas P0
Os 4 motivos (GLOBAL § 10a-bis). Paradas combinadas:
- P0: factcheck acha um item dos dias datados **falso ou fechado** e a correção muda a sequência do dia → leva ao Tobia com 2 alternativas prontas (ele prefere reordenar a cortar · MEMORY)
- P0: o prazo de qui 22h não fecha com tudo → priorizar os 7 dias datados + noite das duas; abas de bairro entram depois, num 2º deploy

## Decidi sozinho
| Decisão | Por quê | Como desfazer | Custo se errado |
|---|---|---|---|
| **Sem abas de bairro no app**: uma aba 🏘️ Bairros com link pra `paris.html` e `marais/` | pedido do Tobia no meio da onda (07/10): "coloque links pra cidade de Paris… que vão entrar os bairros na sessão paralela" | recriar abas no `data.json` | baixo |
| Saída Square Barye → Alma às **15:35** (era 15:45), pela linha 7 em Sully-Morland | factcheck: a linha 10 do roteiro não cruza a 9 e a família perderia o barco das 16:30 | `data.json`, Sáb 10 | baixo |
| Tuileries → Atelier por **Nation** (L1 → L9, ~25 min), não por Franklin D. Roosevelt | factcheck: mais rápido, sem voltar pra oeste | `data.json`, Seg 12 | baixo |
| Notre-Dame: tentar reserva já na **qui 8** | fontes divergem sobre quando abre; o PDF dizia "no próprio domingo" (era sábado) | nota de sex 9 | baixo |
| `audit.py` e `factcheck-gate.py` passam a ler o campo `aprofundar` (fora dos N4 nomeados) | sem isso o campo novo seria canal fora da cobrança de proveniência | reverter 2 linhas no `e3debc8` | baixo |
| `validate.py` usa o tempdir do sistema, não `/tmp` fixo | o sandbox nega `/tmp`; o validate quebrava | reverter 1 linha | nenhum |

## Roteiro de fases
| # | Fase / passo | Quando | Quem / bastão | Chip | Depende de |
|---|---|---|---|---|---|
| 1 | Pesquisa + pré-roteiro + PDF aprovado | 06-07/10 | sessão local_a7da077a | — | ✅ `d23d0b9` |
| 2 | **App paris-amigos-out2026** (fases 2-5 do pipeline) | ✅ 07/10 · `6dfb10b` (template `e3debc8`) | sessão local_9f1d9a16 | este | 1 |
| 3 | Coletâneas de bairro no `paris.html` | depois do 2 no ar | handoff `2026-10-07_coletaneas-bairros-paris.md` | já criado pela sessão-mãe | 2 (evita colisão na landing) |
| 4 | Auditoria externa do app (CLAUDE.md passo 11) | qua 8 ou qui 9 | sessão AUDITORA nova | chip `task_9ef64697` | 2 ✅ |
| 5 | Campo + `wrap-up.sh` + balanço de fontes | depois de 15/out | Tobia + sessão | — | viagem |

## 🔒 CONGELADO
- Sequência e horários dos 7 dias · `entregas/paris-amigos-out2026.ROTEIRO-PROPOSTO.md` · "Aprovado! Vamos construir este roteiro no app!" (Tobia 07/10). Mudar só por erro factual (P0 acima) ou pedido dele.
- PDF `entregas/Paris-Roteiro-proposto-out2026.pdf`: já está com a amiga. Não regerar sem pedido.

## Tentado e falhou
- `git push` dentro do sandbox: `CONNECT tunnel failed, 403` (github.com fora do allowlist) → rodar o push com o sandbox desligado (o `deploy.sh` faz push).
- Sites oficiais do Orsay, da Disneyland, da Tour Eiffel, de Notre-Dame e do Guignol bloqueiam leitura automática (403/Cloudflare) → usar o trecho do buscador com a URL oficial e marcar "(trecho)"; não fingir leitura.
- Nominatim/Mappy bloqueados no sandbox (MEMORY, Marais) → coordenada copiada de fonte com 5 decimais ou `coord_unverified: true` (R7: derivar é proibido).
- Visita dançada 3-5a da Orangerie: dois agentes divergiram → a página oficial diz **"Complet"** (conferida 06/10). Não oferecer.

## Estado inicial verificado
- `main` = GitHub = `d23d0b9` · worktree da mãe limpo · `estado_fechamento.py`: FECHADO.
- Pasta `paris-amigos/` **não existe** (criar) · `paris-fds/data.json` sem `feedback_url` · `maps_region: "France"`.
- Itens `[a confirmar]` herdados (o factcheck decide): preço do Ludo Jardin (€3 vs €2,50) · tempo Tuileries → Voltaire · rota de volta da Torre (L6 Bir-Hakeim → Trocadéro → L9) · Sèvres-Babylone → Solférino (L12) · horário oficial da Disney em 13/10 · fila de segurança da Torre · preços do Freddy's, do Prescription e do Les Galopins.
- Nenhuma outra sessão mexe em `paris-amigos/`. A frente 3 (coletâneas) espera esta no ar.

## Execução
A onda **começa** quando a sessão escreve a linha literal `▶ Onda iniciada`.
### F1 · Template (se o campo de aprofundamento não existir)
Campo opcional aditivo + estilo + prova nas 4 viagens existentes.
### F2 · data.json
`paris-amigos/` com `SLUG.txt` = `paris-amigos-out2026` · **sem `CITY.txt`** (é viagem datada) · 7 dias + abas de bairro (Família + resumo dos outros percursos) + link Marais + aba Trocadéro + `historia[]` curta (prosa do levantamento) · `valeAPena`/`poiCat`/`fontes` com `prova` · `mapsQuery` em toda parada de walking tour · `noMaps` em logística (malhar em casa, preparar a Disney, jantar) · `password: "paris2026"`.
### F3 · Forma
`build.py` → `validate.py` → `audit.py` (≥32 e P0=0) → `maps-audit.py --urls`.
### F4 · Verdade
FACTCHECK por subagentes Opus céticos (contexto limpo) → `paris-amigos/FACTCHECK-AAAA-MM-DD.md (nome com a data do dia)` → corrigir antes do deploy.
### F5 · Deploy
`scripts/deploy.sh "feat: roteiro paris-amigos-out2026 · 7 dias · Paris" "paris-amigos" "paris-amigos-out2026"` · `curl -I` 200 · manchete da entrega = placar do factcheck; nota /40 no rodapé.

## NÃO fazer
- Editar `const DAYS` inline no `index.html` (o sync-check bloqueia, e com razão).
- Pôr nome da amiga, do filho ou da família anfitriã no `data.json` ou no repo: o repo é público. Usar "vocês", "ele", "a gente".
- Criar as coletâneas de bairro no `paris.html` (é a frente 3).

## 🧭 Ao fechar: puxar a próxima fase
Atualiza o «Roteiro de fases» deste handoff (linha 2 ✅ com hash), troca `status: aberto` → `consumido`, cria o chip da linha 4 (auditoria externa) com bastão validado e cita no selo «Puxou a próxima fase: chip `task_…` · linha 4 do roteiro». A linha 3 já tem chip, criado pela mãe.

## Selo de fechamento (07/10/2026)
No ar: https://tsferraro.github.io/viagem/paris-amigos/ (HTTP 200) · 5 gates verdes · factcheck 218 afirmações (162 OK · 16 ERRO corrigidos · 29 RISCO · 11 INCONCLUSIVO) · forma 35/40.
Puxou a próxima fase: chip `task_9ef64697` · linha 4 do roteiro.
