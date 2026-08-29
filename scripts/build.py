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


def _slug_vizinho(data_path: Path) -> str:
    """Lê o SLUG.txt ao lado do data.json. É o identificador da viagem na planilha
    de relatos — sem ele os relatos chegam sem saber de qual roteiro vieram."""
    f = data_path.parent / "SLUG.txt"
    return f.read_text(encoding="utf-8").strip() if f.exists() else ""


def _icone_app(data: dict) -> str:
    """PNG 180x180 em data URI pro `apple-touch-icon`.

    Por que PNG e não SVG: o iOS **ignora SVG** em apple-touch-icon — sem um PNG
    de verdade, o atalho na Home Screen sai com um screenshot da página, que é o
    que o Tobia viu em 2026-08-27. 180px é o tamanho do iPhone @3x; o iOS
    arredonda os cantos sozinho, então a arte vai quadrada e sangrada.

    Fundo = gradiente do 1º dia (gradA→gradB), pra cada viagem ter um ícone
    distinguível na tela cheia de atalhos. Emoji do `auth_emoji` por cima, via
    NotoColorEmoji quando existir; sem ela, cai pras iniciais do nome curto.
    Se o PIL não estiver disponível, devolve "" e o template omite a tag —
    degradar sem ícone é melhor que quebrar o build.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return ""
    import base64, glob, io

    dias = data.get("days") or [{}]
    a = data.get("icon_grad_a") or dias[0].get("gradA") or "#1e3a8a"
    b = data.get("icon_grad_b") or dias[0].get("gradB") or "#3b82f6"
    rgb = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    ca, cb, N = rgb(a), rgb(b), 180

    img = Image.new("RGB", (N, N))
    px = img.load()
    for y in range(N):                       # gradiente diagonal
        for x in range(N):
            t_ = (x + y) / (2 * (N - 1))
            px[x, y] = tuple(round(ca[i] + (cb[i] - ca[i]) * t_) for i in range(3))
    d = ImageDraw.Draw(img)

    emoji = (data.get("icon_emoji") or data.get("auth_emoji") or "").strip()
    fontes = glob.glob("/usr/share/fonts/**/NotoColorEmoji*.ttf", recursive=True)
    if emoji and fontes:
        try:
            # NotoColorEmoji é bitmap: só carrega em 109px, daí reduz-se a imagem.
            # NotoColorEmoji é bitmap: só carrega em 109px. Renderiza grande,
            # RECORTA no bbox real do glifo (senão a folga interna da fonte faz o
            # ícone sair pequeno e torto) e só então escala e centraliza.
            camada = Image.new("RGBA", (218, 218), (0, 0, 0, 0))
            ImageDraw.Draw(camada).text((109, 109), emoji, anchor="mm",
                                        font=ImageFont.truetype(fontes[0], 109),
                                        embedded_color=True)
            camada = camada.crop(camada.getbbox())
            alvo = round(N * 0.62)                    # ocupa ~62% do lado
            w, h = camada.size
            esc = alvo / max(w, h)
            camada = camada.resize((max(1, round(w * esc)), max(1, round(h * esc))),
                                   Image.LANCZOS)
            ox, oy = (N - camada.width) // 2, (N - camada.height) // 2
            sombra = Image.new("RGBA", (N, N), (0, 0, 0, 0))
            sombra.paste(camada, (ox, oy + 5), camada)
            img.paste(Image.new("RGB", (N, N), (0, 0, 0)), (0, 0),
                      sombra.split()[3].point(lambda v: v // 5))
            img.paste(camada, (ox, oy), camada)
        except Exception:
            emoji = ""
    if not emoji or not fontes:
        txt = (data.get("app_short_name") or data.get("auth_title") or "?")[:2].upper()
        try:
            f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 88)
        except OSError:
            f = ImageFont.load_default()
        d.text((N // 2, N // 2 - 4), txt, font=f, anchor="mm", fill=(255, 255, 255))

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def _nome_curto(data: dict) -> str:
    """Rótulo do atalho na Home Screen. O iPhone trunca por volta de 12 chars —
    `title` de viagem quase sempre estoura, então usa-se `app_short_name`."""
    n = (data.get("app_short_name") or "").strip()
    return n or (data.get("auth_title") or data.get("title") or "Roteiro").strip()


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
        "{{APP_SHORT_NAME}}": _nome_curto(data),
        "{{APP_ICON}}": _icone_app(data),
        "{{THEME_COLOR}}": (data.get("days") or [{}])[0].get("gradA", "#111827"),
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
        "{{WT_LABELS}}": data.get("wt_labels", "numbers"),
        "{{DAYS_JSON}}": js_value(data.get("days", []), minify=minify),
        "{{LINKS_MAP_JSON}}": js_value(data.get("links_map", {}), minify=minify),
        "{{TRANSIT_MAP_JSON}}": js_value(data.get("transit_map", {}), minify=minify),
        "{{BAIRROS_CONFIG_JSON}}": js_value(data.get("bairros_config", [{"nome": "📍 Outros", "fallback": True}]), minify=minify),
        "{{HISTORIA_JSON}}": js_value(data.get("historia", []), minify=minify),
        "{{EXTRAS_JSON}}": js_value(data.get("extras", []), minify=minify),
        # Relato de campo · slug identifica a viagem na planilha; cai no SLUG.txt
        # ao lado do data.json se o próprio data.json não declarar.
        "{{ROTEIRO_SLUG}}": data.get("slug") or _slug_vizinho(data_path),
        # Vazio é estado válido: sem URL o relato fica na fila local e é copiável.
        "{{FEEDBACK_URL}}": data.get("feedback_url", ""),
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
