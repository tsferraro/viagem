# Rubrica de Valor · Walking Tour

Pra cada candidato a walking tour, calcular nota antes de propor. Apresentar rubrica + justificativa explícita ao usuário ANTES de gerar conteúdo.

## Tabela de pontuação

| Critério | Pontos |
|---|---|
| Bairro NÃO está no roteiro principal | +2 |
| Bairro está mas só 1 atração planejada | +1 |
| Bairro já tem 3+ stops planejadas | -1 |
| Distância total < 1.5km | +1 |
| Distância total > 3km | -1 |
| Possui 2+ hidden gems documentadas | +1 |
| Não tem ângulo histórico/cultural único | -1 |
| Bairro tem segurança comprovada à noite (se WT noturno) | +1 |
| Acessibilidade média/baixa pra carrinho (escadas, cobblestone) | -1 |

## Interpretação

| Nota | Recomendação | Como apresentar |
|---|---|---|
| **≥ +2** | **Alto** — implementar | "Walking tour de alto valor: <justificativa pontual>. Recomendo gerar." |
| **0 a +1** | **Médio** — opcional | "Walking tour de valor médio: <justificativa>. Quer que eu gere ou prefere pular?" |
| **≤ -1** | **Baixo** — desencorajar | "Walking tour de baixo valor: <motivo>. Sugiro pular — esse bairro já está bem coberto / pesado pra carrinho / sem ângulo único." |

## Componentes da justificativa

Toda apresentação de rubrica precisa cobrir 3 dimensões:

1. **Cobertura**: o bairro está no roteiro? Quantos stops já?
2. **Densidade**: stops cabem em <1.5km, 1.5-3km, ou >3km?
3. **Singularidade**: tem narrativa/ângulo único ou é genérico?

## Exemplos

### Caso alto valor (Alfama em roteiro de Lisboa)

```
| Critério                                | Pontos |
|----------------------------------------|--------|
| Bairro NÃO está no roteiro principal   | +2     |
| Distância total ~1.2km                  | +1     |
| 3 hidden gems (Beco do Carneiro,        | +1     |
|  Tasca do Chico, Mirador secret)        |        |
| Acessibilidade média (degraus)          | -1     |
|----------------------------------------|--------|
| TOTAL                                   | +3     |

VALOR: ALTO · "Alfama é descoberta pura · 1.2km walkable · ângulo fado/vista único"
```

### Caso baixo valor (Times Square WT em roteiro NYC)

```
| Critério                                | Pontos |
|----------------------------------------|--------|
| Bairro já tem 3+ stops planejadas      | -1     |
| Distância total 0.8km                   | +1     |
| Sem hidden gems (turistada)             | 0      |
| Sem ângulo único                        | -1     |
|----------------------------------------|--------|
| TOTAL                                   | -1     |

VALOR: BAIXO · "Times Square já é parada do roteiro · sem hidden gems · pula sem culpa"
```

## Regra final

Se valor é **baixo**, NÃO gerar o JSON do walking tour. Só apresentar a rubrica + recomendação de pular. Usuário pode pedir explicitamente: "gera mesmo assim" — aí gera com nota de cabeçalho "FORÇADO PELO USUÁRIO · valor baixo".
