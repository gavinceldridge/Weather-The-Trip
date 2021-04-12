from flask import Blueprint, jsonify, request
from forms import TripForm
import requests
import re
import os
from datetime import datetime, timezone

api = Blueprint('api', __name__, template_folder="templates")


# from pws import GOOGLE_MAPS_KEY
# from pws import WEATHER_KEY
WEATHER_KEY = os.environ.get('WEATHER_KEY')
GOOGLE_MAPS_KEY = os.environ.get('GOOGLE_MAPS_KEY')


@api.route('/get-weather-report', methods=['POST'])
def weather():
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
        # weather_info = requests.get(
        #     f'https://api.weatherbit.io/v2.0/forecast/hourly?key={WEATHER_KEY}&hours=48&lat={lat}&lon={lng}') DEPRECATED
        weather_info = requests.get(
            f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lng}&appid={WEATHER_KEY}")
        weather_json = weather_info.json()['hourly']
        # import pdb
        # pdb.set_trace()
        for i in range(0, len(weather_json)):
            weather_time = datetime.fromtimestamp(
                weather_json[i]['dt']).strftime('%Y-%m-%dT%H:%M:%S')
            # if json['times'][time] == weather_json['data'][i]['timestamp_local']:

            #     reverse_geo_coded_lat_lng = requests.get(
            #         f'https://maps.googleapis.com/maps/api/geocode/json?key={GOOGLE_MAPS_KEY}&latlng={location}').json()['results'][0]['formatted_address']
            #     result['times'].update({time: json['times'][time]})
            #     result['locations'].update({time: reverse_geo_coded_lat_lng})
            #     result['results'].update(
            #         {time: f"{weather_json['data'][i]['weather']['code']} : {weather_json['data'][i]['weather']['description']}"})
            if json['times'][time] == weather_time:

                reverse_geo_coded_lat_lng = requests.get(
                    f'https://maps.googleapis.com/maps/api/geocode/json?key={GOOGLE_MAPS_KEY}&latlng={location}').json()['results'][0]['formatted_address']
                result['times'].update({time: weather_time})
                result['locations'].update({time: reverse_geo_coded_lat_lng})
                result['results'].update(
                    {time: f"{weather_json[i]['weather'][0]['id']} : {weather_json[i]['weather'][0]['description']}"})

    return jsonify(result)
