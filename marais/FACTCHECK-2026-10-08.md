# FACTCHECK · marais · 2026-10-08

**Escopo**: primeiro factcheck da coletânea (nunca teve artefato) · cards ⭐⭐⭐ (10) afirmação a afirmação, inclusive a narração parada-a-parada das `dicas` · opções ⭐⭐⭐ (2) · **100% das paradas de walking tour** (39 paradas, 7 tours) em existência, endereço, função/status, `mapsQuery` e coordenada · `historia[]`: a coletânea não tem. Itens ⭐⭐ só onde repetiam afirmação corrigida num ⭐⭐⭐ (Maison de Victor Hugo, Hôtel de Rohan, Picasso) — o resto do ⭐⭐ é do re-check pré-viagem.

**Executor**: 4 sub-agentes céticos em paralelo, contexto limpo (receberam só as afirmações, sem fonte nem justificativa de quem escreveu), só leitura · estratos: (A1) museus e praças ⭐⭐⭐ · (A2) doces, lojas e restaurantes ⭐⭐⭐ · (B1) paradas das abas Família e Profundo · (B2) paradas das abas Guloso, Museus e Lojas · + contraprova mecânica da sessão orquestradora (que não escreveu a coletânea) · 2026-10-08

**Nível de verificação**: **nível-página** onde a linha não diz o contrário (`WebFetch` abriu a página e leu a afirmação; coordenadas pelas APIs Nominatim e Photon sobre o OpenStreetMap; status de empresa pela API pública do registro SIRENE). **nível-snippet**, marcado "(trecho)", onde só o resultado do buscador foi lido.

