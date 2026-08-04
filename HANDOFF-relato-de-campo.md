# HANDOFF · a caixa de relato de campo JÁ EXISTE (2026-08-04)

**Para**: qualquer sessão que for mexer em `templates/`, `pais-sardenha/` ou criar `sardenha/`.
**Estado**: implementado, testado e na `main` · commit `1fbcda6`.

---

## ⛔ NÃO construa de novo · e NÃO faça a versão WhatsApp/mailto

Se você chegou aqui com a ideia de "botão no card que abre `wa.me` ou e-mail já preenchido",
**pare**. Essa proposta partiu de uma premissa técnica incorreta:

> "o app é estático no Pages, então não dá pra ter backend: o destino tem que ser o WhatsApp ou e-mail"

**Isso não procede.** Uma página estática pode fazer `POST` pra um **Apps Script Web App** — o
Apps Script *é* o backend, hospedado pelo Google. Não é preciso backend no Pages. A única
limitação real é não conseguir **ler** a resposta (o Apps Script não devolve cabeçalho CORS), e o
desenho já contorna isso.

Além do erro técnico, WhatsApp/mailto **derrota o propósito**: o relato voltaria a cair no
WhatsApp do Tobia → chat → sessão, que é exatamente o gargalo que a função existe pra eliminar
(na Córsega, Le Lido e Auberge Coralli levaram dias pra chegar até uma correção).

---

## O que existe hoje

Tudo no **template compartilhado** — toda viagem herda de graça, presente e futura.

| Peça | Onde |
|---|---|
| `renderRelato(dayIdx)` + fila (`relatoAdicionar` · `relatosEnviar` · `relatosTexto`) | `templates/render-functions.js` |
| Handlers dos botões (guardar · copiar tudo) | idem, em `bindCardHandlers()` |
| `.relato-*` + `@media print` (esconde na impressão) | `templates/styles.css` |
| `ROTEIRO_SLUG` e `FEEDBACK_URL` | `templates/shell.html` |
| Injeção dos dois (slug cai no `SLUG.txt` vizinho) | `scripts/build.py` · `_slug_vizinho()` |
| Código do endpoint + passo-a-passo de publicação | `scripts/apps-script-relatos.gs` |
| Checks que bloqueiam regressão | `scripts/validate.py` (2 features obrigatórias) |
| Documentação | `CLAUDE.md` · seção "Relato de campo" |

**UI**: `<details>` colapsado, último bloco do dia, depois das "Feitas hoje". Uma caixa **por dia**.

**Contrato de dados**: o app preenche 3 das 4 colunas — `Data` (quando escreveu) · `Roteiro`
(`ROTEIRO_SLUG`) · `Dia` (a aba aberta). O viajante escreve **só o relato, solto e tudo junto**.
Separar por tipo é trabalho do Claude depois, não dele. Isso foi decisão explícita do Tobia.

---

## Três invariantes · não reverta nenhuma

1. **Grava primeiro, envia depois.** O relato entra em `localStorage` (`relatos_v1`) ANTES de
   qualquer rede. Praia e estrada sem sinal são a regra, não a exceção. Reenvio automático no
   evento `online`.
2. **Sem confirmação de servidor.** O POST vai em `mode:'no-cors'`; a resposta é opaca por design.
   O botão diz **"guardado"**, nunca "enviado com sucesso" — seria mentira. Não "melhore" isso
   adicionando um check de status: não existe status legível.
3. **`FEEDBACK_URL` vazia é estado VÁLIDO.** Sem endpoint, tudo fica na fila e o botão
   **📋 Copiar tudo** resolve. O app nunca pode ficar refém de um deploy externo. Não adicione
   erro, alerta ou bloqueio quando a URL estiver vazia.

---

## ✅ Endpoint ATIVO desde 2026-08-04 · verificado ponta a ponta

O Apps Script está publicado e a `feedback_url` já está em `corsica/data.json` e
`pais-sardenha/data.json`. O Tobia confirmou os dois testes: `/exec` responde
`{"status":"vivo"}` e um relato escrito no app apareceu na aba **Relatos** da planilha.

**Viagem nova**: copie o valor de `feedback_url` de um `data.json` existente. É a mesma URL pra
todos os roteiros — a planilha separa pela coluna `Roteiro`. Não publique um Apps Script novo.

## ⚠️ Esta sessão NÃO consegue ler a planilha

`docs.google.com` e `script.google.com` estão **bloqueados** no sandbox (`CONNECT tunnel failed,
403`). O conector de Drive também exige aprovação e não resolveu. Ou seja: os relatos chegam na
planilha, mas **a sessão que vai processá-los não os enxerga sozinha**.

Caminhos que funcionam hoje, em ordem de conveniência:
1. Tobia cola o conteúdo no chat (do botão **📋 Copiar tudo**, ou direto da planilha).
2. Uma sessão desktop com conector de Drive autorizado lê e traz.

Não peça credencial de service account pra contornar isso — chave privada em chat é exposição
permanente, e nenhuma tool aqui autentica assim.

---

## Se você vai criar `sardenha/` (família, 16-23/Ago)

- **Não implemente nada de relato.** Vem do template. Só rode `build.py` normalmente.
- Ponha `feedback_url` no `data.json` se a URL já existir; senão deixe ausente (vira `""`).
- Garanta que `sardenha/SLUG.txt` existe **antes** do primeiro build — é de lá que sai o
  `ROTEIRO_SLUG`, e sem ele os relatos chegam na planilha sem saber de qual roteiro vieram.
- Crie `sardenha/DIARIO.md` nos moldes de `corsica/DIARIO.md`.

## Ao PROCESSAR relatos que chegarem

Roteamento por tipo:

| Tipo | Vai para |
|---|---|
| Erro factual (lugar fechou, preço mudou, endereço errado) | `data.json` → rebuild → deploy |
| Dica útil a **qualquer** viajante | card (`dicas`) |
| Preferência da família | `MEMORY.md` |
| Contexto do dia / o que aconteceu | `DIARIO.md` da viagem |

**FRONTEIRA DURA**: preferência da família **NUNCA** entra no card. O roteiro é compartilhável;
*"a filha cansa às 17h"* é verdade sobre eles, não sobre o lugar.

---

## Estado dos roteiros neste commit

Rebuildados com a função: `corsica/`, `pais-sardenha/`, `marais/`.
Smoke test headless (Chromium, CDP): **18/18, zero erros de JS**.
Gate de conteúdo: Córsega 34/40 · pais-sardenha 37/40 · ambos P0=0.

⚠️ `marais/` reprova no `validate.py` por **2 erros PRÉ-EXISTENTES** (35 itens sem `valeAPena`
e 2 ⭐ digitadas à mão) — confirmado que já falhavam antes deste commit. Não foram introduzidos
aqui e não bloqueiam a função. Quem for mexer no `marais/` resolve na mesma passada.

**Antes de tocar em `templates/`: `git pull`.** Este commit mexeu em `render-functions.js`,
`styles.css`, `shell.html`, `build.py` e `validate.py`.
