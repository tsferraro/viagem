# FACTCHECK · paris-fds · 2026-08-27

**Escopo**: viagem nova completa (2 dias · 7 cards · 6 opções · 3 polos de `historia[]`)
**Nível de verificação**: **nível-snippet** — sessão cloud com rede externa filtrada. `WebFetch`/`curl` devolvem `403 Tunnel connection failed` para praticamente todos os hosts (inclusive `chateaudechantilly.fr`, `paris.fr`, Wikipedia e `sortiraparis.com`); **só `WebSearch` funciona**. Ou seja: as fontes abaixo foram lidas via **resultado de busca**, não abrindo a página. Snippet guarda título e trecho de páginas que já podem ter mudado.

**Executor**: ⚠️ **a MESMA sessão que construiu o roteiro.** A regra do repo (CLAUDE.md §9c · `FACTCHECK-EXEC.md`) exige sub-agentes céticos em contexto limpo, e a configuração desta sessão proíbe o uso do Agent tool. Registrado aqui em vez de silenciado: **esta verificação é mais fraca do que o padrão do repo**. O que reduziu (não eliminou) o viés foi atacar cada afirmação com busca nova de refutação, sem reler a justificativa do card. **Recomendação: rodar uma sessão auditora independente antes de sábado.**

**Placar**: 30 itens verificados · **25 OK · 4 ERRO → corrigidos · 1 RISCO**

---

## Estrato 1 · Restaurantes × dia da semana

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| opcao:Le Hameau | "aberto sáb 29/ago · 12h-18h · fecha só às terças" | OK | https://www.chantilly-senlis-tourisme.com/en/restaurants/aux-gouters-champetres/ | 2026-08-27 |
| opcao:Le Hameau | "no parque, no jardim anglo-chinês · crème Chantilly da casa · tel. 03 44 57 46 21" | OK | https://chateaudechantilly.fr/en/plan-your-visit/restaurants-and-shops/ | 2026-08-27 |
| opcao:La Capitainerie | "7 rue du Connétable · sob as abóbadas das cozinhas de Vatel" | OK | https://chateaudechantilly.fr/restaurant-la-capitainerie/ | 2026-08-27 |
| opcao:La Capitainerie | "3,5/5 no TripAdvisor · relatos de +20min de espera mesmo com reserva (2026)" | OK | https://www.tripadvisor.com/Restaurant_Review-g227607-d1330823-Reviews-La_Capitainerie-Chantilly_City_Chantilly_Oise_Hauts_de_France.html | 2026-08-27 |
| opcao:L'Étrier | "8 rue du Connétable · de frente para as Grandes Écuries · terraço" | OK | https://www.chantilly-senlis-tourisme.com/en/restaurants/letter-carrier/ | 2026-08-27 |
| opcao:Papilla | "58 av. du Général Leclerc · **abre aos domingos** · ~€25 médio" | OK | https://www.thefork.fr/restaurant/papilla-boulogne-r822367 · https://www.pagesjaunes.fr/pros/63182192 | 2026-08-27 |
| opcao:Bellota-Bellota | "existe em Boulogne-Billancourt · jamón ibérico · terraço" | OK | https://www.thefork.fr/restaurants/boulogne-billancourt-c62568/terrasse-t370 | 2026-08-27 |
| opcao:La Table du Connétable | "só jantar qui-sáb 19h-21h30 — NÃO serve almoço" (motivo de estar fora do roteiro) | OK | https://www.yonder.fr/les-tops/restaurants/meilleurs-restaurants-chantilly-france | 2026-08-27 |

