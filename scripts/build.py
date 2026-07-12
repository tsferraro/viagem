#!/usr/bin/env python3
"""
build.py — Gera index.html a partir de data.json + templates

Uso:
    python3 build.py /caminho/data.json /caminho/output.html

Templates lidos de ./templates/ (relativo ao script):
    - shell.html        (com placeholders)
    - styles.css        (injetado em {{STYLES_CSS}})
    - render-functions.js (injetado em {{RENDER_FUNCTIONS_JS}})

data.json deve ter campos:
    title, auth_emoji, auth_title, auth_subtitle, header_title, header_sub,
    password, legend_group_text, legend_notes_html,
    days (list), links_map (dict), transit_map (dict), bairros_config (list)
"""

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
TEMPLATES_DIR = SKILL_ROOT / "templates"


def js_value(obj, minify=False):
    """Serializa um valor Python pra JS (JSON-compatible).
    Default: pretty-printed (indent=2) pra facilitar edit manual no mobile.
    minify=True: sem espaços, pra reduzir tamanho em viagens grandes (>14 dias).
    """
    if minify:
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return json.dumps(obj, ensure_ascii=False, indent=2)


def build(data_path: Path, output_path: Path, minify=False):
    # 1. Carregar data
    with data_path.open(encoding="utf-8") as f:
        data = json.load(f)

    # 2. Carregar templates
    shell = (TEMPLATES_DIR / "shell.html").read_text(encoding="utf-8")
    styles = (TEMPLATES_DIR / "styles.css").read_text(encoding="utf-8")
    render_js = (TEMPLATES_DIR / "render-functions.js").read_text(encoding="utf-8")

    # 3. Substituições (ordem importa: placeholders dentro de styles/render NÃO devem ser substituídos)
    replacements = {
        "{{TITLE}}": data.get("title", "Roteiro"),
        "{{AUTH_EMOJI}}": data.get("auth_emoji", "✈️"),
        "{{AUTH_TITLE}}": data.get("auth_title", "Roteiro"),
        "{{AUTH_SUBTITLE}}": data.get("auth_subtitle", "Acesso restrito família"),
        "{{HEADER_TITLE}}": data.get("header_title", "Roteiro"),
        "{{HEADER_SUB}}": data.get("header_sub", ""),
        "{{PASSWORD}}": data.get("password", "viagem"),
        "{{LEGEND_GROUP_TEXT}}": data.get("legend_group_text", "Dia com família"),
        "{{LEGEND_NOTES_HTML}}": data.get("legend_notes_html", ""),
        "{{MODE}}": data.get("mode", "trip"),
        "{{MAPS_REGION}}": data.get("maps_region", ""),
        "{{DAYS_JSON}}": js_value(data.get("days", []), minify=minify),
        "{{LINKS_MAP_JSON}}": js_value(data.get("links_map", {}), minify=minify),
        "{{TRANSIT_MAP_JSON}}": js_value(data.get("transit_map", {}), minify=minify),
        "{{BAIRROS_CONFIG_JSON}}": js_value(data.get("bairros_config", [{"nome": "📍 Outros", "fallback": True}]), minify=minify),
        "{{HISTORIA_JSON}}": js_value(data.get("historia", []), minify=minify),
        "{{EXTRAS_JSON}}": js_value(data.get("extras", []), minify=minify),
    }

    # Substituições simples nos textos
    out = shell
    for key, val in replacements.items():
        out = out.replace(key, str(val))

    # Injeção dos arquivos grandes (CSS + JS) DEPOIS, pra não serem afetados
    out = out.replace("{{STYLES_CSS}}", styles)
    out = out.replace("{{RENDER_FUNCTIONS_JS}}", render_js)

    # 4. Verificar que não sobraram placeholders
    import re
    leftover = re.findall(r"\{\{[A-Z_]+\}\}", out)
    if leftover:
        print(f"⚠️  Placeholders não substituídos: {set(leftover)}", file=sys.stderr)

    # 5. Escrever output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(out, encoding="utf-8")
    size_kb = len(out) // 1024
    print(f"✓ Gerado: {output_path} ({size_kb}KB)")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    minify = "--minify" in flags

    if len(args) < 2:
        print("Uso: python3 build.py /path/data.json /path/output.html [--minify]")
        print("")
        print("Default: JSON pretty-printed (indent=2) · fácil edit manual no mobile")
        print("--minify: JSON compacto · ~15% menor · use só pra viagens >14 dias se passar de 300KB")
        sys.exit(2)

    data_path = Path(args[0])
    output_path = Path(args[1])

    if not data_path.exists():
        print(f"❌ data.json não existe: {data_path}", file=sys.stderr)
        sys.exit(2)

    build(data_path, output_path, minify=minify)


if __name__ == "__main__":
    main()
