from flask import Blueprint, jsonify, request
from forms import TripForm
import requests
import re
import os

api = Blueprint('api', __name__, template_folder="templates")


# try:
from pws import WEATHER_KEY
from pws import GOOGLE_MAPS_KEY
# except:
# WEATHER_KEY = os.environ.get('WEATHER_KEY')
# GOOGLE_MAPS_KEY = os.environ.get('GOOGLE_MAPS_KEY')


# @api.route("/directions")
# def index():
#     form = TripForm
#     if form.validate_on_submit():
#         origin = form.start.data
#         destination = form.end.data
#         result = requests.get(f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}?destination={destination}?key={GOOGLE_MAPS_KEY}')
#         return result
#     return jsonify({'result': 'Form Incomplete'})

@api.route('/get-weather-report', methods=['POST'])
def weather():
    # latitude = request.args.get('lat')
    # longitude = request.args.get('lon')
    # expected_time = request.args.get('time')
    # import pdb; pdb.set_trace()
    result = dict()
    result['times'] = {}
    result['results'] = {}
    result['locations'] = {}
    # result.update({'times'}, {'results'})
    json = request.get_json('response')
    for time in json['times']:
        location = json['locations'][time]
        
        lat = re.search('(\d+.\d+)', location)[1]
        lng = re.search(',\s(.*)', location)[1]
        weather_info = requests.get(f'https://api.weatherbit.io/v2.0/forecast/hourly?key={WEATHER_KEY}&hours=48&lat={lat}&lon={lng}')
        weather_json = weather_info.json()
        for i in range(0, len(weather_json['data'])):
            if json['times'][time] == weather_json['data'][i]['timestamp_local']:
                
                reverse_geo_coded_lat_lng = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?key={GOOGLE_MAPS_KEY}&latlng={location}').json()['results'][0]['formatted_address']
                result['times'].update({time: json['times'][time]})
                result['locations'].update({time: reverse_geo_coded_lat_lng})
                result['results'].update({time: f"{weather_json['data'][i]['weather']['code']} : {weather_json['data'][i]['weather']['description']}"})
    return jsonify(result)

    