## Estrato 2 · Cards ⭐⭐⭐ e ⭐⭐ · preço, horário, dia de fechamento

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| card:Grandes Écuries | ~~"abrem 10h e vão até 20h"~~ | **ERRO → corrigido** (Écuries fecham **18h** de abril a outubro; **20h é o parque**) | https://www.tourisme-en-hautsdefrance.com/offres/chateau-de-chantilly-chantilly-fr-3274893/ | 2026-08-27 |
| card:Château de Chantilly | ~~"as fontes divergem entre €18 e €21"~~ | **ERRO → corrigido** (tarifa **revista para 2026** = **€21 cheio / €17,50 reduzido 7-25**; €18 é a tabela antiga que vários sites ainda ecoam) | https://www.lasourisglobe-trotteuse.fr/chateau-chantilly/ | 2026-08-27 |
| card:Château de Chantilly | "château 10h-18h (abr-out) · parque 10h-20h · fechado às terças · sáb 29 e dom 30 abertos" | OK | https://www.tourisme-en-hautsdefrance.com/offres/chateau-de-chantilly-chantilly-fr-3274893/ · https://chateaudechantilly.fr/en/hours/ | 2026-08-27 |
| card:Château de Chantilly | "só parque €9 (€7 reduzido) · Cabinet des Livres +€3 · <7 anos grátis" | OK | https://www.lasourisglobe-trotteuse.fr/chateau-chantilly/ | 2026-08-27 |
| card:Château de Chantilly | "Grands Appartements e Sala de Leitura acessíveis; capela, galeria dos cervos, galeria de pinturas e logis só por escada · 2 cadeiras de rodas no Hall de Honra · tel. 03 44 27 31 80" | OK | https://chateaudechantilly.fr/en/visitors-with-disabilities/ | 2026-08-27 |
| card:Albert-Kahn | ~~"11h-19h abr-set"~~ (faltava a última entrada) | **corrigido** (acrescentado **última entrada 18h**) | https://otbb.org/en/musee-departemental-albert-kahn/ · https://www.bonjour-ratp.fr/lieux/musee-albert-kahn/ | 2026-08-27 |
| card:Albert-Kahn | "€9 cheio · €6 reduzido · grátis <26 anos · grátis 1º domingo do mês (30/ago NÃO é 1º domingo)" | OK | https://otbb.org/en/musee-departemental-albert-kahn/ | 2026-08-27 |
| card:Albert-Kahn | "aberto domingo 30/ago · fechamentos excepcionais só 1/jan, 1/mai, 25/dez" | OK · nenhuma fonte anuncia fechamento em ago/2026 | https://www.offi.fr/expositions-musees/musee-albert-kahn-1382.html | 2026-08-27 |
| card:Serres d'Auteuil | "estufas fecham antes do jardim · fim de semana" | **RISCO** — fontes divergem entre **16h45 · 17h · 17h30**. Mitigado no card: chegar até 16h · tel. **01 40 72 16 16** | https://www.paris.fr/lieux/jardin-des-serres-d-auteuil-1780 · https://www.offi.fr/a-travers-paris/serres-dauteuil-3182.html | 2026-08-27 |
| card:Serres d'Auteuil | "jardim 9h-20h30 de 1/mai a 31/ago · entrada grátis sempre" | OK | https://www.paris.fr/lieux/jardin-des-serres-d-auteuil-1780 | 2026-08-27 |
| card:Jardin d'Acclimatation | ~~"10h-18h/19h aos fins de semana"~~ | **ERRO → corrigido** (em **agosto de 2026 abre 10h-19h todos os dias**) | https://www.jardindacclimatation.fr/horaires-ouverture-du-jardin | 2026-08-27 |
| card:Jardin d'Acclimatation | "€7 entrada · €5 sênior 60+ · grátis <80cm · atrações à parte €4,50 / passe €46 / combo €19-48" | OK | https://www.jardindacclimatation.fr/preparez-votre-visite | 2026-08-27 |
| card:Jardin d'Acclimatation | "sem estacionamento próprio · ~20min a pé da Porte Maillot · Bois grátis aos domingos" | OK | https://www.jardindacclimatation.fr/preparez-votre-visite | 2026-08-27 |
| card:Aquarium de Paris | ~~"10h-19h, última entrada 18h"~~ | **ERRO → corrigido** (**9h30-19h**, caixas fecham antes das 18h) | https://aquariumdeparis.com/acces-horaire-restauration/ | 2026-08-27 |
| card:Aquarium de Paris | "€27,50 adulto 13+ · €20,50 criança 3-12 (= €130,50 para 4 adultos + 1 criança)" | OK | https://aquariumdeparis.com/tarifs/ | 2026-08-27 |
| card:Aquarium de Paris | "maior tanque de tubarões da França · 3 milhões de litros · ~40 tubarões de 6 espécies · maior Medusarium da Europa" | OK | https://www.anigaido.com/lieux/aquariums-2/aquarium-de-paris | 2026-08-27 |
| card:Aquarium de Paris | "visita real de 1h-1h30 · avaliações mitigadas: caro para o tamanho · sereia dura 5min" | OK (crítica registrada de propósito) | https://allovoyages.fr/destinations/aquarium-de-paris-avis/ | 2026-08-27 |

