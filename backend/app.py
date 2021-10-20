from flask import Flask, request, redirect, url_for, render_template
from mta_api import build_all_train_info, get_upcoming_trains, get_station_code
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

subway_stops = pd.read_excel('./Stations.xls')

def create_station_list(row):
    stops = str(row['Daytime Routes'])
    return stops.split(',')

def normalize_route_id(row):
    return str(row['Route ID'])


subway_stops['train'] = subway_stops.apply(lambda row: create_station_list(row), axis=1)
subway_stops['Route ID'] = subway_stops.apply(lambda row: normalize_route_id(row), axis=1)
subway_stops = subway_stops.explode('train')
subway_stops = subway_stops.drop(columns=['Division', 'Line', 'Borough', 'Daytime Routes', 'Structure', 'ADA', 'ADA Notes'])

train_info = build_all_train_info(mta_links.values(), headers)

@app.route('/sms', methods=['POST'])
def get_trains_sms():
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
def get_stations():
    trains = list(subway_stops['train'].unique())

    train_stops = {}
    # train_stops = []
    for train in trains:
        filter = subway_stops['train'] == train
        stops = dict(zip(subway_stops[filter]['Route ID'], subway_stops[filter]['Stop Name']))
        train_stops[train] = stops

    # print(train_stops)
    return train_stops

# TODO: Look into returning arrays to 'fetch' call from React

# Will need to add direction to this as a parameter, and will need to put build_all_train_info on a loop
@app.route('/trains/<id>', methods=['GET'])
def get_trains():
    train_info_2 = build_all_train_info(mta_links.values(), headers)
    found_trains = get_upcoming_trains(train_info, station_code, limit=5, trains=trains)

    to_return = {}
    for i in range(len(found_trains)):
        to_return[i] = found_trains[i]

    return to_return

if __name__ == '__main__':
    app.debug = True
    app.run()
