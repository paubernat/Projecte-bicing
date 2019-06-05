# Projecte Bicing-Bot

## Introducció

Bicing-Bot es un projecte que sintetitza els coneixements de grafs i sobretot les capacitats de programació i us de llibreries externes.
Aquest projecte es basa en la creació d'un Graph amb les estacions de Bicing de Barcelona i retorna diverses utilitats mitjançant l'us de funcions de teoria de grafs en una amigable interfície com ho és un bot de telgram
El projecte utilitza el llenguatge de programació python i està compost per dues parts principals: l'arxiu de les dades data.py i l'arxiu del bot de telgram bot.py.

Un dels aspectes més importants del treball és l'implementació del bot de telgram, una interfície molt còmode i portàtil per a poder interactuar amb les funcions del data.py.

D'altra banda, val la pena destacar algunes funcions en especial:

- **/distribute 'a' 'b':** dona la distància necessària per a tenir "a" bicis i "b" molls a totes les parades de barcelona.

- **/path 'carrer_a' 'carrer_b':** retorna el camí més curt entre dues direccions de barcelona.  

- **/plotgraph:** pinta el graf creat.


## Estructura 

El projecte, com ja s'ha explicat anteriorment, està estructurat en dos grans blocs: l'arxiu **data.py** i l'arxiu **bot.py**.

El primer arxiu conté una sèrie de funcions com la creació d'un graph amb les estacions de bicing de barcelona, el camí més curt entre dues parades de bicing o quants kilometres caldria recorrer per a distribuir un mínim de x bicis o y molls. Aquestes funcions seran explicades posteriorment i probades en un joc de proves.

La segona part del projecte és el codi per a l'execució d'un bot de telgram Aquest bot respon a certes comandes usant les funcions del data.py.

Aquesta separació entre data i bot permet que les funcions siguin reutilitzables en el cas de que faci falta crear un bot per una altra aplicació o implementar alguna de les funcions en algun altre programa. 
Per últim, totes les funcions s'executen en temps **O(|V|+|E|) log(|V|)**.

D'altra banda, l'arxiu "requeriments.txt" conté instruccions per a la instalació de les llibreries que permeten l'execució dels programes. Tot i això, només tenint un telèfon amb l'aplicació tèlegram esdevè fàcil xatejar amb el bot: només fa falta que busqueu @botbicingbot a Telgram i proveu les comandes que s'expliquen a continuacio.

## Funcions

Les funcions creades en el data.py són les següents:

- **Create_graph(d):** Crea un graf on els nodes són les estacions de Bicing Barcelona i on es crea una aresta entre cada dues estacions separades per menys de la distància d.

- **Print_all(G):** Dibuixa el graf creat amb tots els nodes i arestes.

- **Shortest_path(G,"direccio 1", "direccio 2"):** Troba el camí més curt entre dos punts de Barcelona, tenint en compte que es més ràpid usar una bici que anar caminant.

- **Number_of_non_connex_comonents(G):** Retorna el nombre de components no connexes del graf.

- **Number_of_nodes(G):** Retorna el nombre de estacions de bicing de Barcelona.

- **Number_of_edges(G):** Retorna el nombre de arestes del graf creat.

- **Distribute(G,x,y):** Retorna el nombre de km que s'haurien de realitzar per a poder tenir com a mínim x bicicletes i y espais en totes les estacions.

## Comandes del bot

El bot respon a les comandes següents:

- **/start:** inicia el programa.

- **/graph x:** crea un graf usant la funció Create_graph(x). Cal mencionar que les funcions a continuació que usen un graf G usen aquest graf.

- **/plotgraph:** usa la comanda Print_all(G) per a crear una imatge del graf i la envia.

- **/path "direccio 1" "direccio 2":** usa la comanda Shortest_path(G,"direccio 1", "direccio 2") per a crear i enviar dues imatges, una només amb el camí entre les dues direccions i l'altre amb el graf de Barcelona inclòs.

- **/components: envia un missatge amb el resultat de Number_of_non_connex_comonents(G)

- **/nodes:**envia un misstge amb el resultat de Number_of_nodes(G)

- **/edges:**envia un missatge amb el resultat de Number_of_edges(G)

- **/distribute x y:** usa la comanda distribute(G,x,y) i envia un missatge amb l'aresta amb de cost màxim i el cost total.

- **/authors:** envia un missatge amb el nom dels autors.

- **/help:** envia un missatge amb informació d'ajuda per a l'us de les funcions.

## Joc de proves:

## Autors:

Els autors d'aquest projecte som Andrea García Valdés i Pau Bernat Rodríguez, alumnes del 1er curs del GCED cursants de l'assignatura algorisimia i programació II.

