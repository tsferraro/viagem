# FUTURE · Plano-Master de Evolução

Skills e melhorias planejadas. Cada item tem trigger de quando vale executar.

---

## Fase 2 · Skills companheiras (priorizadas)

| Skill | Função | Trigger | Prioridade |
|---|---|---|---|
| **road-trip-designer** ⭐ | Skill irmã da `walking-tour-designer` pra dias de carro. Stops tipo `drive` com waypoints + tempo real · info de estrada (rodovia/montanha/costa) · estacionamento no destino · pit stops pra criança · combustível/pedágio · Google Maps `mode=driving` · alternativas se trânsito ruim · roadside attractions opcionais | Próximo roteiro com dia de carro (Córsega vai pedir · Açores pedirá) | ⭐ Alta |
| **pre-trip-content-curator** | Cura compilado de "artigos" pra estudar destino antes (history, gastronomia, eventos locais) · output em formato lib pessoal · pode integrar com `research-save` | Quando Tobia pedir "preparação cultural" pra próxima viagem | Média |
| **trip-debrief-skill** | Coleta input pós-viagem ("o que adoraram · pularam · descobriram") · consolida em `MEMORY.md` por destino/composição/temporada · alimenta padrões cross-viagem | Após 1ª viagem REAL executada | Alta (logo após viagem) |
| **itinerary-calendar-sync** | Cria eventos Google Calendar pros dias com reserva timed-entry | Após 2+ viagens com reservas usadas em campo | Média |
| **itinerary-gmail-drafter** | Rascunha emails de reserva pendente pros restaurantes/atrações | Após 1+ viagem com 5+ reservas necessárias | Média |
| **booking-suggester** | Usa MCP Booking.com pra sugerir hospedagem na fase de briefing | Decisão de incluir hospedagem | Baixa |
| **flight-comparison** | Compara vôos via Kiwi/Skyscanner API ou scrape | Quando viagem internacional sem voo definido | Baixa |
| **car-rental-comparison** | Aluguel de carro · Rentcars/DiscoverCars | Quando viagem requer carro alugado (≠ skill `road-trip-designer` que assume carro já disponível) | Baixa |
| **itinerary-drive-archive** | Backup off-GitHub no Google Drive | Se arquivo perdido pelo menos 1x | Baixa |
| **itinerary-shareable** | Link público read-only com QR code pra família | Família pedir versão "embed" pra grupo expandido | Baixa |

---

## Melhorias de privacidade

### Cloudflare Pages + repo private + Access magic-link

**Stack**: 
- `tsferraro/viagem` vira repo PRIVATE
- Cloudflare Pages free tier conecta a repo private (suporta gratuitamente)
- Cloudflare Access free tier (até 50 usuários) com login por email magic-link
- URL: `viagem.tsferraro.com` ou `<slug>.pages.dev`

**Setup** (~30min uma vez):
1. Criar conta Cloudflare (free)
2. Connect repo `tsferraro/viagem` em Cloudflare Pages
3. Build settings: framework=none, output dir=`/`
4. Adicionar app no Cloudflare Access · `viagem.pages.dev/*`
5. Convidar emails da família (magic link automático)

**Trigger de migração**:
- Vazamento sensível
- Família pedir custom domain
- Uso profissional do mesmo stack (WSP, dashboards)

---

## Melhorias técnicas da skill

| Melhoria | Trigger |
|---|---|
| `scripts/rebuild-search.py` · regenera hay strings indexadas | Se busca ficar lenta com 200+ stops |
| Strategy "etapas" implementada visualmente (separador entre grupos no day-tabs) | Quando viagem 25 dias for testada em campo |
| PWA manifest + service worker · funciona offline 100% (incluindo mapa) | Se Tobia reportar uso offline na viagem (Açores rural) |
| Modo "imprimir" · gera PDF a partir do HTML | Se família pedir versão impressa |
| Export GPX dos walking tours · pra GPS hiking | Quando WT incluir hiking trail (Açores, montanha) |
| Multi-device sync de reservas via Cloudflare KV ou Supabase | Se família reclamar de divergência de reservas |

---

## Sessão 2 · Description optimization (skill-creator full workflow)

Trigger: depois de 1+ viagem real executada com a skill.

Fases:
1. Rodar `scripts/run_eval.py` do skill-creator com `evals.json` em paralelo (com-skill vs sem-skill)
2. Review browser via `generate_review.py` · capturar feedback real do Tobia
3. `scripts/run_loop.py --max-iterations 5` pra otimizar a `description`
4. `python scripts/package_skill.py` pra empacotar como `.skill` se quiser distribuir

Esperado: 2-3% melhoria em triggering accuracy.

---

## Plano-Master · onde isso encaixa

Cada item acima é independente. Filosofia: skill nasce do uso · NÃO criar antes de ter caso real.

Quando Tobia executar a viagem Agosto 2026 (Lisboa+Porto+Açores 25 dias), revisar este FUTURE.md e priorizar.
