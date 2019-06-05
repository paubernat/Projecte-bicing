import pandas as pd
from staticmap import StaticMap, CircleMarker, Line
import networkx as nx
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim
import itertools as it
from PIL import Image

# ----------CREATE THE GRAPH IN LINEAR TIME----------##

# create the bounding box of all the bicing stations coordinates
# The function returns the vertices coordinates


def Bounding_box(G):
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

    coords = ((min_lat, min_lon), (max_lat, min_lon),(max_lat, max_lon),  (min_lat, max_lon))
    return coords


def cross(A, i, j, ii, jj, G, d):
    # create the edges between nodes with the correct distance
    for node1 in A[i][j]:
        for node2 in A[ii][jj]:
            if node1 != node2:
                dist = haversine(node1, node2)
                if (dist <= d):
                    G.add_edge(node1, node2, weight=dist)


def add_edge_quadrant(G, A, d, lat_rows, long_columns):
    # look at the necessary quadrants to know the edges that must be added
    for i in range(lat_rows):
        for j in range(long_columns):
            cross(A, i, j, i, j, G, d)
            if (i-1 > 0 and j+1 < long_columns):
                cross(A, i-1, j+1, i, j, G, d)
            if (j+1 < long_columns):
                cross(A, i, j+1, i, j, G, d)
            if (i+1 < lat_rows and j+1 < long_columns):
                cross(A, i+1, j+1, i, j, G, d)
            if (i+1 < lat_rows):
                cross(A, i+1, j, i, j, G, d)


