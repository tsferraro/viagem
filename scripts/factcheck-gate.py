#!/usr/bin/env python3
"""
factcheck-gate.py — gate 4d do deploy.sh: FRESCOR + FORMATO do factcheck (R6 · auditoria 2026-08-08).

POR QUE ISTO EXISTE
-------------------
A auditoria provou que o FACTCHECK era protocolo de honra: nenhum passo deixava artefato, e
"rodei um factcheck completo" era inverificável — a Loggia inventada passou por um no mesmo dia
em que foi desmentida em campo. Este gate cobra o que É cobrável por máquina sem ser gameable
por substring: que o artefato EXISTE, tem FORMATO válido (vereditos por item, fonte com URL) e
é MAIS NOVO que a última mudança de conteúdo sensível. A verdade do conteúdo do factcheck não é
cobrável aqui — é trabalho da sessão auditora e do campo.

USO
---
    python3 scripts/factcheck-gate.py <viagem-dir>            # ex: corsica, pais-sardenha
    python3 scripts/factcheck-gate.py <viagem-dir> --quiet    # só erros (CI/deploy)

Exit: 0 = passa · 1 = BLOQUEIA deploy · 2 = erro de uso.

O QUE BLOQUEIA
--------------
1. Nenhum FACTCHECK-AAAA-MM-DD.md na pasta da viagem.
2. Formato inválido no mais recente: zero linhas de veredito · OK/ERRO/RISCO sem URL ·
   ERRO sem "corrigido" · data no nome do arquivo no futuro (forja).
3. Conteúdo SENSÍVEL mudou depois da data do factcheck: projeção sensível do data.json
   (cards ⭐⭐⭐: sobre/imperdivel/dicas/coord/mapsQuery · TODA parada de walking tour ·
   opções ⭐⭐⭐ · historia[]) difere entre a versão commitada até a data do factcheck e a
   que vai pro ar — e o factcheck não é de hoje. Edit não-sensível passa sem factcheck novo.

Granularidade declarada: DIA. Edit sensível + factcheck do MESMO dia passam juntos (o deploy
roda antes do commit, então não há timestamp de git pra mudança não-commitada). A sessão
auditora testa forja com data antiga/futura; forja com data de hoje só o campo pega.
"""
import json
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

C_OK, C_ERR, C_WARN, C_DIM, C_END = '\033[92m', '\033[91m', '\033[93m', '\033[2m', '\033[0m'

FC_NAME_RE = re.compile(r'^FACTCHECK-(\d{4})-(\d{2})-(\d{2})\.md$')
VEREDITO_RE = re.compile(r'\b(OK|ERRO|RISCO|INCONCLUSIVO)\b')
URL_RE = re.compile(r'https?://\S+')


def projecao_sensivel(data: dict) -> str:
    """Projeção canônica do conteúdo que EXIGE verificação: é a mudança disto que torna um
    factcheck velho. Espelha a lista do handoff/R6: sobre|imperdivel|dicas|opcoes|historia|
    coord de item ⭐⭐⭐ e TODA parada de WT (rota física nunca é 'edit pequeno')."""
    proj = {}
    for day in data.get('days', []) or []:
        for s in day.get('stops', []) or []:
            if s.get('tipo') == 'card' and s.get('valeAPena') == 3:
                proj[f"card3:{s.get('nome','?')}"] = [
                    s.get('sobre'), s.get('imperdivel'), s.get('dicas'),
                    s.get('coord'), s.get('mapsQuery')]
            for wt in s.get('walkingTours', []) or []:
                for st in wt.get('stops', []) or []:
                    proj[f"wt:{wt.get('nome','?')}:{st.get('nome','?')}"] = [
                        st.get('mapsQuery'), st.get('coord')]
            for o in s.get('opcoes', []) or []:
                if o.get('valeAPena') == 3:
                    proj[f"opcao3:{o.get('nome','?')}"] = [o.get('desc'), o.get('coord')]
    for h in data.get('historia', []) or []:
        proj[f"historia:{h.get('titulo','?')}"] = [h.get('prosa_html')]
    return json.dumps(proj, ensure_ascii=False, sort_keys=True)


def _git(repo: Path, *args) -> str:
    r = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ''


