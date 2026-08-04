# HANDOFF · fatos alterados nos dias compartilhados (pra quando `sardenha/` for criado)

**Contexto**: o roteiro dos pais (`pais-sardenha/`, 06→21/Ago) foi trazido ao padrão do repo em
2026-08-03. Os dias **07 a 15/Ago** têm `grupo: true` — são os dias com o Tobia, a esposa e a
neta. O roteiro da família (`sardenha/`, 16-23/Ago) ainda será criado em outra sessão e vai
espelhar parte desses dias.

Abaixo, **só os FATOS que mudaram** (lugar, horário, custo, logística). Julgamento — `risco`,
`valeAPena`, `acessibilidade` — foi calibrado pro casal de avós e **não** deve ser copiado: a
criança de 3 anos muda os três eixos.

---

## 🔴 Erro factual corrigido (o mais importante)

**Gigantes de Mont'e Prama · Museu Civico de Càbras (11/Ago)** — o card dizia
`"~3000 a.C."`. A datação aceita é **séc. IX-VIII a.C.**, com hipótese minoritária no séc. XI a.C.
Erro de dois mil anos, e ele importava: o valor da peça é justamente ser *anterior aos kouroi
gregos*, o que só faz sentido com a data certa. Descoberta em **março de 1974**, por
Sisinnio Poddi e Battista Meli; 5.178 fragmentos → 26 estátuas.

## 🔴 Furo operacional corrigido

**Cala Coticcio, Caprera (19/Ago · dia só dos pais, mas vale registrar)** — desde 2020 o acesso
é contingentado: **só com guia ambiental autorizado pelo Parque Nacional e reserva prévia**,
4 grupos de 15 pessoas, máx. 60/dia, de 1/Mai a 20/Out. €3 de taxa do Parque + ~€25/pessoa de
guia. O card anterior tratava como trilha livre de 30-45min. Plano B sem reserva: Cala Caprarese.

---

## Preços e horários conferidos em ago/2026

