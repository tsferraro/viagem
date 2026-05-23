# MEMORY · Projeto Viagens

Aprendizados de uso da skill `roteiro-viagem` acumulados ao longo das viagens reais. Cresce com cada viagem feita. NÃO contém dados pessoais — apenas lições sobre uso da skill.

Memórias pessoais transversais do Tobia ficam em `~/.claude/projects/.../memory/` (não vão pro repo público).

---

## Por viagem

### NYC · Jul/2026 (em planejamento)
- _A preencher após a viagem real._

### Sprockhövel · 30/Mai-01/Jun/2026 (road-trip curto · em planejamento)
- _A preencher após a viagem real._

---

## Padrões cross-viagem

### O que funcionou bem
- _A registrar conforme viagens acontecerem._

### O que precisou ajustar mid-trip
- _A registrar conforme viagens acontecerem._

---

## Evolução da skill

### v1.0 · 2026-05-16
- Setup inicial · skill `roteiro-viagem` + `walking-tour-designer` embarcadas
- 10 princípios + 6 anti-padrões codificados
- Suporte a roteiros paralelos via SUBDIR
- Quality bar nos cards + anti-invenção de URLs (`validate.py --check-links`)
- JSON pretty-printed por default (mobile edit-friendly)

### v1.2 · 2026-05-23 (lições Sardenha · gap regen landing)

Problema:
- Tobia criou Sardenha (`pais-sardenha/`) no mobile. Subpasta criada, HTML commitado, mas **landing root (`index.html`) NÃO foi atualizada** · continuou listando só NYC + Córsega
- Causa: regen da landing estava SÓ em `wrap-up.sh` (opcional/esquecível) · mobile não rodou
- Sintoma adicional: mobile criou `data-pais.json` no root em vez de `pais-sardenha/data.json`

Mudanças aplicadas:
- **`scripts/regen-landing.py` criado** (standalone · 110 linhas · lê todas subpastas + monta cards)
- **`deploy.sh` agora chama `regen-landing.py` automaticamente** após validate · landing NUNCA esquece
- `wrap-up.sh` enxugado · reusa `regen-landing.py` como segurança extra
- `data-pais.json` movido pra `pais-sardenha/data.json` (convenção: data.json fica dentro da pasta da viagem)
- `CLAUDE.md` atualizado · seção nova "Landing é AUTO-REGENERADA" + nota sobre `regen-landing.py`

Regra reforçada: skill SEMPRE usa `scripts/deploy.sh` pra publicar · nunca `git push` direto (perde regen + validate + backup).

### v1.1 · 2026-05-19 (lições da 1ª iteração mobile · Córsega)

Problemas encontrados ao usar a skill no mobile-cloud com Córsega:
1. Mobile arquivou NYC sem querer ao criar Córsega · conceito de "viagem ativa no root" era frágil
2. Merge em main não foi automático (Tobia teve que fazer manual)
3. Link rota Google Maps mostrou "Com alfinete" em vez de nome dos lugares
4. Sem protocolo de encerramento documentado · sessão fechou sem atualizar MEMORY

Mudanças aplicadas:
- Subpastas como regra obrigatória: TODA viagem vive em subdir desde nascimento. Root tem só landing auto-regenerada
- `deploy.sh` reescrito: requer subdir obrigatório · valida nome reservado · sempre push pra main direto
- `getRouteUrl` V1.4: usa nome do stop em vez de coords puras (fix Maps · aplicado retroativo)
- `scripts/wrap-up.sh` criado: protocolo de encerramento obrigatório
- `FUTURE.md` priorizado: road-trip-designer + pre-trip-content-curator + trip-debrief-skill

### v1.2 · 2026-05-23 (lições da sessão Sardenha pais + road-trip-designer)

1. **Branch drift pós-merge** · PR mergeado mas continuamos commitando na feature branch → `pais-sardenha/` ficou órfão e precisou ser recuperado com `git checkout feature-branch -- files`. Regra: após merge, mudar pra main imediatamente antes de continuar.
2. **Naming de subdir** · `pais/` foi ambíguo → renomeado pra `pais-sardenha/`. Padrão: subdir deve incluir o destino (`pais-sardenha/`, `amigos-corsica/`), não só a relação (`pais/`, `amigos/`).
3. **Roteiro pais · Sardenha** · road trip Olbia → Sul → Maladroxia → Costa Leste → Olbia funciona bem como arco. Walking tours de alto valor: Bosa (+4), Sant'Antioco (+4), Capo Testa (+3), La Maddalena (+3). Reservas críticas: Porto Flavia (25 max · reservar semanas antes), Al Tonno di Corsa Carloforte.
4. **road-trip-designer criada** · skill nova em `skills/road-trip-designer/` com SKILL.md + 3 references + 2 examples (5 dias reais sardenha calibrados). 4 tipos: Hub & Spoke, Linear, Loop, Ferry-integrated. Rubrica pra stops opcionais + pit stop automático >45min + campos `roadType`/`parking`/`fuelAlert`.

