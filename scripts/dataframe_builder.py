
import pandas as pd
import numpy as np
import json
from pathlib import Path

from scripts.constants import *
from scripts import file_handler

def update_dataframe():
    if not Path(SAVE_DIR+RESULTS).is_file():
        pd.DataFrame().to_csv(SAVE_DIR+RESULTS)
    df = pd.read_csv(SAVE_DIR+RESULTS, index_col=0)
    for geo_location in df[df.isna().any(axis=1)].index:
        add_sample(geo_location)
    
    for geo_location in file_handler.get_all_geo_locations():
        if not geo_location in df.index:
            add_sample(geo_location)
    

def add_sample(geo_location):
    df = pd.read_csv(SAVE_DIR+RESULTS, index_col=0)
    
    entry = pd.Series(name = geo_location)
    entry['country'] = get_country(geo_location)
    entry['city'] = get_city(geo_location)
    entry['yelp'] = get_yelp(geo_location)
    entry['four_square'] = get_four_square(geo_location)
    entry['google'] = get_google(geo_location)
    if not entry.name in df.index:
        df = df.append(entry)
    else:
        sample = df.loc[geo_location]
        nan_values = sample[sample.isna()].index
        for column in nan_values:
            df.at[entry.name,column] = entry[column]      
                      
    df.to_csv(SAVE_DIR+RESULTS)



def get_country(geo_location):
    data = file_handler.get_response(LOG_DIR+COUNTRIES, geo_location)
    if data: 
        if 'name' in data.keys():
            return data['name']

    return np.nan
    
def get_city(geo_location):
    data = file_handler.get_response(LOG_DIR+GEO_LOCATIONS, geo_location)
    if data: 
        return data['nearest']['city']
    else:
        return np.nan  
    
def get_yelp(geo_location):
    data = file_handler.get_response(LOG_DIR+YELP, geo_location)
    if data: 
        return data['total']   
    else:
        return np.nan
    
def get_four_square(geo_location):    
    data = file_handler.get_response(LOG_DIR+FOUR_SQUARE, geo_location)
    if data: 
        return len(data['response']['venues'])
    else:
        return np.nan 
    
def get_google(geo_location):
    data = file_handler.get_response(LOG_DIR+GOOGLE, geo_location)
    if data: 
        # value = 0
        # for venue in data['results']:
        #     if 'business_status' in venue.keys():
        #         value += 1  
        # return value
        return len(data['results'])
    else:
        return np.nan
        

