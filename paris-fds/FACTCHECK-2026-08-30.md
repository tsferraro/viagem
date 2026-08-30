# FACTCHECK · paris-fds · 2026-08-30

**Escopo**: reescrita da **aba `🐠` Trocadéro** (única aba tocada). Ela era um dia coberto de 2 paradas (Aquarium + Maison de Balzac) e virou um **dia de duas trilhas paralelas** com 6 paradas, a pedido do Tobia no próprio domingo 30/ago: a chuva prevista não veio, e o grupo passou de 3 para **5 pessoas (4 adultos + a filha de 3 anos)**, com a filha e um adulto no Aquário e os outros três no entorno. Nenhuma outra aba foi tocada.

**Nível de verificação**: **nível-página** — `WebFetch` funcionou nesta sessão (desktop) e abriu as páginas oficiais de Cité de l'architecture, Musée de la Marine, Café du Trocadéro, Amourette, paris.fr (cemitério e jardins), quai Branly, MAM e Guimet. Dois hosts recusaram: `museedelhomme.fr` (**HTTP 403**) e a página de tarifas da Cité (**HTTP 404**) — ambos registrados abaixo como RISCO, não como OK. Coordenadas vieram de **Nominatim/OpenStreetMap**, copiadas com 5 decimais, **nenhuma derivada**.

**Executor**: ⚠️ **a MESMA sessão que construiu a aba.** A regra do repo (CLAUDE.md §9c · `FACTCHECK-EXEC.md`) exige sub-agentes céticos em contexto limpo; a configuração desta sessão proíbe o Agent tool sem pedido explícito do Tobia. Registrado em vez de silenciado: **esta verificação é mais fraca que o padrão do repo e uma passada independente segue pendente.** O que reduziu o viés foi que a pesquisa veio ANTES da escrita — cada card foi escrito a partir da página aberta, não o contrário.

**Placar**: 26 itens verificados · **17 OK · 2 ERRO → corrigidos · 6 RISCO · 1 INCONCLUSIVO**

---

## Estrato 1 · Paradas novas da aba (as que a família vai andar hoje)

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| card:Cimetière de Passy | "2 rue du Commandant-Schloesing · **domingo 09h00-18h00**, de **16 de março a 5 de novembro**" | OK — é o horário que sustenta a trilha B de hoje | https://www.paris.fr/lieux/cimetiere-de-passy-4481 | 2026-08-30 |
| card:Cimetière de Passy | "**ninguém é admitido no último 1/4 de hora** → última entrada 17h45" | OK · achado operacional que não estava em nenhuma fonte secundária | https://www.paris.fr/lieux/cimetiere-de-passy-4481 | 2026-08-30 |
| card:Cimetière de Passy | "**2.600 túmulos** · **290 árvores de 15 essências**" | OK | https://www.paris.fr/lieux/cimetiere-de-passy-4481 | 2026-08-30 |
| card:Cimetière de Passy | "necrópole aristocrática a partir de **1874** · **Manet (1832-1883)**, **Berthe Morisot (1841-1895)**, **Debussy**, Fernandel, Maurice Genevoix" | OK · fonte editorial | https://www.parisladouce.com/2025/04/cimetiere-de-passy-paris-16.html | 2026-08-30 |
| card:Cimetière de Passy | "**grátis**" | **RISCO** — a página oficial do paris.fr **não menciona tarifa**. Sustentado só por fonte editorial. Marcado no próprio card como "gratuidade em fonte editorial" | https://parisjetaime.com/eng/culture/cimetiere-de-passy-p1750 | 2026-08-30 |
| card:Cimetière de Passy | "a prefeitura publica um **plano das sepulturas mais procuradas**" | OK · PDF oficial existe | https://cdn.paris.fr/paris/2022/06/15/7942a72808bfc7085973ff83fbeab723.pdf | 2026-08-30 |
| card:Jardins du Trocadéro | "**aberto 24/24 h** · place du Trocadéro-et-du-11-Novembre · **aire de jeux**, **pontos de água potável**, **mesas de ping-pong**, toaletes móveis, **WIFI na parte alta**, cães na coleira" | OK · tudo listado pela prefeitura | https://www.paris.fr/lieux/jardins-du-trocadero-1789 | 2026-08-30 |
| card:Jardins du Trocadéro | "**carrossel**, balanços e caixa de areia" | **RISCO** — a página oficial lista `Aire de jeux` mas **não** carrossel nem caixa de areia. Atribuído no card a "guias locais" | https://www.jds.fr/paris/parc-avec-aire-de-jeux/jardins-du-trocadero-22258_L | 2026-08-30 |
| card:Jardins du Trocadéro | "cerca de **94.000 m²** · **Fonte de Varsóvia** de **1937** com **20 canhões oblíquos** de alcance **50 metros**" | **RISCO** — só fonte editorial; a prefeitura não publica área nem descrição da fonte | https://www.evous.fr/paris/16eme-Arrondissement/Lieux-cles-Paris-16e/Les-jardins-du-Trocadero/ | 2026-08-30 |
| card:Cité de l'architecture (ALT) | "**11h-19h todos os dias exceto terça**, quinta até 21h · **1, Place du Trocadéro et du 11 Novembre**" | OK · **aberta hoje, domingo** | https://www.citedelarchitecture.fr/fr/informations-pratiques | 2026-08-30 |
| card:Cité de l'architecture (ALT) | "**€9** museu · **€12** museu+exposição · gratuidade para menores" | **RISCO** — a página oficial de tarifas devolveu **HTTP 404** na checagem. Fontes secundárias ainda se contradizem entre `<18` e `<12` para a gratuidade. Marcado `[a confirmar]` no card e no campo `custo` | https://parisjetaime.com/eng/culture/cite-de-l-architecture-du-patrimoine-p3506 | 2026-08-30 |
| card:Cité de l'architecture (ALT) | "**mais de 350 gessos**, alguns com **mais de 10 metros**" | OK · fonte editorial | https://parisjetaime.com/eng/culture/cite-de-l-architecture-du-patrimoine-p3506 | 2026-08-30 |

