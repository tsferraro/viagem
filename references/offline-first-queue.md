# Padrão · fila offline-first pra captura de dados em web app

**O que é**: o padrão que faz um formulário web nunca perder o que o usuário digitou, mesmo sem
rede, sem backend próprio e sem framework. Implementado neste repo em
`templates/render-functions.js` (bloco "RELATO DE CAMPO") e verificado ponta a ponta em ago/2026.

**Pra quem lê isto de fora**: este documento é auto-contido. Não é preciso conhecer o app de
roteiros. O código de referência está no fim, genérico.

---

## 1. O problema que ele resolve

Formulário web comum faz isto:

```
usuário digita → clica enviar → POST → sucesso? mostra ✓ : mostra ✗ (e o texto some)
```

Três cenários quebram isso, e todos são comuns em uso móvel real:

| Cenário | O que acontece no padrão comum |
|---|---|
| Sem sinal (elevador, metrô, estrada, praia) | POST falha · usuário perde o que escreveu ou tem que lembrar de reenviar |
| Sinal instável (2 barras, timeout) | Usuário clica de novo · **duplica** |
| Usuário fecha a aba antes do POST voltar | Perde |

O padrão offline-first inverte a ordem:

```
usuário digita → clica → GRAVA LOCAL (síncrono, não falha) → UI confirma
                                    ↓
                          tenta enviar (assíncrono, pode falhar à vontade)
                                    ↓
                          sucesso? marca como enviado : deixa na fila e tenta depois
```

**A gravação local é a transação.** O envio é um detalhe de sincronização.

---

## 2. A invariante que não pode ser quebrada

> **Nada toca a rede antes de estar durável localmente.**

Parece óbvio e é violado o tempo todo — sempre que alguém escreve
`fetch(...).then(() => salvarLocal())`. Nessa ordem, uma falha de rede perde o dado.

Corolário: **a UI confirma a gravação, não o envio**. O rótulo do botão deve dizer
*"guardado"*, *"salvo"*, *"anotado"* — nunca *"enviado com sucesso"* se você não tem confirmação
do servidor. Mentir aqui é pior que não confirmar nada: o usuário para de conferir.

---

## 3. Escolha do armazenamento

| | `localStorage` | `IndexedDB` |
|---|---|---|
| API | síncrona, 4 métodos | assíncrona, transacional |
| Capacidade | ~5 MB (string) | centenas de MB a GB |
| Tipos | só string (precisa `JSON.stringify`) | objetos, `Blob`, `File`, `ArrayBuffer` |
| Bloqueia a UI thread | sim (irrelevante < ~100 KB) | não |
| Consultável | não (só chave→valor) | índices, cursores, ranges |

**Regra prática:**
- **`localStorage`** se o payload é texto e o volume é de dezenas/centenas de registros pequenos.
  A API síncrona é uma vantagem real aqui: não existe estado "meio gravado".
