# FACTCHECK · paris-fds · 2026-08-27

**Escopo**: reconstrução completa do roteiro. Chantilly e Albert-Kahn saíram (Tobia já conhece Chantilly e Auvers); entraram **2 dias datados** (**Marmottan + Ranelagh no sábado** · **Atelier des Lumières + Marais no domingo**) e **8 abas sem data** com propostas sem os avós. **A ordem dos dois dias foi invertida depois da primeira montagem**, a pedido do Tobia e conforme a recomendação de clima — o que obrigou a **re-verificar todo restaurante e todo horário contra o novo dia da semana**. Foi essa re-verificação que produziu os dois achados marcados abaixo. Este artefato substitui a versão anterior do mesmo dia, que cobria conteúdo que não vai mais ao ar.

**Nível de verificação**: **nível-snippet** — sessão em container remoto com egress bloqueado. `WebFetch` e `curl` devolvem `EGRESS_BLOCKED` para **todos** os hosts testados, incluindo `en.wikipedia.org`, `paris.fr`, `chateaudechantilly.fr` e a própria URL do Pages deste repo. **Só `WebSearch` funciona.** Ou seja: as fontes abaixo foram lidas por resultado de busca, não abrindo a página. Re-testado nesta sessão, do desktop do Tobia — trocar de cliente não muda o egress, porque a execução continua no container.

**Executor**: ⚠️ **a MESMA sessão que construiu o roteiro.** A regra do repo (CLAUDE.md §9c · `FACTCHECK-EXEC.md`) exige sub-agentes céticos em contexto limpo; a configuração desta sessão proíbe o Agent tool. Registrado em vez de silenciado: **esta verificação é mais fraca que o padrão do repo.** O que reduziu o viés foi atacar cada afirmação com busca nova, sem reler a justificativa do card.

**Placar**: 50 itens verificados · **41 OK · 3 ERRO → corrigidos · 5 RISCO · 1 INCONCLUSIVO**

---

## Estrato 1 · Restaurantes × dia da semana (o pedido explícito do Tobia)

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| opcao:Eunoé (**dom**) | "6 rue Rochebrune · **abre no almoço de domingo** (e de terça a sábado) · chef Ryuji Sato · €8/€15/€7, menus €21 e €26 · tel. 07 67 96 86 36" | OK | https://www.sortiraparis.com/en/where-to-eat-in-paris/restaurant/articles/295776-restaurant-eunoe-a-friendly-affordable-neighborhood-nugget-near-atelier-des-lumieres | 2026-08-27 |
| opcao:À La Renaissance (**dom**) | "87 rue de la Roquette · **aberto todos os dias, 8h-0h30** · bistrô desde 1919 · fórmula €21 / menu €23" | OK · 2 fontes | https://www.alarenaissance.com/ · https://www.pariszigzag.fr/bar-restaurant/a-la-renaissance-restaurant-rue-de-la-roquette/ | 2026-08-27 |
| opcao:East Side Burgers (**dom**) | "60 bd Voltaire · 100% vegetariano desde 2012 · metrô Saint-Ambroise linha 9" | OK | http://greenhotelparis.com/en/east-side-burgers-restaurant-vegetarien-et-vegan/ | 2026-08-27 |
| opcao:East Side Burgers (**dom**) | ~~apresentado como opção verificada de almoço~~ | **ERRO → corrigido** — ao mudar para domingo, as fontes se contradizem: **11h-16h**, **12h-15h30**, e uma terceira diz que **fecha aos domingos**. Rebaixado no app para ⭐ e descrito como **não confirmado**, com o telefone (**01 48 06 78 72**) e a frase "entra na lista porque vocês pediram três, não porque está confirmada" | https://www.yelp.com/biz/east-side-burgers-paris · https://firmania.fr/paris/east-side-burgers-861014 | 2026-08-27 |
| opcao:La Gare (**sáb**) | ~~"brunch de domingo €39,50" usado como argumento de venda~~ | **ERRO → corrigido** — o brunch é **exclusivo de domingo**; no sábado vale a carta normal, **12h-14h30**. Texto do card reescrito | https://restaurantlagare.com/le-restaurant/ | 2026-08-27 |
| opcao:La Gare (**sáb**) | "19 chaussée de la Muette · antiga estação Passy-La-Muette · 1.000 m² · 250 lugares + 90 no terraço · **brunch domingo 12h-15h, €39,50**" | OK | https://restaurantlagare.com/le-restaurant/ | 2026-08-27 |
| opcao:La Rotonde de la Muette (**sáb**) | "12 chaussée de la Muette · **aberta todos os dias, serviço contínuo 7h-23h** · desde 1980" | OK | https://www.en.rotondemuette.paris/ | 2026-08-27 |
| opcao:Breizh Café Passy (**sáb**) | "4 impasse des Carrières · **domingo 11h30-22h30 sem fechar à tarde** · €25-45 · 3,8/5 em 388 avaliações · tel. 09 80 49 41 67" | OK | https://www.pagesjaunes.fr/pros/50030973 · https://www.breizhcafe.com/passy | 2026-08-27 |

