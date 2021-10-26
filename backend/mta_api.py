from google.transit import gtfs_realtime_pb2
import pandas as pd
from datetime import datetime
import requests
import os
from build_subway_info import build_subway_info

from dotenv import load_dotenv
load_dotenv()

base_mta_url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs'

subway_stops = build_subway_info('./Stations.xls')

def get_station_name(code):
    return subway_stops[subway_stops['route_id'] == code]['Stop Name'].unique()[0]

# TODO: add function to return all subway stops for given train(s)
def get_station_code(station_name, trains, df):

    station_name = station_name.lower()

    # filter for stop name == station name provided, running on given set of train lines
    # and get parent stop id (not N or S)
    filter = (df['Stop Name'] == station_name) & (df['train'].isin(trains))

    return df[filter]['route_id'].values[0]

def build_all_train_info(lines, headers):

    all_train_info = pd.DataFrame(columns=['route_id','stop_id','arrival', 'depart'])
    for line in lines:
        line_info = build_train_info(line, headers)
        all_train_info = all_train_info.append(line_info)

    return all_train_info

def build_train_info(line, headers):
    '''
    Accepts a mta-api url, headers (containing your api key)
    and then returns a Pandas DataFrame containing train info.
    '''

    url = base_mta_url + line
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(url, headers=headers)
    feed.ParseFromString(response.content)

    train_list = []

    for entity in feed.entity:

        if entity.HasField('trip_update'):

            tu = entity.trip_update

            for stu in tu.stop_time_update:  # Loop over the stop_time_update repeated element

                try:
                    depart_unix = int(stu.departure.time)
                    depart = 'N/A' if depart_unix == 0 else datetime.fromtimestamp(depart_unix)

                except AttributeError:
                    depart = "N/A"

                try:
                    arrive_unix = int(stu.arrival.time)
                    arrive = 'N/A' if arrive_unix == 0 else datetime.fromtimestamp(arrive_unix)
                except AttributeError:
                    arrive = "N/A"

                stop_update = {'route_id': tu.trip.route_id, 'stop_id': stu.stop_id, 'arrival': arrive, 'depart': depart}

                train_list.append(stop_update)

    return train_list

def get_upcoming_trains(df, station_code, direction='N', limit=None, trains=['4', '5' '6']):

    # filter to only stops in list of train_list
    train_line_filter = df['route_id'].isin(trains)

    # filter to only trains at specific stop
    stop_filter = df['stop_id'] == str(station_code) + direction
    df_upcoming_trains = df[train_line_filter & stop_filter].sort_values(by=['arrival'])

    upcoming = []
    now = datetime.now()
    for index, row in df_upcoming_trains.iterrows():
        time = row['depart']

        delta = time - now
        mins = round(delta.total_seconds() / 60 )
        if mins > 0:
            upcoming.append({'route_id': row['route_id'], 'mins': mins, 'time': time})

    return upcoming if limit == None else upcoming[:limit]

def get_upcoming_trains_for_station_list(df, station_list):
    all_results = {}
    for station in station_list:
        stop_name = get_station_name(station)
        station_filter = (df['stop_id'].str.contains(station)) & (df['depart'] != 'N/A')
        station_result = {'stop_name': stop_name, 'trains': df[station_filter][['stop_id', 'route_id', 'depart']].values.tolist()}
        all_results[station] = station_result

    return all_results