## Estrato 3 · Existência, função, posição e coordenadas

Sem walking tours e sem paradas de road trip neste roteiro (decisão de desenho: os avós andam ≤1km, e criar rota a pé seria criar a parada que eles não conseguem fazer). Restam as coordenadas dos cards — **todas copiadas de fonte, nenhuma derivada** (R7).

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| coord:Grandes Écuries | 49.19372 / 2.47901 — de 49°11'37.39"N 2°28'44.44"E · end. 7-9 rue du Connétable | OK · copiada | https://www.wikidata.org/wiki/Q97366464 | 2026-08-27 |
| coord:Château de Chantilly | 49.1938 / 2.4852 | OK · copiada | https://en.wikipedia.org/wiki/Ch%C3%A2teau_de_Chantilly | 2026-08-27 |
| coord:Hameau (parc) | 49.1946 / 2.4937 — de 49°11'40.4"N 2°29'37.4"E | OK · copiada | https://en.wikipedia.org/wiki/Hameau_de_Chantilly · https://www.wikidata.org/wiki/Q3126395 | 2026-08-27 |
| coord:Albert-Kahn | 48.8417 / 2.2278 — de 48°50'30"N 2°13'40"E · end. 10-14 rue du Port | OK · copiada | https://en.wikipedia.org/wiki/Mus%C3%A9e_Albert-Kahn | 2026-08-27 |
| coord:Serres d'Auteuil | 48.8479 / 2.2547 · end. 3 av. de la Porte d'Auteuil | OK · copiada | https://en.wikipedia.org/wiki/Jardin_des_Serres_d'Auteuil | 2026-08-27 |
| coord:Jardin d'Acclimatation | 48.8776 / 2.2699 — de 48.877571 / 2.269944 | OK · copiada | https://en.wikipedia.org/wiki/Jardin_d%27Acclimatation | 2026-08-27 |
| coord:Aquarium de Paris | 48.86222 / 2.29099 · end. 5 av. Albert de Mun | OK · copiada | https://www.google.com/maps/place/Aquarium+de+Paris/@48.8622162,2.2909927,15z/data=!4m5!3m4!1s0x0:0xf88aec5c3eb444e8!8m2!3d48.8622162!4d2.2909927 | 2026-08-27 |
| coord:base Boulogne | 48.8337 / 2.2435 (Marcel Sembat, linha 9) | OK · copiada | https://en.wikipedia.org/wiki/Marcel_Sembat_station | 2026-08-27 |

> **Coordenadas de restaurante**: os 6 itens de `opcoes` ficaram **sem `coord`** de propósito. Tenho o endereço de todos, mas não achei coordenada publicada de nenhum — e derivar coordenada de endereço é justamente o que a R7 proíbe. Consequência assumida: eles **não viram pino** na aba "Tudo no Mapa" (o `validate.py` avisa). O link "Abrir no Maps" de cada um funciona normalmente, via `mapsQuery`.

