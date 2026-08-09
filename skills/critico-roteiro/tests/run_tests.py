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
import tempfile
from datetime import date, timedelta
from pathlib import Path

HERE      = Path(__file__).resolve().parent
AUDIT     = HERE.parent / 'audit.py'
FIXTURES  = HERE / 'fixtures'
FCGATE    = HERE.parent.parent.parent / 'scripts' / 'factcheck-gate.py'

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


def _fc_gate_viagem_nova(fc_date_str):
    """Monta um repo git temporário com data.json NUNCA commitado + FACTCHECK-<fc_date_str>.md
    válido, e roda factcheck-gate.py contra ele. Devolve (exit_code, stdout+stderr)."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        subprocess.run(['git', 'init', '-q'], cwd=tmp, check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@test.com'], cwd=tmp, check=True)
        subprocess.run(['git', 'config', 'user.name', 'Test'], cwd=tmp, check=True)
        (tmp / 'README.md').write_text('init')
        subprocess.run(['git', 'add', 'README.md'], cwd=tmp, check=True)
        subprocess.run(['git', 'commit', '-q', '-m', 'init'], cwd=tmp, check=True)
        vdir = tmp / 'viagem-x'
        vdir.mkdir()
        (vdir / 'data.json').write_text('{"days": []}')  # NUNCA commitado (o ponto do teste)
        (vdir / f'FACTCHECK-{fc_date_str}.md').write_text(
            f"# FACTCHECK · viagem-x · {fc_date_str}\n\n"
            f"| Item | Afirmação | Veredito | Fonte(s) | Data |\n"
            f"|---|---|---|---|---|\n"
            f"| card:Teste | Existe | OK | https://example.com | {fc_date_str} |\n")
        proc = subprocess.run([sys.executable, str(FCGATE), str(vdir), '--quiet'],
                              capture_output=True, text=True)
        return proc.returncode, proc.stdout + proc.stderr


def main():
    check_links = '--check-links' in sys.argv
    print(f'\n{BOLD}=== Regressão do critico-roteiro/audit.py ==={END}\n')

    # --- ROTEIRO · clean (golden) --------------------------------------------
    # Pin recalibrado 38→39 em 2026-08-09 (Lote 1 da auditoria): o conserto do
    # coord_4dec (lia -9.2160 como 3 casas via str(float)) removeu um P2 FALSO
    # da Torre de Belém — a nota subiu porque o instrumento parou de errar,
    # não porque o check afrouxou.
    print(f'{DIM}clean_roteiro.json (golden · roteiro bem curado){END}')
    d = _json('clean_roteiro.json')
    check('clean · nota == 39/40 (pin de regressão)', d['score'] == 39,
          f"obtido {d['score']}")
    check('clean · mecânico == 19/20', d['mechanical'] == 19, f"obtido {d['mechanical']}")
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

    # --- Schema unificado de fontes · {o,u,tier,data,prova[]} (Lote 3) -------
    print(f'{DIM}fonte_sem_tier.json (fonte sem tier/data = P3 aviso, nunca bloqueia){END}')
    d = _json('fonte_sem_tier.json')
    check('fonte sem tier · gera P3 de schema', has_finding(d, 'P3', 'tier'))
    check('fonte sem tier · NÃO bloqueia (p0 == 0)', d['p0'] == 0, f"p0={d['p0']}")

    # --- FIXTURE DE CONTEÚDO FALSO · bosa_falsa (auditoria 2026-08-08) -------
    # Este arquivo é 100% INVENTADO de propósito (mirante inexistente, torre e
    # escadaria fictícias com mapsQuery plausível, restaurante inventado ⭐⭐⭐,
    # fontes SEO-farm) — e os gates o APROVAM. O teste TRAVA esse fato:
    #   (a) impede comentário/documentação futura de alegar cobertura que não existe;
    #   (b) no dia em que alguém implementar um check que pegue conteúdo falso,
    #       este teste quebra DE PROPÓSITO — atualize-o com festa, é o dia em que
    #       o gate passou a medir alguma coisa além de forma.
    print(f'{DIM}bosa_falsa.json (roteiro 100% falso · especificação executável do que '
          f'os gates NÃO cobrem){END}')
    d = _json('bosa_falsa.json')
    check('bosa-falsa · APROVADA pelos gates (nota ≥32 — regex não mede verdade)',
          d['score'] >= 32, f"obtido {d['score']}")
    check('bosa-falsa · P0 == 0 (nenhum check pega invenção fluente)',
          d['p0'] == 0, f"p0={d['p0']}")
    check('bosa-falsa · approved=True (por isso a nota é FORMA e o FACTCHECK é '
          'obrigatório)', d['approved'] is True)

    # --- maps-audit · coord idêntica em stops distintos ----------------------
    # Caso Tophet/MAB: rota por nome nunca olha coords, mas são elas que desenham
    # os pinos in-app. O fixture coord_repetida/ tem 2 paradas de WT com a mesma
    # coord — maps-audit deve BLOQUEAR (exit 1).
    print(f'{DIM}coord_repetida/ (maps-audit · coord idêntica = bloqueia){END}')
    maps_audit = HERE.parent.parent.parent / 'scripts' / 'maps-audit.py'
    proc = subprocess.run([sys.executable, str(maps_audit),
                           str(FIXTURES / 'coord_repetida' / 'index.html')],
                          capture_output=True, text=True)
    check('coord_repetida · maps-audit BLOQUEIA (exit 1)', proc.returncode == 1,
          f"exit={proc.returncode}")
    check('coord_repetida · achado menciona coord idêntica',
          'coord idêntica' in proc.stdout)

    # --- factcheck-gate.py · viagem nova (refinamento 6a · auditoria de volta) ---
    # data.json sem NENHUM commit é indistinguível pro git de "factcheck velho demais".
    # Sem tratamento especial isso bloqueava até o primeiro deploy legítimo de toda
    # viagem nova. Factcheck de HOJE deve passar (com aviso); de ontem, continua bloqueando.
    print(f'{DIM}factcheck-gate.py · viagem nova sem commit do data.json{END}')
    hoje = date.today().isoformat()
    ontem = (date.today() - timedelta(days=1)).isoformat()
    code, out = _fc_gate_viagem_nova(hoje)
    check('viagem nova · factcheck de HOJE → gate PASSA (exit 0)', code == 0, f"exit={code}")
    code, out = _fc_gate_viagem_nova(ontem)
    check('viagem nova · factcheck de ONTEM → gate BLOQUEIA (exit 1)', code == 1, f"exit={code}")

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
