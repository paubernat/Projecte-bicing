import pandas as pd
from staticmap import StaticMap, CircleMarker, Line
import networkx as nx
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim
import itertools as it
from PIL import Image

#haversine (lat,lon)
#staticmap (lon,lat)
#ourgraph (lat,lon)

def Bounding_box(G):
    #Bounding Box
    L = list(G.node())
    max_lat, max_lon = L[0]
    min_lat, min_lon = L[0]
    for node in L:
        if node[1] < min_lon:
            min_lon = node[1]
        if node[1] > max_lon:
            max_lon = node[1]
        if node[0] < min_lat:
            min_lat = node[0]
        if node[0] > max_lat:
            max_lat = node[0]

    coords = ((min_lat, min_lon),(max_lat, min_lon),(max_lat, max_lon),(min_lat, max_lon))
    return coords

def cross (A,i,j,ii,jj,G,d):
    for node1 in A[i][j]:
        for node2 in A[ii][jj]:
            dist = haversine(node1,node2)
            if (dist <= d):
                G.add_edge(node1,node2,weight=dist)

def add_edge_quadrant (G,A,d,lat_rows, long_columns):
    for i in range (lat_rows):
        for j in range (long_columns):
            cross (A,i,j,i,j,G,d)
            if (i-1>0 and j+1<long_columns):
                cross (A,i-1,j+1,i,j,G,d)
            if (j+1<long_columns):
                cross (A,i,j+1,i,j,G,d)
            if (i+1<lat_rows and j+1<long_columns):
                cross (A,i+1,j+1,i,j,G,d)
            if (i+1<lat_rows):
                cross (A,i+1,j,i,j,G,d)

def edge_adder (G,d):
    coord = Bounding_box(G)
    lat_m, long_m = haversine (coord[0],coord[1]), haversine (coord[1],coord[2])
    lat_ang, long_ang = coord [1][0] - coord [0][0], coord [2][1]- coord [1][1]
    dist_ang = (d*lat_ang)/lat_m
    lat_rows, long_columns = int((lat_ang//dist_ang)+1), int((long_ang//dist_ang)+1)
    A = [[[] for i in range (long_columns)] for j in range (lat_rows)]
    for node in list(G.node()):
        lat,lon = int((node[0]-coord[0][0])//dist_ang),int((node[1]-coord[0][1])//dist_ang)
        A[lat][lon].append(node)

    add_edge_quadrant (G,A,d,lat_rows, long_columns)
    print ("edges", number_of_edges(G))


#creates the graph with n size as the maximum size of an edge.
def create_graph():
    #we using a data base from Barcelona's bicing stations
    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')
    G = nx.Graph()
    for st in bicing.itertuples():
        G.add_node((st.lat,st.lon),bikes= 0, docks=0)

    #we add all edges smaller than n.
    edge_adder(G,0.9)
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

    image = m.render()
    image.save('mapa.png')
    
#funcio per actualiztar la info de
def actualize_g (G):
    url_info = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    url_status = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_status'
    stations = DataFrame.from_records(pd.read_json(url_info)['data']['stations'], index='station_id')
    bikes = DataFrame.from_records(pd.read_json(url_status)['data']['stations'], index='station_id')

    stations = stations[['lat','lon']]
    bikes = bikes[['num_bikes_available', 'num_docks_available']] # We only select the interesting columns
    print(bikes)
    print(stations)
    #no passo d'aqui no entenc que collons haig de fer jaja

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

    #afegim els punts de origen i de arribada com a nodes.
    #per a evitar operacions innecessàries, la velocitat bici es va a 10km/h i caminant a 4km/h,
    #sabem que es trigarà 2,5 vegades més anant caminant, per tant, multipliquem la distancia de
    #trobar el shortest_path serà el mateix

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
    return nx.number_connected_components(G)

def number_of_nodes (G):
    return len(G)

def number_of_edges (G):
    return nx.number_of_edges(G)



G = create_graph()
actualize_g(G)
