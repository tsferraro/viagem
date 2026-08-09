#!/usr/bin/env python3
"""
sync-check.py — o index.html que vai pro ar veio MESMO do data.json? (Lote 7a · 2026-08-09)

POR QUE EXISTE
--------------
Até hoje o CLAUDE.md mandava, pra "mudança pequena", editar inline o `const DAYS` dentro do
index.html. Isso abre dois buracos:

  (i)  DRIFT · `data.json` deixa de ser a fonte de verdade. O próximo rebuild (que sempre
       vem, mais cedo ou mais tarde) apaga em silêncio o que só existia no HTML.
  (ii) BURLA DO GATE 4d · o `factcheck-gate.py` projeta o conteúdo sensível (⭐⭐⭐ · paradas
       de walking tour · historia[]) a partir do **data.json**. Um edit inline muda o que a
       família LÊ sem mexer na projeção — o gate de frescor não vê nada e deixa passar.

Este script é o cadeado: se o HTML não bate com o data.json, o deploy para.

MÉTODO (a "projeção estável")
-----------------------------
Comparar os dois arquivos byte a byte NÃO serve: qualquer mexida em `templates/styles.css`
ou `render-functions.js` mudaria o HTML sem que uma vírgula de conteúdo mudasse, e o gate
viraria ruído. Então:

  1. o data.json é buildado num HTML temporário com os templates ATUAIS;
  2. de cada um dos dois HTMLs extraem-se os **blocos de dados** que o build injeta —
     as consts `DAYS · LINKS_MAP · TRANSIT_MAP · BAIRROS_CONFIG · HISTORIA · EXTRAS`
     (JSON) e os escalares `AUTH_PASSWORD · APP_MODE · MAPS_REGION · WT_LABELS ·
     ROTEIRO_SLUG · FEEDBACK_URL`;
  3. compara-se valor a valor, já parseado (indentação e ordem de serialização não contam
     — o que conta é o dado).

Tudo que vem de template (CSS, funções de render, markup) fica de fora de propósito: não é
conteúdo, e um roteiro buildado antes de um ajuste de template não é um roteiro adulterado.

O QUE ESTE GATE **NÃO** COBRE (dito aqui pra ninguém alegar cobertura que não existe)
-------------------------------------------------------------------------------------
- Os campos de cabeçalho/auth (`title`, `auth_title`, `header_sub`, `legend_notes_html`…)
  viram markup, não const JS. Um edit inline ali passa. É superfície de moldura, não de
  afirmação sobre o mundo — e extrair markup por regex quebraria a cada ajuste de template,
  trocando um furo estreito por falso-bloqueio recorrente.
- A VERDADE do conteúdo. Isso é FACTCHECK (`skills/critico-roteiro/FACTCHECK-EXEC.md`).

USO
---
    python3 scripts/sync-check.py <viagem>                    # ex: corsica
    python3 scripts/sync-check.py <viagem> --quiet            # modo deploy (só falha fala alto)
    python3 scripts/sync-check.py <data.json> <index.html>    # par explícito (deploy usa isto)

Exit: 0 = em sincronia · 1 = DESSINCRONIZADO ou data.json ausente · 2 = erro de uso.
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
BUILD_PY = SCRIPT_DIR / "build.py"

# Consts que o build injeta como JSON puro (`const X = {...};`)
JSON_CONSTS = ["DAYS", "LINKS_MAP", "TRANSIT_MAP", "BAIRROS_CONFIG", "HISTORIA", "EXTRAS"]

# Consts que o build injeta como string literal. AUTH_PASSWORD usa aspas simples no shell;
# os demais, aspas duplas — a regex aceita as duas pra não depender desse detalhe.
STR_CONSTS = ["AUTH_PASSWORD", "APP_MODE", "MAPS_REGION", "WT_LABELS", "ROTEIRO_SLUG",
              "FEEDBACK_URL"]

_decoder = json.JSONDecoder()


def extract_json_const(html: str, name: str):
    """Devolve (achou, valor) da const `name` no HTML.

    Usa raw_decode a partir do `=` em vez de regex greedy: o JSON é pretty-printed e cheio
    de chaves aninhadas, então casar "até o `;`" pegaria o arquivo inteiro ou pararia cedo.
    """
    m = re.search(r"^const\s+" + name + r"\s*=\s*", html, re.M)
    if not m:
        return False, None
    try:
        value, _ = _decoder.raw_decode(html, m.end())
    except ValueError as e:
        raise ValueError(f"const {name} não é JSON válido no HTML: {e}")
    return True, value


def extract_str_const(html: str, name: str):
    m = re.search(r"^const\s+" + name + r"\s*=\s*(['\"])(.*?)\1\s*;", html, re.M)
    if not m:
        return False, None
    return True, m.group(2)


def project(html: str) -> dict:
    """Projeção estável de um HTML: só os dados que vieram do data.json."""
    proj = {}
    for name in JSON_CONSTS:
        found, val = extract_json_const(html, name)
        if found:
            proj[name] = val
    for name in STR_CONSTS:
        found, val = extract_str_const(html, name)
        if found:
            proj[name] = val
    return proj


def _sample(val, limit=160):
    s = json.dumps(val, ensure_ascii=False) if not isinstance(val, str) else val
    return s[:limit] + ("…" if len(s) > limit else "")


def _first_diff(a, b, path="") -> str:
    """Aponta a PRIMEIRA divergência em profundidade — dizer só 'DAYS diferem' num roteiro
    de 16 dias não ajuda ninguém a achar o edit inline."""
    if type(a) is not type(b):
        return f"{path or '(raiz)'}: tipo {type(a).__name__} vs {type(b).__name__}"
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                return f"{path}.{k}: só no data.json"
            if k not in b:
                return f"{path}.{k}: só no HTML"
            if a[k] != b[k]:
                return _first_diff(a[k], b[k], f"{path}.{k}")
        return path
    if isinstance(a, list):
        if len(a) != len(b):
            return f"{path}: {len(a)} itens no HTML vs {len(b)} no data.json"
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                return _first_diff(x, y, f"{path}[{i}]")
        return path
    return f"{path}\n      HTML      : {_sample(a)}\n      data.json : {_sample(b)}"


def check(data_path: Path, html_path: Path, quiet=False) -> int:
    if not html_path.exists():
        print(f"❌ sync-check: HTML não encontrado: {html_path}")
        return 1
    if not data_path.exists():
        print(f"❌ sync-check: {data_path} não existe.")
        print("   Desde o Lote 7a o data.json é a fonte de verdade obrigatória: o HTML tem que")
        print("   sair de `build.py data.json index.html`. Sem data.json não há o que conferir")
        print("   — e é exatamente por esse caminho que um edit inline burla o gate 4d.")
        print("   Override explícito (assumindo o risco): VIAGEM_SKIP_GATES=1")
        return 1

    deployed = html_path.read_text(encoding="utf-8")

    with tempfile.TemporaryDirectory() as tmp:
        rebuilt_path = Path(tmp) / "rebuilt.html"
        proc = subprocess.run(
            [sys.executable, str(BUILD_PY), str(data_path), str(rebuilt_path)],
            capture_output=True, text=True)
        if proc.returncode != 0:
            print(f"❌ sync-check: build.py falhou ao rebuildar {data_path}")
            print(proc.stderr.strip() or proc.stdout.strip())
            return 1
        rebuilt = rebuilt_path.read_text(encoding="utf-8")

    try:
        p_html = project(deployed)
        p_data = project(rebuilt)
    except ValueError as e:
        print(f"❌ sync-check: {e}")
        return 1

    divergentes = []
    for key in sorted(set(p_html) | set(p_data)):
        if key not in p_html:
            divergentes.append((key, f"const {key} ausente no HTML que vai pro ar"))
        elif key not in p_data:
            divergentes.append((key, f"const {key} ausente no rebuild (template mudou?)"))
        elif p_html[key] != p_data[key]:
            divergentes.append((key, _first_diff(p_html[key], p_data[key], key)))

    if divergentes:
        print(f"❌ index.html NÃO veio do data.json · {len(divergentes)} bloco(s) divergente(s)")
        for key, detalhe in divergentes:
            print(f"   • {detalhe}")
        print()
        print(f"   Conserto: edite {data_path} e rode")
        print(f"     python3 scripts/build.py {data_path} {html_path}")
        print("   (edit inline no HTML morreu no Lote 7a: dessincroniza o data.json e o gate")
        print("    de factcheck — que projeta o data.json — não enxerga a mudança.)")
        return 1

    if not quiet:
        blocos = ", ".join(sorted(p_html))
        print(f"✅ sync OK · {html_path} bate com {data_path}")
        print(f"   blocos conferidos: {blocos}")
        print("   (fora do escopo: CSS/JS de template, cabeçalho/auth e a VERDADE do conteúdo)")
    return 0


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    quiet = "--quiet" in sys.argv

    if len(args) == 1:
        base = Path(args[0])
        if not base.is_dir():
            print(f"❌ {base} não é uma pasta de viagem")
            return 2
        data_path, html_path = base / "data.json", base / "index.html"
    elif len(args) == 2:
        data_path, html_path = Path(args[0]), Path(args[1])
    else:
        print(__doc__.strip().split("USO\n---\n")[-1])
        return 2

    return check(data_path, html_path, quiet=quiet)


if __name__ == "__main__":
    sys.exit(main())
