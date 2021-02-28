import pandas as pd
import numpy as np
import os
from config import Config
import seaborn as sns
import matplotlib.pyplot as plt
import textwrap
from imblearn.over_sampling import SMOTENC
from imblearn.under_sampling import RandomUnderSampler
from collections import Counter

def extract_location(row, pos):
    temp = row['grid_67'].replace('(', '').replace(')', '').split(',')
    x = round(float(temp[pos]))
    return x

#We apply the SMOTE NC algorithms in order to over_sampling data
def over_under_sampling(col, strategy):
    y = data[col]
    X = data.drop([col], axis=1)
    sampler = SMOTENC(k_neighbors=2, categorical_features=[1, 2, 3, 4, 5, 6, 7], sampling_strategy=strategy, n_jobs=2)
    X, y = sampler.fit_resample(X, y)
    under_sampler = RandomUnderSampler(sampling_strategy='majority')
    X,y = under_sampler.fit_resample(X, y)
    print('Balancing for {} finished. Result:'.format(col))
    print(Counter(y))
    return pd.concat([X, y], axis=1)

#read the dataset
data = pd.read_csv(os.path.join(os.pardir, Config.data_folder, Config.clean_data))

#preparation of the data
data = data[data['grid_67'].notna()]
data = data[['POSTED_SPEED_LIMIT', 'WEATHER_CONDITION', 'LIGHTING_CONDITION', 'ROADWAY_SURFACE_COND', 'CRASH_WEEKDAY', 'CRASH_HOUR', 'CRASH_Month', 'grid_67']]
data['x'] = data.apply(lambda row: extract_location(row, 0), axis=1)
data['y'] = data.apply(lambda row: extract_location(row, 1), axis=1)
data = data.drop(['grid_67'], axis=1)

target_size = 60000

##VISUALIZATION PART

# weather condition
print('weather...')
weather_strategy = {'RAIN': target_size, 'CLOUDY/OVERCAST': target_size, 'SNOW': target_size}
sampled_weather = over_under_sampling('WEATHER_CONDITION', weather_strategy)

# lighting_conditions #darkness, Lightes Road = special snowflake
print('light...')
lighting_strategy = {'DARKNESS, LIGHTED ROAD': 120000, 'DAWN': target_size, 'DARKNESS': target_size, 'DUSK': target_size}
sampled_lighting = over_under_sampling('LIGHTING_CONDITION', lighting_strategy)

# road_conditions
print('road...')
road_strategy = {'SNOW OR SLUSH': target_size, 'WET': target_size}
sampled_road = over_under_sampling('ROADWAY_SURFACE_COND', road_strategy)

sampled_data = pd.concat([sampled_road, sampled_lighting, sampled_weather]).drop_duplicates().reset_index(drop=True)
#sampled_data = sampled_data.sample(n=500000)
sampled_data.to_csv('augmented', index=False)


cols = ['CRASH_WEEKDAY', 'CRASH_HOUR', 'CRASH_Month']
hues = ['WEATHER_CONDITION', 'LIGHTING_CONDITION', 'ROADWAY_SURFACE_COND']

max_width = 10
i=0
for col in sampled_data[cols]:
    for hue in sampled_data[hues]:
        plt.figure(i, figsize=(15.0,10.0))
        b = sns.countplot(x=col, hue=hue, data=sampled_data)
        b.tick_params(labelsize=15)
        b.set_xticklabels(textwrap.fill(x.get_text(), max_width) for x in b.get_xticklabels())
        i+=1
        plt.show()

print(data)