---
status: aberto
de: sessão "Roteiro de viagem Paris" (local_a7da077a · 06-07/10/2026)
para: sessão nova · coletâneas de bairro de Paris no formato Marais
---

# Sessão · 5 coletâneas de bairro de Paris no `paris.html` (formato Marais)

modo: onda
modelo/esforço: Opus 5.5 · alto — conteúdo profundo com proveniência e factcheck; erro aqui fica publicado e compartilhável
1ª ação: get_session (self) — confira modelo e esforço; fora do pedido, diga em 1 linha e siga
subagentes: Sonnet 5.5 (montar o data.json de um bairro a partir do levantamento) · Opus 5.5 (FACTCHECK cético, contexto limpo)
orçamento de agentes: até 9 (até 1 de montagem + 1 de factcheck por bairro, sem passar de 9)
onde roda: local
gerador do que a sessão publica: `scripts/build.py` + `scripts/deploy.sh` do repo (já existem, versionados no repo)
canal de decisão: chat — sem Mesa ativa
componentes a reusar: coletânea `marais/` (molde de abas-tema, `hideStopMarkers`, `CITY.txt`) · `templates/` · o campo de aprofundamento recolhido, se a frente do app tiver criado
recarga (§ 10a.0): `CLAUDE.md` do repo · este handoff · `MEMORY.md` (seção Marais + dicas de campo de Paris) · `git log -15`
paradas P0: só os 4 do GLOBAL § 10a-bis
definição de pronto: 5 pastas novas com `CITY.txt` = `Paris`, cada uma no ar via `deploy.sh` com os 5 gates verdes e listada em `https://tsferraro.github.io/viagem/paris.html` (HTTP 200) · 1 `FACTCHECK-<data>.md` por bairro

## ⏳ Quando começar
**Só depois que o app `paris-amigos-out2026` estiver no ar.** Confira com `git log origin/main --oneline | grep "feat: roteiro paris-amigos-out2026"`. Sem essa linha, **pare e diga ao Tobia em 1 linha**: as duas frentes regeram a landing e colidem no `main`. Prazo desta frente: nenhum (patrimônio). Pode rodar com calma, um bairro por onda.

## 👁 Visível ao Tobia
Nada pendente: o levantamento está no `main` (`d23d0b9`).

## O pedido, literal
> *"Mas aproveite pra criar as páginas de cada bairro na cidade Paris da lançadora conforme o Marais"* (Tobia, 07/10)
> e antes, em 06/10: *"faz tempo que quero complementar essa aba guarda-chuva com bairros no formato do Marais"*

1. Uma coletânea por bairro, no formato da `marais/` (cada aba é uma walking tour completa por tema), aparecendo na página da cidade `paris.html`.
2. Os 5 bairros levantados: **Saint-Germain · Odéon · Luxembourg** · **Quartier Latin** · **Île de la Cité + Île Saint-Louis** · **Louvre · Tuileries · Palais-Royal** · **Montmartre**.

## Fontes canônicas (seguir literal · REGRA ZERO)
| # | Fonte | O que buscar |
|---|---|---|
| 1 | `entregas/paris-bairros-out2026.md` | **matéria-prima**: por bairro, 4-5 abas com paradas em ordem, gancho de história + "o que observar", veredito, ★, horário/preço datado e **fonte por parada (URL + tier)** · onde comer · história & curiosidades · pula sem culpa · alertas |
| 2 | `marais/data.json` | molde: estrutura de abas-tema, `nota` por aba, densidade de `sobre`/`imperdivel`/`dicas`, `hideStopMarkers: true` |
| 3 | `CLAUDE.md` · "Padrão-ouro de storytelling" + "Numeração no mapa" | padrão de profundidade e de WT multi-parte |
| 4 | `MEMORY.md` · "Marais" + "Paris · dicas de campo" | abas-tema dispensam o toggle · Berthillon superestimado · Grande Galerie em destaque |