## Estrato 4 · `historia[]` · afirmações mais específicas

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| historia:Chantilly | "Vatel era intendente (não chef) · suicídio em abril de 1671, festa de 3 dias para Luís XIV, peixe que não chegou" | OK | https://www.uliege.be/cms/c_10297893/fr/les-grands-mythes-de-la-gastronomie-vatel-et-l-invention-de-la-creme-chantilly | 2026-08-27 |
| historia:Chantilly | "primeira receita de creme batido publicada na Inglaterra por volta de 1545 · nome 'Chantilly' aparece em 1784 com a baronesa Marie Féodorovna · Pierre Lacam cria a atribuição a Vatel em 1893" | OK · 2 fontes independentes | https://www.uliege.be/cms/c_10297893/... · https://chateaudechantilly.fr/en/who-is-the-inventor-of-the-creme-chantilly/ | 2026-08-27 |
| historia:Chantilly | "Grandes Écuries 1719-1735 · Jean Aubert · Louis-Henri de Bourbon, 7º príncipe de Condé · 240 cavalos e 500 cães · cúpula de 28m · naves de 70m" | OK | https://chateaudechantilly.fr/grandes-ecuries/histoire-des-grandes-ecuries/ | 2026-08-27 |
| historia:Chantilly | "maiores cavalariças da Europa" (superlativo) | OK | https://www.sncf-connect.com/article/les-ecuries-de-chantilly-les-plus-grandes-ecuries-du-monde-67871 | 2026-08-27 |
| historia:Chantilly | "Hameau de 1774 · Jean-François Leroy · Louis Joseph de Condé · inspirou o Hameau de la Reine de Marie-Antoinette" | OK | https://en.wikipedia.org/wiki/Hameau_de_Chantilly | 2026-08-27 |
| historia:Chantilly | "jogo da oca gigante do séc. XVIII em 3,5 ha · kangourou albina Ice nascida em 2013 · labirinto-horta · aire de jeux" | OK | https://parismomes.fr/se-balader-en-famille/le-parc-du-chateau-de-chantilly/ | 2026-08-27 |
| historia:Albert-Kahn | "Albert Kahn 1860-1940 · Archives de la Planète iniciadas em 1909 · operadores em +50 países entre 1909 e 1931 · +72.000 autochromes · 170 km de filme · arruinado pela crise de 1929" | OK · 2 fontes independentes | https://phototrend.fr/2022/04/musee-albert-kahn-archives-de-la-planete/ · https://publicdomainreview.org/essay/albert-kahns-archives-of-the-planet/ | 2026-08-27 |
| historia:Albert-Kahn | "museu reaberto com edifício de 2.300 m² de Kengo Kuma · auditório com estrutura de madeira dele" | OK | https://www.club-innovation-culture.fr/nouveau-musee-albert-kahn-regard-humain-innovant-monde-voyage/ | 2026-08-27 |
| historia:Bois de Boulogne | "Serres d'Auteuil: jardim botânico desde 1761 sob Luís XV · estufas de Jean-Camille Formigé 1895-1898 · ~5.000 espécies · palmarium" | OK | https://parisjetaime.com/eng/culture/jardin-des-serres-d-auteuil-jardin-botanique-de-paris-p938 | 2026-08-27 |
| historia:Bois de Boulogne | "Jardin d'Acclimatation aberto em 6/out/1860 · 19 ha · hoje da LVMH · Guignol desde 1953" | OK | https://en.wikipedia.org/wiki/Jardin_d%27Acclimatation · https://www.visitparisregion.com/fr/jardin-d-acclimatation | 2026-08-27 |