### v1.4 · 2026-05-23 (bugs alts 🔄 + legenda dup · guardrails)

Dois bugs caçados em campo (Tobia testou Sprockhovel-2026 no mobile):

1. **Cards 🔄 ALT poluíam rota Maps do dia** · `getRouteUrl()` filtrava só `tipo!=='transit'`, então cards alternativos `tipo: card` viravam destino da rota → Google Maps puxava direção pra Valenciennes (oposto do trajeto Mons→SPK).
   - Fix: `getRouteUrl()` V1.5 filtra `!nome.startsWith('🔄')`
   - Convenção codificada: cards de alternativa SEMPRE começam com `🔄` no nome
   - validate.py: `check_alt_cards_excluded_from_route` (bloqueia se houver 🔄 sem filtro)

2. **Legenda do semáforo duplicada** (re-bug) · `shell.html` já renderiza pills 🟢🟡🔴 automaticamente, mas eu repeti em `legend_notes_html`. Mesmo bug que apareceu em pais-sardenha (v1.2) e que voltou em Sprockhovel-2026 + estava em corsica não detectado.
   - Fix: `legend_notes_html` deve ter SÓ notas extras (bases · convenções 🔄 · pit stops)
   - validate.py: `check_legend_no_dup` (bloqueia · regex no HTML gerado)
   - corsica corrigida retroativamente (bug latente que ninguém viu até validate ficar mais rígido)

**Padrão meta**: bugs visuais de roteiro são DIFÍCEIS de pegar em revisão local (HTML grande, edge cases sub-perceptíveis). Adicionar regra `validate.py` SEMPRE que um bug for visto na vida real · "se aconteceu uma vez é gambiarra, duas vezes é guardrail" agora codificado nos checks.

### v1.3 · 2026-05-23 (lições road-trip curto Sprockhövel)

Padrões pra road-trips de **fim-de-semana com destino único** (festa/evento · 2-3 dias máximo):

1. **Estrutura 3-dias com festa no meio é canônica** · Dia 1 ida com 1 parada cultural curta · Dia 2 evento dia inteiro · Dia 3 volta direta (sem parada, ou parada curta opcional). Tentar adicionar paradas em AMBOS os dias de viagem (cenário "D" Mons+Cambrai) fica exaustivo · cortar uma.
2. **Cadência de pit stops 1h30 com filha de 3a é firme** · não 2h. Skill `road-trip-designer` já assume isso (45-60min é regra default mas pra crianças <5a fica 1h30 fixo). Documentar essa diferença na sub-skill.
3. **Alternativas inline 🔄 ao invés de subdirs paralelos** · 3 alts marcadas no mesmo HTML (Valenciennes/Schwebebahn/Cambrai) com instruções claras tipo "SE QUISER ESSA OPÇÃO: marca antes do build". Subdir paralelo (`/alternativas`) seria overkill pra alts decididas dia da viagem.
4. **Valet Orly > parking oficial pra 3-4 dias** · BlueValet/Ector custa €11-15/dia (vs P éco €20+), com entrega no terminal — vence sempre com filha pequena + bagagem.
5. **Aires específicas BE/DE que confirmei top** · `Aire de Verlaine` (E42 Belgium · top aire belga · ponte panorâmica + park infantil) · `Aachener Land Süd` (A4 DE Eschweiler · Shell+Coffee Fellows) · `Aire d'Hélécine` (E40 BE Leuven · família).
6. **Densidade Mons 2h** funciona como sweet-spot · walking tour express 30min (Grand-Place + Beffroi · sem subida) + almoço · cabe sem pressão. Walking tour completo (Sainte-Waudru + Mundaneum) requer 3h+ — documentei como "estendido" no `walkingTours` mas sem forçar.
7. **roteiro como "outra viagem" → instrução de escopo** · Tobia disse "É uma outra viagem de 3 dias" → sinal pra NÃO emendar com outro plano da semana. Respeitar limite estrito do escopo solicitado.

### Próximas lições serão registradas aqui após uso real.
