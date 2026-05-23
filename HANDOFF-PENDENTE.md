# 🔄 HANDOFF PENDENTE · sincronizar memory local

> Criado em **2026-05-23** na sessão mobile-cloud (Sprockhövel road-trip).
> Quando próxima sessão Claude Code desktop rodar, **copiar lições privadas abaixo pro memory pessoal** (`~/.claude/projects/.../memory/`) e **deletar este arquivo + commitar a remoção**.

---

## Contexto da viagem (privado · NÃO comitar no MEMORY.md público)

- **Sprockhövel road-trip · 30/Mai → 01/Jun 2026**
- Composição: Tobia + esposa + filha 3a (sem avós · sem amigos · só núcleo)
- **Festa** = motivo da viagem · em casa de amigos em Sprockhövel · começa tarde domingo 31/Mai · vai até após 20h
- Sem endereço/coord da festa registrado (genérico no roteiro)
- Pernoite: casa dos amigos (não hotel) · 2 noites (sáb + dom)
- **Voo Orly · seg 01/Jun · 18-19h** · destino não especificado
- Carro alugado Paris (não especificado modelo/locadora)
- Aniversário no domingo (esposa? amigo? Tobia não confirmou claramente · sondar)

## Lições pessoais que valem pro memory privado

1. **Tobia diferencia escopo de viagem com clareza** · disse "É uma outra viagem de 3 dias" → sinal de não emendar com plano da semana · respeitar limites estritos do que foi pedido
2. **Cadência pit stop 1h30 com filha 3a é firme** · não 2h · documentar como preferência permanente
3. **Valet Orly preferido sobre parking oficial** pra 3-4 dias · BlueValet/Ector
4. **Tobia gosta de 4-cenários comparativos com totais explícitos** · funciona muito bem pra decisão (cenário A/B/C/D Mons+Cambrai)
5. **Tobia confia em apresentação de tabelas com horários + km + janela total** · não prosa
6. **Quando pede "ajustar antes", responder com hipóteses listadas em vez de pergunta aberta** · acelera bastante

## Lições skill já registradas em MEMORY.md (público · v1.3)

Ver `MEMORY.md` seção `v1.3 · 2026-05-23 (lições road-trip curto Sprockhövel)`.
- Estrutura 3-dias com festa no meio
- Alternativas inline 🔄 em vez de subdirs paralelos
- Aires BE/DE confirmadas (Verlaine · Aachener Land Süd · Hélécine)
- Densidade Mons 2h sweet-spot

## Checklist pós-sincronização (apaga este arquivo)

- [ ] Copiar bullets do bloco "Lições pessoais" pro memory privado
- [ ] Registrar composição+contexto da viagem Sprockhövel se útil pra futuras
- [ ] `rm HANDOFF-PENDENTE.md` (só depois de Tobia decidir sobre as pendências abaixo)
- [ ] `git commit -m "chore: sincroniza memory · remove handoff Sprockhövel"`
- [ ] `git push origin main`

---

## Bugs latentes em outras viagens (Tobia decide quando refixar)

Descobertos durante sessão Sprockhövel via validate atualizado. NÃO foram fixados nesta sessão (scope creep evitado). Tobia decide:

### 1. corsica/ · legenda duplicada (semáforo 🟢🟡🔴 repetido)
- Bug presente desde maio · você nunca viu
- Fix: editar `corsica/data.json` linha 10 (`legend_notes_html`) removendo "🟢 Verde · 🟡 Amarelo · 🔴 Vermelho" + `python3 scripts/build.py corsica/data.json corsica/index.html`
- Ou só editar `corsica/index.html` direto (mais rápido) · mas data.json fica divergente

### 2. pais-sardenha/data.json · legenda divergente do HTML
- O HTML está correto (você fixou em 2026-05-23 commit `93af72d` manualmente)
- O data.json ainda tem a duplicação · próximo rebuild via build.py vai trazer o bug de volta
- Fix: editar `pais-sardenha/data.json` linha 10 pra alinhar com HTML atual

### 3. Walking tour URL "Com alfinete" · LATENTE em corsica/nyc/pais-sardenha
- Mesmo bug que fixei em Sprockhövel · `getWalkingTourUrl()` no HTML antigo usa coords puras
- Bug latente: só manifesta quando alguém clica botão "🚶 Walking Tour" no Maps mobile · provável que ninguém testou ainda
- Fix por viagem: ou rebuild via `build.py` (pega o template novo automaticamente) ou patch direto no `function getWalkingTourUrl` do HTML
- **Cuidado**: rebuild de pais-sardenha desfaz sua correção manual de legenda · fixar data.json primeiro (item 2)
