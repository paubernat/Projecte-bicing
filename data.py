import pandas as pd
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim



url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')
jaj