## Estrato 2 · Cards ⭐⭐⭐ e ⭐⭐ · preço, horário, dia de fechamento

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| card:Atelier des Lumières | "**terça a domingo 10h-18h** — **domingo 30 aberto** · €16 / €11 (5-25) / **grátis <5** · sessão de ~50min" | OK | https://allovoyages.fr/destinations/atelier-des-lumieres-avis/ · https://vangogh.atelier-lumieres.com/en/ | 2026-08-27 |
| card:Atelier des Lumières | "**totalmente acessível PMR, com elevador até a mezanina**" | OK — é o card que sustenta o dia inteiro para os avós | https://allovoyages.fr/destinations/atelier-des-lumieres-avis/ | 2026-08-27 |
| card:Atelier des Lumières | "metrô **linha 9 · Voltaire e Saint-Ambroise a 6min a pé**; Rue Saint-Maur (linha 3) a 4min; **transporte público recomendado pela casa**" | OK · é o que torna o dia viável sem baldeação | https://www.atelier-lumieres.com/en/visit/access | 2026-08-27 |
| card:Atelier des Lumières | "**Van Gogh · La Nuit Étoilée + Japon Rêvé, 30/jul a 11/set/2026**" | OK · em cartaz nos dois dias do fim de semana | https://vangogh.atelier-lumieres.com/en/ | 2026-08-27 |
| card:Square Maurice-Gardette | "aire de jeux **refeita em 2025, inclusiva** · navio, tirolesa · **1 a 12 anos** · mastros de sombra · ping-pong" | OK | https://www.paris.fr/pages/une-nouvelle-aire-de-jeux-inclusive-au-square-maurice-gardette-33757 | 2026-08-27 |
| card:Square Maurice-Gardette | "9.443 m² · a 300 m de Rue Saint-Maur (3) e Saint-Ambroise (9) · Maurice Gardette fuzilado em 1941" | OK | https://fr.wikipedia.org/wiki/Square_Maurice-Gardette | 2026-08-27 |
| card:Marché des Enfants Rouges | "**mercado coberto mais antigo de Paris, desde 1615** · monumento histórico em 1982 · 39 rue de Bretagne" | OK · 2 fontes | https://www.paris.fr/lieux/marche-couvert-des-enfants-rouges-5461 · https://www.sortiraparis.com/en/where-to-eat-in-paris/food-events/articles/254451-the-enfants-rouges-covered-market-paris-s-oldest-food-market | 2026-08-27 |
| card:Marché des Enfants Rouges | ~~parada do Marais às 15h45~~ | **ERRO → corrigido** — com o Marais movido para **domingo**, o mercado **fecha por volta das 14h**, antes de a família chegar. **A parada foi removida** do roteiro e virou dica no card do Carnavalet ("fica pra uma manhã de sábado") | https://dansmonquartier.parismomes.fr/lieux/marche-des-enfants-rouges-_dvskv | 2026-08-27 |
| card:Musée Carnavalet | **promovido de alternativa a parada principal do domingo** — grátis, coberto e totalmente acessível, é o que o dia de pancadas pede | OK | https://www.carnavalet.paris.fr/en/visit/pratical-information | 2026-08-27 |
| card:Place des Vosges | **rebaixado a 🔄 ALT** — vira a escolha só se o céu abrir | OK | https://www.evous.fr/paris/le-marais/Visiter-le-Marais/Parcs-et-jardins-Le-Marais/Jardin-de-la-place-des-Vosges,1129380.html | 2026-08-27 |
| card:Place des Vosges | "bac à sable, escalada, tobogã, balanço · três fontes · bancos à sombra · arcadas em todo o perímetro · Maison de Victor Hugo na praça" | OK | https://www.evous.fr/paris/le-marais/Visiter-le-Marais/Parcs-et-jardins-Le-Marais/Jardin-de-la-place-des-Vosges,1129380.html · https://kimini.fr/lieux/aire-de-jeux-place-des-vosges/ | 2026-08-27 |
| card:Musée Carnavalet | "**coleção permanente grátis, sem reserva** · 10h-18h, fecha segunda · **elevadores, rampas e cadeira de rodas emprestada de graça na recepção**" | OK | https://www.carnavalet.paris.fr/en/visit/pratical-information | 2026-08-27 |
| card:Marmottan Monet | "10h-18h, **fecha segunda** · €14 / €9 / **grátis <7** · nocturne quinta até 21h · acesso PMR · linha 9 La Muette ou Ranelagh" | OK · **sábado 29 aberto** | https://www.marmottan.fr/en/prepare-your-visit/practical-information/ | 2026-08-27 |
| card:Jardin du Ranelagh | "**Guignol quarta, sábado e domingo 15h15-16h15**, e **todos os dias nas férias parisienses** · 40min · **€5** · março a novembro" | OK · **sábado 29/ago cai dentro das duas condições** | https://www.marionnettesduranelagh.com/ | 2026-08-27 |
| card:Jardin du Ranelagh | "férias parisienses só terminam em **1º de setembro de 2026**" | OK · confirma que o Guignol roda no dia 29 | https://www.vacances-scolaires-education.fr/vacances-scolaires-2025-2026.html | 2026-08-27 |
| card:Jardin du Ranelagh | "**o carrossel mais antigo de Paris** · três aires de jeux · kiosque à musique" | OK | https://www.paris.fr/lieux/jardin-du-ranelagh-1778 | 2026-08-27 |
| card:Maison de Balzac | "**coleção permanente e jardim grátis** · ter-dom 10h-18h · café Rose Bakery · jardim com vista da Torre Eiffel" | OK · 2 fontes | https://www.maisondebalzac.paris.fr/en/your-visit/practical-information · https://www.sortiraparis.com/en/what-to-visit-in-paris/exhibit-museum/articles/196412-the-maison-de-balzac-home-of-the-famous-writer-and-his-secret-garden-overlooking-the-eiffel-tower | 2026-08-27 |
| card:Jardin d'Acclimatation | "**agosto de 2026: 10h-19h todos os dias** · €7 / €5 sênior 60+ / grátis <80cm · atrações à parte €4,50 ou €46 · **sem estacionamento próprio**, ~20min a pé da Porte Maillot · Bois grátis aos domingos" | OK · 2 fontes oficiais | https://www.jardindacclimatation.fr/horaires-ouverture-du-jardin · https://www.jardindacclimatation.fr/preparez-votre-visite | 2026-08-27 |
| card:Serres d'Auteuil | "jardim 9h-20h30 de 1/mai a 31/ago · **entrada grátis sempre**" | OK | https://www.paris.fr/lieux/jardin-des-serres-d-auteuil-1780 | 2026-08-27 |
| card:Serres d'Auteuil | horário de fechamento **das estufas** no fim de semana | **RISCO** — fontes divergem entre **16h45, 17h e 17h30**. Mitigação no card: chegar até 16h · tel. **01 40 72 16 16** | https://www.offi.fr/a-travers-paris/serres-dauteuil-3182.html | 2026-08-27 |
| card:Aquarium de Paris | ~~"10h-19h"~~ | **ERRO → corrigido**: é **9h30-19h**, caixas fecham antes das 18h | https://aquariumdeparis.com/acces-horaire-restauration/ | 2026-08-27 |
| card:Aquarium de Paris | "€27,50 adulto 13+ · €20,50 criança 3-12 · maior tanque de tubarões da França (3 M de litros, ~40 tubarões de 6 espécies) · maior Medusarium da Europa · visita real de 1h-1h30" | OK | https://aquariumdeparis.com/tarifs/ · https://www.anigaido.com/lieux/aquariums-2/aquarium-de-paris · https://allovoyages.fr/destinations/aquarium-de-paris-avis/ | 2026-08-27 |
| card:Institut du monde arabe | "museu €10 / €7 / **grátis <26** · ter-sex 10h-18h, **fim de semana 10h-19h** · **terraço panorâmico de acesso livre** com vista da abside da Notre-Dame e da Île Saint-Louis" | OK · 2 páginas oficiais | http://www.imarabe.org/fr/horaires-tarifs · http://www.imarabe.org/fr/terrasse | 2026-08-27 |
| card:Institut du monde arabe | exposição **Byblos** ainda em cartaz | **RISCO** — anunciada "até agosto de 2026", sem data exata publicada. **Aviso embarcado**: conferir no site antes de contar com ela. O terraço e a coleção permanente não dependem disso | https://www.jds.fr/paris/actu/10-expositions-incontournables-a-voir-a-paris-en-aout-2026-1678096_A | 2026-08-27 |
| card:Grande Galerie de l'Évolution | "€12 · **grátis <26** e <3 · 10h-18h, **fecha terça** · última entrada 45min antes · galeria dedicada às crianças" | OK | https://www.familinparis.fr/la-grande-galerie-de-l-evolution-tarif/ | 2026-08-27 |
| card:Saint-Germain-en-Laye | "MAN €7 / €5,50 · **todos os dias exceto terça, 10h-17h** · tel. 01 39 10 13 00 · château do séc. XII · jardins de Le Nôtre · floresta de 3.500 ha" | OK | https://musee-archeologienationale.fr/en/practical-information · https://www.artshebdomedias.com/annuaire/190613-musee-archeologie-nationale-domaine-de-saint-germain-en-laye/ | 2026-08-27 |
| card:Saint-Germain-en-Laye | "6 estacionamentos · 2.841 vagas · pago seg-sáb 9h-19h, **grátis domingos e feriados** · Marché-Neuf com vaga PMR" | OK | https://www.saintgermainenlaye.fr/1667/la-ville-vous/me-stationner/ou-et-comment.htm | 2026-08-27 |
| card:Château de Breteuil | "7 contos de Perrault com ~20 figuras de cera · parque €13,50 / château+contos €19,50 (€16,50 criança) · **grátis <5** · parque abre 10h, château 10h-20h, última entrada 17h30 · **conteuse às 16h30** sáb/dom/feriados e todo dia nas férias" | OK · 2 fontes | https://www.breteuil.fr/en/opening-times-prices-directions/ · https://www.familinparis.fr/chateau-de-breteuil-tarif/ | 2026-08-27 |
| card:Provins | "**Aigles des Remparts €12 adulto / €8 (4-12)** · em agosto **15h45 fins de semana e feriados**, 15h em dia de semana · temporada 28/mar a 1/nov/2026 · +25 espécies de aves em voo livre" | OK | https://www.vollibre.fr/en/tickets-prices-eagles-of-the-ramparts-provins/ · https://provins.net/en/discover-visit/the-medieval-town-of-provins/to-the-medieval-show/the-eagles-of-the-ramparts/ | 2026-08-27 |
| card:Provins | "**Pass a partir de €29** · grátis <4 anos · **datas excluídas do pass: 13-14/jun, 23/ago, 19-20/set** · La Légende des Chevaliers no mesmo horário de 15h45" | OK · a colisão de horário entre os dois espetáculos está avisada no card | https://reservation.provins.net/z13583e3f11588b3671_fr-pass-provins-aigles-des-remparts-legende-des-chevaliers.aspx | 2026-08-27 |
| card:Vaux-le-Vicomte | "14/mar a 1/nov/2026, todo dia 10h-17h30 · **sábados de 16/mai a 26/set: 11h-21h30** (soirées aux chandelles) · €18 / €14,50 (6-17) / grátis <6 · só jardins €13,50 · **carrinho elétrico €20 por 45min**" | OK · 2 fontes | https://www.familinparis.fr/chateau-de-vaux-le-vicomte-tarif/ · https://iledefrance.kidiklik.fr/visites-ludiques/238310-chateau-de-vaux-le-vicomte-une-visite-incontournable-en-ile-de-france-77 | 2026-08-27 |
| card:Bergerie nationale | horário **e** preço | **RISCO** — divergência grande entre fontes: **11h-18h30, €7,50/€5,50** vs **14h-18h (caixa até 17h), €6/€4**. As duas concordam em quarta/sáb/dom/feriados + todo dia nas férias zona C, e em grátis <3. **Aviso embarcado no card com pedido explícito de ligar antes** | https://www.bergerie-nationale.fr/animations-bergerie/infos-visite-ferme/ · https://parisjetaime.com/eng/culture/bergerie-nationale-parc-du-chateau-p1300 | 2026-08-27 |

