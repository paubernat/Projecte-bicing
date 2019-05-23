import pandas as pd
from staticmap import StaticMap, CircleMarker, Line
import networkx as nx
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim

#haversine (lat,lon)
#staticmap (lon,lat)
#ourgraph (lat,lon)

#creates the graph with n size as the maximum size of an edge.
def create_graph(d):
    #we using a data base from Barcelona's bicing stations
    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')

    G = nx.Graph()
    for st in bicing.itertuples():
        G.add_node((st.lat,st.lon))

    #we add all edges smaller than n.
    for node in list(G.node()):
        for node2 in list(G.node()):
            distance = haversine(node,node2)
            if (distance <= d and distance != 0):
                if (not G.has_edge(node, node2)):
                    G.add_edge(node, node2, weight=distance)
    return G

#prints the graph edges and nodes using StaticMap
def print_all(G):
    m = StaticMap(800, 800)
    for node in list(G.node()):
        marker = CircleMarker((node[1],node[0]), 'black', 5)
        m.add_marker(marker)

    for edge in list(G.edges()):
        coords = ((edge[0][1],edge[0][0]),(edge[1][1],edge[1][0]))
        line = Line(coords, 'purple', 1)
        m.add_line(line)
    return m

#transforms adresses to coordinates
def addressesTOcoordinates(addresses):
    try:
        geolocator = Nominatim(user_agent="bicing_bot")
        address1, address2 = addresses.split(',')
        location1 = geolocator.geocode(address1 + ', Barcelona')
        location2 = geolocator.geocode(address2 + ', Barcelona')
        return (location1.latitude, location1.longitude), (location2.latitude, location2.longitude)
    except:
        return None

def complete_known_edge (G, coords):
    for node in list(G.node()):
        if (not G.has_edge(node, coords)):
            distance = haversine (node,coords)
            if (distance!=0):
                G.add_edge (node, coords, weight= distance*2.5)

#matches a new node with every single node
def complete_new_edge (G,coords):
    G.add_node(coords)
    for node in list(G.node()):
        distance = haversine (node,coords)
        if (distance!=0):
            G.add_edge(node, coords, weight= distance*2.5)

#matches an existent node with every single node
def print_path_in_graph (G, path):

    m = StaticMap(800, 800)

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
    image.save('path_in_graph.png')

#prints the smallest path between 2 points
def print_path_solo (path):

    m = StaticMap(800,800)

    for node in path:
        marker = CircleMarker((node[1],node[0]), 'blue', 3)
        m.add_marker(marker)

    for i in range (len(path)-1):
        coords = ((path[i][1],path[i][0]),(path[i+1][1],path[i+1][0]))
        line = Line(coords, 'blue', 2)
        m.add_line(line)

    image = m.render()
    image.save('path_solo.png')

#prints the smallest distance in time between 2 points.
def shortest_path(G, adresses):
    #funcio que la direccio es un node conegut.(g.has_node("dirreccio"))
    coords = addressesTOcoordinates(adresses)
    if coords == None:
        return None
    coords1, coords2 = coords

    if (not G.has_node(coords1)):
        complete_new_edge(G,coords1)
    else:
        complete_known_edge(G,cords1)

    if (not G.has_node(coords2)):
        complete_new_edge(G,coords2)
    else:
        complete_known_edge(G,cords2)

    lenght, path = nx.bidirectional_dijkstra(G,coords1,coords2)

    G.remove_node(coords1)
    G.remove_node(coords2)

    print_path_in_graph (G,path)
    print_path_solo (path)


def number_of_non_connex_components (G):
    return str(nx.number_connected_components(G))

def number_of_nodes (G):
    return str(len(G))

def number_of_edges (G):
    return str(nx.number_of_edges(G))
