/**
 * RELATOS DE CAMPO · endpoint da planilha única
 * ---------------------------------------------------------------------------
 * Recebe o POST da caixa "📣 Como foi este dia?" dos apps de roteiro e grava
 * uma linha na aba "Relatos".
 *
 * COMO PUBLICAR (2 min, uma vez só — serve todos os roteiros):
 *   1. Abra a planilha → Extensões → Apps Script
 *   2. Cole este arquivo inteiro (substitua o Code.gs que vier)
 *   3. Implantar → Nova implantação → tipo "App da Web"
 *        · Executar como:    Eu
 *        · Quem pode acessar: Qualquer pessoa            ← precisa ser este
 *   4. Copie a URL que termina em /exec
 *   5. Mande a URL pro Claude · ela entra em feedback_url no data.json
 *
 * Por que "Qualquer pessoa": o app é uma página estática no GitHub Pages, sem
 * login. A URL /exec é o segredo. Ela só ACEITA escrita (não devolve dados),
 * então o pior caso de vazamento é alguém escrever lixo na planilha — não ler
 * os relatos da família. Se vazar, é só criar nova implantação e trocar a URL.
 */

var ABA = 'Relatos';
var CABECALHO = ['Data', 'Roteiro', 'Dia', 'Relato'];

function doPost(e) {
  try {
    var p = (e && e.parameter) || {};
    var sh = _aba();
    sh.appendRow([
      p.data || new Date().toISOString(),
      p.roteiro || '',
      p.dia || '',
      p.texto || ''
    ]);
    return _ok({ status: 'ok' });
  } catch (err) {
    // Nunca lança: o app envia em no-cors e não lê a resposta de qualquer forma.
    // Um erro aqui viraria silêncio no cliente — melhor registrar no log do Script.
    console.error(err);
    return _ok({ status: 'erro', msg: String(err) });
  }
}

function doGet() {
  return _ok({ status: 'vivo', aba: ABA });
}

function _aba() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(ABA);
  if (!sh) {
    sh = ss.insertSheet(ABA);
    sh.appendRow(CABECALHO);
    sh.getRange(1, 1, 1, CABECALHO.length).setFontWeight('bold');
    sh.setFrozenRows(1);
    sh.setColumnWidth(1, 160);
    sh.setColumnWidth(2, 150);
    sh.setColumnWidth(3, 150);
    sh.setColumnWidth(4, 640);
  }
  return sh;
}

function _ok(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
