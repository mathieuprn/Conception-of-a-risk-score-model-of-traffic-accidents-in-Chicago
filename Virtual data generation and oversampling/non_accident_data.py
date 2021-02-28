import json
import pandas as pd
from map_grid import MapGrid
from config import Config
from tqdm import tqdm
from os.path import join


def get_midpoint(shape):
    lat_1 = shape[0]['latitude']
    lon_1 = shape[0]['longitude']
    lat_2 = shape[1]['latitude']
    lon_2 = shape[1]['longitude']

    lon_diff = abs(lon_1 - lon_2)/2
    lat_diff = abs(lat_1 - lat_2)/2

    if lat_1 <= lat_2:
        lat_mid = round(lat_1 + lat_diff, 5)
    else:
        lat_mid = round(lat_2 + lat_diff, 5)

    if lon_1 <= lon_2:
        lon_mid = round(lon_1 + lon_diff, 5)
    else:
        lon_mid = round(lon_2 + lon_diff, 5)

    return lat_mid, lon_mid

#load .json from drive and put into data folder of your local github repository
with open(join(Config.data_folder, 'jobs_2151686_results_first_report.json')) as f:
    data = json.load(f)

segment_results = data['network']['segmentResults']

segments = []
for entry in tqdm(segment_results):
    lat, lon = get_midpoint(entry['shape'])
    count = entry['segmentProbeCounts'][0]['probeCount']
    # https://developer.tomtom.com/traffic-stats/support/faq/what-are-functional-road-classes-frc
    # 0 = motorway/highway -> 7 = minor local roadway / smaller number = more important
    street_type = entry['frc']
    segments.append([count, lat, lon, street_type])

data = pd.DataFrame(segments, columns=['count', 'LATITUDE', 'LONGITUDE', 'street_type'])

print('1/4')
city_map = MapGrid(Config.city, Config.city_boundaries, 33, 33)
data["grid_33"] = data.apply(lambda x: city_map.get_grid(x['LONGITUDE'], x['LATITUDE']), axis=1)

print('2/4')
city_map = MapGrid(Config.city, Config.city_boundaries, 48, 48)
data["grid_48"] = data.apply(lambda x: city_map.get_grid(x['LONGITUDE'], x['LATITUDE']), axis=1)

print('3/4')
city_map = MapGrid(Config.city, Config.city_boundaries, 67, 67)
data["grid_67"] = data.apply(lambda x: city_map.get_grid(x['LONGITUDE'], x['LATITUDE']), axis=1)

print('4/4')
city_map = MapGrid(Config.city, Config.city_boundaries, 96, 96)
data["grid_96"] = data.apply(lambda x: city_map.get_grid(x['LONGITUDE'], x['LATITUDE']), axis=1)

#===== change grid config here =====
data_per_cell = data.groupby(['grid_67']).sum()
data_per_cell.drop(['LATITUDE', 'LONGITUDE', 'steet_type'], inplace=True, axis=1)

data_per_cell.to_csv('zone_capacity.csv')