from flask import Flask, request, redirect, url_for, render_template
import os
import pandas as pd
import sys
from twilio.twiml.messaging_response import MessagingResponse, Message
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

import mta_api
from build_subway_info import build_subway_info

app = Flask(__name__)
CORS(app)

base_mta_url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs'
headers = {
  "x-api-key": os.getenv('MTA_API_KEY')
}

mta_links = {'ace':'-ace', 'bdfm':'-bdfm', 'g':'-g', 'jz':'-jz', 'nqrw':'-nqrw', 'l':'-l', '1234567':''}


subway_stops = build_subway_info('./Stations.xls')
train_info = mta_api.build_all_train_info(mta_links.values(), headers)

@app.route('/sms', methods=['POST'])
def get_trains_sms():
    '''
    This function is used to return upcoming trains when texted a station (via twilio).
    '''

    trains = ['4', '5', '6']

    station_lower = request.form['Body']
    station_lower = station_lower.lower()

    station_code = mta_api.get_station_code(station_lower, trains, subway_stops)
    found_trains = mta_api.get_upcoming_trains(train_info, station_code, limit=5, trains=trains)

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
    for train in trains:
        filter = subway_stops['train'] == train
        stops = dict(zip(subway_stops[filter]['route_id'], subway_stops[filter]['Stop Name']))
        train_stops[train] = stops

    north_south = dict(zip(subway_stops['route_id'].values, subway_stops[['North Direction Label', 'South Direction Label']].values.tolist()))
    mta_info = {'direction': north_south, 'train_stops': train_stops}
    return mta_info

# TODO: Look into returning arrays to 'fetch' call from React

# Will need to add direction to this as a parameter, and will need to put build_all_train_info on a loop
@app.route('/trains/<train>/<station_id>/<direction>', methods=['GET'])
def get_trains(train, station_id, direction):

    train_info_2 = mta_api.build_all_train_info(mta_links.values(), headers)
    found_trains = mta_api.get_upcoming_trains(train_info, station_id, direction=direction, trains=[train])
    to_return = {}
    for i in range(len(found_trains)):
        # to_return[i] = found_trains[i]['mins']
        to_return[i] = found_trains[i]['time']

    return to_return

@app.route('/trains/<favorites>')
def get_trains_for_favorites(favorites):
    favorite_station_ids = list(favorites.split(','))
    train_info_2 = mta_api.build_all_train_info(mta_links.values(), headers)
    trains = mta_api.get_upcoming_trains_for_station_list(train_info_2, favorite_station_ids);
    return trains

if __name__ == '__main__':
    app.debug = True
    app.run()