def checa_formato(texto: str, quiet: bool):
    """Valida o formato do artefato. Devolve lista de problemas (vazia = ok)."""
    problemas = []
    linhas_veredito = []
    for ln in texto.splitlines():
        if not ln.strip().startswith('|'):
            continue
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        if len(cells) < 3:
            continue
        m = VEREDITO_RE.search(ln)
        if not m or set(cells) & {'---', ':---', '---:'} or 'Veredito' in ln:
            continue
        linhas_veredito.append((ln, m.group(1)))
    if not linhas_veredito:
        problemas.append('zero linhas de veredito — factcheck vazio/tocado não é factcheck '
                         '(formato: | item | afirmação | veredito | fonte | data |)')
        return problemas, 0
    for ln, v in linhas_veredito:
        if v in ('OK', 'ERRO', 'RISCO') and not URL_RE.search(ln):
            problemas.append(f'veredito {v} sem fonte com URL: {ln.strip()[:80]}…')
        if v == 'ERRO' and 'corrigid' not in ln.lower():
            problemas.append(f'ERRO sem marca de correção ("→ corrigido") — erro conhecido '
                             f'não corrigido não deploya: {ln.strip()[:80]}…')
    return problemas, len(linhas_veredito)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    quiet = '--quiet' in sys.argv
    if not args:
        print(__doc__)
        return 2
    vdir = Path(args[0]).resolve()
    if not vdir.is_dir():
        print(f"{C_ERR}✗{C_END} pasta não existe: {vdir}")
        return 2

    def say(msg):
        if not quiet:
            print(msg)

    say(f"\n→ Gate de factcheck (frescor+formato) · {vdir.name}")

    # 1 · existe artefato?
    fcs = sorted([p for p in vdir.glob('FACTCHECK-*.md') if FC_NAME_RE.match(p.name)])
    if not fcs:
        print(f"{C_ERR}✗ BLOQUEADO: nenhum FACTCHECK-AAAA-MM-DD.md em {vdir.name}/ — "
              f"verificação sem artefato não conta (ver skills/critico-roteiro/FACTCHECK-EXEC.md){C_END}")
        return 1
    fc = fcs[-1]
    y, mo, d = map(int, FC_NAME_RE.match(fc.name).groups())
    try:
        fc_date = date(y, mo, d)
    except ValueError:
        print(f"{C_ERR}✗ BLOQUEADO: data inválida no nome {fc.name}{C_END}")
        return 1
    if fc_date > date.today():
        print(f"{C_ERR}✗ BLOQUEADO: {fc.name} tem data FUTURA — factcheck forjado{C_END}")
        return 1

    # 2 · formato válido (vereditos por item)?
    problemas, n_itens = checa_formato(fc.read_text(encoding='utf-8'), quiet)
    if problemas:
        print(f"{C_ERR}✗ BLOQUEADO: {fc.name} com formato inválido:{C_END}")
        for p in problemas[:8]:
            print(f"  {C_ERR}•{C_END} {p}")
        return 1
    say(f"  {C_OK}✓{C_END} {fc.name}: {n_itens} item(ns) com veredito e fonte")

    # 3 · frescor: conteúdo sensível mudou DEPOIS do factcheck?
    data_json = vdir / 'data.json'
    if not data_json.exists():
        say(f"  {C_WARN}⚠{C_END} sem data.json — frescor não conferível por projeção "
            f"(só existência+formato)")
        return 0
    try:
        proj_now = projecao_sensivel(json.loads(data_json.read_text(encoding='utf-8')))
    except Exception as e:
        print(f"{C_ERR}✗ BLOQUEADO: data.json ilegível: {e}{C_END}")
        return 1

    top = _git(vdir, 'rev-parse', '--show-toplevel')
    repo = Path(top) if top else vdir.parent
    rel = data_json.relative_to(repo)
    base_rev = _git(repo, 'rev-list', '-1', f'--before={fc_date.isoformat()}T23:59:59',
                    'HEAD', '--', str(rel))
    if not base_rev:
        print(f"{C_ERR}✗ BLOQUEADO: {fc.name} é anterior ao primeiro commit do data.json — "
              f"o factcheck não pode ter verificado este conteúdo{C_END}")
        return 1
    base_txt = _git(repo, 'show', f'{base_rev}:{rel}')
    try:
        proj_base = projecao_sensivel(json.loads(base_txt)) if base_txt else ''
    except Exception:
        proj_base = ''

    if proj_now == proj_base:
        say(f"  {C_OK}✓{C_END} conteúdo sensível intacto desde {fc_date.isoformat()} — fresco")
        return 0
    if fc_date == date.today():
        say(f"  {C_WARN}⚠{C_END} conteúdo sensível mudou, mas o factcheck é de HOJE — "
            f"passa (granularidade de dia · confira que ele cobre o que mudou)")
        return 0

    # lista o que mudou pra orientar o factcheck novo
    a, b = json.loads(proj_base or '{}'), json.loads(proj_now)
    mudados = sorted(set(k for k in set(a) | set(b) if a.get(k) != b.get(k)))
    print(f"{C_ERR}✗ BLOQUEADO: conteúdo SENSÍVEL mudou depois de {fc.name} "
          f"({len(mudados)} item(ns)) — rode factcheck novo (FACTCHECK-EXEC.md):{C_END}")
    for k in mudados[:10]:
        print(f"  {C_ERR}•{C_END} {k}")
    if len(mudados) > 10:
        print(f"  {C_DIM}… +{len(mudados)-10}{C_END}")
    return 1


if __name__ == '__main__':
    sys.exit(main())