| Dia | Item | Antes | Agora |
|---|---|---|---|
| 07 e 08/Ago | Ferry Santa Teresa ↔ Bonifacio | `€17-35 passageiro` | **~€29/passageiro por trecho** · Moby / Blu Navy · ~50min · até 8 travessias/dia no verão |
| 07/Ago | Bonifacio · Bastion de l'Étendard | (ausente) | **€3,50** |
| 07/Ago | Bonifacio · Escalier du Roi d'Aragon | `€2.50` | €2,50 · **187 degraus a 45°**, dá pra ficar no topo |
| 09/Ago | Tharros | `€6.50 · €10 combinado` | **€18 integrado** (Tharros + Museu de Càbras + Torre di San Giovanni + Mont'e Prama) · **€15 acima de 65 anos** |
| 09/Ago | Is Arutas · estacionamento | `€10/dia` | **€3,50/2h · €5,50/4h · €7/6h · €8/dia** · lota ~10h |
| 10/Ago | Bosa · Castello Malaspina | `€3` | **€4** · 10h-19h30 |
| 11/Ago | Museu Civico de Càbras | `€5 · €10 combinado` | Coberto pelo integrado de €18 · **fecha às segundas** · ter-dom 10h-18h |
| 13/Ago | Sant'Antioco · Tophet + MAB | `€10-15` | **€7** cumulativo museu+Tophet · **€10** bilhete único de todos os sítios · 9h-19h (mar-out) |
| 14/Ago | Ferry Calasetta ↔ Carloforte | `€4-5 passageiro · €17 carro` | **~€17,40 carro+motorista · ~€5 a pé** · Delcomar · 30min · com veículo, chegar 30min antes |
| 15/Ago | Porto Flavia | `€10/€6.50 senior` | Confirmado · **reserva obrigatória** · visitas 9h30/10h30/11h30/12h30 (seg-sex) + 14h30/15h30 (sáb-dom) · chegar **15min antes** ou perde |

## Fatos operacionais novos

- **Porto Flavia**: galeria principal são ~600m planos; a **galeria inferior tem 108 degraus** —
  dá pra ficar em cima. 13-15°C lá dentro o ano todo, casaco fino mesmo em agosto.
- **15/Ago é Ferragosto** — o feriado mais movimentado da Itália. Praias e estradas cheias.
  O roteiro dos pais tem Porto Flavia de manhã com reserva + Cala Domestica de tarde; para a
  família, com criança, considerar inverter ou encurtar.
- **Areia de Is Arutas**: lei regional 16/2017 proíbe levar areia, seixos ou conchas de qualquer
  praia sarda. **Multa de €500 a €3.000**, e em jul/ago os scanners dos aeroportos da ilha
  checam bagagem procurando exatamente isso. Vale um aviso explícito num roteiro com criança —
  criança enche o bolso de areia sem pensar.
- **Uber não opera na Sardenha** (ilha inteira). Táxi entre polos é proibitivo. Tudo é carro.
- **Spiaggia La Bobba (Carloforte)**: a coord anterior estava ~3km fora. Correta:
  `39.09611, 8.29472`. O card foi renomeado pra `Spiaggia La Bobba (Isola di San Pietro)`.

## Mudança de schema que o roteiro novo já deve nascer usando

- **`transit_map` reescrito** com `carro` como modo primário (rota + km + tempo), `ferry` com
  operador/preço/antecedência e `rota` pra dicas de janela de horário. O schema antigo
  (`uber`/`taxi`) foi abandonado: numa ilha sem Uber, "🚕 Uber · Não opera" em 17 stops é ruído.
- **`maps_region`**: `"Sardegna, Italia"`.
- **`historia[]`**: 5 polos escritos (nurágicos/Mont'e Prama · Tharros e os fenícios ·
  Carloforte tabarchina · Sulcis e Porto Flavia · Garibaldi em Caprera). **Reaproveitáveis
  inteiros** — são história do lugar, não do público.

---

## O que NÃO copiar do roteiro dos pais

`risco`, `valeAPena` e `acessibilidade` foram calibrados pro casal. Com a neta de 3 anos:

- Sítio arqueológico e museu **valem menos** (Tharros, Mont'e Prama, Sant'Antioco estão ⭐⭐⭐ lá).
- Praia rasa **vale mais** (Maladroxia, Putzu Idu, La Bobba).
- O tour de barco de dia inteiro no Golfo di Orosei (8h) é ⭐⭐⭐ pro casal e provavelmente
  inviável com criança de 3 anos — reavaliar do zero, não herdar.

---

## ⚠️ Restaurantes: 15 dos 55 eram fantasma (varredura 2026-08-03)

**Todos os dias compartilhados foram afetados.** O roteiro da família NÃO deve herdar as opções
de refeição do roteiro anterior — herde as desta versão corrigida, ou refaça com busca própria.

Removidos por não existirem / estarem fechados:

| Onde | Fantasma | Substituído por (confirmado, com endereço) |
|---|---|---|
| Olbia | `Ristorante Gallura` — **fechado por despejo desde jan/2014** | By Night (Viale Aldo Moro 201/A) |
| Olbia | `Da Rino`, `Trattoria Da Romolo` | Il Vecchio Porto · Bistrot Bontade (Via Genova 65) |
| Bosa | `Ai Pescatori` | Locanda di Corte (Via del Pozzo 7) · Borgo Sant'Ignazio |
| Sinis | `Ristorante Mediterraneo` | Quiosques de San Giovanni (sazonais, sem nome fixo) · Da Cesare/Maluentu (Via Lungomare 36, Putzu Idu) |
| Santa Teresa | `Ristorante La Torre`, `Trattoria del Borgo`, `L'Osteria` | Millo (via Garibaldi 4, Michelin) · da Thomas (via Val d'Aosta) · La Lampara (Via Sandro Pertini 6) · Il Grottino (Via del Mare 14) |
| Sant'Antioco | `Locanda del Borgo` | I Vinattieri (Corso V. Emanuele) · Is Solus Bistrot (Corso V. Emanuele 11) · Max Pizzeria (Corso V. Emanuele 85) |
| Nuoro | `Trattoria Marrosu` | Il Rifugio (Via A. Mereu 28) — **fecha quartas** |
| Cala Gonone | `Pizzeria Pulcinella`, `Trattoria del Marinaio` | San Francisco (Via Magellano 8) · La Poltrona (Via Vasco de Gama 22) · Zio Pedrillo (Lungomare Palmasera) |
| La Maddalena | `Da Lucio`, `Trattoria Aurora` | Ristorante Caprera (via T. Zonza 3) · Noir Lounge (Piazza XXIII Febbraio 10) |
| San Pantaleo | `Café Nina` | Bares da praça (genérico assumido) |

Endereços corrigidos em estabelecimentos que existem:

- **Il Caminetto (Càbras)**: era "Via Cristoforo Colombo 8" → **Via Cesare Battisti 8**. O endereço
  errado era, na verdade, o do *I Due Fratelli* em Sant'Antioco (Lungomare Cristoforo Colombo 72) —
  um endereço migrou de um estabelecimento pro outro.
- **Hotel Ristorante Lounge Maladroxia** → **Lu' Hotel Maladroxia, Via Golfo di Palmas 16**.

Fechamento semanal a respeitar (conferir contra as datas do roteiro novo):

| Estabelecimento / sítio | Fecha |
|---|---|
| Sa Bell'e Crabasa (Càbras) | segundas |
| Il Rifugio (Nuoro) | quartas |
| Bistrot Bontade (Olbia) | segundas |
| Museo Civico de Càbras | segundas |
| Compendio Garibaldino (Caprera) | segundas |

No roteiro dos pais isso já causou um erro: **Sa Bell'e Crabasa estava como jantar de segunda 10/Ago**.

---

## 🔬 FACTCHECK completo · 2026-08-04 · 13 correções factuais

Protocolo `skills/critico-roteiro/FACTCHECK.md` rodado sobre o roteiro inteiro, postura adversarial
(tentar refutar cada afirmação). Placar: **9 confirmados · 11 desatualizados/refutados (corrigidos) ·
1 não encontrado (removido)**. Tudo abaixo vale para o roteiro da família também.

### Refutados

| Afirmação | Verdade |
|---|---|
| Sant'Antioco ligada por "ponte romana **ainda em uso**" | O **Pontimannu** é monumento desde **1954** — a ligação hoje é a estrada de variante |
| Base americana em La Maddalena "até 2007" | US Navy de **1/jan/1973 a 25/jan/2008**, na ilha de Santo Stefano, ~4.000 americanos |
| Estrada Dorgali–Cala Gonone feita por "engenheiros suíços" | **Sem fonte nenhuma** — removido. O verificável: túnel de **115m escavado à mão entre 1838 e 1860** |
| Bosa: "35 tanarias fechadas desde 1960" | **~30 curtumes**, o último fechou em **1962** |
| Stella Maris (Porto Cervo) de "1968", quadro doado por "um frequentador" | **1966**, projeto de Michele Busiri Vici · a *Mater Dolorosa* foi doada pela **baronesa Tissen-Bentinck**, mulher do embaixador holandês em Paris |

### Desatualizados — preços e regras que mudaram

| Item | Estava | É |
|---|---|---|
| **Compendio Garibaldino** | €6 · 9h-20h · sem reserva | **€8** · **só com reserva**, grupos de 20 a cada 15min entre 8h30 e 18h30 · visita de **máx. 40min** · chegar 10min antes |
| **Coddu Vecchiu** | €2,50 | **€3,00** (€2,50 só grupos de 20+) |
| **Ferry Santa Teresa ↔ Bonifacio** | ~€29/passageiro | **~€31-40** por trecho · e as tabelas de Moby (4 partidas 07h-18h30) e Blu Navy (09h/12h/17h/20h) **não coincidem** — confirmar na compra |
| **Porto Flavia** | "reserva obrigatória" | Reserva **exclusivamente online**, e a venda **fecha à meia-noite do dia anterior** — nem bilheteria, nem telefone, nem e-mail |
| **Cala Coticcio** | "~€25/pessoa de guia" | €3 do Parque (grátis até 12 anos) + valor da guia **a combinar direto com ela** — varia por duração e tamanho do grupo |

### Confirmados (sem alteração)

Tharros/Museu **€18 integrado · €15 acima de 65** (CoopCulture) · Porto Flavia **€10/€6,50** e horários ·
Castello Malaspina **1112** · Pan di Zucchero **133m** · Porto Flavia **500 t/h** · nuraghi **>7.000**,
Idade do Bronze **1800-1100 a.C.** · Gigantes de Mont'e Prama **séc. IX-VIII a.C.** · relógio de Garibaldi
parado às **18h20** · Sant'Antioco e Compendio fecham **segundas**.

### Ganhos de precisão colhidos no caminho

- Carloforte foi fundada em **17 de abril de 1738**, com ~500 colonos desembarcando.
- O cerco de Bonifacio durou de **21/out/1420 a 5/jan/1421** — Afonso V chegou com 31 naus e 23 trirremes.
- Quem parou o relógio de Garibaldi foi o filho **Menotti**. Na tarde de 2/jun/1882 ele viu **duas toutinegras** no peitoril, pensou nas duas filhas mortas e pediu que não as espantassem.
- O granito de Capo Testa é *provavelmente* (não certamente) o das colunas do Panteão · em **1162** o pedreiro pisano **Cioneto** tirou dali as colunas do Duomo de Pisa.
- Castello Malaspina: torre-mestra acrescentada em **1300** por Giovanni Càpula.