## Estrato 5 · Logística (o que decide o fim de semana)

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| logística:Rock en Seine | "26 a 30/ago/2026 · Domaine national de Saint-Cloud · +80 shows · +100.000 festivaleiros" | OK | https://www.offi.fr/concerts/festival/rock-en-seine-8624.html | 2026-08-27 |
| logística:Rock en Seine | "Grille du Mail (Sèvres): veículo **e pedestre** fechados 11h→7h30 de qua 26 a sáb 29 · **9h30→7h30 no dom 30**" | OK · confirmado literalmente | https://www.saintcloud.fr/actualite/rock-en-seine-restrictions-de-circulation | 2026-08-27 |
| logística:Rock en Seine | "Avenue/Grille d'Honneur e Grille des Communs: veículo fechado 11h→2h de 26 a 30 · pedestre e bicicleta passam · horários podem mudar por decisão do Prefeito dos Hauts-de-Seine" | OK | https://www.saintcloud.fr/actualite/rock-en-seine-restrictions-de-circulation | 2026-08-27 |
| logística:Rock en Seine | "organizadores não previram estacionamento de carro · acesso oficial por metrô linha 10 (Boulogne–Pont de Saint-Cloud) e tram T2" | OK | https://blog.indigoneo.fr/ou-se-garer-festival-rock-en-seine/ | 2026-08-27 |
| logística:estrada | "Boulogne-Billancourt → Chantilly ~56 km · ~53-55min · Autoroute du Nord (A1) + périphérique/A86 · rota inteira ao norte" | OK | https://www.l-itineraire.com/de_chantilly_a_boulogne-billancourt · https://www.viamichelin.com/routes/results/chantilly-60500-oise-hauts_de_france-france-to-boulogne_billancourt-92100-hauts_de_seine-ile_de_france-france | 2026-08-27 |
| logística:clima | "sáb 29: rajadas frequentes de 50-60 km/h da Bretanha e Vale do Loire à Bélgica · dom 30: pancadas fortes sobre a Île-de-France, rajadas ~50 km/h · 20-24°C entre as pancadas" | OK · previsão, não fato — **reconferir na sexta à noite** | https://www.meteo-paris.com/actualites/nouvelle-offensive-automnale-apres-les-violents-orages-de-jeudi · https://www.sortiraparis.com/en/news/in-paris/articles/332748-weather-in-paris-and-ile-de-france-forecast-for-august-24-30-rain-and-thunderstorms-on-the-agenda | 2026-08-27 |
| logística:calendário | "as férias de verão francesas só terminam em 1º/set/2026 (rentrée terça 1/set) — 29-30/ago ainda é alta temporada" | OK | https://www.vacances-scolaires-education.fr/vacances-scolaires-2025-2026.html | 2026-08-27 |
| logística:Chantilly | "espetáculo equestre de verão *Un jour à Paris* rodou 11/jul→16/ago/2026 às 14h30 — **NÃO há espetáculo em 29-30/ago**" | OK · é a armadilha nº4 do levantamento | https://www.jds.fr/paris/spectacles/spectacle-equestre-un-jour-a-paris-aux-grandes-ecuries-de-chantilly-1426813_A | 2026-08-27 |
| logística:Chantilly | "preços de voiturette / barca / rosalie / petit train" | **INCONCLUSIVO** — nenhuma fonte publica valor. Marcado **`[a confirmar]`** no card e na estimativa de orçamento. Perguntar na bilheteria · tel. 03 44 27 31 80 | — | 2026-08-27 |

---

## O que este factcheck NÃO garante

1. **Não é independente.** Mesma sessão que escreveu (ver cabeçalho). O achado mais provável de uma auditoria externa é justamente um card que eu li com os olhos de quem o escreveu.
2. **É nível-snippet.** Nenhuma página oficial foi aberta e lida — a rede da sessão bloqueia. Três URLs "confirmadas por busca" já foram 404 na história deste repo (2026-08-03).
3. **Preços das atividades do parque de Chantilly seguem em aberto** (`[a confirmar]`), e é o único buraco assumido do orçamento.
4. **Clima é previsão**, não fato. Feita em 27/ago para 29-30/ago. Reconferir na sexta à noite.
5. **Horário das estufas de Auteuil está em RISCO** (16h45 / 17h / 17h30 conforme a fonte). Mitigação embarcada no card: chegar até 16h.

## Próximas verificações agendadas

- **Auditoria externa independente** — antes de sábado 29/ago, sessão nova, protocolo adversarial. É o passo que esta sessão não conseguiu executar.
- **Re-check pré-viagem (R11)** — não se aplica: a viagem é em 2 dias, e este factcheck já é o re-check operacional.
