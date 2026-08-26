# Coletar feedback numa página estática no GitHub Pages

**Snippet mínimo funcional.** Em produção em `tsferraro/viagem` desde 04/ago/2026,
em `pais-sardenha/index.html` e `corsica/index.html`, com URL de Apps Script real embutida.

---

## Antes do código: as duas perguntas que precisam ser separadas

| Pergunta | Resposta |
|---|---|
| Página estática no Pages consegue **colher** feedback? | **Sim.** É o que este snippet faz. |
| Página estática consegue saber **quem verificadamente** respondeu? | **Não.** Sem sessão autenticada não há identidade — só o que a pessoa digitar. |

As duas coisas são independentes. A segunda é uma limitação real; a primeira não é.

---

## 1 · Servidor: Google Apps Script (~2 min, uma vez só)

Planilha → **Extensões → Apps Script** → cole:

```javascript
var ABA = 'Relatos';
var CABECALHO = ['Data', 'Origem', 'Contexto', 'Texto'];

function doPost(e) {
  try {
    var p = (e && e.parameter) || {};
    _aba().appendRow([
      p.data || new Date().toISOString(),
      p.origem  || '',
      p.contexto || '',
      p.texto   || ''
    ]);
    return _ok({ status: 'ok' });
  } catch (err) {
    // Nunca lança: o cliente envia em no-cors e não lê a resposta.
    // Um throw aqui viraria silêncio do lado de lá.
    console.error(err);
    return _ok({ status: 'erro', msg: String(err) });
  }
}

function doGet() { return _ok({ status: 'vivo' }); }   // teste rápido no browser

function _aba() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(ABA);
  if (!sh) {
    sh = ss.insertSheet(ABA);
    sh.appendRow(CABECALHO);
    sh.getRange(1, 1, 1, CABECALHO.length).setFontWeight('bold');
    sh.setFrozenRows(1);
  }
  return sh;
}

function _ok(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
                       .setMimeType(ContentService.MimeType.JSON);
}
```

**Implantar → Nova implantação → App da Web**
- Executar como: **Eu**
- Quem pode acessar: **Qualquer pessoa** ← precisa ser este

Copie a URL que termina em `/exec`.

### Por que "Qualquer pessoa" e por que isso é aceitável aqui

A página é estática e sem login: não há credencial pra apresentar. **A URL `/exec` é o segredo.**

O ponto que decide o risco: **esse endpoint só ACEITA escrita — `doPost` faz `appendRow` e devolve
`{status:'ok'}`. Ele não lê nem devolve nada da planilha.** O pior caso de vazamento da URL é
alguém escrever lixo numa linha; ninguém consegue *ler* o que já está lá. Se vazar, cria-se nova
implantação e troca-se a URL.

⚠️ Se o seu caso precisar de leitura pelo endpoint, esse raciocínio **não vale** e a conta muda.

---

## 2 · Cliente: o HTML no Pages

```html
<textarea id="fb" rows="4" placeholder="Escreva aqui"></textarea>
<button id="fb-send">Guardar</button>
<button id="fb-copy">📋 Copiar tudo</button>
<div id="fb-status"></div>

<script>
// Vazio é ESTADO VÁLIDO — ver decisão 3
const FEEDBACK_URL = "https://script.google.com/macros/s/SEU_ID/exec";
const KEY = 'feedback_v1';

const fila  = () => { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; } };
const salva = q  => { try { localStorage.setItem(KEY, JSON.stringify(q)); } catch {} };

function enfileira(texto) {
  const q = fila();
  q.push({ data: new Date().toISOString(), origem: location.pathname,
           contexto: document.title, texto });
  salva(q);
}

// no-cors: o Apps Script não devolve cabeçalho CORS, então a resposta é opaca
// POR DESIGN. Não dá pra ler status — ver decisão 2.
function tentaEnviar() {
  if (!FEEDBACK_URL) return Promise.resolve(false);
  const q = fila();
  if (!q.length) return Promise.resolve(false);
  return Promise.all(q.map(item => {
    const body = new URLSearchParams(item);   // form-encoded → cai em e.parameter
    return fetch(FEEDBACK_URL, { method: 'POST', mode: 'no-cors', body });
  })).then(() => { salva([]); return true; })
     .catch(() => false);                     // sem sinal? fica na fila
}

document.getElementById('fb-send').onclick = () => {
  const t = document.getElementById('fb').value.trim();
  if (!t) return;
  enfileira(t);                               // GRAVA PRIMEIRO — ver decisão 1
  document.getElementById('fb').value = '';
  document.getElementById('fb-status').textContent = 'guardado';  // nunca "enviado"
  tentaEnviar();                              // envia depois, best-effort
};

document.getElementById('fb-copy').onclick = () => {
  const txt = fila().map(i => `[${i.data}] ${i.contexto}\n${i.texto}`).join('\n\n');
  navigator.clipboard.writeText(txt || '(nada pendente)');
};

window.addEventListener('online', tentaEnviar);   // reenvia sozinho
tentaEnviar();                                    // e ao abrir a página
</script>
```

---

## As 3 decisões de desenho que fazem isso funcionar

**1 · Grava primeiro, envia depois.** O texto entra na fila `localStorage` **antes** de qualquer
rede. Praia e estrada sem sinal são a regra, não a exceção. O `online` reenvia sozinho.

**2 · Sem confirmação de servidor, e o botão não mente.** `mode:'no-cors'` porque o Apps Script
não devolve cabeçalho CORS — a resposta é **opaca por design**, não dá pra ler status. Por isso o
botão diz **"guardado"**, nunca "enviado com sucesso": seria mentira.

**3 · `FEEDBACK_URL` vazia é estado válido.** Sem endpoint, tudo fica na fila e o **📋 Copiar tudo**
resolve. A página nunca fica refém de um deploy externo.

---

## O que isto NÃO resolve

**Identidade verificada.** A página não tem sessão autenticada, então não existe de onde tirar um
nome — só de onde a pessoa digitou. Um `<select>` com nomes é honesto e custa um clique, mas é
**auto-declarado e repudiável**: qualquer um escolhe qualquer nome. Isso não é a mesma afirmação
que "e-mail verificado", e a diferença importa quando o dado vira prova.

Se o requisito for *quem verificadamente respondeu*, hospedagem estática é a forma errada — e aí
o diagnóstico do outro lado está certo. Só que esse é um requisito **diferente** de "colher".

**Publicidade.** Pages serve conteúdo público. Se o conteúdo da própria página for sensível, o
problema é a hospedagem, não o formulário — e nenhum snippet resolve isso.