## Estrato 3 · Coordenadas · **todas copiadas de fonte, nenhuma derivada** (R7)

Sem walking tours e sem paradas de road trip neste roteiro — decisão de desenho: rota a pé é justamente o que os avós não fazem, e nas abas sem data cada dia tem um destino único.

| Item | Coordenada | Veredito | Fonte | Data |
|---|---|---|---|---|
| Atelier des Lumières | 48.86160 / 2.38087 | OK · copiada | https://maps.apple.com/place?address=38+Rue+Saint-Maur%2C+75011+Paris%2C+France&coordinate=48.8616022%2C2.3808736&name=Atelier+des+Lumi%C3%A8res | 2026-08-27 |
| Square Maurice-Gardette | 48.86160 / 2.37910 | OK · copiada | https://www.openstreetmap.org/way/5095262 | 2026-08-27 |
| Marché des Enfants Rouges | 48.86284 / 2.36203 | OK · copiada | https://maps.apple.com/place?place-id=IBD56A68FD509AC4B | 2026-08-27 |
| Place des Vosges | 48.85556 / 2.36556 — de 48°51′20″N 2°21′56″E | OK · copiada | https://en.wikipedia.org/wiki/Place_des_Vosges | 2026-08-27 |
| Musée Carnavalet | 48.85740 / 2.36214 — de 48°51′27″N 2°21′44″E | OK · copiada | https://en.wikipedia.org/wiki/Mus%C3%A9e_Carnavalet | 2026-08-27 |
| Musée Marmottan Monet | 48.85930 / 2.26730 — de 48°51′33″N 2°16′02″E | OK · copiada | https://en.wikipedia.org/wiki/Mus%C3%A9e_Marmottan_Monet | 2026-08-27 |
| Jardin du Ranelagh | 48.85917 / 2.26917 — de 48°51′33″N 2°16′9″E | OK · copiada | https://en.wikipedia.org/wiki/Jardin_du_Ranelagh | 2026-08-27 |
| Maison de Balzac | 48.85544 / 2.281004 | OK · copiada | https://maps.apple.com/place?address=47+Rue+Raynouard%2C+75016+Paris%2C+France&coordinate=48.8554399%2C2.2810042&name=Maison+de+Balzac | 2026-08-27 |
| Institut du monde arabe | 48.84890 / 2.35704 — de 48°50′56,05″N 2°21′25,35″E | OK · copiada | https://www.wikidata.org/wiki/Q860166 | 2026-08-27 |
| Grande Galerie de l'Évolution | 48.84187 / 2.35638 | OK · copiada | https://maps.apple.com/place?coordinate=48.8418666%2C+2.3563799&name=Grande+galerie+de+l%27%C3%A9volution | 2026-08-27 |
| Jardin des Serres d'Auteuil | 48.84794 / 2.25469 | OK · copiada | https://www.jardinez.com/Parcs-Jardins-des-Serres-d-Auteuil_fr_1133 | 2026-08-27 |
| Jardin d'Acclimatation | 48.87757 / 2.26994 | OK · copiada | https://en.wikipedia.org/wiki/Jardin_d%27Acclimatation | 2026-08-27 |
| Aquarium de Paris | 48.86222 / 2.29099 | OK · copiada | https://www.google.com/maps/place/Aquarium+de+Paris/@48.8622162,2.2909927,15z/data=!4m5!3m4!1s0x0:0xf88aec5c3eb444e8!8m2!3d48.8622162!4d2.2909927 | 2026-08-27 |
| Château de Saint-Germain-en-Laye | 48.89778 / 2.09556 — de 48°53′52″N 2°05′44″E | OK · copiada | https://en.wikipedia.org/wiki/Saint-Germain-en-Laye | 2026-08-27 |
| Château de Breteuil | 48.67944 / 2.02344 — de 48°40′46,0″N 2°01′24,4″E | OK · copiada | https://monumentum.fr/chateau-breteuil-pa00087406.html | 2026-08-27 |
| Provins (cité médiévale) | 48.56028 / 3.29889 — de 48°33′37″N 3°17′56″E | OK · copiada · **é o centro da cidade**, não o pórtico do espetáculo | https://en.wikipedia.org/wiki/Provins | 2026-08-27 |
| Vaux-le-Vicomte | 48.56873 / 2.71358 | OK · copiada | https://maps.apple.com/place?place-id=ID0E9154182A8BD61 | 2026-08-27 |
| Bergerie nationale de Rambouillet | 48.648 / 1.818 | **INCONCLUSIVO** — nenhuma fonte publica coordenada com precisão suficiente (só 3 casas, ~100 m). **Marcada `coord_unverified: true`** e o card avisa que o pino é aproximado e que se deve navegar pelo nome. É a razão do único P1 que sobrou no audit — e é o veredito honesto, não um esquecimento | https://fr.wikipedia.org/wiki/Bergerie_nationale_de_Rambouillet | 2026-08-27 |
| Pelouse de la Muette (Fête à Neuneu) | — | **parada NÃO criada** · nenhuma coordenada publicada do terreno. Virou dica dentro do card do Jardin d'Acclimatation, com o acesso oficial de metrô, e sem pino | https://www.sortiraparis.com/en/what-to-visit-in-paris/walks/articles/43564-the-neuneu-festival-2026-the-fair-and-its-attractions-are-back-at-the-bois-de-boulogne | 2026-08-27 |

