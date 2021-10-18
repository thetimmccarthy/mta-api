from flask import Flask, request, redirect, url_for, render_template
from mta_api import build_all_train_info, get_upcoming_trains
import os
import pandas as pd
import sys
from twilio.twiml.messaging_response import MessagingResponse, Message
from flask_cors import CORS



from dotenv import load_dotenv
load_dotenv()

from mta_api import get_station_code, build_train_info, get_upcoming_trains

app = Flask(__name__)
CORS(app)

base_mta_url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs'
headers = {
  "x-api-key": os.getenv('MTA_API_KEY')
}

mta_links = {'ace':'-ace', 'bdfm':'-bdfm', 'g':'-g', 'jz':'-jz', 'nqrw':'-nqrw', 'l':'-l', '1234567':''}

subway_stops = pd.read_csv('./nyc_subway_stops.csv')

def normalize_stop_name(row):
    return row['stop_name'].lower()

def add_train_line(row):
    return row['stop_id'][0]

# subway_stops['stop_name'] = subway_stops.apply(lambda row: normalize_stop_name(row), axis=1)
subway_stops['train'] = subway_stops.apply(lambda row: add_train_line(row), axis=1)

train_info = build_all_train_info(mta_links.values(), headers)

@app.route('/sms', methods=['POST'])
def get_trains():
    '''
    This function is used to return upcoming trains when texted a station (via twilio).
    '''

    trains = ['4', '5', '6']

    station_lower = request.form['Body']
    station_lower = station_lower.lower()

    station_code = get_station_code(station_lower, trains, subway_stops)
    found_trains = get_upcoming_trains(train_info, station_code, limit=5, trains=trains)

    train_response = ['{} train coming in {} mins. \n '.format(train['route_id'], train['mins']) for train in found_trains]
    joined_response = 'The following trains are coming: \n' + ''.join(train_response)

    resp = MessagingResponse()
    resp.message(joined_response)
    return str(resp)

@app.route('/stations', methods=['GET'])
# @cross_origin
def get_stations_trains():
    train = '5'
    filters = (subway_stops['train'] == train) & (subway_stops['location_type'] == 1)
    trains = subway_stops[filters]['stop_name'].to_dict()

    return trains



if __name__ == '__main__':
    app.debug = True
    app.run()