**Placar**: 232 linhas (215 dos verificadores + 17 da contraprova) · **165 OK · 29 ERRO → corrigidos · 23 RISCO · 15 INCONCLUSIVO**. Dos ERRO: 16 de coordenada (todas a 86-254 m do lugar; as novas conferidas a 0-23 m do endereço), 1 loja fechada (L'Éclair de Génie saiu do tour Guloso), 1 pátio fechado ao público (Hôtel de Rohan), 1 `mapsQuery`, 10 de conteúdo. RISCO com ajuste no card: 21 de 23. INCONCLUSIVO que viraram `[a confirmar]` ou saíram do texto: 7 de 15.

**Pós-correção**: `build.py` ok (favicon + meta tags gerados) · `validate.py` ok · `audit.py` 30/40 (forma · igual a antes) · P0 0 · `maps-audit.py` limpo · `sync-check` ok · dívida de proveniência 36 → 34 (só encolhe).

**Decisão de montagem tomada junto** (não é fato, é consequência): sem a L'Éclair de Génie, o tour Guloso passa a nascer na Une Glace à Paris, que só abre às 13h — o horário dela foi de 11:15 para 13:00 e o do Breizh Café de 12:30 para 13:30. Distância recalculada: ~1,7 km.

---
## Estrato A1 · cards ⭐⭐⭐ de museus e praças (Place des Vosges, Enfants Rouges, Flamel, Carnavalet, Picasso, Chasse)

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| card:Place des Vosges | "inaugurada em 1612 como Place Royale" | OK | https://fr.wikipedia.org/wiki/Place_des_Vosges | 2026-10-08 |
| card:Place des Vosges | "mandada construir por Henri IV" | OK | https://fr.wikipedia.org/wiki/Place_des_Vosges | 2026-10-08 |
| card:Place des Vosges | "praça planejada mais antiga de Paris" | OK (nuance: a Place Dauphine é quase contemporânea) | https://fr.wikipedia.org/wiki/Place_des_Vosges · https://sixtysixmag.com/pavillon-de-la-reine/ (trecho) | 2026-10-08 |
| card:Place des Vosges | "36 pavilhões" | OK | https://fr.wikipedia.org/wiki/Place_des_Vosges | 2026-10-08 |
| card:Place des Vosges | "nome atual em 1800 · Vosges o primeiro a pagar impostos" | OK (13/09/1800) | https://parcoursrevolution.paris.fr/en/points-of-interest/15-a-royal-square-during-the-revolution · https://fr.wikipedia.org/wiki/Place_des_Vosges | 2026-10-08 |
| card:Place des Vosges | "gramados onde é permitido sentar e pisar" | OK | https://www.paris.fr/lieux/square-louis-xiii-36 | 2026-10-08 |
| card:Place des Vosges | "fonte em cada canto" | OK | https://www.paris.fr/lieux/square-louis-xiii-36 · https://fr.wikipedia.org/wiki/Place_des_Vosges | 2026-10-08 |
| card:Place des Vosges | "tanque de areia e brinquedos no canto do jardim" | OK | https://www.paris.fr/lieux/square-louis-xiii-36 | 2026-10-08 |
| card:Place des Vosges | "sob as tílias" | OK | https://www.paris.fr/lieux/square-louis-xiii-36 | 2026-10-08 |
| card:Place des Vosges | "Pavillon du Roi ao sul, sobre a rue de Birague" | OK | https://fr.vikidia.org/wiki/Pavillon_du_Roi (trecho) · https://homepages.bluffton.edu/~sullivanm/vosges/vosges.html (trecho) | 2026-10-08 |
| card:Place des Vosges | "Pavillon de la Reine ao norte · os dois mais altos" | OK | https://fr.wikipedia.org/wiki/Place_des_Vosges | 2026-10-08 |
| card:Place des Vosges | "estátua de Luís XIII · original virou canhão na Revolução" | OK (bronze de 1639 fundido em 1792) | https://www.paris.fr/pages/paris-un-musee-a-ciel-ouvert-les-statues-royales-20266 | 2026-10-08 |
| card:Place des Vosges | "arcadas em todo o perímetro, com galerias e cafés" | OK | https://fr.wikipedia.org/wiki/Place_des_Vosges | 2026-10-08 |
| card:Place des Vosges | "custo grátis" (sem horário) | RISCO → corrigido (o jardim fecha: 8h/9h-19h30 em out/2026; horário entrou na dica) | https://www.paris.fr/lieux/square-louis-xiii-36 | 2026-10-08 |
| card:Place des Vosges | "jardim plano, carrinho roda fácil" | OK (acessível PMR) | https://www.paris.fr/lieux/square-louis-xiii-36 | 2026-10-08 |
| card:Place des Vosges | "arcadas têm 1 degrau em alguns trechos" | INCONCLUSIVO — nenhuma fonte; conferir em campo (é um aviso a favor do carrinho, mantido) | — | 2026-10-08 |
| card:Place des Vosges (WT 1) | "no nº 6 morou Victor Hugo (1832-48)" | OK | https://www.maisonsvictorhugo.paris.fr/en | 2026-10-08 |
| card:Place des Vosges (WT 1) | "onde escreveu parte de Os Miseráveis" | OK | https://www.napoleon.org/magazine/lieux/maison-de-victor-hugo-paris/ (trecho) | 2026-10-08 |
| card:Place des Vosges (WT 1) | "Maison de Victor Hugo tem coleção grátis" | RISCO → corrigido (entrada paga durante exposição temporária: "Hugo et l'architecture" até 22/11/2026, €11, grátis -18) | https://www.maisonsvictorhugo.paris.fr/en/paris/visit/practical-information · https://parismusees.paris.fr/en/exposition/victor-hugo-and-architecture | 2026-10-08 |
| card:Place des Vosges (WT 1) | "salão chinês que ele mesmo desenhou" | OK | https://www.pariszigzag.fr/sortir-paris/tendances-culture/expositions/exposition-hugo-decorateur-maison-victor-hugo/ | 2026-10-08 |
| card:Place des Vosges (WT 1) | "banheiro limpo" (no museu) | INCONCLUSIVO → trocado por "banheiro público no jardim" (paris.fr: toilettes oui) | https://www.paris.fr/lieux/square-louis-xiii-36 | 2026-10-08 |
| card:Place des Vosges (WT 1) | Maison VH fecha 2ª (omitido no card) | RISCO → corrigido (dica diz "fecha 2ª") | https://www.maisonsvictorhugo.paris.fr/en/paris/visit/practical-information | 2026-10-08 |
| card:Place des Vosges (WT 2) | "Hôtel de Sully, 62 rue Saint-Antoine" | OK | https://fr.wikipedia.org/wiki/H%C3%B4tel_de_Sully | 2026-10-08 |
| card:Place des Vosges (WT 2) | "passadiço no canto sudoeste liga a praça ao jardim" | OK | https://fr.wikipedia.org/wiki/H%C3%B4tel_de_Sully | 2026-10-08 |
| card:Place des Vosges (WT 2) | "palacete de 1630" | OK (obras 1625-1630) | https://fr.wikipedia.org/wiki/H%C3%B4tel_de_Sully | 2026-10-08 |
| card:Place des Vosges (WT 2) | "atalho" (subentendido sempre aberto) | RISCO → corrigido (passagem aberta 9h-18h) | https://www.pariszigzag.fr/?p=89988 | 2026-10-08 |
| card:Place des Vosges (WT 3) | "Carnavalet, coleção permanente grátis, com jardins" | OK | https://www.carnavalet.paris.fr/en/visit/pratical-information | 2026-10-08 |
| card:Place des Vosges (WT 3) | "Madame de Sévigné morou aqui" | OK (1677-1696) | https://fr.wikipedia.org/wiki/Mus%C3%A9e_Carnavalet | 2026-10-08 |
| card:Place des Vosges (WT 4) | "rue des Rosiers, coração do Pletzl" | OK | https://en.wikipedia.org/wiki/Pletzl | 2026-10-08 |
| card:Place des Vosges (WT 4) | "almoço de falafel (L'As du Fallafel)" | OK | https://en.wikipedia.org/wiki/L%27As_du_Fallafel (trecho) | 2026-10-08 |
| card:Place des Vosges (WT 5) | "Fontaine Stravinsky, 16 esculturas" | OK | https://www.paris.fr/pages/la-fontaine-stravinsky-retrouve-son-eclat-decouvrez-ses-secrets-24204 | 2026-10-08 |
| card:Place des Vosges (WT 5) | "pretas de Tinguely, coloridas de Niki de Saint Phalle" | OK | https://www.paris.fr/pages/la-fontaine-stravinsky-retrouve-son-eclat-decouvrez-ses-secrets-24204 · https://en.wikipedia.org/wiki/Stravinsky_Fountain | 2026-10-08 |
| card:Place des Vosges (WT 5) | "inspiradas em obras de Stravinsky" | OK | https://www.paris.fr/pages/la-fontaine-stravinsky-retrouve-son-eclat-decouvrez-ses-secrets-24204 | 2026-10-08 |
| card:Place des Vosges (WT 5) | "ao lado do Centre Pompidou" | RISCO → corrigido (Pompidou fechado em obra até 2030; fonte acessível, entorno em obra) | https://www.centrepompidou.fr/en/pompidou-plus/magazine/article/secrets-darchi-la-place-igor-stravinsky-et-sa-fontaine (trecho) | 2026-10-08 |
| card:Enfants Rouges | "39 rue de Bretagne, 3e" | OK | https://www.paris.fr/equipements/marche-couvert-des-enfants-rouges-5461 | 2026-10-08 |
| card:Enfants Rouges | "aberto em 1615" | OK (a Wikipédia também cita 1628 para a construção) | https://www.sortiraparis.com/hotel-restaurant/tendances-food/articles/254451-le-marche-couvert-des-enfants-rouges-le-plus-ancien-marche-alimentaire-de-paris | 2026-10-08 |
| card:Enfants Rouges | "mercado coberto mais antigo de Paris" | OK (ainda em atividade) | https://fr.wikipedia.org/wiki/March%C3%A9_des_Enfants-Rouges | 2026-10-08 |
| card:Enfants Rouges | "nome vem do orfanato, crianças de vermelho" | OK | https://www.pariszigzag.fr/?p=111059 · https://fr.wikipedia.org/wiki/March%C3%A9_des_Enfants-Rouges | 2026-10-08 |
| card:Enfants Rouges | "bancas marroquina, japonesa, italiana e libanesa" | OK | https://www.sortiraparis.com/hotel-restaurant/tendances-food/articles/254451-le-marche-couvert-des-enfants-rouges-le-plus-ancien-marche-alimentaire-de-paris | 2026-10-08 |
| card:Enfants Rouges | "tajine do traiteur marroquino" | OK | https://www.pariszigzag.fr/?p=111059 | 2026-10-08 |
| card:Enfants Rouges | "crêpes/galettes" | OK | https://www.untappedcities.com/le-marche-des-enfants-rouges-an-eclectic-food-market-hidden-in-the-marais/ (trecho) | 2026-10-08 |
| card:Enfants Rouges | "fecha 2ª-feira" | OK (ter-sáb 8h30-20h30, qui até 21h30, dom até 17h → "dom até 17h" entrou na dica) | https://www.paris.fr/equipements/marche-couvert-des-enfants-rouges-5461 | 2026-10-08 |
| card:Enfants Rouges | "banca japonesa Chez Taeko" | OK | https://lefooding.com/en/restaurants/restaurant-chez-taeko-paris (trecho) | 2026-10-08 |
| card:Enfants Rouges | "€10-16 por prato" | OK | https://lefooding.com/en/restaurants/restaurant-chez-taeko-paris (trecho) | 2026-10-08 |
| card:Enfants Rouges | "padarias (Bontemps no nº 57)" | RISCO → corrigido (é pâtisserie de sablés, fecha 2ª e 3ª) | https://www.doitinparis.com/fr/bontemps-la-patisserie-branchee-du-petit-sable-19328 (trecho) · https://bontemps.paris/ | 2026-10-08 |
| card:Enfants Rouges | "saída norte cai colado no Square du Temple" | RISCO → corrigido ("uns 200 m adiante") | https://www.sortiraparis.com/arts-culture/balades/articles/249380-le-square-du-temple-un-jardin-parisien-ou-il-fait-bon-vivre (trecho) | 2026-10-08 |
| card:Enfants Rouges | "lota 12h-14h no fim de semana" | INCONCLUSIVO — dado de campo, sem fonte publicada | — | 2026-10-08 |
| card:Flamel | "51 rue de Montmorency, 3e" | OK | https://fr.wikipedia.org/wiki/Maison_de_Nicolas_Flamel | 2026-10-08 |
| card:Flamel | "1407, gravado no friso sobre o térreo" | OK | https://fr.wikipedia.org/wiki/Maison_de_Nicolas_Flamel | 2026-10-08 |
| card:Flamel | "casa mais antiga de Paris que se pode datar com certeza" | OK | https://fr.wikipedia.org/wiki/Maison_de_Nicolas_Flamel | 2026-10-08 |
| card:Flamel | "escrivão e livreiro rico" | OK | https://en.wikipedia.org/wiki/Nicolas_Flamel (trecho) | 2026-10-08 |
| card:Flamel | "térreo comércio, andares de cima abrigo gratuito" | OK | https://fr.wikipedia.org/wiki/Maison_de_Nicolas_Flamel | 2026-10-08 |
| card:Flamel | "rezar de manhã e à noite pela alma do casal Flamel" | ERRO → corrigido (a inscrição pede todo dia um Pai-Nosso e uma Ave-Maria pelos pobres pecadores falecidos) | https://fr.wikipedia.org/wiki/Maison_de_Nicolas_Flamel · https://en.wikipedia.org/wiki/Nicolas_Flamel (trecho) | 2026-10-08 |
| card:Flamel | "aparece em Harry Potter e O Código Da Vinci" | OK | https://en.wikipedia.org/wiki/Nicolas_Flamel (trecho) · https://en.wikipedia.org/wiki/The_Da_Vinci_Code (trecho) | 2026-10-08 |
| card:Flamel | "letras e símbolos originais de 1407" | INCONCLUSIVO → "originais" saiu do card (fachada restaurada; ficha Mérimée não consultada) | — | 2026-10-08 |
| card:Flamel | "Auberge Nicolas Flamel, restaurante estrelado" | ERRO → corrigido ("selecionado pelo Guia Michelin, sem estrela") | https://guide.michelin.com/fr/fr/ile-de-france/paris/restaurant/auberge-nicolas-flamel · https://www.gillespudlowski.com/critiques/lauberge-nicolas-flamel (trecho) | 2026-10-08 |
| card:Flamel | "restaurante €€€€" | ERRO → corrigido (€€€ no Michelin · fecha domingo) | https://guide.michelin.com/be/nl/ile-de-france/paris/restaurant/auberge-nicolas-flamel | 2026-10-08 |
| card:Flamel | "interior é o Auberge (gastronômico, reserva)" | OK | https://guide.michelin.com/be/nl/ile-de-france/paris/restaurant/auberge-nicolas-flamel | 2026-10-08 |
| card:Flamel | "Arts et Métiers: autômatos, pêndulo de Foucault" | OK | https://parisjetaime.com/culture/musee-des-arts-et-metiers-p3596 (trecho) | 2026-10-08 |
| card:Flamel | "galerias Perrotin e Thaddaeus Ropac no Haut Marais" | OK | https://parisjetaime.com/culture/galerie-thaddaeus-ropac-paris-marais-p1735 (trecho) | 2026-10-08 |
| card:Flamel | "Merci, 111 bd Beaumarchais, Fiat vermelho" | OK | https://merci-merci.com/en/le-111-beaumarchais | 2026-10-08 |
| card:Carnavalet | "23 rue de Sévigné, 3e" | OK | https://www.carnavalet.paris.fr/en/visit/pratical-information | 2026-10-08 |
| card:Carnavalet | "permanente grátis" | OK (temporárias pagas) | https://www.carnavalet.paris.fr/en/visit/pratical-information | 2026-10-08 |
| card:Carnavalet | "fecha 2ª" | OK (ter-dom 10h-18h) | https://www.carnavalet.paris.fr/en/visit/pratical-information | 2026-10-08 |
| card:Carnavalet | "dois palacetes, um do séc. XVI onde morou Sévigné" | OK | https://fr.wikipedia.org/wiki/Mus%C3%A9e_Carnavalet | 2026-10-08 |
| card:Carnavalet | "da pré-história ao séc. XX" | RISCO → corrigido ("aos dias de hoje") | https://fr.wikipedia.org/wiki/Mus%C3%A9e_Carnavalet | 2026-10-08 |
| card:Carnavalet | "reformado em 2021" | OK (reabriu 29/05/2021) | https://www.paris.fr/dossiers/la-reouverture-du-musee-carnavalet-49 | 2026-10-08 |
| card:Carnavalet | "letreiros de rua originais / lojas reconstituídas" | OK | https://www.paris.fr/dossiers/la-reouverture-du-musee-carnavalet-49 | 2026-10-08 |
| card:Carnavalet | "a cela de Maria Antonieta" | ERRO → corrigido (são objetos do cativeiro da família real na prisão do Temple; a cela dela era na Conciergerie) | https://parcoursrevolution.paris.fr/en/points-of-interest/9-the-carnavalet-museum · https://fr.wikipedia.org/wiki/Mus%C3%A9e_Carnavalet | 2026-10-08 |
| card:Carnavalet | "quarto de cortiça onde Proust escreveu" | RISCO → corrigido ("reconstituição", com os móveis dele e pedaços da cortiça) | https://www.paris.fr/dossiers/la-reouverture-du-musee-carnavalet-49 · https://www.theparisreview.org/blog/?p=95590 (trecho) | 2026-10-08 |
| card:Carnavalet | "acessível (reforma de 2021)" | OK | https://www.carnavalet.paris.fr/en/en-situation-de-handicap | 2026-10-08 |
| card:Picasso | "Hôtel Salé, 5 rue de Thorigny" | OK | https://www.museepicassoparis.fr/en/practical-information | 2026-10-08 |
| card:Picasso | "Hôtel Salé 1659, dono enriqueceu com o imposto do sal" | OK | https://www.museepicassoparis.fr/en/hotel-sale | 2026-10-08 |
| card:Picasso | "maior coleção pública de Picasso · ~5.000 obras" | OK | https://www.museepicassoparis.fr/en/collection | 2026-10-08 |
| card:Picasso | "escadaria barroca monumental" | OK | https://www.museepicassoparis.fr/en/hotel-sale | 2026-10-08 |
| card:Picasso | "percurso cronológico das fases" | OK | https://www.museepicassoparis.fr/wp-content/uploads/2026/08/Picasso_RA25_Mai2026_Web-1.pdf (trecho) | 2026-10-08 |
| card:Picasso | "~€16" | OK | https://www.museepicassoparis.fr/en/practical-information | 2026-10-08 |
| card:Picasso | "grátis -18" | OK | https://www.museepicassoparis.fr/en/practical-information | 2026-10-08 |
| card:Picasso | "compra online evita fila" | OK | https://www.museepicassoparis.fr/en/practical-information | 2026-10-08 |
| card:Picasso | "fecha 2ª" | OK (ter-dom 9h30-18h) | https://www.museepicassoparis.fr/en/practical-information | 2026-10-08 |
| card:Picasso | "acessível com elevador" | OK | https://www.museepicassoparis.fr/en/practical-information | 2026-10-08 |
| card:Chasse | "62 rue des Archives, 3e" | OK | https://www.chassenature.org/acces-horaires | 2026-10-08 |
| card:Chasse | "Hôtel de Guénégaud (1655), único hôtel de Mansart que sobrou" | OK | https://en.wikipedia.org/wiki/Mus%C3%A9e_de_la_Chasse_et_de_la_Nature (trecho) | 2026-10-08 |
| card:Chasse | "salas por bicho (lobo, javali)" | OK | https://frenchglimpses.com/2026/06/26/why-you-must-visit-the-musee-de-la-chasse-et-de-la-nature-in-paris/ (trecho) | 2026-10-08 |
| card:Chasse | "teto com uma coruja que te observa" | RISCO → corrigido (teto de Jan Fabre com várias corujas de olhos humanos) | https://www.timeout.fr/paris/musee-de-la-chasse-et-de-la-nature/jan-fabre/la-nuit-de-diane (trecho) | 2026-10-08 |
| card:Chasse | "gavetas-surpresa" | OK | https://frenchglimpses.com/2026/06/26/why-you-must-visit-the-musee-de-la-chasse-et-de-la-nature-in-paris/ (trecho) | 2026-10-08 |
| card:Chasse | "pago · fecha 2ª" | OK (ter-dom 11h-18h) | https://www.chassenature.org/acces-horaires | 2026-10-08 |
| card:Chasse | "~€12" | OK (€11-13 conforme exposição) | https://chassenature.tickeasy.com/fr-FR/tarifs | 2026-10-08 |
| card:Chasse | "grátis -18" | OK | https://chassenature.tickeasy.com/fr-FR/tarifs | 2026-10-08 |
| card:Chasse | "acessibilidade parcial (escadas)" | ERRO → corrigido (site oficial: acessível a cadeira de rodas; carrinho de bebê NÃO entra nas salas) | https://www.chassenature.org/acces-horaires | 2026-10-08 |

## Estrato A2 · cards ⭐⭐⭐ de doces e loja + opções ⭐⭐⭐ (Une Glace, Breizh, Genin, Merci, L'As du Fallafel, Miznon)

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| card:Une Glace | existe em 15 rue Sainte-Croix-de-la-Bretonnerie | OK | https://uneglaceaparis.fr/web/ · https://fr.gaultmillau.com/fr/artisans/une-glace-a-paris | 2026-10-08 |
| card:Une Glace | "Emmanuel Ryon, MOF sorveteiro" | OK | https://uneglaceaparis.fr/web/ · https://www.timeout.fr/paris/restaurants/une-glace-a-paris | 2026-10-08 |
| card:Une Glace | "campeão mundial de pâtisserie" | OK (1999) | https://uneglaceaparis.fr/web/ · https://www.debic.com/en/world-renowned-pastry-chef-emmanuel-ryon | 2026-10-08 |
| card:Une Glace | "caramelo defumado em fogo de lenha" (sobre + imperdível) | ERRO → corrigido (o defumado da casa é a baunilha defumada na faia) | https://www.timeout.fr/paris/restaurants/une-glace-a-paris · https://fr.gaultmillau.com/fr/artisans/une-glace-a-paris | 2026-10-08 |
| card:Une Glace | "baunilha de verdade" | OK | https://parisbymouth.com/une-glace-a-paris/ | 2026-10-08 |
| card:Une Glace | "pâtisseries geladas de autor" | OK | https://uneglaceaparis.fr/web/ | 2026-10-08 |
| card:Une Glace | "aberto o ano inteiro" | OK | https://uneglaceaparis.fr/web/ | 2026-10-08 |
| card:Une Glace | "talvez o melhor sorvete de Paris" | OK (opinião sustentada) | https://parisbymouth.com/une-glace-a-paris/ · https://fr.gaultmillau.com/fr/artisans/une-glace-a-paris | 2026-10-08 |
| card:Une Glace | "abre 13h" | OK | https://uneglaceaparis.fr/web/ | 2026-10-08 |
| card:Une Glace | "fecha 2ª e 3ª" | INCONCLUSIVO → card diz "[a confirmar]" (site oficial: todo dia; guias de 2026: fechado 2ª-3ª) · ligar antes | — | 2026-10-08 |
| card:Une Glace | "~€4-6" | INCONCLUSIVO → card diz "[a confirmar]" com os preços de 2015 | — | 2026-10-08 |
| card:Une Glace | "loja térrea · rua plana" | INCONCLUSIVO — sem fonte; conferir em campo | — | 2026-10-08 |
| card:Breizh | existe em 109 rue Vieille-du-Temple | OK | https://www.breizhcafe.com/le-marais | 2026-10-08 |
| card:Breizh | "abre ~9h" | OK (seg-dom 9h-23h) | https://www.breizhcafe.com/le-marais | 2026-10-08 |
| card:Breizh | "reserva ajuda" | OK | https://www.breizhcafe.com/le-marais | 2026-10-08 |
| card:Breizh | "épicerie ao lado vende cidras" | OK (111 rue Vieille-du-Temple) | https://www.breizhcafe.com/le-marais-epiceries | 2026-10-08 |
| card:Breizh | "vive cheio" | OK | https://www.theinfatuation.com/paris/reviews/breizh-cafe | 2026-10-08 |
| card:Breizh | "melhores galettes de Paris" | OK (opinião sustentada) | https://www.timeout.com/paris/en/restaurants/breizh-cafe · https://www.gillespudlowski.com/?p=16221 | 2026-10-08 |
| card:Breizh | "versões com peixe defumado" | OK | https://www.gillespudlowski.com/?p=16221 | 2026-10-08 |
| card:Breizh | "galette complète e crêpe de caramelo salgado" | OK | https://www.gillespudlowski.com/?p=16221 | 2026-10-08 |
| card:Breizh | "cidra numa tigela (bolée)" | INCONCLUSIVO — cidras confirmadas, serviço em bolée não | — | 2026-10-08 |
| card:Breizh | "fica atrás do Museu Picasso" | OK aproximado (~120 m) | https://parisjetaime.com/eng/restaurant/breizh-cafe-p414 (trecho) | 2026-10-08 |
| card:Breizh | "€12-18" | RISCO → corrigido ("galette €6,50-16,50 · com cidra + crêpe, ~€25-35") | https://www.timeout.fr/paris/restaurants/breizh-cafe-le-marais | 2026-10-08 |
| card:Breizh | "térreo · espera em pé" | INCONCLUSIVO — piso não informado | — | 2026-10-08 |
| card:Genin | existe em 133 rue de Turenne | OK | https://www.jacquesgenin.fr/magasins | 2026-10-08 |
| card:Genin | "fecha 2ª" | OK (ter-dom 11h-19h, sáb até 19h30) | https://www.jacquesgenin.fr/magasins | 2026-10-08 |
| card:Genin | "fondeur en chocolat" | OK | https://www.jacquesgenin.fr | 2026-10-08 |
| card:Genin | "fornecia os melhores hotéis de Paris" | OK | https://www.timeout.fr/paris/shopping/jacques-genin-turenne | 2026-10-08 |
| card:Genin | "se recusa a abrir filial" | ERRO → corrigido (tem 2 lojas, Marais e Rive Gauche) | https://www.jacquesgenin.fr/magasins · https://www.timeout.fr/paris/shopping/jacques-genin-turenne | 2026-10-08 |
| card:Genin | "caramelos de manga" | OK (manga-maracujá) | https://thewanderingeater.com/2010/07/19/jacques-genin-french-caramels-and-millefeuille-heaven/ | 2026-10-08 |
| card:Genin | "caramelos de framboesa" | RISCO → corrigido (framboesa só em pâte de fruit; lista de caramelos refeita) | https://parisbymouth.com/?p=14666 | 2026-10-08 |
| card:Genin | "pâtes de fruits, caixas de presente" | OK | https://www.jacquesgenin.fr/collection/caramels-nougats | 2026-10-08 |
| card:Genin | "millefeuille montado na hora no salão de chá" | RISCO → corrigido (site oficial lista pâtisseries só sob encomenda; salão "[a confirmar]") | https://www.jacquesgenin.fr/magasins · https://www.timeout.fr/paris/shopping/jacques-genin-turenne | 2026-10-08 |
| card:Genin | "millefeuille de baunilha" | INCONCLUSIVO → "baunilha" saiu do card | — | 2026-10-08 |
| card:Genin | "melhor chocolate e caramelo de Paris" | RISCO → corrigido (cat virou "chocolates e caramelos de referência") | https://www.timeout.fr/paris/shopping/jacques-genin-turenne · https://www.chocoparis.com/jacques-genin/ | 2026-10-08 |
| card:Genin | "salão no andar de cima por escada" | ERRO → corrigido (o andar de cima é o laboratório; loja térrea) | https://thewanderingeater.com/2010/07/19/jacques-genin-french-caramels-and-millefeuille-heaven/ · https://www.timeout.fr/paris/shopping/jacques-genin-turenne | 2026-10-08 |
| card:Genin | "ponta norte (Filles du Calvaire)" | OK | https://viewfromtheback.com/2022/04/17/french-fancies-jacques-genin/ | 2026-10-08 |
| card:Merci | existe em 111 bd Beaumarchais | OK | https://merci-merci.com/en/le-111-beaumarchais | 2026-10-08 |
| card:Merci | "seg-sáb 10h-19h30 · fecha domingo" | ERRO → corrigido (abre todo dia: 2ª-4ª 10h30-19h30 · 5ª-6ª 10h30-20h · sáb 10h-20h · dom 10h-19h30) | https://merci-merci.com/en/le-111-beaumarchais · https://www.visitparisregion.com/fr/merci | 2026-10-08 |
| card:Merci | "antiga fábrica têxtil do séc. XIX" | OK aproximado (prédio do séc. XIX de firma de tecidos de decoração) | https://merci-merci.com/en/le-111-beaumarchais | 2026-10-08 |
| card:Merci | "3 andares-loft" | OK | https://merci-merci.com/en/le-111-beaumarchais | 2026-10-08 |
| card:Merci | "Fiat 500 vermelho no pátio" | OK | https://merci-merci.com/en/le-111-beaumarchais | 2026-10-08 |
| card:Merci | "todo o lucro vai pra fundação que educa mulheres e crianças" | RISCO → corrigido ("fundo de dotação que financia educação em Madagascar") | https://merci-merci.com/en/pages/le-fonds-de-dotation · https://hipparis.com/merci-shopping-for-a-cause-in-paris/ | 2026-10-08 |
| card:Merci | "o concept store mais famoso de Paris" | OK (opinião) | https://www.visitparisregion.com/fr/merci | 2026-10-08 |
| card:Merci | "tem 3 cafés dentro" | ERRO → corrigido (2: Used Book Café e Café Noir) | https://merci-merci.com/en/le-111-beaumarchais · https://merci-merci.com/en/pages/le-cine-cafe | 2026-10-08 |
| card:Merci | "Used Book Café, almoço/lanche" | OK (sem reserva → entrou no card) | https://merci-merci.com/en/pages/le-used-book-cafe | 2026-10-08 |
| card:Merci | "elevador entre andares" | INCONCLUSIVO → card diz "[a confirmar]" | — | 2026-10-08 |
| opcao:L'As du Fallafel | existe em 34 rue des Rosiers | OK | https://www.theinfatuation.com/paris/reviews/las-du-fallafel | 2026-10-08 |
| opcao:L'As du Fallafel | "€8-10" | OK no teto (pitas €9-14 → preço do card ajustado) | https://rankeat.fr/restaurants/las-du-fallafel-paris-4e | 2026-10-08 |
| opcao:L'As du Fallafel | "a fila anda rápido" | OK | https://www.theinfatuation.com/paris/reviews/las-du-fallafel | 2026-10-08 |
| opcao:L'As du Fallafel | "o falafel mais famoso de Paris" | OK (opinião) | https://www.timeout.fr/paris/restaurants/las-du-fallafel | 2026-10-08 |
| opcao:L'As du Fallafel | (omissão) dia de fechamento | RISCO → corrigido ("fecha sábado e sexta à tarde") | https://rankeat.fr/restaurants/las-du-fallafel-paris-4e · https://parisjetaime.com/restaurant/l-as-du-fallafel-p455 (trecho) | 2026-10-08 |
| opcao:L'As du Fallafel | "come na praça" | INCONCLUSIVO → saiu do texto | — | 2026-10-08 |
| opcao:Miznon | existe em 22 rue des Écouffes | OK | https://parisbymouth.com/miznon · https://fr.gaultmillau.com/fr/restaurant/miznon | 2026-10-08 |
| opcao:Miznon | "chef Eyal Shani" | OK | https://fr.gaultmillau.com/fr/restaurant/miznon | 2026-10-08 |
| opcao:Miznon | "couve-flor inteira assada é o hit" | OK | https://parisbymouth.com/miznon | 2026-10-08 |
| opcao:Miznon | "€12-16" | OK | https://parisbymouth.com/miznon | 2026-10-08 |
| opcao:Miznon | "casual, barulhento" | OK | https://parisbymouth.com/miznon | 2026-10-08 |
| opcao:Miznon | "adora criança" | INCONCLUSIVO → saiu do texto | — | 2026-10-08 |
| opcao:Miznon | (omissão) dia de fechamento | RISCO → corrigido ("fecha sábado e sexta a partir de ~16h · sem reserva") | https://parisbymouth.com/miznon · https://theinfatuation.com/paris/reviews/miznon | 2026-10-08 |
| opcao:Miznon | "1min a pé" do L'As du Fallafel | INCONCLUSIVO — rue des Écouffes cruza a rue des Rosiers; não medido | — | 2026-10-08 |

## Estrato B1 · paradas de WT das abas Família e Profundo (20 paradas · 100%)

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| wt:Coração do Marais:Place des Vosges | existe · mapsQuery buscável · coord ~10 m | OK | https://nominatim.openstreetmap.org/search?q=Place+des+Vosges,+Paris&format=json&limit=3 | 2026-10-08 |
| wt:Coração do Marais:Maison de Victor Hugo | museu em 6 Place des Vosges · ter-dom 10h-18h · coord ~3 m | OK | https://www.maisonsvictorhugo.paris.fr/en/paris/visit/practical-information · https://nominatim.openstreetmap.org/search?q=Maison+de+Victor+Hugo,+Paris&format=json | 2026-10-08 |
| wt:Coração do Marais:Hôtel de Sully | 62 rue Saint-Antoine · pátio e jardim atravessáveis · coord ~17 m | OK | https://en.wikipedia.org/wiki/H%C3%B4tel_de_Sully (trecho) · https://nominatim.openstreetmap.org/search?q=H%C3%B4tel+de+Sully,+Paris&format=json | 2026-10-08 |
| wt:Coração do Marais:Carnavalet | entrada em 23 rue de Sévigné · coord ~9 m do nº 23 | OK | https://www.paris.fr/lieux/musee-carnavalet-histoire-de-paris-1518 (trecho) · https://photon.komoot.io/api/?q=23+Rue+de+S%C3%A9vign%C3%A9,+Paris | 2026-10-08 |
| wt:Coração do Marais:L'As du Fallafel | existe em 34 rue des Rosiers · coord ~3 m | OK | https://parisjetaime.com/restaurant/l-as-du-fallafel-p455 (trecho) · https://nominatim.openstreetmap.org/search?q=L%27As+du+Fallafel,+Paris&format=json | 2026-10-08 |
| wt:Coração do Marais:L'As du Fallafel | aberto quando a família passar | RISCO → corrigido (fecha sábado e sexta à tarde · aviso entrou na opção do almoço) | https://parisjetaime.com/restaurant/l-as-du-fallafel-p455 (trecho) | 2026-10-08 |
| wt:Coração do Marais:Fontaine Stravinsky | existe · reaberta 07/11/2023 · acesso livre · coord ~2 m | OK | https://www.timeout.fr/paris/actualites/apres-un-an-et-demi-de-travaux-la-mythique-fontaine-stravinsky-de-niki-de-saint-phalle-et-jean-tinguely-rouvre-ses-jets-a-cote-du-centre-pompidou-110723 (trecho) · https://nominatim.openstreetmap.org/search?q=Fontaine+Stravinsky,+Paris&format=json | 2026-10-08 |
| wt:Mercado & Playground:Musée Picasso | 5 rue de Thorigny · ter-dom 9h30-18h · coord ~23 m do nº 5 | OK | https://www.museepicassoparis.fr/sites/default/files/2025-11/Plan_musee_SEP_2025_FR.pdf (trecho) · https://photon.komoot.io/api/?q=5+Rue+de+Thorigny,+Paris | 2026-10-08 |
| wt:Mercado & Playground:Enfants Rouges | 39 rue de Bretagne · coord ~6 m | OK | https://www.paris.fr/equipements/marche-couvert-des-enfants-rouges-5461 (trecho) · https://nominatim.openstreetmap.org/search?q=March%C3%A9+des+Enfants+Rouges,+Paris&format=json | 2026-10-08 |
| wt:Mercado & Playground:Enfants Rouges | aberto quando a família passar | RISCO → corrigido (fecha 2ª, dom até 17h · ambos no card) | https://www.paris.fr/equipements/marche-couvert-des-enfants-rouges-5461 (trecho) | 2026-10-08 |
| wt:Mercado & Playground:Square du Temple | jardim com playground (64 rue de Bretagne) · mapsQuery buscável · coord na borda sul, entrada da rue de Bretagne | OK | https://www.paris.fr/lieux/square-du-temple-elie-wiesel-2425 (trecho) · https://photon.komoot.io/api/?q=Square+du+Temple+Elie+Wiesel | 2026-10-08 |
| wt:Mercado & Playground:Carreau du Temple | halle em 4 rue Eugène Spuller · coord ~6 m | OK | https://www.lecarreaudutemple.eu/ · https://nominatim.openstreetmap.org/search?q=Carreau+du+Temple,+Paris&format=json | 2026-10-08 |
| wt:Mercado & Playground:Carreau du Temple | público entra quando quiser | RISCO (entrada do público pela 2 rue Perrée; domingo só com evento) — parada de passagem, sem card próprio | https://www.lecarreaudutemple.eu/ · https://parisjetaime.com/culture/le-carreau-du-temple-p1652 (trecho) | 2026-10-08 |
| wt:Marais Sul:Saint-Gervais | igreja em 13 rue des Barres | OK | https://parisjetaime.com/culture/eglise-saint-gervais-saint-protais-p1248 (trecho) · https://dioceseparis.fr/accueil-visite-de-saint-gervais.html (trecho) | 2026-10-08 |
| wt:Marais Sul:Saint-Gervais | mapsQuery "Église Saint-Gervais & Rue des Barres, 13 rue des Barres" inequívoca | ERRO → corrigido (`Église Saint-Gervais, 13 rue des Barres, Paris` no card e na parada) | https://parisjetaime.com/culture/eglise-saint-gervais-saint-protais-p1248 | 2026-10-08 |
| wt:Marais Sul:Saint-Gervais | coord 48.8562, 2.3522 | ERRO → corrigido (~198 m, do lado do Hôtel de Ville · certo 48.8555, 2.3547) | https://photon.komoot.io/api/?q=Saint-Gervais-Saint-Protais&lat=48.857&lon=2.36 | 2026-10-08 |
| wt:Marais Sul:Hôtel de Sens | 1 rue du Figuier · Bibliothèque Forney · coord ~5 m do nº 1 | OK | https://www.paris.fr/lieux/bibliotheque-forney-18 (trecho) · https://photon.komoot.io/api/?q=1+Rue+du+Figuier,+Paris | 2026-10-08 |
| wt:Marais Sul:Village Saint-Paul | pátios de antiquários entre rue Saint-Paul e Jardins-Saint-Paul · mapsQuery buscável | OK | https://www.visitparisregion.com/fr/village-saint-paul (trecho) | 2026-10-08 |
| wt:Marais Sul:Village Saint-Paul | coord 48.8526, 2.3633 | ERRO → corrigido (~180 m, quarteirão errado · certo 48.8534, 2.3611) | https://photon.komoot.io/api/?q=Village+Saint-Paul&lat=48.857&lon=2.36 | 2026-10-08 |
| wt:Marais Sul:Sainte-Catherine | praça pedonal · coord ~46-61 m dos objetos da praça | OK | https://www.yonder.fr/cityguides/paris/decouvrir/la-place-du-marche-sainte-catherine (trecho) · https://photon.komoot.io/api/?q=Place+du+March%C3%A9+Sainte-Catherine,+Paris | 2026-10-08 |
| wt:Marais Sul:MEP | museu em 5/7 rue de Fourcy · programação 2026 ativa · coord ~5 m | OK | https://parisjetaime.com/culture/mep-maison-europeenne-de-la-photographie-p3515 (trecho) · https://photon.komoot.io/api/?q=Maison+Europ%C3%A9enne+de+la+Photographie | 2026-10-08 |
| wt:Marais Sul:MEP | aberto quando a família passar | RISCO (fecha 2ª e 3ª — o card já dizia) | https://parisjetaime.com/culture/mep-maison-europeenne-de-la-photographie-p3515 (trecho) | 2026-10-08 |
| wt:Haut Marais:Mariage Frères | loja e salão de chá em 30 rue du Bourg-Tibourg | OK | https://parisjetaime.com/shopping/mariage-freres-le-marais-p2556 (trecho) · https://parisbymouth.com/mariage-freres/ (trecho) | 2026-10-08 |
| wt:Haut Marais:Mariage Frères | coord 48.8573, 2.3551 | ERRO → corrigido (~111 m · certo 48.8577, 2.3565) | https://photon.komoot.io/api/?q=30+Rue+du+Bourg-Tibourg,+Paris | 2026-10-08 |
| wt:Haut Marais:Free'P'Star | brechó em 61 rue de la Verrerie | OK | https://www.timeout.fr/paris/shopping/freepstar | 2026-10-08 |
| wt:Haut Marais:Free'P'Star | coord 48.8577, 2.3540 | ERRO → corrigido (~103 m · certo 48.8580, 2.3527) | https://photon.komoot.io/api/?q=61+Rue+de+la+Verrerie,+Paris | 2026-10-08 |
| wt:Haut Marais:Hôtel de Rohan | existe em 87 rue Vieille-du-Temple · relevo dos Chevaux du Soleil no pátio das cavalariças | OK | https://pop.culture.gouv.fr/notice/merimee/PA00086155 (trecho) | 2026-10-08 |
| wt:Haut Marais:Hôtel de Rohan | "entrar no pátio (livre)" pra ver os Chevaux du Soleil | ERRO → corrigido (pátio fechado ao público durante a reforma, aviso oficial sem data · card virou 🟡 "confira no portão", com plano B nos jardins do Hôtel de Soubise) | https://www.archives-nationales.culture.gouv.fr/en/infos-pratiques/practical-information-hotel-de-rohan-la-chancellerie-dorleans · https://unidivers.fr/event/visite-guidee-de-lhotel-de-rohan-et-des-decors-de-la-chancellerie-dorleans-archives-nationales-site-de-paris-paris-2026-09-19t1300000200/ | 2026-10-08 |
| wt:Haut Marais:Hôtel de Rohan | coord 48.8601, 2.3603 (~86 m do prédio, lado oposto da rua) | ERRO → corrigido (certo 48.8595, 2.3599, nº 87) | https://photon.komoot.io/api/?q=87+Rue+Vieille+du+Temple,+Paris | 2026-10-08 |
| wt:Haut Marais:Hôtel de Soubise | 60 rue des Francs-Bourgeois · Musée des Archives · jardins reabertos 06/06/2026 | OK | https://www.rfgenealogie.com/infos/les-archives-nationales-rouvrent-leurs-jardins-au-coeur-du-marais · https://parisjetaime.com/culture/musee-des-archives-nationales-hotel-de-soubise-p1001 (trecho) | 2026-10-08 |
| wt:Haut Marais:Hôtel de Soubise | coord 48.8593, 2.3593 | ERRO → corrigido (~166 m · certo 48.8600, 2.3573, portão do nº 60) | https://photon.komoot.io/api/?q=60+Rue+des+Francs-Bourgeois,+Paris | 2026-10-08 |
| wt:Haut Marais:Nicolas Flamel | casa de 1407 em 51 rue de Montmorency · hoje restaurante · coord ~8 m | OK | https://en.wikipedia.org/wiki/House_of_Nicolas_Flamel · https://photon.komoot.io/api/?q=51+Rue+de+Montmorency,+Paris | 2026-10-08 |

## Estrato B2 · paradas de WT das abas Guloso, Museus e Lojas (19 paradas · 100%)

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| wt:Guloso:L'Éclair de Génie | existe e está aberta em 14 rue Pavée | ERRO → corrigido (estabelecimento fechado no registro oficial desde 17/03/2025; nenhuma pâtisserie no endereço no OSM · parada e card removidos, tour renumerado) | https://recherche-entreprises.api.gouv.fr/search?q=14%20rue%20pavee&code_postal=75004 · https://photon.komoot.io/reverse?lat=48.8562&lon=2.36062&limit=8&radius=0.05 | 2026-10-08 |
| wt:Guloso:Une Glace à Paris | sorveteria em 15 rue Sainte-Croix-de-la-Bretonnerie · coord ~2 m | OK | https://photon.komoot.io/api/?q=Une+Glace+a+Paris · https://nominatim.openstreetmap.org/search?q=15+rue+Sainte-Croix-de-la-Bretonnerie,+Paris&format=json&limit=3 | 2026-10-08 |
| wt:Guloso:Une Glace à Paris | horário | INCONCLUSIVO — este verificador leu qua-dom; o de A2 leu "todo dia" no site oficial · card diz "[a confirmar]" | — | 2026-10-08 |
| wt:Guloso:Breizh Café | crêperie em 109 rue Vieille-du-Temple | OK | https://www.breizhcafe.com/ · https://parisjetaime.com/eng/restaurant/breizh-cafe-p414 | 2026-10-08 |
| wt:Guloso:Breizh Café | coord 48.8597, 2.3609 | ERRO → corrigido (~123 m · certo 48.86063, 2.36182) | https://photon.komoot.io/api/?q=Breizh+Caf%C3%A9+Paris | 2026-10-08 |
| wt:Guloso:Popelini | pâtisserie de choux em 29 rue Debelleyme · empresa ativa | OK | https://recherche-entreprises.api.gouv.fr/search?q=popelini%20debelleyme · https://www.timeout.fr/paris/shopping/popelini | 2026-10-08 |
| wt:Guloso:Popelini | coord 48.8606, 2.3636 | ERRO → corrigido (~205 m · certo 48.86243, 2.36384) | https://photon.komoot.io/api/?q=Popelini+Paris | 2026-10-08 |
| wt:Guloso:Bontemps | pâtisserie em 57 rue de Bretagne · empresa ativa · fecha 2ª e 3ª | OK | https://bontemps.paris/ · https://recherche-entreprises.api.gouv.fr/search?q=bontemps%20rue%20de%20bretagne | 2026-10-08 |
| wt:Guloso:Bontemps | coord 48.8628, 2.3633 | ERRO → corrigido (~229 m · certo 48.86387, 2.36063) | https://nominatim.openstreetmap.org/search?q=57+rue+de+Bretagne,+Paris&format=json&limit=3 | 2026-10-08 |
| wt:Guloso:Jacques Genin | chocolatier em 133 rue de Turenne · ter-dom 11h-19h | OK | https://www.jacquesgenin.fr/magasins | 2026-10-08 |
| wt:Guloso:Jacques Genin | coord 48.8623, 2.3657 | ERRO → corrigido (~254 m · certo 48.86447, 2.36462) | https://nominatim.openstreetmap.org/search?q=133+rue+de+Turenne,+Paris&format=json&limit=3 | 2026-10-08 |
| wt:Museus:Victor Hugo | museu em 6 place des Vosges · coord ~3 m | OK | https://www.maisonsvictorhugo.paris.fr/en | 2026-10-08 |
| wt:Museus:Victor Hugo | card ⭐⭐ "coleção grátis" (cat, sobre, dicas, custo) | RISCO → corrigido (mesma fonte do estrato A1: paga até 22/11/2026, €11) | https://www.maisonsvictorhugo.paris.fr/en/paris/visit/practical-information | 2026-10-08 |
| wt:Museus:Carnavalet | museu em 23 rue de Sévigné · coord ~43 m | OK | https://www.paris.fr/lieux/musee-carnavalet-histoire-de-paris-1518 | 2026-10-08 |
| wt:Museus:Cognacq-Jay | museu em 8 rue Elzévir · aberto (fechamento pós-assalto terminou 10/12/2024) · coord ~33 m | OK | https://www.paris.fr/lieux/musee-cognacq-jay-1519 | 2026-10-08 |
| wt:Museus:Picasso | museu em 5 rue de Thorigny · coord ~36 m | OK | https://www.museepicassoparis.fr/fr/horaires-et-acces | 2026-10-08 |
| wt:Museus:Picasso | elevador (card: "acessível com elevador") | RISCO → corrigido (elevador do 3º andar fora de serviço; aviso no card) | https://www.museepicassoparis.fr/fr/horaires-et-acces | 2026-10-08 |
| wt:Museus:Chasse et Nature | museu em 62 rue des Archives · programação ativa | OK | https://www.chassenature.org/ | 2026-10-08 |
| wt:Museus:Chasse et Nature | coord 48.8604, 2.3584 | ERRO → corrigido (~99 m · certo 48.86126, 2.35878) | https://nominatim.openstreetmap.org/search?q=Mus%C3%A9e+de+la+Chasse+et+de+la+Nature,+Paris&format=json&limit=3 | 2026-10-08 |
| wt:Lojas:Fleux | concept store em 39 rue Sainte-Croix-de-la-Bretonnerie · ativa | OK | https://recherche-entreprises.api.gouv.fr/search?q=fleux · https://www.visitparisregion.com/fr/fleux | 2026-10-08 |
| wt:Lojas:Fleux | coord 48.8581, 2.3552 | ERRO → corrigido (~104 m · certo 48.85874, 2.35417) | https://nominatim.openstreetmap.org/search?q=39+rue+Sainte-Croix-de-la-Bretonnerie,+Paris&format=json&limit=3 | 2026-10-08 |
| wt:Lojas:Sézane | loja em 33 rue des Blancs-Manteaux (aberta 31/03/2023) | OK | https://fashionunited.fr/actualite/retail/ouverture-prochaine-d-une-boutique-sezane-dans-le-marais-parisien/2023032031671 · https://recherche-entreprises.api.gouv.fr/search?q=sezane%20blancs%20manteaux | 2026-10-08 |
| wt:Lojas:Sézane | coord 48.8585, 2.3576 | ERRO → corrigido (~171 m · certo 48.85940, 2.35571) | https://nominatim.openstreetmap.org/search?q=33+rue+des+Blancs-Manteaux,+Paris&format=json&limit=3 | 2026-10-08 |
| wt:Lojas:CSAO | artesanato da África Ocidental em 9 rue Elzévir · ativa · coord ~59 m | OK | https://www.csao.fr/fr/content/21-coordonnees · https://recherche-entreprises.api.gouv.fr/search?q=csao%20elzevir | 2026-10-08 |
| wt:Lojas:Muji | loja Muji em 47 rue des Francs-Bourgeois | OK | https://nominatim.openstreetmap.org/search?q=47+rue+des+Francs-Bourgeois,+Paris&format=json&limit=3 · https://www.evous.fr/paris/shopping/Maison-et-decoration-a-Paris/Les-magasins-Muji-a-Paris,1177530.html | 2026-10-08 |
| wt:Lojas:Muji | coord 48.8581, 2.3614 | ERRO → corrigido (~167 m · certo 48.85831, 2.35914) | https://nominatim.openstreetmap.org/search?q=47+rue+des+Francs-Bourgeois,+Paris&format=json&limit=3 | 2026-10-08 |
| wt:Lojas:French Trotters | concept store em 128 rue Vieille-du-Temple | OK | https://www.frenchtrotters.fr/ | 2026-10-08 |
| wt:Lojas:French Trotters | coord 48.8617, 2.3628 | ERRO → corrigido (~101 m · certo 48.86167, 2.36418) | https://photon.komoot.io/api/?q=French+Trotters+Paris | 2026-10-08 |
| wt:Lojas:Empreintes | concept store de métiers d'art em 5 rue de Picardie · ter-sáb 11h-19h | OK | https://empreintes.com/boutique/empreintes-paris-3/ · https://ateliersdart.com/action-economique/reseau-de-vente/empreintes-concept-store/ | 2026-10-08 |
| wt:Lojas:Empreintes | coord 48.8633, 2.3644 | ERRO → corrigido (~162 m · certo 48.86334, 2.36219) | https://photon.komoot.io/api/?q=5+rue+de+Picardie+Paris | 2026-10-08 |
| wt:Lojas:Bonton | concept store infantil em 5 bd des Filles du Calvaire · seg-sáb 10h-19h · coord ~62 m | OK | https://www.bonton.fr/en/pages/boutiques/filles-du-calvaire · https://fashionunited.fr/actualite/business/bonton-rachetee-par-le-groupe-zannier/2024042534876 | 2026-10-08 |
| wt:Lojas:Merci | concept store em 111 bd Beaumarchais · coord ~8 m | OK | https://www.merci-merci.com/ · https://photon.komoot.io/api/?q=111+boulevard+Beaumarchais+Paris | 2026-10-08 |

## Contraprova mecânica (sessão orquestradora · depois da correção)

Cada coordenada nova foi geocodificada de novo pelo endereço no Photon/OpenStreetMap, sem passar pelos verificadores; e o fechamento da L'Éclair de Génie foi relido direto na API do registro de empresas.

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| fechamento:L'Éclair de Génie | estabelecimento da 14 rue Pavée fechado | OK (estado F, fechamento 2025-03-17; o da 43 rue Sainte-Croix também fechado desde 2018) | https://recherche-entreprises.api.gouv.fr/search?q=eclair%20de%20genie&code_postal=75004 | 2026-10-08 |
| coord nova:Saint-Gervais | 48.8555, 2.3547 | OK (1 m da igreja) | https://photon.komoot.io/api/?q=%C3%89glise+Saint-Gervais-Saint-Protais+Paris | 2026-10-08 |
| coord nova:Village Saint-Paul | 48.8534, 2.3611 | OK (78 m do ponto do OSM, que é uma área) | https://photon.komoot.io/api/?q=Village+Saint-Paul+Paris | 2026-10-08 |
| coord nova:Mariage Frères | 48.8577, 2.3565 | OK (1 m do nº 30) | https://photon.komoot.io/api/?q=30+Rue+du+Bourg-Tibourg+Paris | 2026-10-08 |
| coord nova:Free'P'Star | 48.8580, 2.3527 | OK (4 m do nº 61) | https://photon.komoot.io/api/?q=61+Rue+de+la+Verrerie+Paris | 2026-10-08 |
| coord nova:Hôtel de Soubise | 48.8600, 2.3573 | OK (63 m do centro do museu · é o portão do nº 60) | https://photon.komoot.io/api/?q=60+Rue+des+Francs-Bourgeois+Paris | 2026-10-08 |
| coord nova:Hôtel de Rohan | 48.8595, 2.3599 | OK (3 m do nº 87) | https://photon.komoot.io/api/?q=87+Rue+Vieille+du+Temple+Paris | 2026-10-08 |
| coord nova:Breizh Café | 48.86063, 2.36182 | OK (3 m do nº 109) | https://photon.komoot.io/api/?q=109+Rue+Vieille+du+Temple+Paris | 2026-10-08 |
| coord nova:Popelini | 48.86243, 2.36384 | OK (3 m do nº 29) | https://photon.komoot.io/api/?q=29+Rue+Debelleyme+Paris | 2026-10-08 |
| coord nova:Bontemps | 48.86387, 2.36063 | OK (3 m do nº 57) | https://photon.komoot.io/api/?q=57+Rue+de+Bretagne+Paris | 2026-10-08 |
| coord nova:Jacques Genin | 48.86447, 2.36462 | OK (0 m do nº 133) | https://photon.komoot.io/api/?q=133+Rue+de+Turenne+Paris | 2026-10-08 |
| coord nova:Musée de la Chasse | 48.86126, 2.35878 | OK (1 m do museu) | https://photon.komoot.io/api/?q=62+Rue+des+Archives+Paris | 2026-10-08 |
| coord nova:Fleux | 48.85874, 2.35417 | OK (5 m do nº 39) | https://photon.komoot.io/api/?q=39+Rue+Sainte-Croix+de+la+Bretonnerie+Paris | 2026-10-08 |
| coord nova:Sézane | 48.85940, 2.35571 | OK (7 m do nº 33) | https://photon.komoot.io/api/?q=33+Rue+des+Blancs-Manteaux+Paris | 2026-10-08 |
| coord nova:Muji | 48.85831, 2.35914 | OK (23 m do nº 47) | https://photon.komoot.io/api/?q=47+Rue+des+Francs+Bourgeois+Paris | 2026-10-08 |
| coord nova:French Trotters | 48.86167, 2.36418 | OK (5 m do nº 128) | https://photon.komoot.io/api/?q=128+Rue+Vieille+du+Temple+Paris | 2026-10-08 |
| coord nova:Empreintes | 48.86334, 2.36219 | OK (0 m do nº 5) | https://photon.komoot.io/api/?q=5+Rue+de+Picardie+Paris | 2026-10-08 |

## Pendências pra quem for usar em campo (não bloqueiam)

- **Une Glace à Paris**: dias de fechamento e preço seguem `[a confirmar]` — as fontes divergem. Ligar antes.
- **Jacques Genin**: o salão de chá pode não existir mais; o millefeuille é sob encomenda.
- **Hôtel de Rohan**: o aviso oficial de pátio fechado não tem data — conferir no portão.
- **Re-check pré-viagem (7-10 dias antes)**: os ⭐⭐ (Mariage Frères, MEP, Popelini, Bontemps, lojas da aba Lojas) não tiveram o operacional verificado afirmação a afirmação — só existência, endereço e coordenada.
