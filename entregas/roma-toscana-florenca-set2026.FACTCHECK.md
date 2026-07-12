# FACTCHECK · roma-toscana-florenca-set2026 · rodado 2026-07-12

Primeira execução real do protocolo `skills/critico-roteiro/FACTCHECK.md` (3 sub-agentes céticos, ~30 afirmações operacionais, fontes T1 priorizadas). **Correções AINDA NÃO aplicadas ao `.md`** — aguardando o lote de revisões do Tobia pra aplicar tudo junto e regerar o PDF 1×.

**Placar: 18 confirmados · 12 desatualizados/imprecisos · 0 invenções.**

## Correções a aplicar (DESATUALIZADO)

### Roma
| # | No documento | Correto (fonte) |
|---|---|---|
| R1 | Coliseu Ático €26 | **~€22** (fontes 2026 majoritárias; re-checar ticketing.colosseo.it na compra) |
| R2 | Museus Vaticanos seg-sáb 9h-18h (últ. 16h) | **8h-20h, última entrada 18h** (esquema 2026) |
| R3 | Cúpula São Pedro €10 elevador / €8 escada | **€22 elevador / €17 escada** no canal oficial booking.basilicasanpietro.va (inclui audioguia); €8/€10 era o preço antigo de guichê |
| R4 | Castel Sant'Angelo "a partir de €20" · <5 grátis | **€16** (+€1 pré-venda CoopCulture) · **menores de 18 grátis** + UE 18-25 €2 — MELHOR pro grupo |
| R5 | Roma Pass 72h €52-63 | **€62,90** |
| R6 | Barco laghetto Villa Borghese ~€3/20min | **~€5/pessoa/20min** (valores antigos €3/€1,50) |
| R7 | Trevi (caveat novo) | Taxa €2 confirmada · **seg e sex a bacia só abre 11h30** (limpeza); pós-22h livre |

### Toscana / carro
| # | No documento | Correto (fonte) |
|---|---|---|
| T1 | ~12 trens diretos/dia Roma→Chiusi | **~8 diretos/dia** (15 com conexões) · 1h21-1h30 no rápido OK |
| T2 | Chiusi→Florença 1h30-2h (~120-150km) | **~124-130km · 1h15-1h30** sem trânsito (2h só com trânsito pesado) |
| T3 | One-way fee €0-140 | **€0-50 típico** dentro da Itália (€140 sem fonte verificável) — confirmar na cotação |
| T4 | Autonoleggio Il Girasole "local em Chiusi" | É de **Cortona/Sinalunga com delivery/collection** na estação Chiusi C.T. · horários limitados (sáb só manhã, dom fechado) |
| T5 | Cadeirinha ~€10-15/dia | Majors cobram até **€25/dia (Avis, teto 3 diárias=€75)** · avaliar levar a própria de Paris. Lei: obrigatória <150cm (critério altura, Art. 172 CdS) |

### Florença
| # | No documento | Correto (fonte) |
|---|---|---|
| F1 | Accademia ter-dom 8h15-18h30 (últ. 17h30) | **8h15-18h50, última entrada 18h20** · novidade mar/2026: combinado Accademia+Bargello €26 (48h) |
| F2 | Santa Croce €9,50 | Provável **€10** em 2026 (+€1 fee online) · grátis <12 · usar €10 como valor de trabalho |
| F3 | Pitti+Boboli €22 | **€22 só antecipado online · €25 no dia** · bilhete do Boboli JÁ inclui o Bardini grátis |
| F4 | Piazzale Michelangelo ~100m de desnível | **~50-55m** de subida real (20-30min a pé) — segue valendo ir de ônibus 12/13 com o grupo |

## Confirmados de alto risco (novidades recentes que poderiam ser invenção — não eram)

- ✅ **Trevi €2** desde 2/fev/2026 (T1 turismoroma) — real
- ✅ **Uffizi pós-16h €20 online/€16 balcão** desde 1/jan/2026 (T1 uffizi.it/notices) — real
- ✅ **Pantheon €7** desde 1/jul/2026 (T1 direzionemuseiroma) — real
- ✅ **Batistério em restauro ATÉ 2028** → em set/2026 a abóbada ainda estará coberta pelo andaime. **Impacto de veredito**: o "confirme antes de pagar" do documento vira certeza — mosaicos indisponíveis; Ghiberti Pass vale pelo Museo dell'Opera (Pietà de Michelangelo + Portas originais), não pelo interior do Batistério
- ✅ Passes Duomo €30/€20/€15 · grátis <7 · Duomo fora da Firenze Card
- ✅ Coliseu 24h €18, 30 dias antes (venda abre 8h45 hora de Roma), sem bilheteria
- ✅ Borghese €18/slots 2h/360 pessoas · São Pedro grátis 7h-20h (desde 1/jun/2026)
- ✅ Firenze Card €85/72h (novidade: "Restart" +48h €28) · vasconi San Casciano grátis ~39°C · Theia 33-36°C com área kids · Poggio Piglia confirmado (sazonal, fecha fim de out — set OK) · carteira UE dispensa IDP · ZTL €80-335 + taxa locadora, chega até 1 ano depois

## Nota metodológica

Sites oficiais italianos (colosseo.it, museivaticani.va, uffizi.it, etc.) retornam 403 a fetch direto de bot — vereditos T1 obtidos via snippets de busca dos próprios domínios oficiais + corroboração cruzada de ≥2 fontes 2026. Custo da rodada: ~200k tokens de sub-agentes (3 céticos; acima do alvo lean de 50-80k porque a entrega NÃO tinha proveniência claim-level — foi produzida antes do protocolo. Com proveniência desde a pesquisa, a próxima rodada cai pro alvo).
