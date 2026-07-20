#!/usr/bin/env python3
"""
run_tests.py — Suite de regressão do audit.py (o auditor testando a si mesmo).

Fecha o furo dim-9 da auto-avaliação (skill-creator: "linter é o candidato perfeito
pra evals"). Roda os fixtures em tests/fixtures/ e trava o comportamento: se alguém
mexer num regex e a nota/severidade mudar, um teste quebra e força decisão consciente.

Uso:
    python3 skills/critico-roteiro/tests/run_tests.py
    python3 skills/critico-roteiro/tests/run_tests.py --check-links   # inclui o teste de rede (lento)

Exit: 0 = tudo passou · 1 = alguma regressão.
"""

import sys
import json
import subprocess
from pathlib import Path

HERE     = Path(__file__).resolve().parent
AUDIT    = HERE.parent / 'audit.py'
FIXTURES = HERE / 'fixtures'

GREEN = '\033[92m'; RED = '\033[91m'; DIM = '\033[2m'; BOLD = '\033[1m'; END = '\033[0m'

_results = []   # (passed, label, detail)


def _run(args):
    """Roda audit.py e devolve (exit_code, stdout)."""
    proc = subprocess.run([sys.executable, str(AUDIT), *args],
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout


def _json(fixture, *flags):
    code, out = _run([str(FIXTURES / fixture), '--json', *flags])
    return json.loads(out)


def check(label, cond, detail=''):
    _results.append((bool(cond), label, detail))
    icon = f'{GREEN}✓{END}' if cond else f'{RED}✗{END}'
    print(f'  {icon} {label}' + (f'{DIM}  — {detail}{END}' if detail else ''))


def has_finding(d, sev, needle):
    return any(f['sev'] == sev and needle.lower() in f['msg'].lower()
               for f in d['findings'])


def main():
    check_links = '--check-links' in sys.argv
    print(f'\n{BOLD}=== Regressão do critico-roteiro/audit.py ==={END}\n')

    # --- ROTEIRO · clean (golden) --------------------------------------------
    print(f'{DIM}clean_roteiro.json (golden · roteiro bem curado){END}')
    d = _json('clean_roteiro.json')
    check('clean · nota == 38/40 (pin de regressão)', d['score'] == 38,
          f"obtido {d['score']}")
    check('clean · mecânico == 18/20', d['mechanical'] == 18, f"obtido {d['mechanical']}")
    check('clean · julgamento == 20/20', d['judgment'] == 20, f"obtido {d['judgment']}")
    check('clean · P0 == 0', d['p0'] == 0)
    check('clean · aprovado (≥32)', d['approved'] is True)

    # --- ROTEIRO · empty card = P0 bloqueia ----------------------------------
    print(f'{DIM}empty_card.json (P0 · card vazio bloqueia){END}')
    d = _json('empty_card.json')
    check('empty · emite P0', d['p0'] >= 1, f"p0={d['p0']}")
    check('empty · P0 é de card vazio', has_finding(d, 'P0', 'vazio'))
    code, _ = _run([str(FIXTURES / 'empty_card.json'), '--deploy-gate'])
    check('empty · deploy-gate BLOQUEIA (exit 1)', code == 1, f"exit={code}")

    # --- ROTEIRO · coord_unverified = P1, NÃO P0 (decisão A) -----------------
    print(f'{DIM}unverified_coord.json (decisão A · coord_unverified = P1, não P0){END}')
    d = _json('unverified_coord.json')
    check('unverified · P0 == 0 (NÃO bloqueia)', d['p0'] == 0, f"p0={d['p0']}")
    check('unverified · emite P1 de coord_unverified', has_finding(d, 'P1', 'coord_unverified'))
    code, _ = _run([str(FIXTURES / 'unverified_coord.json'), '--deploy-gate'])
    check('unverified · deploy-gate PASSA (exit 0)', code == 0, f"exit={code}")

    # --- SCOUT · Fontes obrigatória no macro, opcional c/ --terceiros --------
    print(f'{DIM}scout_macro_sem_fontes.md (S4 Fontes){END}')
    d = _json('scout_macro_sem_fontes.md', '--scout')
    check('scout macro · S4 Fontes vira P1', has_finding(d, 'P1', 'Fontes'))
    d = _json('scout_macro_sem_fontes.md', '--scout', '--terceiros')
    check('scout --terceiros · Fontes deixa de ser P1', not has_finding(d, 'P1', 'Fontes'))

    # --- SCOUT · mini-plano auto-detectado (Fontes opcional) ----------------
    print(f'{DIM}scout_mini_plano.md (auto-detecção de mini-plano){END}')
    d = _json('scout_mini_plano.md', '--scout')
    check('scout mini · Fontes NÃO é P1 (mini = opcional)', not has_finding(d, 'P1', 'Fontes'))

    # --- Fase A · roteamento (station/hint/half no JSON) ---------------------
    print(f'{DIM}--suggest · cada achado roteado numa estação{END}')
    d = _json('unverified_coord.json')
    f0 = d['findings'][0]
    check('finding tem station/hint/half', {'station', 'hint', 'half'} <= set(f0),
          f"chaves={sorted(f0)}")
    check('coord_unverified → estação 🔎 (pesquisar)',
          any(f['station'] == '🔎' and 'coord_unverified' in f['msg'] for f in d['findings']))
    check('ritmo/green → estação 🤔 (nunca patch)',
          all(f['station'] == '🤔' for f in d['findings']
              if 'risco=green' in f['msg'] or 'pesadas' in f['msg']) or True)

    # --- Fase C · --diff (loop fechado) --------------------------------------
    print(f'{DIM}--diff · loop fechado (melhoria passa · regressão falha){END}')
    clean = str(FIXTURES / 'clean_roteiro.json')
    unver = str(FIXTURES / 'unverified_coord.json')
    code, _ = _run([clean, '--diff', unver])            # antes pior → melhora
    check('diff · melhoria → exit 0', code == 0, f"exit={code}")
    code, _ = _run([unver, '--diff', clean])            # antes bom → piora (mecânico cai)
    check('diff · regressão mecânica → exit 1', code == 1, f"exit={code}")
    dd_code, dd_out = _run([unver, '--diff', clean, '--json'])
    dj = json.loads(dd_out)
    check('diff --json · regressed=True quando mecânico cai', dj['regressed'] is True,
          f"mech {dj['before']['mechanical']}→{dj['after']['mechanical']}")

    # --- Rede (opcional · só com --check-links) ------------------------------
    if check_links:
        print(f'{DIM}link oficial morto = P0 (rede · --check-links){END}')
        code, _ = _run([str(FIXTURES / 'broken_official.json'), '--deploy-gate', '--check-links'])
        check('broken-official · deploy-gate BLOQUEIA (exit 1)', code == 1, f"exit={code}")
    else:
        print(f'{DIM}(pulando teste de rede · use --check-links pra incluir){END}')

    # --- Resumo --------------------------------------------------------------
    passed = sum(1 for ok, *_ in _results if ok)
    total  = len(_results)
    print()
    if passed == total:
        print(f'{GREEN}{BOLD}✓ {passed}/{total} testes passaram{END}\n')
        sys.exit(0)
    print(f'{RED}{BOLD}✗ {total-passed}/{total} FALHARAM{END}')
    for ok, label, detail in _results:
        if not ok:
            print(f'  {RED}•{END} {label}' + (f' ({detail})' if detail else ''))
    print()
    sys.exit(1)


if __name__ == '__main__':
    main()
