
import pandas as pd
from staticmap import StaticMap, CircleMarker, Line
import networkx as nx
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim


def create_graph():
    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')

    G = nx.Graph()
    for st in bicing.itertuples():
        G.add_node((st.lon,st.lat))

    for node in list(G.node(data=True)):
        for node2 in list(G.node(data=True)):
            distance = haversine(node[0],node2[0])
            if (distance <= 0.800 and distance != 0):
                if (not G.has_edge(node[0], node2[0])):
                    G.add_edge(node[0], node2[0], distance=distance)
    return G


def print_all(G):
    m = StaticMap(800, 800)
    for node in list(G.node(data=True)):
        marker = CircleMarker((node[0]), 'black', 5)
        m.add_marker(marker)

    for edge in list(G.edges()):
        '''
        coords = (edge[0][0],edge[0][1],edge[1][0],edge[1][1])
        '''
        coords = (edge[0], edge[1])
        line = Line(coords, 'purple', 1)
        m.add_line(line)

    print(G.number_of_edges(), G.number_of_nodes())
    image = m.render()
    image.save('mapa.png')


'''

def addressesTOcoordinates(addresses):

    Returns the two coordinates of two addresses of Barcelona
    in a single string separated by a comma. In case of failure, returns None.

    Examples:

    >>> addressesTOcoordinates('Jordi Girona, Plaça de Sant Jaume')
    ((41.3875495, 2.113918), (41.38264975, 2.17699121912479))
    >>> addressesTOcoordinates('Passeig de Gràcia 92, La Rambla 51')
    ((41.3952564, 2.1615724), (41.38082045, 2.17357087674997))
    >>> addressesTOcoordinates('Avinguda de Jordi Cortadella, Carrer de Jordi Petit')
    None
    >>> addressesTOcoordinates('foo')
    None
    >>> addressesTOcoordinates('foo, bar, lol')
    None

    try:
        geolocator = Nominatim(user_agent="bicing_bot")
        address1, address2 = addresses.split(',')
        location1 = geolocator.geocode(address1 + ', Barcelona')
        location2 = geolocator.geocode(address2 + ', Barcelona')
        return (location1.latitude, location1.longitude), (location2.latitude, location2.longitude)
    except:
        return None

'''

def shortest_path(G, adresses):
    #funcio que la direccio es un node conegut.(g.has_node("dirreccio"))

    coords = addressesTOcoordinates(adresses)
    # aqui un error estaria gucci
    print (origen_adress, desti_adress)
    print (coords)
    #bucle
    coord_origen, coord_desti = coords
    print (coord_origen[0])


    for node in list(G.node(data=True)):
        print (node)

    if G.has_node (coord_origen, lat=coord_origen[0], lon=coord_origen[1]):
        print ("tamo gucci")
    else:
        print ("nword")

    for node in list(G.node(data=True)):


    coord_origen, coord_desti = coords
    print (coord_origen, coord_desti)

    if not g.has_node(origen_adress, lat=coords_origen[0], lan=coords_desti[1]):
        g.add_node (origen_adress, lat=coords_origen[0], lan=coords_desti[1])
        for node in list(G.node(data=True)):
            add_edge (haversine (node,))


    for (node in list(G.node(data=true))):
        add_edge ()
    add_node("end", lat1, lon2)
    #malament

    for (node in list(G.node(data=true))):
        distance = haversine((node[1]['lon'], node[1]['lat']), (node2[1]['lon'], node2[1]['lat']))
        if (distance <= 0.600 and !=0)

'''
G = create_graph()
print_all(G)

'''
shortest_path(create_graph(),"BRUC 45, Passeig de Gràcia 24")
'''
