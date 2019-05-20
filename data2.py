import pandas as pd
from staticmap import StaticMap, CircleMarker, Line
import networkx as nx
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim

#haversine (lat,lon)
#staticmap (lon,lat)
#ourgraph (lat,lon)

def create_graph():
    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')

    G = nx.Graph()
    for st in bicing.itertuples():
        G.add_node((st.lat,st.lon))

    for node in list(G.node()):
        for node2 in list(G.node()):
            distance = haversine(node,node2)
            if (distance <= 0.500 and distance != 0):
                if (not G.has_edge(node, node2)):
                    G.add_edge(node, node2, weight=distance)
    return G


def print_all(G):
    m = StaticMap(800, 800)
    for node in list(G.node()):
        marker = CircleMarker((node[1],node[0]), 'black', 5)
        m.add_marker(marker)

    for edge in list(G.edges()):

        coords = ((edge[0][1],edge[0][0]),(edge[1][1],edge[1][0]))
        line = Line(coords, 'purple', 1)
        m.add_line(line)

    print(G.number_of_edges(), G.number_of_nodes())
    image = m.render()
    image.save('mapa.png')

def addressesTOcoordinates(addresses):
    '''
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
    '''
    try:
        geolocator = Nominatim(user_agent="bicing_bot")
        address1, address2 = addresses.split(',')
        location1 = geolocator.geocode(address1 + ', Barcelona')
        location2 = geolocator.geocode(address2 + ', Barcelona')
        return (location1.latitude, location1.longitude), (location2.latitude, location2.longitude)
    except:
        return None


def shortest_path(G, adresses):
    #funcio que la direccio es un node conegut.(g.has_node("dirreccio"))

    coords = addressesTOcoordinates(adresses)
    if coords == None:
        return None

    coords1, coords2 = coords

    if (not G.has_node(coords1)):
        G.add_node(coords1)
        for node in list(G.node()):
            distance = haversine (node,coords1)
            if (distance!=0):
                G.add_edge(node, coords1, weight= distance*2.5)
    else:
        for node in list(G.node()):
            if (not G.has_edge(node, coords1)):
                distance = haversine (node,coords1)
                if (distance!=0):
                    G.add_edge (node, coords1, weight= distance*2.5)


    if (not G.has_node(coords2)):
        G.add_node(coords2)
        for node in list(G.node()):
            distance = haversine (node,coords2)
            if (distance!=0):
                G.add_edge(node, coords2, weight= distance*2.5)
    else:
        for node in list(G.node()):
            if (not G.has_edge(node, coords2)):
                distance = haversine (node,coords2)
                if (distance!=0):
                    G.add_edge (node, coords2, weight= distance*2.5)

    for node in list(G.node()):
        print (node)


    for edge in list (G.edges()):
        print (edge)

    lenght, path = nx.bidirectional_dijkstra(G,coords1,coords2)
    print (path)
    print (lenght)

    m = StaticMap(800, 800)

    G.remove_node(coords1)
    G.remove_node(coords2)

    for node in list(G.node()):

        marker = CircleMarker((node[1],node[0]), 'black', 5)
        m.add_marker(marker)

    for edge in list(G.edges()):

        coords = ((edge[0][1],edge[0][0]),(edge[1][1],edge[1][0]))
        line = Line(coords, 'grey', 1)
        m.add_line(line)


    for node in path:

        marker = CircleMarker((node[1],node[0]), 'blue', 3)
        m.add_marker(marker)

    for i in range (len(path)-1):
        coords = ((path[i][1],path[i][0]),(path[i+1][1],path[i+1][0]))
        line = Line(coords, 'blue', 2)
        m.add_line(line)

    image = m.render()
    image.save('path.png')







G = create_graph()
shortest_path(G, "Gran via corts catalanes 760, La Rambla 51" )