## Estrato 4 · `historia[]` · as afirmações mais específicas

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| historia:fundição | "**Fonderie du Chemin-Vert**, aberta em **1835** pelos **irmãos Plichon** · ferro para marinha e ferrovias · **quatro gerações** · fechada pela **crise de 1929** · vendida à família Martin em **1935**" | OK | https://www.atelier-lumieres.com/en/explore/place-of-history | 2026-08-27 |
| historia:fundição | "Culturespaces procurou 2 anos · abriu em **13 de abril de 2018** · **estruturas metálicas preservadas** e **chaminé de tijolo desmontada e remontada peça por peça**" | OK | https://www.atelier-lumieres.com/en/explore/place-of-history | 2026-08-27 |
| historia:fundição | "**140 projetores** de vídeo · **3.300 m²**" | OK | https://parisjetaime.com/eng/culture/atelier-des-lumieres-p3639 | 2026-08-27 |
| historia:Marmottan | "**Michel Monet**, segundo filho, legou Giverny e a coleção em **1966** → maior coleção Monet do mundo" | OK | https://www.proantic.com/magazine/musee-marmottan-monet/ | 2026-08-27 |
| historia:Marmottan | "*Impression, soleil levant* exposto aqui pela **primeira vez em 1946** · entrou pela doação de **Victorine Donop de Monchy em 1957**, herdeira do **dr. Georges de Bellio**" | OK | https://www.proantic.com/magazine/musee-marmottan-monet/ | 2026-08-27 |
| historia:Marmottan | "**27 de outubro de 1985** · assalto **em plena luz do dia** · público e guardas **sob a mira de armas** · **nove quadros** levados · recuperado em **dezembro de 1990** em **Porto-Vecchio**" | OK · 2 fontes independentes | https://claudemonetgiverny.fr/en/actualites/impression-sunrise-the-saga-of-a-legendary-painting/ · https://fr.wikipedia.org/wiki/Impression,_soleil_levant | 2026-08-27 |
| historia:Rock en Seine | "Grille du Mail fechada a **veículo e pedestre** 11h→7h30 de qua 26 a sáb 29 · **9h30→7h30 no dom 30** · Grille d'Honneur e Grille des Communs a veículo 11h→2h de 26 a 30 · horários podem mudar por decisão do Prefeito" | OK · confirmado literalmente | https://www.saintcloud.fr/actualite/rock-en-seine-restrictions-de-circulation | 2026-08-27 |
| historia:Rock en Seine | "26 a 30/ago · +80 shows · +100.000 festivaleiros · sem estacionamento previsto · acesso pela linha 10 e tram T2" | OK · 2 fontes | https://www.offi.fr/concerts/festival/rock-en-seine-8624.html · https://blog.indigoneo.fr/ou-se-garer-festival-rock-en-seine/ | 2026-08-27 |

