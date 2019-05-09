import pandas as pd
from staticmap import StaticMap, CircleMarker, Line
import networkx as nx
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim




def stations():
    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')

    G = nx.Graph()
    for st in bicing.itertuples():
        G.add_node(st.name, lat=st.lat,lon= st.lon)
    return G


def print_stations(G):
    m = StaticMap(800, 800)
    for node in list(G.node(data=True)):
        marker = CircleMarker((node[1]['lon'], node[1]['lat']), 'red', 8)
        m.add_marker(marker)
    image = m.render()
    image.save('mapa.png')

print_stations(stations())
