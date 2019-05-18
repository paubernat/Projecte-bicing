
import pandas as pd
from staticmap import StaticMap, CircleMarker, Line
import networkx as nx
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim


def create_graph(d):
    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')

    G = nx.Graph()
    for st in bicing.itertuples():
        G.add_node((st.lon,st.lat))

    for node in list(G.node(data=True)):
        for node2 in list(G.node(data=True)):
            distance = haversine(node[0],node2[0])
            if (distance <= d and distance != 0):
                if (not G.has_edge(node[0], node2[0])):
                    G.add_edge(node[0], node2[0], weight=distance)
    return G


def print_all(G):
    m = StaticMap(800, 800)
    for node in list(G.node(data=True)):
        print(node)
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

def addressesTOcoordinates(addresses):
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
        for node in list(G.node(data=True)):
            distance = haversine (node[0],coords1)
            if (distance!=0):
                G.add_edge(node[0], coords1, weight= distance*2.5)
    else:
        for node in list(G.node(data=True)):
            if (not G.has_edge(node, coords1)):
                distance = haversine (node[0],coords1)
                if (distance!=0):
                    G.add_edge (node[0], coords1, weight= distance*2.5)


    if (not G.has_node(coords2)):
        G.add_node(coords2)
        for node in list(G.node(data=True)):
            distance = haversine(node[0],coords2)
            if (distance!=0):
                G.add_edge(node[0], coords2, weight=distance*2.5)
    else:
        for node in list(G.node(data=True)):
            if (not G.has_edge(node, coords2)):
                distance = haversine(node[0],coords2)
                if (distance!= 0):
                    G.add_edge (node[0], coords2, weight=distance*2.5)


    path = nx.shortest_path(G, coords1, coords2, weight='weight')
    print(path)

    m = StaticMap(800, 800)

    print ("mida path =", len(path))
    print ("nodes:",path)

    for node in path:
        marker = CircleMarker((node[1],node[0]), 'red', 8)
        m.add_marker(marker)

    print ("ara punts:")
    for i in range (len(path)-1):
        coords = ((path[i][1],path[i][0]),(path[i+1][1],path[i+1][0]))
        line = Line(coords, 'green', 9)
        m.add_line(line)

    image = m.render()
    image.save('path.png')
