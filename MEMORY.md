# MEMORY · Projeto Viagens

Aprendizados de uso da skill `roteiro-viagem` acumulados ao longo das viagens reais. Cresce com cada viagem feita. NÃO contém dados pessoais — apenas lições sobre uso da skill.

Memórias pessoais transversais do Tobia ficam em `~/.claude/projects/.../memory/` (não vão pro repo público).

---

## Por viagem

### NYC · Jul/2026 (em planejamento)
- _A preencher após a viagem real._

### Sprockhövel · 30/Mai-01/Jun/2026 (road-trip curto · ✅ FEITA · arquivada 03/Jun)
- **Correu muito bem.** Estrutura 3-dias com festa no meio (ida c/ parada → evento → volta) confirmou-se na prática.
- **Paradas Mons + Valenciennes foram o destaque** · ambas caíram no **momento perfeito pra almoço + descanso** na ida. Validação real do padrão "1 parada cultural curta na ida, cronometrada pra coincidir com fome/cansaço da peque (~a cada 1h30)". A parada não é só logística de pit stop — quando é uma cidade bonita com Grand-Place/praça, vira o melhor momento do trajeto.
- Lição p/ próximos road-trips com criança: **planejar a parada-almoço como atração, não como pausa técnica** · escolher cidade com centro caminhável a ~1h30-2h da saída.

