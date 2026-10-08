#!/usr/bin/env python3
"""icone.py — ícone (favicon + atalho na Home Screen + imagem de pré-visualização) e meta tags.

Usado por `build.py` (cada app de viagem) e `regen-landing.py` (lançadora e páginas de cidade).
Regra (Tobia 2026-10-08): **toda página entregue já sai com favicon e meta tags** — o
`validate.py` bloqueia app sem eles.

Por que ARQUIVO e não data URI: o `og:image` (a miniatura do link no WhatsApp) exige URL
absoluta de um arquivo, e o Safari do iPhone não mostrava o favicon em data URI. Por que PNG
e não SVG: o iOS ignora SVG em apple-touch-icon e o atalho sai com um screenshot da página.

Arte: fundo em gradiente diagonal (a→b) + o emoji centralizado. A fonte de emoji é a do
sistema — Noto Color Emoji (Linux/cloud) ou Apple Color Emoji (Mac). Sem nenhuma das duas,
cai pras iniciais. Sem PIL, devolve {} e as páginas saem sem as tags de ícone (degrada, não quebra).
"""
import glob
import html
import re
from pathlib import Path

SITE_BASE = "https://tsferraro.github.io/viagem/"

# (caminho, tamanho em que a fonte bitmap carrega)
_FONTES_EMOJI = [(p, 109) for p in glob.glob("/usr/share/fonts/**/NotoColorEmoji*.ttf", recursive=True)]
_FONTES_EMOJI += [(p, 160) for p in ("/System/Library/Fonts/Apple Color Emoji.ttc",) if Path(p).exists()]


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _png(emoji, grad_a, grad_b, n, iniciais):
    from PIL import Image, ImageDraw, ImageFont
    ca, cb = _rgb(grad_a), _rgb(grad_b)
    # gradiente diagonal em 180px e depois escala (rápido e liso)
    base = Image.new("RGB", (180, 180))
    px = base.load()
    for y in range(180):
        for x in range(180):
            t = (x + y) / 358
            px[x, y] = tuple(round(ca[i] + (cb[i] - ca[i]) * t) for i in range(3))
    img = base.resize((n, n), Image.BICUBIC)
    feito = False
    for caminho, tam in _FONTES_EMOJI:
        if not emoji:
            break
        try:
            camada = Image.new("RGBA", (tam * 2, tam * 2), (0, 0, 0, 0))
            ImageDraw.Draw(camada).text((tam, tam), emoji, anchor="mm",
                                        font=ImageFont.truetype(caminho, tam), embedded_color=True)
            bbox = camada.getbbox()
            if not bbox:
                continue
            camada = camada.crop(bbox)
            alvo = round(n * 0.62)
            esc = alvo / max(camada.size)
            camada = camada.resize((max(1, round(camada.width * esc)), max(1, round(camada.height * esc))),
                                   Image.LANCZOS)
            ox, oy = (n - camada.width) // 2, (n - camada.height) // 2
            sombra = Image.new("RGBA", (n, n), (0, 0, 0, 0))
            sombra.paste(camada, (ox, oy + max(2, n // 36)), camada)
            img.paste(Image.new("RGB", (n, n), (0, 0, 0)), (0, 0), sombra.split()[3].point(lambda v: v // 5))
            img.paste(camada, (ox, oy), camada)
            feito = True
            break
        except Exception:
            continue
    if not feito:
        d = ImageDraw.Draw(img)
        try:
            f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", round(n * 0.45))
        except OSError:
            try:
                f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", round(n * 0.45))
            except OSError:
                f = ImageFont.load_default()
        d.text((n // 2, n // 2), (iniciais or "?")[:2].upper(), font=f, anchor="mm", fill=(255, 255, 255))
    return img


def escrever_icones(pasta, emoji, grad_a="#1e3a8a", grad_b="#3b82f6", iniciais="?", prefixo=""):
    """Grava `<prefixo>apple-touch-icon.png` (180) e `<prefixo>icon-512.png` em `pasta`.
    Devolve {'touch': nome, 'grande': nome} (nomes relativos à pasta) ou {} sem PIL."""
    try:
        import PIL  # noqa: F401
    except ImportError:
        return {}
    pasta = Path(pasta)
    out = {}
    for chave, nome, n in (("touch", f"{prefixo}apple-touch-icon.png", 180),
                           ("grande", f"{prefixo}icon-512.png", 512)):
        _png(emoji, grad_a, grad_b, n, iniciais).save(pasta / nome, format="PNG", optimize=True)
        out[chave] = nome
    return out


def meta_tags(titulo, descricao, url_pagina, icones, url_base_icones, cor="#111827"):
    """Bloco <head> com favicon + atalho + Open Graph. `url_base_icones` é a URL absoluta
    da pasta onde os PNGs estão (o og:image precisa de URL absoluta)."""
    t = html.escape(re.sub(r"<[^>]+>", "", titulo or "").strip(), quote=True)
    d = html.escape(re.sub(r"<[^>]+>", "", descricao or "").strip(), quote=True)
    linhas = [
        f'<meta name="description" content="{d}">',
        f'<meta name="theme-color" content="{cor}">',
        '<meta property="og:type" content="website">',
        '<meta property="og:locale" content="pt_BR">',
        f'<meta property="og:title" content="{t}">',
        f'<meta property="og:description" content="{d}">',
        f'<meta property="og:url" content="{url_pagina}">',
        '<meta name="twitter:card" content="summary">',
    ]
    if icones:
        linhas += [
            f'<meta property="og:image" content="{url_base_icones}{icones["grande"]}">',
            '<meta property="og:image:width" content="512">',
            '<meta property="og:image:height" content="512">',
            f'<link rel="icon" type="image/png" sizes="512x512" href="{icones["grande"]}">',
            f'<link rel="apple-touch-icon" sizes="180x180" href="{icones["touch"]}">',
        ]
    return "\n".join(linhas)
