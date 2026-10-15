# FACTCHECK · copenhagen · 2026-10-15

**Escopo**: viagem nova completa: todos os cards ⭐⭐/⭐⭐⭐, todas as opções de refeição, a `nota` de cada dia, o `transit_map`, a legenda, a aba `historia[]` e as coordenadas dos pontos de rota.
**Executor**: 3 sub-agentes céticos (Sonnet) com contexto limpo, um por estrato (restaurantes · cards · logística + história). Receberam só as afirmações e as coordenadas, sem as `fontes` nem a justificativa da sessão construtora. ERRO exige ≥2 fontes independentes ou 1 oficial explícita.
**Nível**: **nível-página** para as fontes oficiais lidas por fetch (tivoli.dk, bakken.dk, nationalmuseet.dk, stromma.com, denkongeligesamling.dk, glyptoteket.com, denblaaplanet.dk, parkmuseerne.dk, tholstrup.dk, locale21.dk, torvehallernekbh.dk, restaurantkronborg.dk, m.dk, radicalstorage.com). O fetch devolve um resumo da página, não o texto bruto. **nível-snippet** para dinoffentligetransport.dk, lex.dk, Naturstyrelsen, o calendário escolar e a tabela da DSB. As coordenadas foram conferidas contra a API da Wikipedia ou o OSM/Nominatim.
**Base anterior**: o levantamento que alimenta o app já passou por auditoria externa na mesma data (`entregas/copenhagen-out2026.AUDITORIA.md`: 41 OK, 2 ERRO corrigidos).
**Placar**: 74 linhas · **52 OK · 2 ERRO (corrigidos) · 11 RISCO · 9 INCONCLUSIVO**. Doze linhas viraram ajuste de texto (`→ corrigido`), e os inconclusivos restantes estão marcados `[a confirmar]` no app.

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| opcao:Nyhavns Færgekro | "Nyhavn 5 · cozinha 11:00-21:00 todos os dias (qui 12:45 ok)" | OK | https://tholstrup.dk/nyhavns-faergekro/ | 2026-10-15 |
| opcao:Nyhavns Færgekro | "sildebord 195 kr · smørrebrød 95-145 kr · frikadeller 120 kr" | OK | https://tholstrup.dk/nyhavns-faergekro/ | 2026-10-15 |
| opcao:Nyhavns Færgekro | "lugar pra carrinho e cadeirão" | OK | https://tholstrup.dk/nyhavns-faergekro/ | 2026-10-15 |
| opcao:Nyhavns Færgekro | "coord 55.68071, 12.58799" | OK — OSM Nyhavn 5 a ~20 m | https://nominatim.openstreetmap.org/search?q=Nyhavn+5,+Copenhagen&format=json | 2026-10-15 |
| opcao:Nyhavns Færgekro | "~10 min a pé da praça" | RISCO — sem fonte; Nyhavn 5 fica a poucos minutos de Kongens Nytorv → corrigido (texto passou a "no cais de Nyhavn") | https://nominatim.openstreetmap.org/search?q=Nyhavn+5,+Copenhagen&format=json | 2026-10-15 |
| opcao:Cap Horn | "Nyhavn 21 · cozinha 11:00-21:00 diária · almoço 125-215 kr · smørrebrød 85-165 kr · noite 175-295 kr" | OK | https://tholstrup.dk/cap-horn/ | 2026-10-15 |
| opcao:Cap Horn | "cardápio publicado pode ser sazonal" | RISCO — página sem data; ligar +45 33 12 85 04 | https://tholstrup.dk/cap-horn/ | 2026-10-15 |
| opcao:Locale 21 | "Ny Østergade 21 · jantar qui desde 17:30 · massas 148-188 kr · pratos 298-345 kr · reserva Book bord" | OK | https://www.locale21.dk | 2026-10-15 |
| opcao:Locale 21 | "cadeirão não informado" | RISCO — site não fala de crianças; ligar +45 33 93 44 12 (texto já marca [a confirmar]) | https://www.locale21.dk | 2026-10-15 |
| opcao:Torvehallerne | "Frederiksborggade 21 · sábado 10:00-18:00" | OK | https://www.torvehallernekbh.dk | 2026-10-15 |
| opcao:Torvehallerne | "dois pavilhões · pizza, pão, fruta · ~10 min a pé do Kongens Have" | RISCO — sem página que cite; distância ~600 m do Rosenborg → corrigido (texto: "mercado coberto de bancas, pizzaria ao lado", "~600 m do Rosenborg") | https://www.afar.com/places/hallernes-smorrebrod-copenhagen | 2026-10-15 |
| opcao:Hallernes Smørrebrød | "75-125 kr a peça · balcão de 16 lugares, sem reserva" | INCONCLUSIVO — verificador não achou lista oficial legível; texto suavizado para "a partir de ~75-80 kr", "balcão pequeno, sem reserva [a confirmar]" | — | 2026-10-15 |
| opcao:Café Daisy | "dentro do Nationalmuseet · smørrebrød, sorvete, opções pra criança" | OK | https://www.visitcopenhagen.com/copenhagen/planning/cafe-daisy-gdk1159436 · https://www.nationalmuseet.dk/en/page/food-and-beverages | 2026-10-15 |
| opcao:Café Daisy | "abre domingo no almoço" | INCONCLUSIVO — só o museu (10-17, dom incluso) tem horário publicado; ligar +45 53 61 14 16 (texto já marca [a confirmar]) | — | 2026-10-15 |
| opcao:Restaurant Kronborg | "Brolæggerstræde 12 · domingo 11:00-18:00, cozinha até 17:00 · tel. 33 13 07 08" | OK | https://www.restaurantkronborg.dk | 2026-10-15 |
| opcao:Restaurant Kronborg | "coord 55.6776, 12.5744 · poucas quadras ao norte do museu" | OK — OSM a ~400 m ao norte | https://nominatim.openstreetmap.org/search?q=Brolæggerstræde+12,+Copenhagen&format=json | 2026-10-15 |
| card:Troca da guarda · Amalienborg | "troca todo dia às 12:00" | OK | https://www.kongehuset.dk/en/palaces-and-the-royal-yacht/changing-of-the-guard/ | 2026-10-15 |
| card:Troca da guarda · Amalienborg | "4 palácios de Eigtved pra Frederico V · família real desde 1794 (incêndio de Christiansborg)" | RISCO — os palácios foram feitos para 4 famílias nobres → corrigido; resto OK | https://en.wikipedia.org/wiki/Amalienborg | 2026-10-15 |
| card:Troca da guarda · Amalienborg | "coord 55.68403, 12.59333" | OK | https://en.wikipedia.org/wiki/Amalienborg | 2026-10-15 |
| card:Passeio de barco | "Stromma: Nyhavn 3 · 1 h · 149 kr · adulto a partir de 16 anos · barcos cobertos nos meses frios · carrinho fica no cais" | OK | https://www.stromma.com/en-dk/copenhagen/sightseeing/sightseeing-by-boat/grand-tour/ | 2026-10-15 |
| card:Passeio de barco | "149 kr" como preço único | RISCO — online varia por canal (135/199) → corrigido ("na saída de Nyhavn; online varia") | https://www.stromma.com/en-dk/copenhagen/sightseeing/sightseeing-by-boat/ · https://www.visitcopenhagen.com/copenhagen/planning/classic-canal-tour-gdk410731 | 2026-10-15 |
| card:Passeio de barco | "Netto-Bådene 80/40 kr · 3-14 anos · 10:00-17:00 · Holmens Kirke ou Nyhavn" | OK | https://www.visitcopenhagen.com/copenhagen/planning/netto-boats-gdk585017 | 2026-10-15 |
| card:Passeio de barco | "coord 55.6797, 12.5906" | OK | https://en.wikipedia.org/wiki/Nyhavn | 2026-10-15 |
| card:Tivoli Gardens · Halloween | "Halloween 2/out-1/nov · 20.000+ abóboras · labirinto · Little Ghost Train · Witch's Carousel · Rasmus Klump incluído" | OK | https://www.tivoli.dk/en/opening-hours-and-seasons/halloween-in-tivoli | 2026-10-15 |
| card:Tivoli Gardens · Halloween | "Haunted House e Villa Vendetta fora do Ride Pass · combo 150 kr · não pra criança pequena" | OK | https://www.tivoli.dk/en/rides/the-haunted-house | 2026-10-15 |
| card:Tivoli Gardens · Halloween | "re-entrada com carimbo na saída do Tivoli Food Hall · ingresso vale só na data" | OK | https://www.tivoli.dk/en/practical-information/faq | 2026-10-15 |
| card:Tivoli Gardens · Halloween | "adulto 489-509 kr · criança 3-7 anos 244-254 kr" | INCONCLUSIVO — preço dinâmico, sem tabela pública; conferido pelo Tobia no app (F5) | — | 2026-10-15 |
| card:Tivoli Gardens · Halloween | "feriado escolar dinamarquês" | OK | https://calendar.center/dk/skoleferier/kobenhavns-kommune/2026-2027/ | 2026-10-15 |
| card:Tivoli Gardens · Halloween | "coord 55.6747, 12.5657 (entrada Vesterbrogade)" | OK | https://nominatim.openstreetmap.org/search?q=Tivoli+Vesterbrogade | 2026-10-15 |
| card:Tivoli · 2º turno | "abóboras e lanternas acendem ao entardecer · parque aberto até ~19:30" | INCONCLUSIVO — fechamento de 16/out não publicado; achado show Halloween Illuminations 21:30 → corrigido (texto marca [a confirmar] e cita o show das 21:30); ligar +45 33 15 10 01 | https://www.tivoli.dk/en/programme/events/illuminationer-hit-2026 | 2026-10-15 |
| card:Glyptotek | "sexta 10:00-17:00 · 135 kr online / 150 kr · menor de 18 grátis" | OK | https://www.glyptoteket.com/visit/opening-hours · https://www.glyptoteket.com/visit/tickets | 2026-10-15 |
| card:Glyptotek | "coord 55.6725, 12.5719" | OK | https://en.wikipedia.org/wiki/Ny_Carlsberg_Glyptotek | 2026-10-15 |
| card:Kongens Have + Rosenborg | "Rosenborg sáb 10:00-17:00 · horário marcado a cada 10 min · 140/150 kr · menor de 18 grátis · carrinho não entra" | OK | https://denkongeligesamling.dk/en/rosenborg-castle/plan-your-visit/ · https://denkongeligesamling.dk/en/rosenborg-castle/plan-your-visit/opening-hours/ | 2026-10-15 |
| card:Kongens Have + Rosenborg | "parque 7:00-19:00 · parquinho no meio com dragão e figuras de madeira" | OK | https://www.parkmuseerne.dk/en/parker/kongens-have · https://www.visitcopenhagen.com/copenhagen/planning/the-kings-garden-playground-gdk566087 | 2026-10-15 |
| card:Kongens Have + Rosenborg | "coord 55.68508, 12.57998" | OK — ~85 m do parquinho, dentro do parque | https://www.openstreetmap.org/way/118353598 | 2026-10-15 |
| card:Den Blå Planet | "feriado 10:00-21:00 · 229/259 kr adulto · 123/136 kr criança 3-11 · M2 até Kastrup + 600 m" | OK | https://denblaaplanet.dk/en/visit-us/prices-and-opening-hours/ · https://denblaaplanet.dk/en/visit-us/practical-information/ | 2026-10-15 |
| card:Den Blå Planet | "coord 55.6381, 12.6561" | OK | https://www.openstreetmap.org/way/211672803 | 2026-10-15 |
| card:Bakken | "aberto 10-18/out e 23-25/out · After Dark 18:30 · Monsterbal 12:30 · Onkel Reje 14:00" | OK | https://bakken.dk | 2026-10-15 |
| card:Bakken | "MiniTurbånd 249/279 kr · até 115 cm · 17 brinquedos · Turbånd 349/379 · 39 brinquedos · entrada grátis" | OK — página-guia antiga do site diz 16/38 | https://www.bakken.dk/planlaeg-dit-besog/priser-billetter/ · https://shop.bakken.dk/miniturbaand2026 | 2026-10-15 |
| card:Bakken | "basta um adulto ter pulseira pra acompanhar" | INCONCLUSIVO — nenhuma fonte; ligar +45 39 63 35 44 → corrigido (texto manda perguntar na bilheteria, [a confirmar]) | — | 2026-10-15 |
| card:Bakken | "caminho da estação atravessa a Dyrehaven com cervos · trilha de terra, carrinho sacoleja" | OK | https://www.copenhagentourism.org/?p=1075 | 2026-10-15 |
| card:Bakken | "coord 55.7758, 12.5748" | OK | https://en.wikipedia.org/wiki/Dyrehavsbakken | 2026-10-15 |
| card:Kastellet + Langelinie | "parquinho de Langelinie junto da Pequena Sereia · barcos, escorregador com torre, caixas de areia" | OK | https://bornibyen.dk/articles/the-5-secret-playgrounds | 2026-10-15 |
| card:Kastellet + Langelinie | "fortaleza em estrela com moinho · ~1,1 km, ~13 min do Amalienborg · coord 55.6911, 12.5939" | OK | https://en.wikipedia.org/wiki/Kastellet,_Copenhagen | 2026-10-15 |
| card:Børnenes Museum | "última chance 18/out/2026 · novo museu no verão de 2027 · Børnenes fecha 16:30 · museu 10:00-17:00" | OK | https://nationalmuseet.dk/udstillinger/boernenes-museum · https://nationalmuseet.dk/en/ | 2026-10-15 |
| card:Børnenes Museum | "adulto 150 kr / 135 online · menor de 18 grátis" | OK | https://nationalmuseet.dk/en/ | 2026-10-15 |
| card:Børnenes Museum | "coord 55.6747, 12.5747" | OK | https://en.wikipedia.org/wiki/National_Museum_of_Denmark | 2026-10-15 |
| transit:Aeroporto → Frederiksstaden | "M2 direto Lufthavnen → Kongens Nytorv ~13 min" | OK | https://en.wikipedia.org/wiki/Copenhagen_Metro · https://www.routesnorth.com/copenhagen/getting-from-copenhagen-airport-to-the-city-centre/ | 2026-10-15 |
| transit:Aeroporto → Frederiksstaden | "coord Kongens Nytorv 55.6793, 12.5852" | OK | https://en.wikipedia.org/wiki/Kongens_Nytorv_station | 2026-10-15 |
| transit:Frederiksstaden → Aeroporto | "coord 55.6181, 12.6561 (estação)" | ERRO → corrigido (era o centróide do aeroporto, ~1,5 km da estação; agora Lufthavnen 55.6308, 12.6492) | https://en.wikipedia.org/wiki/Lufthavnen_station · https://en.wikipedia.org/wiki/Copenhagen_Airport | 2026-10-15 |
| transit:Marmorkirken → Rådhuspladsen | "M3 sem baldeação · 2 zonas 24 kr · coord 55.6764, 12.5681" | OK | https://m.dk/en/travel-with-the-metro/tickets/ · https://en.wikipedia.org/wiki/Rådhuspladsen_station | 2026-10-15 |
| transit:Marmorkirken → Gammel Strand | "coord 55.6778, 12.5797" | OK | https://en.wikipedia.org/wiki/Gammel_Strand_station | 2026-10-15 |
| transit:Marmorkirken → Gammel Strand | "~4 min a pé até o Nationalmuseet" | INCONCLUSIVO — sem medição em fonte; conferir no Google Maps | — | 2026-10-15 |
| transit:S-tog Østerport ↔ Klampenborg | "coords Klampenborg 55.7772, 12.5881 · Østerport 55.6922, 12.5875" | OK | https://en.wikipedia.org/wiki/Klampenborg_station · https://en.wikipedia.org/wiki/Østerport_station | 2026-10-15 |
| transit:S-tog Østerport → Klampenborg | "linha C a cada 10 min de dia, 20 min à noite; parte dos trens não vai até Klampenborg" | RISCO — tabela da DSB não lida; o texto já manda olhar o painel | https://en.wikipedia.org/wiki/C_(S-train) | 2026-10-15 |
| transit:S-tog Østerport → Klampenborg | "10 a 13 min a pé do trem ao Bakken" | INCONCLUSIVO — verificador não achou fonte própria (o levantamento auditado cita ivh.ku.dk) | — | 2026-10-15 |
| transit:metrô · preços | "3 zonas 30 kr · 2 zonas 24 kr" | OK — o texto mantém [conferir no app DOT] | https://m.dk/en/travel-with-the-metro/tickets/ · https://denmarkguide.dk/en/oplev-danmark/transport-og-mobilitet/offentlig-transport/copenhagen-public-transport-fares-2026/ | 2026-10-15 |
| nota:legenda | "cada adulto leva até 2 crianças <12 anos grátis" | OK | https://m.dk/en/travel-with-the-metro/tickets/ · https://dinoffentligetransport.dk/en/how-to-travel/children | 2026-10-15 |
| nota:Qui 15/Out | "consigna só com reserva online · 10:00–18:00" | OK | https://radicalstorage.com/luggage-storage/copenhagen/amalienborg-palace/luggage-storage-amalienborg | 2026-10-15 |
| card:Malas na consigna | "~€5-6 por mala por dia" | RISCO — página dá €3,90-5 (+ seguro opcional €1,99); nada sustenta €6 → corrigido ("~€4-5, valor final no checkout") | https://radicalstorage.com/da/bagageopbevaring/kobenhavn/amalienborg-slot | 2026-10-15 |
| nota:Sex 16/Out | "sair e voltar com carimbo na mão na saída do Tivoli Food Hall" | OK — ressalva oficial de grandes eventos/lotação já no texto | https://www.tivoli.dk/en/practical-information/exchange-for-a-tivoli-pass | 2026-10-15 |
| nota:Sex 16/Out | "sexta 16 não tem Fredagsrock (série de verão)" | OK | https://www.tivoli.dk/en/programme/friday-rock | 2026-10-15 |
| nota:Sex 16/Out | "horário de fechamento da sexta [a confirmar]" | INCONCLUSIVO — calendário não legível; conferir no app do Tivoli | — | 2026-10-15 |
| nota:Sáb 17/Out | "Bakken fecha depois de domingo" | RISCO — fecha 19-22/out e reabre 23-25/out → corrigido | https://www.bakken.dk | 2026-10-15 |
| nota:Dom 18/Out | "crianças grátis · adulto online" | OK | https://nationalmuseet.dk/en/page/opening-hours | 2026-10-15 |
| historia:Nationalmuseet | "museu infantil fecha 18/out/2026 · substituto em 2027" | OK | https://nationalmuseet.dk/en/exhibitions/the-childrens-museum | 2026-10-15 |
| historia:Bakken | "1583, Kirsten Piil, fonte (segundo a lenda)" | RISCO — lenda (lex.dk: Piil provavelmente inventada); o texto já diz "segundo a lenda do próprio parque" | https://en.wikipedia.org/wiki/Dyrehavsbakken · https://lex.dk/Kirsten_Piils_kilde | 2026-10-15 |
| historia:Bakken | "o mais antigo em funcionamento no mundo (Wikipédia)" | OK | https://en.wikipedia.org/wiki/Dyrehavsbakken · https://eng.naturstyrelsen.dk/experience-nature/in-the-countryside/jaegersborg-deer-park/attractions | 2026-10-15 |
| historia:Dyrehaven | "aberta ao público em 1756" | OK | https://eng.naturstyrelsen.dk/experience-nature/explore-denmark-s-nature-with-our-guides/jaegersborg-deer-park/history | 2026-10-15 |
| historia:Bakken | "a meia hora um do outro (Bakken e Tivoli)" | INCONCLUSIVO — sem fonte → corrigido (frase removida) | — | 2026-10-15 |
| historia:Tivoli | "15/08/1843 · Carstensen · Cristiano VIII" | OK | https://www.tivoli.dk/en/om/about/history · https://en.wikipedia.org/wiki/Tivoli_Gardens | 2026-10-15 |
| historia:Tivoli | "5 anos · 1848 guerra contra a Prússia · Alhambra · morreu aos 44 antes da inauguração" | RISCO — a guerra é a Primeira Guerra de Schleswig → corrigido; o resto OK | https://en.wikipedia.org/wiki/Georg_Carstensen · https://lex.dk/Georg_Carstensen | 2026-10-15 |
| historia:Amalienborg | "Frederico V lançou o bairro nos anos 1750" | ERRO → corrigido (bairro lançado em 1748; palácios dos anos 1750) | https://en.wikipedia.org/wiki/Amalienborg · https://kongernessamling.dk/en/amalienborg/beletagen-2 | 2026-10-15 |
| historia:Amalienborg | "4 palácios para nobres · Eigtved · família real desde 1794 após incêndio de Christiansborg" | OK | https://en.wikipedia.org/wiki/Amalienborg · https://kongernessamling.dk/en/amalienborg/beletagen-2 | 2026-10-15 |

## Ligar ou conferir antes (o que nenhuma fonte pública fecha)

| O quê | Como |
|---|---|
| Fechamento do Tivoli na sexta 16 | app do Tivoli · +45 33 15 10 01 |
| Adulto precisa de pulseira pra acompanhar nos brinquedos infantis do Bakken? | bilheteria · +45 39 63 35 44 |
| Cadeirão no Locale 21 / Cap Horn / Kronborg | +45 33 93 44 12 · +45 33 12 85 04 · 33 13 07 08 |
| Café Daisy aberto no domingo | +45 53 61 14 16 |
| Preço final da consigna | checkout da reserva |