- **`IndexedDB`** (via [`idb`](https://github.com/jakearchibald/idb), ~1 KB) se houver anexos,
  fotos, áudio, milhares de registros, ou necessidade de consulta.

Neste repo é `localStorage`: relatos são texto curto, dezenas por viagem. Se um dia entrar áudio
ou foto, o armazenamento tem que migrar para IndexedDB — `localStorage` não guarda `Blob` e 5 MB
somem com dois áudios.

### Formato da fila

Um array de objetos sob uma chave versionada:

```js
const FILA_KEY = 'relatos_v1';   // o _v1 permite migrar o formato depois sem quebrar quem tem dado antigo
```

Versionar a chave desde o dia 1 custa nada e evita ter que escrever código de migração
adivinhando o formato antigo.

---

## 4. ⚠️ Idempotência — o ponto onde a implementação deste repo é DELIBERADAMENTE simples

**Leia esta seção antes de copiar o código para um app de trabalho.**

Uma fila com retry entrega **at-least-once**, nunca exactly-once. A janela é real:

```
cliente envia → servidor grava → resposta se perde no caminho de volta
             → cliente acha que falhou → tenta de novo → LINHA DUPLICADA
```

Este repo **aceita** esse risco porque o custo de uma linha duplicada num diário de viagem é
zero — um humano lê e ignora. **Num app de trabalho quase nunca é zero** (pedido duplicado,
lançamento contábil duplicado, e-mail disparado duas vezes).

A correção é barata e deve ser feita desde o início:

```js
// CLIENTE: id estável gerado UMA vez, no momento da criação do registro.
// Nunca regenerar no retry — é justamente o id que identifica a mesma tentativa.
const item = {
  id: (crypto.randomUUID?.() || String(Date.now()) + Math.random().toString(36).slice(2)),
  criadoEm: new Date().toISOString(),
  payload: { texto: valorDoCampo },
  enviado: false
};
```

```js
// SERVIDOR: rejeita id já visto (aqui em Apps Script; num backend real, UNIQUE INDEX no id)
function jaProcessado(id) {
  var cache = CacheService.getScriptCache();
  if (cache.get(id)) return true;
  cache.put(id, '1', 21600);          // 6h · janela de retry realista
  return false;
}
```

Com `UNIQUE INDEX` no banco, o retry vira um no-op e o cliente pode ser burro à vontade. **Essa é
a arquitetura certa**: idempotência no servidor, retry ingênuo no cliente. Tentar resolver isso só
no cliente é impossível — ele nunca sabe se a resposta perdida representava sucesso.

---

## 5. Transporte: quando `no-cors` e quando NÃO

Neste repo o POST vai assim:

```js
fetch(URL, { method:'POST', mode:'no-cors', body: new URLSearchParams({ texto: valor }) })
```

`mode:'no-cors'` faz o navegador enviar a requisição mas devolve uma **resposta opaca**:
`status` é sempre `0`, corpo ilegível, headers inacessíveis. Você sabe que a requisição *saiu*.
Não sabe se o servidor gravou.

**Isso não é uma virtude — é uma concessão.** Foi necessário porque o destino é um **Google Apps
Script Web App**, que não devolve cabeçalho `Access-Control-Allow-Origin`. Vantagem: backend
grátis, zero infra, publicação em 2 minutos.

**Num app de trabalho com backend próprio, NÃO use `no-cors`.** Configure CORS direito e tenha
confirmação real:

```js
// servidor devolve Access-Control-Allow-Origin: https://seu-app.exemplo
const r = await fetch(URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(item)
});
if (!r.ok) throw new Error('HTTP ' + r.status);   // AGORA dá pra distinguir 4xx de 5xx
```

A diferença prática é grande:

| | `no-cors` | CORS configurado |
|---|---|---|
| Sabe se gravou | não | sim |
| Distingue "servidor fora" de "payload inválido" | não | sim (5xx vs 4xx) |
| Retry inteligente (não insistir em 4xx) | impossível | possível |
| UI pode dizer "enviado" | **não** | sim |

**Regra de retry com CORS**: `4xx` (exceto `408`/`429`) é erro permanente — **não** retentar,
mover pro estado "falhou, precisa de intervenção". `5xx`, `408`, `429` e falha de rede são
transitórios — retentar com backoff.

Outro detalhe que morde: usar `Content-Type: application/json` dispara **preflight `OPTIONS`**.
`application/x-www-form-urlencoded`, `text/plain` e `multipart/form-data` são "simple requests" e
não disparam. Em rede ruim, evitar o preflight economiza um round-trip inteiro.

---

## 6. Quando tentar reenviar

Três gatilhos cobrem quase tudo:

```js
window.addEventListener('online', flush);                  // conexão voltou
document.addEventListener('visibilitychange', () => {       // app voltou pro primeiro plano
  if (document.visibilityState === 'visible') flush();
});
flush();                                                    // ao carregar
```

**`navigator.onLine` mente.** Ele diz apenas se há *interface de rede*, não se há *internet*.
Wi-Fi de hotel com portal cativo, ou 4G sem sinal real, reportam `online: true`. Use o evento
como *dica* para tentar — nunca como condição para gravar. O fluxo aqui grava sempre e usa o
evento só pra chamar o flush.

**Backoff** (necessário assim que houver mais de um usuário — senão um servidor caindo leva uma
tempestade de retries):

```js
const espera = Math.min(30000, 1000 * 2 ** tentativas) + Math.random() * 1000;  // jitter evita sincronia
```

O `Math.random()` (jitter) não é enfeite: sem ele, todos os clientes que falharam juntos retentam
juntos e derrubam o servidor de novo no mesmo instante.

**Concorrência**: o flush pode ser disparado por dois gatilhos ao mesmo tempo. Proteja com um
flag simples (`if (flushing) return; flushing = true; ... finally { flushing = false }`), senão o
mesmo item sai duas vezes.

---

## 7. Os modos de falha do próprio armazenamento

Duas coisas quebram `localStorage` e **as duas são invisíveis se você não testar**:

### 7.1 Cota estourada

```js
function gravar(fila) {
  try {
    localStorage.setItem(KEY, JSON.stringify(fila));
    return true;
  } catch (e) {
    // QuotaExceededError. No Safari em modo privado ANTIGO, o setItem lançava SEMPRE.
    // Não deixe passar em silêncio: o usuário precisa saber que o dado NÃO foi guardado.
    return false;
  }
}
```

Sempre devolva um booleano e **trate o `false` na UI**. O pior resultado possível é o app dizer
"guardado ✓" quando nada foi guardado.

Política de retenção: descartar os itens **já enviados** mais antigos quando a cota apertar —
nunca descartar pendentes.

### 7.2 Storage que não persiste

Navegador em modo privado e **webview embutida em app** (Instagram, WhatsApp, LinkedIn — onde
muito link é aberto) usam armazenamento efêmero: funciona durante a sessão e some ao fechar.
O usuário não faz ideia.

Sonda barata:

```js
function storagePersiste() {
  try {
    localStorage.setItem('__probe', '1');
    const ok = localStorage.getItem('__probe') === '1';
    localStorage.removeItem('__probe');
    return ok;
  } catch (e) { return false; }
}
```

Detecção de webview embutida (heurística, imperfeita mas útil):

```js
const embutido = /FBAN|FBAV|Instagram|Line\/|WhatsApp/i.test(navigator.userAgent);
```

Se qualquer dos dois der positivo, mostre um aviso e ofereça "abrir no navegador". Este repo faz
isso em `maybeWarnStorage()`.

---

## 8. O nível seguinte: Service Worker + Background Sync

O padrão descrito aqui só sincroniza **com o app aberto**. Se o usuário escreve no túnel e fecha
a aba, o envio só acontece na próxima abertura.

A **Background Sync API** resolve — o navegador envia depois, mesmo com a aba fechada:

```js
// na página
const reg = await navigator.serviceWorker.ready;
await reg.sync.register('enviar-fila');

// no service worker
self.addEventListener('sync', e => {
  if (e.tag === 'enviar-fila') e.waitUntil(enviarTudoDoIndexedDB());
});
```

**A ressalva que decide**: Background Sync é **Chromium-only**. Safari (todo iOS, inclusive
Chrome no iOS, que é Safari por baixo) e Firefox **não implementam**. Se o público inclui iPhone
— e num app de campo quase sempre inclui — ela é uma **otimização progressiva**, nunca a
estratégia principal. O flush no `online`/`visibilitychange` continua sendo obrigatório.

Note também que dentro do Service Worker não existe `localStorage` (API síncrona é proibida lá).
Se você for por esse caminho, a fila **tem** que estar em IndexedDB desde o começo. É o argumento
mais forte pra escolher IndexedDB mesmo com payload pequeno, caso Background Sync esteja no
horizonte.

---

## 9. Segurança · o que fica exposto

**Todo endpoint chamado pelo cliente é público.** Está no código-fonte, visível em "ver fonte" ou
na aba Network. Não existe segredo no front-end. Consequências:

- **Nunca** coloque chave de API, token ou credencial no cliente. Chamada que precisa de segredo
  vai por um proxy no seu servidor.
- Um endpoint de escrita anônima **vai** receber lixo eventualmente. Mitigações por ordem de
  custo: rate-limit por IP → CAPTCHA invisível → token de sessão curto emitido pelo backend.
- Neste repo, o endpoint é *write-only* (não devolve dados) e o conteúdo é de baixo valor, então
  a exposição foi aceita conscientemente. **Num app de trabalho, decida isso explicitamente** —
  e registre a decisão.

E o inverso: **o que fica na fila local também está exposto**, a quem tiver o aparelho. Não
guarde dado sensível em `localStorage` sem criptografia — e criptografia no cliente com chave no
cliente não é criptografia.

---

## 10. Como testar (o que de fato pegou bugs aqui)

Três técnicas, em ordem de valor:

**a) Servidor falso local** — sobe um `http.createServer` em `127.0.0.1`, aponta o app pra ele e
inspeciona o corpo recebido. É o único jeito de provar que o payload chega com os campos certos.

**b) Substituir `fetch` pra simular queda de rede** — muito mais confiável que o checkbox
"Offline" do DevTools, e roda em CI:

```js
const original = window.fetch;
window.fetch = () => Promise.reject(new Error('offline'));
// ... escreve, verifica que ficou na fila e que nada saiu ...
window.fetch = original;
window.dispatchEvent(new Event('online'));
// ... verifica que drenou ...
```

**c) Chromium headless via CDP** — sem dependência de framework de teste; conecta no
`--remote-debugging-port`, avalia expressões e captura `Runtime.exceptionThrown`. O script deste
repo tem ~60 linhas e cobre o ciclo inteiro.

Casos que precisam estar no teste (todos já quebraram algum app real):

- [ ] grava com rede caída · nada sai · fila cresce
- [ ] volta a rede · drena sozinho · fila zera
- [ ] **não reenvia** o que já foi enviado
- [ ] envio duplicado (dois cliques rápidos) não gera duas linhas
- [ ] campo vazio/só espaços não entra na fila
- [ ] a fila sobrevive a navegação e a reload
- [ ] `localStorage` bloqueado (modo privado) → UI avisa, não mente
- [ ] payload com aspas, quebra de linha, emoji e acento chega íntegro

---

## 11. Implementação de referência (genérica, ~70 linhas)

```js
const FILA_KEY = 'fila_v1';
const ENDPOINT = '';          // vazio é estado válido: fica tudo local
let flushing = false;

const ler     = () => { try { return JSON.parse(localStorage.getItem(FILA_KEY) || '[]'); } catch { return []; } };
const gravar  = a  => { try { localStorage.setItem(FILA_KEY, JSON.stringify(a)); return true; } catch { return false; } };
const novoId  = () => crypto.randomUUID?.() || Date.now() + '-' + Math.random().toString(36).slice(2);

/** Enfileira. Devolve false se o storage recusou — a UI PRECISA tratar isso. */
function enfileirar(payload) {
  const fila = ler();
  fila.push({ id: novoId(), criadoEm: new Date().toISOString(), payload, enviado: false, tentativas: 0 });
  return gravar(fila);
}

/** Tenta esvaziar. Silenciosa: sem endpoint, sem rede ou servidor fora, só não marca nada. */
async function flush() {
  if (flushing || !ENDPOINT) return;
  flushing = true;
  try {
    const fila = ler();
    for (const item of fila.filter(i => !i.enviado)) {
      try {
        const r = await fetch(ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id: item.id, ...item.payload })   // id vai junto: servidor deduplica
        });
        if (r.ok) item.enviado = true;
        else if (r.status >= 400 && r.status < 500 && r.status !== 408 && r.status !== 429) {
          item.erroPermanente = true;    // não adianta retentar payload inválido
          item.enviado = true;           // sai da fila de retry, fica marcado pra inspeção
        } else item.tentativas++;
      } catch { item.tentativas++; }     // falha de rede: fica pra próxima
    }
    gravar(fila.filter(i => !i.enviado || Date.now() - Date.parse(i.criadoEm) < 30 * 864e5));  // poda enviados > 30d
  } finally { flushing = false; }
}

window.addEventListener('online', flush);
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') flush(); });
flush();

/** Saída de emergência: se o endpoint nunca funcionar, o usuário ainda extrai o que escreveu. */
function pendentesComoTexto() {
  return ler().filter(i => !i.enviado).map(i => JSON.stringify(i.payload)).join('\n');
}
```