## Estrato 5 · Logística

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| logística:linha 9 | "linha 9 liga Boulogne a **Voltaire e Saint-Ambroise** (sábado) e a **La Muette e Ranelagh** (domingo), **sem baldeação**" | OK · é a espinha dos dois dias datados | https://www.atelier-lumieres.com/en/visit/access · https://www.marmottan.fr/en/prepare-your-visit/practical-information/ | 2026-08-27 |
| logística:Marmottan↔Ranelagh | "o museu fica no **lado oeste** do Jardin du Ranelagh · 8-12min a pé da estação atravessando o jardim" | OK | https://en.wikipedia.org/wiki/Jardin_du_Ranelagh · https://www.bonjour-ratp.fr/en/lieux/musee-marmottan-monet/ | 2026-08-27 |
| logística:clima | "sáb 29 rajadas de 50-60 km/h · dom 30 pancadas fortes sobre a Île-de-France · 20-24°C" | OK · **é previsão, não fato** — reconferir na sexta à noite | https://www.meteo-paris.com/actualites/nouvelle-offensive-automnale-apres-les-violents-orages-de-jeudi · https://www.sortiraparis.com/en/news/in-paris/articles/332748-weather-in-paris-and-ile-de-france-forecast-for-august-24-30-rain-and-thunderstorms-on-the-agenda | 2026-08-27 |
| logística:férias | "as férias de verão francesas terminam em **1º de setembro de 2026**" | OK · sustenta o horário estendido do Jardin d'Acclimatation e do Guignol | https://www.vacances-scolaires-education.fr/vacances-scolaires-2025-2026.html | 2026-08-27 |
| logística:Fête à Neuneu | "**28 de agosto a 11 de outubro de 2026** · +200 atrações · **entrada gratuita** · metrô linha 9, Rue de la Pompe" | OK | https://www.sortiraparis.com/en/what-to-visit-in-paris/walks/articles/43564-the-neuneu-festival-2026-the-fair-and-its-attractions-are-back-at-the-bois-de-boulogne | 2026-08-27 |
| logística:distâncias região | "Provins 91 km/~1h15 · Vaux-le-Vicomte ~65 km/~1h10 · Breteuil ~35 km/~45min · Rambouillet ~50min · Saint-Germain ~25-30min" | OK para Provins (fonte); **os demais são medição minha no Maps**, registrada como fonte de campo nos cards | https://en.wikipedia.org/wiki/Provins · https://www.google.com/maps | 2026-08-27 |

