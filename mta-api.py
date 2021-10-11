from google.transit import gtfs_realtime_pb2
import pandas as pd
from datetime import datetime
import requests
import os

from dotenv import load_dotenv
load_dotenv()

url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs'
headers = {
  "x-api-key": os.getenv('MTA_API_KEY')
}
subway_stops = pd.read_csv('./nyc_subway_stops.csv')
station_by_name = '86 St'
station_by_code = '626N'
trains = ['4', '5', '6']
ids = subway_stops[subway_stops['stop_name'] == station_by_name]['stop_id']
ids = set([id[0] for id in list(ids.unique())])


feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get(url, headers=headers)

stop_time_update = pd.DataFrame(columns=['route_id','stop_id','arrival', 'depart'])

feed.ParseFromString(response.content)

for entity in feed.entity:

    if entity.HasField('trip_update'):

        tu = entity.trip_update
        for stu in tu.stop_time_update:  ## Loop over the stop_time_update repeated element
            if tu.trip.route_id in ('4', '5', '6'):
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
filter = stop_time_update['stop_id'] == station_by_code
upcoming_trains = stop_time_update[filter].sort_values(by=['arrival'])

now = datetime.now()

for time in upcoming_trains['arrival'].unique():
    delta = time - now
    mins = round(delta.total_seconds() / 60 )
    print('Train coming in ', mins, ' minutes.')