---

## 12. Checklist de revisão

- [ ] A gravação local acontece **antes** de qualquer chamada de rede
- [ ] A UI confirma **gravação**, não envio (a menos que haja confirmação real via CORS)
- [ ] Falha de `setItem` (cota, modo privado) é tratada e comunicada — nunca silenciosa
- [ ] Cada item tem **id estável** e o servidor **deduplica** por ele
- [ ] Retry distingue erro permanente (4xx) de transitório (5xx/rede)
- [ ] Backoff **com jitter**
- [ ] Flush protegido contra execução concorrente
- [ ] Chave de storage **versionada** (`_v1`)
- [ ] Existe **saída manual** (copiar/exportar) pra quando o endpoint nunca funcionar
- [ ] Nenhum segredo no cliente · endpoint tratado como público
- [ ] Teste automatizado cobre: offline → fila → online → drena → não duplica

---

## 13. A decisão de produto por trás disso

O ganho real não foi técnico. Antes, a correção de campo dependia de: lembrar → mandar mensagem →
alguém ler → alguém aplicar. Cada elo perdia informação e adicionava dias de atraso.

A caixa não ficou melhor porque sincroniza offline. Ficou melhor porque **está no lugar e no
momento em que a pessoa tem a informação na cabeça**, e porque **não pede nada dela além do
texto** — quem escreve não classifica, não escolhe categoria, não preenche campo obrigatório.
Toda fricção que você adiciona no momento da captura é paga em dado que nunca chega.

O offline-first é o que torna isso confiável o bastante pra virar hábito. Um formulário que perde
o que a pessoa escreveu uma vez não é usado uma segunda.
