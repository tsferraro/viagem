# -*- coding: utf-8 -*-
"""
_deps.py — dependências e fontes dos scripts de export (md_to_docx.py · docx_to_pdf.py).

Existe porque o export quebrava em qualquer máquina que não fosse Linux de CI (Mac do Tobia,
sessão com sandbox): pip sem permissão de escrita, PyPI bloqueado e fonte DejaVu em caminho
que só existe no Linux. Aqui cada falha tem plano B e mensagem que diz o que fazer.
"""
import glob
import os
import subprocess
import sys
import tempfile

# pasta gravável em qualquer ambiente (sandbox inclusive) pra instalar pacotes sem tocar no sistema
LIBS = os.path.join(tempfile.gettempdir(), "destination-scout-pylibs")


def ensure(mod, pkg=None):
    """Importa `mod`; se faltar, instala (normal -> --user -> --target gravável) e tenta de novo."""
    if os.path.isdir(LIBS) and LIBS not in sys.path:
        sys.path.append(LIBS)
    try:
        __import__(mod)
        return
    except ImportError:
        pass
    pkg = pkg or mod
    base = [sys.executable, "-m", "pip", "install", "--quiet", "--disable-pip-version-check"]
    for extra in ([], ["--user"], ["--target", LIBS]):
        print(f"Instalando {pkg} ({' '.join(extra) or 'padrão'})...", file=sys.stderr)
        r = subprocess.run(base + extra + [pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if r.returncode == 0:
            if LIBS not in sys.path:
                sys.path.append(LIBS)
            try:
                __import__(mod)
                return
            except ImportError:
                continue
    sys.exit(
        f"ERRO: não consegui instalar '{pkg}'.\n"
        f"  Rode no seu terminal (fora de sandbox):  python3 -m pip install --user {pkg}\n"
        f"  Se o pip estiver sem rede (sandbox), libere pypi.org e files.pythonhosted.org."
    )


# (regular, negrito) em ordem de preferência. A 1ª que existir vence.
# Arial Unicode (macOS) cobre ★ ● · e acentos; DejaVu (Linux) cobre tudo; Arial/Calibri no Windows.
_CANDIDATES = [
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ("/usr/share/fonts/dejavu/DejaVuSans.ttf", "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"),
    ("/Library/Fonts/Arial Unicode.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
]


def find_fonts():
    """Devolve (regular, negrito). `PDF_FONT_DIR` (com DejaVuSans*.ttf) tem prioridade."""
    d = os.environ.get("PDF_FONT_DIR")
    if d:
        reg, bold = os.path.join(d, "DejaVuSans.ttf"), os.path.join(d, "DejaVuSans-Bold.ttf")
        if os.path.exists(reg) and os.path.exists(bold):
            return reg, bold
    for reg, bold in _CANDIDATES:
        if os.path.exists(reg) and os.path.exists(bold):
            return reg, bold
    found = glob.glob("/usr/share/fonts/**/DejaVuSans.ttf", recursive=True)
    if found:
        b = found[0].replace("DejaVuSans.ttf", "DejaVuSans-Bold.ttf")
        if os.path.exists(b):
            return found[0], b
    sys.exit(
        "ERRO: nenhuma fonte com acentos encontrada (DejaVu, Arial Unicode ou Arial).\n"
        "  Aponte uma pasta com DejaVuSans.ttf e DejaVuSans-Bold.ttf em PDF_FONT_DIR."
    )
