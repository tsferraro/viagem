# MEMORY · Lições das viagens

Lições aprendidas durante a construção de cada roteiro. Consultado antes de iniciar qualquer viagem nova.

---

## Córsega · `corsica-jul2026` · Mai/2026

### Estrutura e deploy
- **Subpasta pra roteiros paralelos** · roteiro novo vai em `<destino>/index.html`, não substitui raiz · raiz reservada pra viagem ativa principal · usar `deploy.sh modo paralelo` na próxima
- **GitHub Pages** · serve só a branch `main` · mudanças ficam invisíveis até PR ser mergeado · deixar PR aberto e avisar Tobia mergear
- **Archive só arquiva quando slug da raiz muda** · se NYC fica na raiz, não entra no archive · erro inicial: arquivei NYC erroneamente

### Dados e coordenadas
- **`coord_unverified`** marcado em: Saparale (`~41.5800, 8.9500`), Tour Capanella mirador (`~41.7050, 8.7895`), belvédère Roccapina (`~41.5050, 8.9100`) · verificar antes da viagem
- **Walking tour Cidadela Bonifacio** · stops 2-4 (Bastion, Sainte-Marie, Loggia) têm coords aproximadas no cluster ~300m · funcionais, não precisam
- **Sartène walking tour** · Place de la Libération `41.6211, 8.9719` e Sainte-Marie `41.6210, 8.9723` verificadas por Monumentum (PA00099116) · alta confiança

### Rotas Google Maps
- **`origin`/`destination` como lat,lng puro** → Maps exibe "Com alfinete" · usar nome de lugar (`"Porto Pollo, Corsica"`) no campo `baseName` do day
- **`transport: "driving"` + `baseCoord` + `baseName`** no day → `getRouteUrl` gera rota ida e volta da base em modo carro
- **Dias de carro Córsega**: Filitosa (29/Jul), Sartène (31/Jul), Bavella (1/Ago), Rocapina (2/Ago) → base Porto Pollo · Piantarella (5/Ago), Rondinara (6/Ago) → base Bonifacio

### Walking tours
- **Rubrica aplicada**: Bonifacio Cidadela +2 (Alto) · Sartène +4 (Alto) · Porto Pollo -2 (pula) · Propriano +1 (médio/pulável)
- **Sartène** é cidade compacta ~400m · 5 stops em 45min funciona bem · mercado de sexta + Maniguedda + Échauguette são os diferenciais reais

### Logística família (filha 3a)
- **Filitosa**: canguru/pochete obrigatório · trilha irregular sem piso firme
- **Polischellu**: só primeiras piscinas com criança · verificar se ainda exige guia (mudou 2024)
- **Escalier Roi d'Aragon**: avós podem ficar no topo · 187 degraus a 45° é puxado
- **Día 8/Ago transição** risco RED · sair 7h pra ferry 08:30 · dia mais pesado do roteiro
- **Piantarella** = melhor praia toddler da Córsega do Sul · lagoa rasa por dezenas de metros
- **Rondinara** = top-3 praia da Córsega · baía em concha · perfeita com filha

### Validações pendentes antes da viagem
- [ ] Confirmar coord Saparale · ligar `04 95 77 15 52` antes de ir
- [ ] Confirmar Polischellu ainda livre sem guia (OT Solenzara)
- [ ] Confirmar drop-off carro em Bonifacio (não Figari) com locadora
- [ ] Ferry Bonifacio→Santa Teresa: reservar antes (alta enche)
