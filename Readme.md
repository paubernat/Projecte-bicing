Projecte Bicing-Bot
'''
Introducci�
'''
Bicing-Bot es un projecte que sintetitza els coneixements de grafs i sobretot les capacitats de programaci� i us de llibreries externes.
Aquest projecte es basa en la creaci� d'un Graph amb les estacions de Bicing de Barcelona i retorna diverses utilitats mitjan�ant l'us de funcions de teoria de grafs en una amigable interf�cie com ho �s un bot de telgram
El projecte utilitza el llenguatge de programaci� python i est� compost per dues parts principals: l'arxiu de les dades data.py i l'arxiu del bot de telgram bot.py.
Un dels aspectes m�s importants del treball �s l'implementaci� del bot de telgram, una interf�cie molt c�mode i port�til per a poder interactuar amb les funcions del data.py.
D'altra banda, val la pena destacar algunes funcions en especial:
->/distribute "a" "b": dona la dist�ncia necess�ria per a tenir "a" bicis i "b" molls a totes les parades de barcelona.
->/path "carrera" "carrer": retorna el cam� m�s curt entre dues direccions de barcelona.  
->/plotgraph: pinta el graf creat.
'''
Estructura 
'''
El projecte, com ja s'ha explicat anteriorment, est� estructurat en dos grans blocs: l'arxiu data.py i l'arxiu bot.py.
El primer arxiu cont� una s�rie de funcions com la creaci� d'un graph amb les estacions de bicing de barcelona, el cam� m�s curt entre dues parades de bicing o
quants kilometres caldria recorrer per a distribuir un m�nim de x bicis o y molls. Aquestes funcions seran explicades posteriorment i probades en un joc de proves.
La segona part del projecte �s el codi per a l'execuci� d'un bot de telgram. Aquest bot respon a certes comandes usant les funcions del data.py.
Aquesta separaci� entre data i bot permet que les funcions siguin reutilitzables en el cas de que faci falta crear un bot per una altra aplicaci� o 
implementar alguna de les funcions en algun altre programa. 
Per �ltim, totes les funcions s'executen en temps O(|V|+|E|)log(|V|).
D'altra banda, l'arxiu "requeriments.txt" cont� instruccions per a la instalaci� de les llibreries que permeten l'execuci� dels programes.
Tot i aix�, nom�s tenint un tel�fon amb l'aplicaci� t�legram esdev� f�cil xatejar amb el bot: nom�s fa falta que busqueu @botbicingbot i proveu les comandes que s'expliquen a continuacio.
'''
Funcions
'''
Les funcions creades en el data.py s�n les seg�ents:
->Create_graph(d): Crea un graf on els nodes s�n les estacions de Bicing Barcelona i on es crea una aresta entre cada dues estacions separades per menys de la dist�ncia d.
->Print_all(G): Dibuixa el graf creat amb tots els nodes i arestes.
->Shortest_path(G,"direccio 1", "direccio 2"): Troba el cam� m�s curt entre dos punts de Barcelona, tenint en compte que es m�s r�pid usar una bici que anar caminant.
->Number_of_non_connex_comonents(G): Retorna el nombre de components no connexes del graf.
->Number_of_nodes(G): Retorna el nombre de estacions de bicing de Barcelona
->Number_of_edges(G): Retorna el nombre de arestes del graf creat.
->Distribute(G,x,y): Retorna el nombre de km que s'haurien de realitzar per a poder tenir com a m�nim x bicicletes i y espais en totes les estacions.
'''
Comandes del bot
'''
El bot respon a les comandes seg�ents:
->/start: inicia el programa.
->/graph x: crea un graf usant la funci� Create_graph(x). Cal mencionar que les funcions a continuaci� que usen un graf G usen aquest graf.
->/plotgraph: usa la comanda Print_all(G) per a crear una imatge del graf i la envia.
->/path "direccio 1" "direccio 2": usa la comanda Shortest_path(G,"direccio 1", "direccio 2") per a crear i enviar dues imatges, una nom�s amb el cam� entre les dues direccions i l'altre amb el graf de Barcelona incl�s.
->/components: envia un missatge amb el resultat de Number_of_non_connex_comonents(G)
->/nodes:envia un misstge amb el resultat de Number_of_nodes(G)
->/edges:envia un missatge amb el resultat de Number_of_edges(G)
->/distribute x y: usa la comanda distribute(G,x,y) i envia un missatge amb l'aresta amb de cost m�xim i el cost total.
->/authors: envia un missatge amb el nom dels autors.
->/help: envia un missatge amb informaci� d'ajuda per a l'us de les funcions.
'''
Joc de proves:
'''
Autors:
Els autors d'aquest projecte som Andrea Garc�a Vald�s i Pau Bernat Rodr�guez, alumnes del 1er curs del GCED cursants de l'assignatura algorisimia i programaci� II.