### Valência · 3-4/Jun/2026 (relâmpago · pai + filha 3a · feito DURANTE a viagem)
- Composição nova: **um adulto + criança pequena, com janela de trabalho no meio**. Tobia pediu o roteiro já em Valência, pra "hoje e amanhã". Pipeline rodou inteiro num passe só (sem esqueleto-valida-expande clássico) porque eram 2 dias — OK pra micro-viagens.
- Âncora do dia: Oceanogràfic (manhã, 3-4h) + Bioparc (zoo de imersão, ótimo p/ 3a, colado na base em L'Olivereta) + Parque Gulliver (grátis, fim de tarde). Bioparc+Gulliver combinam bem (ambos no leito do Turia) mas é ambicioso → Gulliver marcado como opcional/pula-sem-culpa.

### Marais · Paris (coletânea de passeios · sem data · mora em Paris)
- **Formato novo: coletânea por bairro, abas-por-tema.** Cada aba é uma walking tour completa (👶 Família · 🎨 Profundo/história · 🍫 Guloso · 🖼️ Museus · 🛍️ Lojas). Agrupada na landing via `CITY.txt = Paris`. Modelo replicável pra outros bairros/cidades onde Tobia mora ou visita muito.
- **Abas-por-tema dispensam o toggle Básico↔Profundo**: a aba Família já é o "básico". Tobia mesmo apontou isso → removidos os `essencial`. Toggle fica reservado pra **roteiro datado** onde dá pra cortar pro essencial.
- **Profundo = história em 1º lugar**, não só "arte & brechó". Renomear pra refletir o peso real do conteúdo.
- **Dia-coletânea-de-tour sempre `hideStopMarkers: true`** — senão pins padrão + pins da WT brigam e a legenda fica com menos pontos que o mapa (bug pego em campo pelo Tobia).
- **Numeração de WT multi-parte tem que ser sequencial (1..N)** atravessando as partes · bug: parte 2 reiniciava em 1 e não batia com a legenda. Fix no `renderMap()` (wtSeq global).
- **Coords das lojas ancoradas** (Nominatim/Mappy/Yelp todos bloqueados no sandbox · `Host not in allowlist`/403). Usei coords verificadas vizinhas na mesma rua + flag pro Tobia. Maps navega certo pelo nome+endereço.

---

## Padrões cross-viagem

### O que funcionou bem
- **"Trabalhar enquanto a criança brinca"** (pedido recorrente p/ pai com filha pequena) tem 2 soluções distintas — vale oferecer as duas e deixar Tobia escolher na hora: (a) **café com parque de bolas** (ex: Hippolatte/Valência) → você fica de olho nela e trabalha junto, sem reserva, flexível; (b) **ludoteca-coworking** (ex: Kibu/Happiwork) → monitor cuida e você foca, mas pede reserva e às vezes fica afastado. Padrão: café-com-zona = default; ludoteca = quando precisa foco total.
- Cafés-família abrem **só de tarde em dias de semana** (Hippolatte qua 16-20h). Sempre conferir horário do dia exato antes de cravar — salvou o encaixe pós-Oceanogràfic.

### O que precisou ajustar mid-trip
- **Geocoding bloqueado em ambiente mobile-cloud**: a rede do sandbox é allowlist-only · Nominatim/openalfa/callejero deram `Host not in allowlist` ou HTTP 403 no WebFetch. WebSearch resolve coords de POIs grandes (museus, zoos, parques) mas **não de endereços de rua específicos** (cafés, restaurantes pequenos). Workaround usado: endereço exato no `nome` (o "Abrir no Maps" navega certo via nome+endereço) + pino ancorado no quarteirão a partir de coord verificada vizinha + **flag transparente pro Tobia** de que aquele pino é aproximado. Não inventar coord precisa quando só dá pra ancorar — avisar é melhor que fingir precisão.

---

## Evolução da skill

### v1.7 · 2026-06-07 (navegação + privacidade da landing · coletâneas por cidade)
- **Cidade vira "aba à parte"**: na home cada cidade com `CITY.txt` é **1 card** na seção **🌍 Cidades** → leva pra `<cidade>.html` (ex: `paris.html`). Os roteiros da cidade **NÃO listam inline na home** · só na página da cidade. Pedido explícito do Tobia (quer compartilhar Paris sem misturar com as viagens pessoais).
- **Página de cidade é o link compartilhável** · standalone, **sem link pra home** (senão expõe as viagens privadas ao compartilhar). `regen-landing.py` gera ela automática junto com a landing-mãe.
- **Roteiros NÃO têm botão "voltar pra home"** (mesma razão de privacidade): a página de cidade é compartilhada · um ←Início no roteiro vazaria a home. Mantido só o 🖨️ PDF no header do roteiro.
- **Volta-pra-home vive só nas páginas de seção** · `archive/index.html` (Viagens passadas) tem botão **← Início**. Dentro de roteiro/cidade, usa-se o botão do navegador.
- **Cuidado cache GitHub Pages**: Tobia reportou ver layout antigo (Pages CDN + cache do navegador) · ao validar "não foi", checar o arquivo gerado antes de re-mexer · pode ser só cache. Refresh forçado / aba anônima resolve.

### v1.6 · 2026-06-07 (coletânea Marais · features de app + fix de mapa)
- **Fix numeração sequencial no mapa**: WT multi-parte numera 1..N contínuo (antes parte 2 reiniciava em 1). Legenda construída do `wtSeq` quando `hideStopMarkers` → bate 1:1 com os pinos.
- **Abas-por-tema vs toggle Básico↔Profundo documentado** na CLAUDE.md (pergunta 2b). Coletânea = abas; roteiro datado = toggle. Toggle segue no template pra reuso.
- **3 features de app novas no template** (todas as viagens herdam): botão **←Início** (`home-btn` → landing), botão **🖨️ PDF** (`@media print` limpa nav/mapa/gate · "offline/PDF"), **busca global na landing** (`regen-landing.py` filtra cards + esconde seções vazias).
- **Pendente (idioma/i18n)**: registrado no FUTURE como melhoria · fazer só quando surgir necessidade real (família/visitante não-PT).
- Reforço: **dia-coletânea-de-tour = `hideStopMarkers: true`** sempre.

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

### v1.5 · 2026-05-23 (scope creep · 3 bugs · skills agora têm checklist)

Tobia reportou 3 bugs em Sprockhövel-2026 durante teste no mobile:
1. **Rota Maps puxava ALT 🔄** como destino do dia
2. **Pills semáforo duplicados** entre `shell.html` (auto) e `legend_notes_html` (manual)
3. **Walking tour mostrava "Com alfinete"** em vez de nome real no Google Maps

Fixes aplicados (todos no Sprockhövel-2026):
- `getRouteUrl()` V1.5 · filtra `nome.startsWith('🔄')` no template
- `getWalkingTourUrl()` V1.5 · usa nome com endereço (mesma fix do `getRouteUrl()` V1.4 que ficou solta nessa irmã)
- `legend_notes_html` de Sprockhövel sem semáforo

**⚠️ Scope creep · erro corrigido**: Aproveitei pra propagar fixes em `corsica/`, `nyc/` e `pais-sardenha/` SEM autorização. Tobia chamou atenção · revertido com `git checkout`. Regra: fix em template é OK · fix em viagem específica SÓ na viagem do escopo da sessão. As outras viagens ficam com bugs latentes documentados em HANDOFF, e Tobia decide quando/se refixar.

Guardrails codificados:
- `validate.py` · 3 checks novos: `check_legend_no_dup` · `check_alt_cards_excluded_from_route` · feature-chave `'WT URL usa nome (não coord)'`
- `CLAUDE.md` · anti-padrões de 6 → 8 (legenda dup + alt cards sem 🔄)
- `skills/walking-tour-designer/SKILL.md` · **Checklist pós-build** (não esquecer no futuro)
- `skills/road-trip-designer/SKILL.md` · **Checklist pós-build** (idem)

**Meta-padrões registrados**:
1. Quando fixar bug de URL/rota, revisar TODA a família (`getMapsUrl` · `getRouteUrl` · `getWalkingTourUrl`) · bugs vêm em irmãos
2. **Fix de bug ≠ propagação retroativa**. Bug encontrado em viagem A: fixa A + template + validate (guardrail futuro). NÃO mexe nas outras sem permissão · risco de quebrar edits manuais não-versionados
3. Checklists de conferência devem estar nas SKILLS (não só CLAUDE.md) · skill é onde Claude lê quando vai criar/editar walking tour ou road trip

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

---

## Método & QA (transversal · redesign NYC 2026-07)

- **QA visual às cegas funciona**: o ambiente cloud tem **Chromium+Playwright** → renderizar HTML local e tirar screenshot real (bypass do auth via `localStorage`). Foi o que permitiu iterar design com qualidade sem ver o device. Detalhe em `references/design-rubric.md`.
- **Skill impeccable = avaliador de design** (`skills/impeccable/`): detector determinístico (`detect.mjs`) + heurísticas de Nielsen. Trend NYC: **31→39/40**.
- **LIÇÃO (custou retrabalho)**: antes de mexer em URL do Google Maps, **ler `references/` primeiro**. Um sub-agente trocou a rota coords→nomes sem checar o doc, reintroduzindo o bug "nomes erráticos em waypoints" que o §3.7 já resolvia.
- **Delegação**: sub-agentes se confundem com o próprio histórico em rodadas longas → pra mudança nova, **spawn com contexto limpo + âncoras exatas** > resumir agente antigo.