## Estrato 2 · Almoço (3 opções · todas conferidas contra DOMINGO)

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| opcao:Café du Trocadéro | "**8 Place du Trocadéro et du 11 Novembre** · **aberto todos os dias 07:00-02:00** · terraço vasto + sala · reserva online · **grupo de 15+ só por e-mail**" | OK · aberto hoje | https://cafedutrocadero.com/ | 2026-08-30 |
| opcao:Café du Trocadéro | preço | **INCONCLUSIVO** — a casa **não publica preços**. Registrado no card como aviso ("contem com caro"), não como número inventado | https://cafedutrocadero.com/ | 2026-08-30 |
| opcao:Amourette | "**10 Boulevard Delessert** · **Mon-Sun 11:30-02:00** · **200 lugares no terraço** · entradas **€12-28**, pratos **€24-45** · tel. **09 52 86 14 47**" | OK · aberto hoje | https://www.amourette-passy.fr/en/ | 2026-08-30 |
| opcao:Amourette | "€150-200 pra cinco" | **RISCO** — é **estimativa minha** a partir da carta, não preço publicado. Marcado no card como "(estimativa, não é preço de menu)" | https://www.amourette-passy.fr/en/ | 2026-08-30 |
| opcao:Amourette | coordenada do nº 10 bd Delessert | **RISCO** — o Nominatim devolve o POI **"Marcello"** nesse endereço, não "Amourette". Coord marcada `coord_unverified: true`; o endereço vem do site oficial da própria casa | https://nominatim.openstreetmap.org/ | 2026-08-30 |
| opcao:Breizh Café Passy | "4 impasse des Carrières · **domingo 11h30-22h30 sem fechar à tarde** · €25-45 · 3,8/5 em 388 avaliações · tel. 09 80 49 41 67" | OK · re-confirmado do factcheck de 27/ago | https://www.pagesjaunes.fr/pros/50030973 · https://www.breizhcafe.com/passy | 2026-08-30 |

