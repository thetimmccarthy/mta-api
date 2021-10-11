from flask import Flask, request, redirect, url_for, render_template
from mta_api import build_train_info, get_upcoming_trains
import os
import pandas as pd
import sys
from dotenv import load_dotenv
load_dotenv()

from mta_api import get_station_code, build_train_info, get_upcoming_trains

app = Flask(__name__)

url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs'
headers = {
  "x-api-key": os.getenv('MTA_API_KEY')
}

trains = ['4', '5', '6']

subway_stops = pd.read_csv('./nyc_subway_stops.csv')

def normalize_stop_name(row):
    return row['stop_name'].lower()

def add_train_line(row):
    return row['stop_id'][0]

subway_stops['stop_name'] = subway_stops.apply(lambda row: normalize_stop_name(row), axis=1)
subway_stops['train'] = subway_stops.apply(lambda row: add_train_line(row), axis=1)

train_info = build_train_info(url, headers, trains)

@app.route('/')
def home():
    print(request, flush=True)

    return 'Hello'

@app.route('/station/<station>')
def get_trains(station):

    station_lower = station.lower()
    code = get_station_code(station_lower, trains, subway_stops)
    found_trains = get_upcoming_trains(train_info, code, limit=5)

    return render_template('index.html', t=found_trains, station=station.title())

if __name__ == '__main__':
    app.run(debug=True)
