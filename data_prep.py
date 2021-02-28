from config import Config
from map_grid import MapGrid
import pandas as pd
import numpy as np
import os

curr_dir = os.path.dirname(__file__)
data_path = os.path.join(curr_dir, Config.data_folder, Config.org_data)

data = pd.read_csv(data_path)
data = data.drop(columns=['CRASH_RECORD_ID', 'RD_NO', 'CRASH_DATE_EST_I', 'LANE_CNT', 'ALIGNMENT', 'ROAD_DEFECT',
                        'REPORT_TYPE', 'HIT_AND_RUN_I', 'DATE_POLICE_NOTIFIED', 'BEAT_OF_OCCURRENCE', 'PHOTOS_TAKEN_I',
                        'STATEMENTS_TAKEN_I', 'DOORING_I', 'WORK_ZONE_I', 'WORK_ZONE_TYPE', 'WORKERS_PRESENT_I',
                        'NUM_UNITS', 'MOST_SEVERE_INJURY', 'INJURIES_TOTAL',	'INJURIES_FATAL',
                        'INJURIES_INCAPACITATING', 'INJURIES_NON_INCAPACITATING', 'INJURIES_REPORTED_NOT_EVIDENT',
                        'INJURIES_NO_INDICATION', 'INJURIES_UNKNOWN', 'CRASH_HOUR', 'CRASH_DAY_OF_WEEK',
                        'CRASH_MONTH', 'LOCATION'])

data.drop_duplicates()
#data = data.iloc[0:10] #use this until code is debugged and then run once for complete data set

#removing all rows which do not have lat/long
data['LONGITUDE'].replace('', np.nan, inplace=True)
data['LATITUDE'].replace('', np.nan, inplace=True)
data.dropna(axis=0, subset=['LONGITUDE', 'LATITUDE'], inplace=True)

#convert object to datetime format
#try:
data['CRASH_DATE'] = pd.to_datetime(data['CRASH_DATE']) #, format='%m/%d/%Y %I:%M:%S %p'
#except:
 #   data['CRASH_DATE'] = pd.to_datetime(data['CRASH_DATE'], format='%m/%d/%Y %I:%M')
#Monday = 0, Sunday = 6
data['CRASH_WEEKDAY'] = data['CRASH_DATE'].dt.dayofweek
data['CRASH_HOUR'] = data['CRASH_DATE'].dt.hour
data['CRASH_Month'] = data['CRASH_DATE'].dt.month

# #assigning every sample an area in a grid overlay on chicago
# city_map = MapGrid(Config.city, Config.city_boundaries, 32, 32)
# #latitude -> the higher the more north, Longitude -> the higher the more east in grid, origin of gird = ll = (0,0)
# data["grid"] = data.apply(lambda x: city_map.get_grid(x['LONGITUDE'], x['LATITUDE']), axis=1)

data = data.loc[data['WEATHER_CONDITION'].isin(['CLEAR', 'RAIN', 'CLOUDY/OVERCAST', 'SNOW'])]
data = data.loc[~data['LIGHTING_CONDITION'].isin(['UNKNOWN'])]
data = data.loc[data['ROADWAY_SURFACE_COND'].isin(['DRY', 'WET', 'SNOW OR SLUSH'])]

#=========temporary==========
city_map = MapGrid(Config.city, Config.city_boundaries, 33, 33)
data["grid_33"] = data.apply(lambda x: city_map.get_grid(x['LONGITUDE'], x['LATITUDE']), axis=1)

city_map = MapGrid(Config.city, Config.city_boundaries, 48, 48)
data["grid_48"] = data.apply(lambda x: city_map.get_grid(x['LONGITUDE'], x['LATITUDE']), axis=1)

city_map = MapGrid(Config.city, Config.city_boundaries, 67, 67)
data["grid_67"] = data.apply(lambda x: city_map.get_grid(x['LONGITUDE'], x['LATITUDE']), axis=1)

city_map = MapGrid(Config.city, Config.city_boundaries, 96, 96)
data["grid_96"] = data.apply(lambda x: city_map.get_grid(x['LONGITUDE'], x['LATITUDE']), axis=1)


#saving cleaned data
save_path = os.path.join(curr_dir, Config.data_folder, Config.clean_data)
print('saving cleaned data')
data.to_csv(save_path, index=False)