## Estrato 3 · Erros pegos e corrigidos ANTES do deploy

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| Musée de la Marine · tarifa | ~~"€14 online / €15 na caixa"~~ (fonte secundária, citada numa busca) | **ERRO → corrigido** — a página oficial de tarifas **não menciona preço online diferente**. O roteiro usa **€15** e o card do cemitério explicita "€15 por adulto". Também confirmado que **não existe tarifa de idoso**: o reduzido de **€12** é só `familles nombreuses` e `anciens combattants` — o que muda a conta dos avós | https://www.musee-marine.fr/nos-musees/paris/visiter/informations-pratiques/acces-horaires-tarifs.html | 2026-08-30 |
| Panthéon Bouddhique (Guimet) | ~~"jardim japonês de 450 m², acesso inteiramente gratuito"~~ — circula assim em vários blogs de Paris e era candidato a parada | **ERRO → corrigido** — a **Maison Guimet (Hôtel d'Heidelbach, 19 av. d'Iéna) está fechada**; só visita guiada com reserva, de 11/out a 20/dez/2026. **A parada não foi criada** | https://www.guimet.fr/en/access-and-opening-hours | 2026-08-30 |

## Estrato 4 · Verificado e deliberadamente NÃO usado

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| Musée de la Marine · oferta família | "**sac du marin** · **3 a 5 anos** · **gratuito** · empréstimo na recepção contra documento de identidade, até acabar o estoque" | OK — é o argumento que sustenta a dica "guardem a Marine pro dia em que a filha for" | https://www.musee-marine.fr/nos-musees/paris/visiter/offre-culturelle/loffre-destinee-aux-familles/visiter-en-autonomie.html | 2026-08-30 |
| Musée de l'Homme | "11h-19h, fecha terça · €13" | **RISCO** — o site oficial devolveu **HTTP 403**; só busca agregada sustenta. **Não virou parada**, exatamente por isso | https://www.offi.fr/expositions-musees/musee-de-lhomme-2462.html | 2026-08-30 |
| Musée d'Art Moderne (MAM) | "ter-dom 10h-18h, fecha segunda · **coleção permanente gratuita, sem reserva** · 11 av. du Président Wilson" | OK · aberto hoje. Não virou parada: não achei fonte sobre o que funciona para 3 anos | https://www.mam.paris.fr/fr/informations-pratiques | 2026-08-30 |
| Musée du quai Branly · jardim | "o jardim abre 09h15-19h30 e abre **na segunda**, quando o museu fecha" | **RISCO** — o horário separado é indício de acesso livre, mas **nenhuma página oficial confirma entrada sem bilhete**. Não virou parada | https://www.quaibranly.fr/en/useful-information/come/schedules-rates-and-access | 2026-08-30 |
| Marché Président Wilson | "**quarta 7h-14h30 · sábado 7h-15h**" | OK — e é justamente por isso que **não entrou**: hoje é domingo, está fechado | https://www.paris.fr/lieux/marche-president-wilson-5510 | 2026-08-30 |
| Fondation Le Corbusier / Maison La Roche | "ter-sáb 10h-18h · €10/€5" | OK — **fecha aos domingos**, descartada da aba por isso | https://www.fondationlecorbusier.fr/visite/maison-la-roche-paris/ | 2026-08-30 |

## Estrato 5 · Coordenadas

| Item | Afirmação verificada | Veredito | Fonte(s) | Data |
|---|---|---|---|---|
| coords novas | Cimetière de Passy `48.86248, 2.28509` · Cité de l'architecture `48.86289, 2.28898` · Jardins du Trocadéro `48.86135, 2.28936` · Breizh Café `48.85846, 2.28134` | OK — **todas copiadas do Nominatim com 5 decimais, nenhuma derivada** (R7) | https://nominatim.openstreetmap.org/ | 2026-08-30 |
| coords aproximadas | Café du Trocadéro e Amourette usam o **nó de endereço**, não o POI da casa | **RISCO** — ambas marcadas `coord_unverified: true`; a navegação real vai pelo `mapsQuery`, que carrega o endereço completo | https://nominatim.openstreetmap.org/ | 2026-08-30 |

---

## O que este factcheck NÃO cobre

1. **Distâncias a pé entre as paradas novas não foram medidas.** O card Aquário→Balzac mantém o "~2 km" medido em campo em 27/ago; nenhuma outra distância foi aferida, e nenhuma foi afirmada em número.
2. **Acessibilidade em campo** — degraus na entrada do cemitério, desnível dos jardins e elevadores da Cité estão marcados `[a confirmar]` nos próprios cards.
3. **Executor não-independente** (ver cabeçalho). Uma passada de sub-agentes céticos sobre esta aba segue pendente.
