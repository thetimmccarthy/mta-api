import os
import pandas as pd
import sys


def create_station_list(row):
    stops = str(row['Daytime Routes'])
    return stops.split(',')

def normalize_route_id(row):
    return str(row['Route ID'])

def build_subway_info(path):

    subway_stops = pd.read_excel(path)

    subway_stops['train'] = subway_stops.apply(lambda row: create_station_list(row), axis=1)
    subway_stops['route_id'] = subway_stops.apply(lambda row: normalize_route_id(row), axis=1)
    subway_stops = subway_stops.explode('train')
    subway_stops = subway_stops.drop(columns=['Route ID','Division', 'Line', 'Borough', 'Daytime Routes', 'Structure', 'ADA', 'ADA Notes'])
    subway_stops = subway_stops.fillna(0)

    return subway_stops