def edge_adder(G, d):
    # create a matrix using the boundingbox and divide it into quadrants
    # according to the established distance, then reverse the nodes in
    # the quadrants according to their coordinates
    coord = Bounding_box(G)
    lat_m, long_m = haversine(coord[0], coord[1]), haversine(coord[1], coord[2])
    lat_ang, long_ang = coord[1][0] - coord[0][0], coord[2][1] - coord[1][1]
    dist_ang = (d*lat_ang) / lat_m
    lat_rows, long_columns = int((lat_ang//dist_ang)+1), int((long_ang//dist_ang)+1)
    A = [[[] for i in range(long_columns)] for j in range(lat_rows)]
    for node in list(G.node()):
        lat = int((node[0] - coord[0][0]) // dist_ang)
        lon = int((node[1] - coord[0][1]) // dist_ang)
        A[lat][lon].append(node)
    add_edge_quadrant(G, A, d, lat_rows, long_columns)


def create_graph(dist):
    # creates the graph with n size as the maximum size of an edge.
    # we using a data base from Barcelona's bicing stations
    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')
    G = nx.Graph()
    for st in bicing.itertuples():
        G.add_node((st.lat, st.lon))

    # we add all edges smaller than n.
    edge_adder(G, dist)
    return G

# #---------------------------------------------------##


# prints the graph edges and nodes using StaticMap
def print_all(G):
    m = StaticMap(800, 800)
    for node in list(G.node()):
        marker = CircleMarker((node[1], node[0]), 'black', 5)
        m.add_marker(marker)
    for edge in list(G.edges()):
        coords = ((edge[0][1], edge[0][0]), (edge[1][1], edge[1][0]))
        line = Line(coords, 'purple', 1)
        m.add_line(line)
    return m


# transforms adresses to coordinates
def addressesTOcoordinates(addresses):
    try:
        geolocator = Nominatim(user_agent="bicing_bot")
        address1, address2 = addresses.split(',')
        location1 = geolocator.geocode(address1 + ', Barcelona')
        location2 = geolocator.geocode(address2 + ', Barcelona')
        return (location1.latitude, location1.longitude),(location2.latitude, location2.longitude)
    except:
        return None


def complete_known_edge(G, coords):
    for node in list(G.node()):
        if (not G.has_edge(node, coords)):
            distance = haversine(node, coords)
            if (distance != 0):
                G.add_edge(node, coords, weight=distance*2.5)


# matches a new node with every single node
def complete_new_edge(G, coords):
    G.add_node(coords)
    for node in list(G.node()):
        distance = haversine(node, coords)
        if (distance != 0):
            G.add_edge(node, coords, weight=distance*2.5)


# matches an existent node with every single node
def print_path_in_graph(G, path):
    m = StaticMap(800, 800)
    for node in list(G.node()):
        marker = CircleMarker((node[1], node[0]), 'black', 5)
        m.add_marker(marker)
    for edge in list(G.edges()):
        coords = ((edge[0][1], edge[0][0]), (edge[1][1], edge[1][0]))
        line = Line(coords, 'grey', 1)
        m.add_line(line)
    for node in path:
        marker = CircleMarker((node[1], node[0]), 'blue', 3)
        m.add_marker(marker)
    for i in range(len(path)-1):
        coords = ((path[i][1], path[i][0]), (path[i+1][1], path[i+1][0]))
        line = Line(coords, 'blue', 2)
        m.add_line(line)
    return m


# prints the smallest path between 2 points using StaticMap
def print_path_solo(path):
    m = StaticMap(800, 800)
    for node in path:
        marker = CircleMarker((node[1], node[0]), 'blue', 3)
        m.add_marker(marker)
    for i in range(len(path)-1):
        coords = ((path[i][1], path[i][0]), (path[i+1][1], path[i+1][0]))
        line = Line(coords, 'blue', 2)
        m.add_line(line)
    return m


# prints the smallest distance in time between 2 points.
def shortest_path(G, adresses):
    # funcio que la direccio es un node conegut.(g.has_node("dirreccio"))
    coords = addressesTOcoordinates(adresses)
    if coords is None:
        return None
    coords1, coords2 = coords

    # We add the origin and arrival points as nodes.
    # to avoid unnecessary operations, bike speed is at 10km / h and
    # walking at 4km / h,
    # we know that it will take 2.5 times more walking, therefore,
    # we multiply the distance of
    # checking the shortest_path will be the same
    if (not G.has_node(coords1)):
        complete_new_edge(G, coords1)
    else:
        complete_known_edge(G, cords1)
    if (not G.has_node(coords2)):
        complete_new_edge(G, coords2)
    else:
        complete_known_edge(G, cords2)
    lenght, path = nx.bidirectional_dijkstra(G, coords1, coords2)
    G.remove_node(coords1)
    G.remove_node(coords2)
    return path


# Returns the number of connex components of the graph
def number_of_non_connex_components(G):
    return nx.number_connected_components(G)


# Returns the number of nodes of the graph
def number_of_nodes(G):
    return len(G)


# Returns the number of edges of the graph
def number_of_edges(G):
    return nx.number_of_edges(G)


# Distributes the  bikes the way each station has a minimum of
# bikes and docks, creating a flow
def distribute(requiredBikes, requiredDocks, R):
    url_info = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    url_status = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_status'
    stations = DataFrame.from_records(pd.read_json(url_info)['data']['stations'], index='station_id')
    bikes = DataFrame.from_records(pd.read_json(url_status)['data']['stations'], index='station_id')
    nbikes = 'num_bikes_available'
    ndocks = 'num_docks_available'
    bikes = bikes[[nbikes, ndocks]]  # We only select the interesting columns
    TotalBikes = bikes[nbikes].sum()
    TotalDocks = bikes[ndocks].sum()

    G = nx.DiGraph()
    G.add_node('TOP')  # The green node
    demand = 0

    for st in bikes.itertuples():
        idx = st.Index
        if idx not in stations.index:
            continue
        # if the stations are not in both DataFrame's, ignore them
        idx = st.Index
        stridx = str(idx)

        # The blue (s), black (g) and red (t) nodes of the graph
        s_idx, g_idx, t_idx = 's'+stridx, 'g'+stridx, 't'+stridx
        G.add_node(g_idx)
        G.add_node(s_idx)
        G.add_node(t_idx)

        b, d = st.num_bikes_available, st.num_docks_available
        req_bikes = max(0, requiredBikes - b)
        req_docks = max(0, requiredDocks - d)

        G.add_edge('TOP', s_idx)
        G.add_edge(s_idx, g_idx, capacity=max(0, b-requiredBikes))
        G.add_edge(g_idx, t_idx, capacity=max(0, d-requiredDocks))
        G.add_edge(t_idx, 'TOP')

        if req_bikes > 0:
            demand += req_bikes
            G.nodes[t_idx]['demand'] = req_bikes
        elif req_docks > 0:
            demand -= req_docks
            G.nodes[s_idx]['demand'] = -req_docks

    G.nodes['TOP']['demand'] = -demand
    for edge in (R.edges(data=True)):
        coords1, coords2 = edge[0], edge[1]
        dist = int(edge[2]['weight']*1000)
        idx1, idx2 = stations.index[stations['lon'] == coords1[1]], stations.index[stations['lon'] == coords2[1]]
        idx1, idx2 = idx1[0], idx2[0]
        if idx1 not in bikes.index or idx2 not in bikes.index:
            continue
        G.add_edge('g'+str(idx1), 'g'+str(idx2), weight=dist)
        G.add_edge('g'+str(idx2), 'g'+str(idx1), weight=dist)

    err = False

    try:
        flowCost, flowDict = nx.network_simplex(G)
    except nx.NetworkXUnfeasible:
        err = True
        return -1, 0
    except:
        err = True
        return -2, 0
    if not err:
        c = ("The total cost of transfering bikes is", flowCost/1000, "km")
    # We update the status of the stations according to the calculated transportation of bicycles
    disb = []
    for src in flowDict:
        if src[0] != 'g':
            continue
        idx_src = int(src[1:])
        for dst, b in flowDict[src].items():
            if dst[0] == 'g' and b > 0:
                idx_dst = int(dst[1:])
                dis = [(G.edges[src, dst]['weight'])*b, idx_src, idx_dst]
                disb.append(dis)
                bikes.at[idx_src, nbikes] -= b
                bikes.at[idx_dst, nbikes] += b
                bikes.at[idx_src, ndocks] += b
                bikes.at[idx_dst, ndocks] -= b
    # Returns the total cost of transfering bikes and the maximum
    # cost between two stations
    return c, max(disb)

G = create_graph(0.6)
print_all(G)
