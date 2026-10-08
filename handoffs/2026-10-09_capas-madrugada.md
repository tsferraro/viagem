---
status: aberto
de: sessão "Construir o app do roteiro paris-amigos-out2026" (local_9f1d9a16 · 08/10/2026)
para: a MESMA sessão, acordada por despertar único às 02:17 de sex 09/10 (CronCreate)
---

# Madrugada · capas ilustradas (og:image) de Paris e dos bairros

modo: onda · roda sozinha, o Tobia dormindo · relatório = a resposta final da sessão (ele lê de manhã)
pedido literal (08/10): *"Faz as capas ilustradas de Paris e dos bairros mas hoje de madrugada pra não comer meu limite de 5h em horário comercial."*
recarga: este arquivo · `CLAUDE.md` do repo (regra do favicon e meta tags, gates) · `~/.claude/skills/infografico-mandu/SKILL.md` (Rota A, etapas 6-7) · `scripts/icone.py`

## Escopo (o que vai ao ar)
Capa = a imagem que aparece no link compartilhado (WhatsApp etc.), `og:image` 1200×630.

| Página | Arquivo da capa | Tema da ilustração (lugares que de fato estão na coletânea) |
|---|---|---|
| `paris.html` (página da cidade) | `paris-capa-og.png` (raiz) | Paris em panorama: Sena, pontes, telhados de zinco, Torre Eiffel ao fundo |
| `marais/` | `marais/capa-og.png` | arcadas e jardim da Place des Vosges |
| `saint-germain/` | `saint-germain/capa-og.png` | Jardin du Luxembourg (Fontaine Médicis, barquinhos) e o campanário de Saint-Germain-des-Prés |
| `ilhas/` | `ilhas/capa-og.png` | Notre-Dame vista do Sena, Pont Saint-Louis, Île Saint-Louis |
| `quartier-latin/` | `quartier-latin/capa-og.png` | cúpula do Panthéon, ruelas, Jardin des Plantes |
| `louvre-tuileries/` | `louvre-tuileries/capa-og.png` | pirâmide do Louvre e o carrossel das Tuileries |
| `paris-fds/` | `paris-fds/capa-og.png` | Jardin du Ranelagh e um carrossel antigo (Marmottan ao fundo) |
| bairro novo que a frente paralela tiver publicado até a hora (ex.: `montmartre/`) | `<pasta>/capa-og.png` | os lugares da aba Família dela |

Fora: a home (`index.html`) e o app datado `paris-amigos/` (não pedidos).

## Regras da arte (decididas na avaliação de 08/10 · aprovadas pelo pedido)
- **Ilustração assumida, nunca foto** — imagem gerada com cara de foto de um lugar real é foto inventada (REGRA ZERO em imagem).
- **Zero texto na imagem** (título e descrição já vão no `og:title`/`og:description`): elimina o risco de erro de grafia, que é o ponto fraco do gerador.
- Sem pessoas reconhecíveis; no máximo silhuetas pequenas.
- **Um estilo só pra todas**: gere a de Paris primeiro e passe-a como `--ref` (âncora de estilo) em todas as outras.
- Estilo-base: ilustração editorial em guache/aquarela, traço solto, paleta quente de fim de tarde de outono (ocre, azul-ardósia, verde-oliva), luz baixa, composição horizontal com o assunto no terço central (o WhatsApp corta as bordas).

## Execução (na ordem)
1. `get_session` (self). `git fetch origin main` + `git merge --ff-only origin/main` (fora do sandbox). `git worktree list` + `git status` em cada worktree: pasta de bairro com mudança não commitada em outra sessão → **pula essa pasta** (a frente paralela pode estar nela) e registra.
2. **Código** (pequeno, aditivo):
   - `scripts/icone.py` · `meta_tags(..., capa=None)`: com capa, `og:image` = a capa (1200×630) e `twitter:card` = `summary_large_image`; sem capa, igual a hoje.
   - `scripts/build.py`: se existir `capa-og.png` ao lado do `data.json`, passa como capa.
   - `scripts/regen-landing.py`: página de cidade usa `<slug-da-cidade>-capa-og.png` da raiz se existir.
   - `validate.py` já exige `og:image` `.png` absoluto; não mexer.
3. **Gerar** com `sh ~/.claude/skills/infografico-mandu/scripts/gerar-chatgpt.sh <prompt.md> <saida.png> [--ref paris.png]` (fora do sandbox, 1-3 min cada, UMA por vez). Prompts e PNGs brutos no scratchpad da sessão, não no repo. Proporção 16:9.
4. **Olhar cada PNG** (Read). Reprova: texto/letra na imagem · cara de foto · monumento visivelmente errado (ex.: Notre-Dame com flecha errada não importa; Torre Eiffel deformada importa). Conserto: `--editar`, **teto de 2 edições**; persistiu → regera 1 vez; persistiu → essa página fica sem capa e entra no relatório.
5. **Recortar** pro centro em 1200×630 (PIL, LANCZOS) e gravar no caminho da tabela.
6. **Rebuild + gates** por pasta: `build.py` → `sync-check` · `validate` · `audit --deploy-gate` · `maps-audit` · `factcheck-gate`. Gate vermelho → **não publica essa pasta** (o PNG pode ficar commitado, a tag não muda) e registra. `VIAGEM_SKIP_*` **proibido** (a autorização do Marais em 08/10 foi pontual). Depois `regen-landing.py`.
7. Commit `feat: capas ilustradas (og:image) de Paris e dos bairros` + `git push origin HEAD:main` + `git -C <checkout principal> merge --ff-only origin/main` (fora do sandbox). `curl` 200 em cada `capa-og.png`.
8. **Relatório** = resposta final no formato ▶ Para você, com `### Resultado` (página · capa no ar ✅/❌ · prova) e uma folha de contato (as capas lado a lado num PNG só, enviada com SendUserFile pro celular dele).
9. Fecha este handoff (`status: consumido`) e o selo de encerramento.

## Paradas
- Codex sem login ou cota da assinatura esgotada → para, nada vai ao ar, relatório diz qual (o gesto é do Tobia: `codex login`).
- `main` com conflito no merge → 1 tentativa; persistiu → para e relata.
- Nenhuma pergunta ao Tobia durante a noite: o que for micro vai pra «Decidi sozinho».

## Pré-condições físicas (gesto do Tobia antes de dormir)
Mac **na tomada**, **tampa aberta**, app aberto com **esta sessão aberta e ociosa** (o despertar só dispara com a sessão parada) e o Mac impedido de dormir.
