from google.transit import gtfs_realtime_pb2
import pandas as pd
from datetime import datetime
import requests
import os

from dotenv import load_dotenv
load_dotenv()

# TODO: add function to return all subway stops for given train(s)

def get_station_code(station_name, trains, df):
    station_name = station_name.lower()

    # filter for stop name == station name provided, running on given set of train lines
    # and get parent stop id (not N or S)
    filter = (df['stop_name'] == station_name) & (df['train'].isin(trains)) \
        & df['location_type'] == 1

    return df[filter]['stop_id'].values[0]

# Need to test, but guessing this is what is slowing down the application
def build_train_info(url, headers, trains):

    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(url, headers=headers)
    feed.ParseFromString(response.content)

    stop_time_update = pd.DataFrame(columns=['route_id','stop_id','arrival', 'depart'])

    for entity in feed.entity:

        if entity.HasField('trip_update'):

            tu = entity.trip_update
            for stu in tu.stop_time_update:  # Loop over the stop_time_update repeated element
                if tu.trip.route_id in trains:
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
                    stop_time_update = stop_time_update.append(stop_update, ignore_index=True)

    return stop_time_update

def get_upcoming_trains(df, station_code, direction='N', limit=None):

    filter = df['stop_id'] == str(station_code) + direction
    upcoming_trains = df[filter].sort_values(by=['arrival'])

    trains = []
    now = datetime.now()
    for index, row in upcoming_trains.iterrows():
        time = row['arrival']
        delta = time - now
        mins = round(delta.total_seconds() / 60 )
        if mins > 0:
            trains.append({'route_id': row['route_id'], 'mins': mins})

    return trains if limit == None else trains[:limit]
