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
        G.add_node(st.name, lat=st.lat,lon= st.lon)
    for node in list(G.node(data=True)):
        for node2 in list(G.node(data=True)):
            distance = haversine((node[1]['lon'], node[1]['lat']), (node2[1]['lon'], node2[1]['lat']))
            if(distance <= 1.000 and distance != 0):
                if not G.has_edge(node2[0], node[0]):
                    G.add_edge(node[0], node2[0], distance=distance)
    return G


def print_all(G):
    m = StaticMap(800, 800)
    for node in list(G.node(data=True)):
        marker = CircleMarker((node[1]['lon'], node[1]['lat']), 'red', 8)
        m.add_marker(marker)
    print(G.number_of_edges(), G.number_of_nodes())
    image = m.render()
    image.save('mapa.png')

print_all(create_graph())
