# tests/ · regressão do critico-roteiro

O auditor testando a si mesmo. Fecha o furo que a própria auto-avaliação apontou (dim 9 · skill-creator: "um linter é o candidato perfeito pra evals").

```bash
python3 skills/critico-roteiro/tests/run_tests.py                # 14 checks (offline)
python3 skills/critico-roteiro/tests/run_tests.py --check-links  # +1 check de rede
```

**Rode sempre que mexer no `audit.py`.** Se um regex mudar e a nota/severidade mudar junto, um teste quebra e te obriga a decidir se a mudança é intencional (aí atualiza o valor fixado) ou regressão.

## Fixtures (comportamentos travados)

| Fixture | Trava |
|---|---|
| `clean_roteiro.json` | roteiro bem curado = **38/40** (mec 18 · julg 20) · aprovado. Pin exato: qualquer drift de scoring quebra |
| `empty_card.json` | card `tipo=card` vazio = **P0** · deploy-gate exit 1 |
| `unverified_coord.json` | `coord_unverified` = **P1, não P0** (decisão A · Tobia 2026-07-01) · deploy-gate exit 0 |
| `broken_official.json` | link `type=official` morto = **P0** (só com `--check-links` · usa TLD `.invalid`) |
| `scout_macro_sem_fontes.md` | S4 Fontes = P1 no macro · **some com `--terceiros`** |
| `scout_mini_plano.md` | auto-detecção de mini-plano · Fontes opcional |