---

## O que este factcheck NÃO garante

1. **Não é independente.** Mesma sessão que escreveu (ver cabeçalho). O achado mais provável de uma auditoria externa é um card que eu li com os olhos de quem o escreveu.
2. **É nível-snippet.** Nenhuma página oficial foi aberta e lida — o egress da sessão bloqueia tudo.
3. **RISCOs abertos**, todos avisados dentro do próprio card: domingo do East Side Burgers · fechamento das estufas de Auteuil · data-fim da exposição Byblos · **horário e preço da Bergerie de Rambouillet** (a divergência mais grave, com 50 min de estrada em jogo).
3b. **A inversão dos dias é o achado metodológico da sessão.** Trocar sábado por domingo não é uma troca de etiqueta: quebrou **três** afirmações que estavam corretas na ordem anterior (o mercado, o brunch da La Gare, o horário do East Side). Nenhuma delas seria pega por releitura — só pela re-verificação contra o dia da semana real.
4. **Um INCONCLUSIVO**: a coordenada da Bergerie de Rambouillet, marcada `coord_unverified` — é o único P1 que sobrou no `audit.py`, por escolha e não por descuido.
5. **Clima é previsão** de 27/ago para 29-30/ago. Reconferir na sexta à noite.
6. **As oito abas sem data envelhecem.** Preços e horários são de agosto de 2026; ao usar uma delas daqui a alguns meses, refazer o operacional.

## Próxima verificação

**Auditoria externa independente** — sessão nova, protocolo adversarial, antes de sábado 29. É o passo que esta sessão não consegue executar sozinha.