## Decisões já tomadas (NÃO redecidir)
| # | Decisão | Quem · quando |
|---|---|---|
| 1 | Formato Marais: abas-tema, **sem** toggle Básico↔Profundo (a aba Família já é o básico) | decisão Marais 2026-06-07 · MEMORY |
| 2 | Profundidade Marais ("história em 1º lugar", guia que precisa ganhar a gorjeta). Aprofundamento extra em bloco recolhido, se o template tiver o campo | Tobia 06-07/10 |
| 3 | Coletânea = **sem data**: o que no levantamento é de out/2026 (Guignol fechado até 18/out, Fête des Vendanges, corrida de 20 km, visitas infantis lotadas) **não** vira texto permanente. Fechamento longo (Square Jean-XXIII até jun/2027, Galerie de Paléontologie até 2027, Orsay em obras até 2028, Mur des je t'aime) entra com a data | (sugestão Claude · validar) — é a leitura do "formato Marais" |
| 4 | Berthillon: no máximo citado com a ressalva "famoso, mas a gente acha que não vale o hype" | esposa do Tobia 07/10 |
| 5 | Nome da pasta = nome curto do bairro (`saint-germain/`, `quartier-latin/`, `ilhas/`, `louvre-tuileries/`, `montmartre/`) | (sugestão Claude · validar) |

## Envelope de autonomia
| Campo | Valor |
|---|---|
| (a) orçamento | agentes: até 9 · semanal: até 10 pontos · teto que fecha: 85% → fecha o bairro em curso, entrega e passa o bastão dos restantes |
| (b) N4 pré-aprovados, por nome | nenhum (template e scripts **não** se mexem aqui; se faltar algo no template, estacionar e levar à entrega) |
| (c) pode sair para fora sozinho | `deploy.sh` de cada coletânea (push no `main` → GitHub Pages), **só com os 5 gates verdes** |
| (d) portão reprovado | aquele bairro não sobe, selo 🔴 na entrega · `VIAGEM_SKIP_*` proibido sem o Tobia |

## Paradas P0
Os 4 motivos (GLOBAL § 10a-bis). Paradas combinadas:
- P0: contexto passando de ~400 mil tokens → fecha o bairro em curso e passa o bastão dos que faltam (`passar-o-bastao`)

## Decidi sozinho
| Decisão | Por quê | Como desfazer | Custo se errado |
|---|---|---|---|
| Onda iniciada 07/10 antes do app paris-amigos estar no ar | ordem do Tobia ("faça agora", 07/10) | — | colisão da landing no `main`: no deploy, `git pull --rebase` e re-rodar `regen-landing.py` antes do push |

## Roteiro de fases
| # | Fase / passo | Quando | Quem / bastão | Chip | Depende de |
|---|---|---|---|---|---|
| 1 | Levantamento dos 5 bairros | 06/10 | sessão local_a7da077a | — | ✅ `fdd9b17` |
| 2 | App paris-amigos-out2026 | até qui 8/out | handoff `2026-10-07_app-paris-amigos.md` | criado pela mãe | 1 |
| 3 | **Coletâneas: um bairro por onda**, na ordem Saint-Germain → Quartier Latin → Ilhas → Louvre/Tuileries → Montmartre | depois do 2 no ar | esta sessão | este | 2 |
| 4 | Auditoria externa das coletâneas | depois do 3 | sessão AUDITORA nova | **esta sessão cria** | 3 |

## 🔒 CONGELADO
- `marais/` (coletânea pronta, em uso) · `paris-fds/` · `paris-amigos/` (dona: frente 2). Não editar.

## Tentado e falhou
- `git push` no sandbox: `CONNECT tunnel failed, 403` → push com o sandbox desligado.
- Sites oficiais do Orsay, de Notre-Dame, da Tour Eiffel e do Guignol bloqueiam leitura automática → trecho do buscador com URL oficial, marcado "(trecho)".
- Nominatim/Mappy bloqueados → coordenada copiada de fonte com 5 decimais ou `coord_unverified: true` (derivar é proibido, R7).
- Visita dançada 3-5a da Orangerie: o levantamento chegou a dizer "reservar já". O oficial diz **"Complet"** (06/10). Não oferecer.

## Estado inicial verificado
- `main` = GitHub = `d23d0b9` · levantamento: `entregas/paris-bairros-out2026.md` (~138 paradas · scout gate 17/20, P0=0).
- Pendências do scout gate: 11 distâncias vagas ("perto") → trocar por min/km com fonte ou tirar.
- O levantamento é calibrado para criança de 4 anos e out/2026. Na coletânea, o veredito pra criança vale pra aba Família; as outras abas são pra adulto.

## Execução
A onda **começa** quando a sessão escreve a linha literal `▶ Onda iniciada`. Um bairro por onda:
data.json (com `CITY.txt` = `Paris`, `SLUG.txt`, `hideStopMarkers: true`, `mapsQuery` em **toda** parada, `fontes` com `prova`, `historia[]`) → `build.py` → `validate.py` → `audit.py` ≥32 e P0=0 → `maps-audit.py --urls` → FACTCHECK por subagente cético → `deploy.sh "feat: coletânea <bairro> · Paris" "<pasta>" "<pasta>"` → conferir que o bairro aparece em `paris.html`.

## NÃO fazer
- Copiar alerta datado de out/2026 como texto permanente.
- Criar parada que o levantamento marcou como sem fonte de existência.
- Mexer no template ou nos scripts.

## 🧭 Ao fechar: puxar a próxima fase
Atualiza o «Roteiro de fases» (linha 3 ✅ com os hashes por bairro), troca `status: aberto` → `consumido`, cria o chip da linha 4 (auditoria) com bastão validado e cita no selo «Puxou a próxima fase: chip `task_…` · linha 4 do roteiro».

## Nota da frente 2 (app paris-amigos · 07/10/2026, depois do deploy `6dfb10b`)
- O portão desta frente abriu: `feat: roteiro paris-amigos-out2026` já está no `origin/main`.
- **Mudou o escopo a favor desta frente**: por pedido do Tobia (07/10), o app **não tem abas de bairro**. Ele tem uma aba 🏘️ Bairros que só aponta pra `https://tsferraro.github.io/viagem/paris.html` e pra `marais/`. Os bairros dos dias deles (ilhas, Saint-Germain/Luxembourg, Tuileries, Montmartre) existem **só** aqui.
- O campo de aprofundamento recolhido existe: `aprofundar` (HTML, só em `card`) · ver `references/data-schema.md`.
- Correções do factcheck que valem pra matéria-prima `entregas/paris-bairros-out2026.md`: Luxembourg 1-15/out abre 7h45-18h45 · carrossel do Luxembourg em 48.84622, 2.33420 (canto sudoeste) · Place de Furstemberg aberta c. 1699 (não 1691) · Saint-Germain-des-Prés é "uma das igrejas mais antigas" (o campanário, c. 990, é o mais antigo) · Pont Saint-Louis: 1ª ponte concluída em 1634 · Point Zéro é de latão, 1769 "segundo a tradição" · tirolesa do Ludo Jardin é da área 7-12 · Square Barye → Alma pela linha 7 (Sully-Morland). Detalhe e URLs: `paris-amigos/FACTCHECK-2026-10-07.md`.
