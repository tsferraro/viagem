# family-driving · regras pra viagem de carro com criança pequena

Referência específica pra família do Tobia: casal + filha 3 anos (2026). Atualizar conforme a criança cresce.

---

## Regra dos 45min

Criança de 3 anos começa a ficar agitada após 40-50min contínuos no carro. **Parada obrigatória a cada ~45min em trechos longos.**

Não perguntar — inserir automaticamente no JSON como `pitStop: true` quando trecho longo.

---

## Como escolher uma boa parada

**Prioridade de boa parada** (em ordem):
1. **Área de repouso com WC** (autostrada, rodovias italianas têm boa cobertura)
2. **Restaurante/café na beira da estrada** com espaço externo → criança corre + WC
3. **Vila pequena en route** → parada de 10min, ela estica pernas na praça
4. **Parada panorâmica/mirador** → esticar pernas + foto boa (só se seguro sair do carro)
5. **Evitar**: apenas parar no acostamento sem estrutura → não tem WC, não é seguro

---

## Horário de saída recomendado

| Tipo de dia | Saída recomendada | Motivo |
|---|---|---|
| Hub-spoke com <30min de carro | 08:30-09:00 | Chega antes do pico nas praias/sítios |
| Hub-spoke com >1h de carro | 08:00-08:30 | Aproveita manhã fresca |
| Estrada de montanha (loop/Bavella) | 07:30-08:00 | Sol forte >11h · estrada quente + congestionamento turístico |
| Ferry com horário fixo | Calcular: horário ferry − drive − 30min margem | Ferry não espera |
| Dia linear (troca de base) | 09:00-10:00 | Check-in mínimo 14h · não precisa sair cedo |

---

## Sombra e temperatura

- **Carro para em sol direto >5min**: interior sobe 20°C. Nunca deixar criança esperando.
- **Parking com sombra**: quando houver escolha, priorizar. Mencionar em `parking` se árvores/cobertura disponíveis.
- **Proteção solar no carro**: janelas laterais não têm UV-block standard → parasol de ventosa, especialmente lado da criança.

---

## Checklist antes de sair (não vai no JSON — é orientação pro Tobia)

Itens que normalmente o itinerary omite mas fazem diferença:

- [ ] Lanche e água no carro (não depender de parada pra comer — atrasa tudo)
- [ ] Tablet/música baixada offline pra trechos de >30min
- [ ] Primeiro kit (vômito, enjoo: criança 3a é vulnerável em curvas de montanha)
- [ ] Protetor solar acessível sem parar o carro
- [ ] Carregador USB no carro

---

## Enjoo em curvas

Estradas de montanha (Bavella, SS292 Bosa, qualquer serrana) têm curvas fechadas contínuas. Criança de 3 anos com enjoo: sintoma aparece aos ~20-30min de curvas.

**Se for estrada de montanha**:
- Mencionar em `dicas` do transit: "Estrada com curvas · janela semi-aberta · olhar pro horizonte se enjoar"
- Não marcar `risco: red` só por isso — é informação útil, não bloqueio

---

## Ferry com criança

- **Embarque de carro**: ficar no carro até autorizado a sair → criança fica contida
- **A bordo**: deck externo > salão fechado pra criança com energia
- **Duração tolerável sem problema**: até ~45min. Acima de 1h → levar lanche + tablet
- **Enjoo de mar**: 15-30% das crianças de 3a enjoam. Boa ventilação, olhar pro horizonte, evitar ler/tela dentro.
- **Custo**: sempre verificar se carro vai ou fica em terra — às vezes ferry de passageiro é muito mais barato e ilha é walkable

---

## Alerta risco RED · dias com ferry horário fixo

Se o ferry tem último horário antes das 20h, marcar o dia inteiro com `risco: "red"` se:
- Dia tem 3+ atividades além do ferry
- Ferry de volta está lotado e não há alternativa noturna

Inserir aviso explícito no último transit antes do ferry de volta:
```json
{
  "emoji": "⛴️",
  "tipo": "transit",
  "nome": "Ferry Carloforte → Calasetta · último da tarde",
  "cat": "~18h30 · check horário Delcomar · próximo só às 20h",
  "risco": "yellow"
}
```
