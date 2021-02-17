from flask import Blueprint, jsonify, request
from forms import TripForm
import requests
from pws import GOOGLE_MAPS_KEY
import re

api = Blueprint('api', __name__, template_folder="templates")


try:
    from pws import WEATHER_KEY
except:
    WEATHER_KEY = os.environ.get('WEATHER_KEY')


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
            # print(f'time: {time}\njson["times"][time]: {json["times"][time]}\nresult: {result}\nweather_json["data"][i]["timestamp"]: {weather_json["data"][i]["timestamp_local"]}')
            if json['times'][time] == weather_json['data'][i]['timestamp_local']:
                # if(result == {}):
                #     result['times'] = {time: json['times'][time]}
                #     result['locations'] = {time: location}
                #     result['results'] = {time: f"{weather_json['data'][i]['weather']['code']} : {weather_json['data'][i]['weather']['description']}"}
                # else:     
                result['times'].update({time: json['times'][time]})
                result['locations'].update({time: location})
                result['results'].update({time: f"{weather_json['data'][i]['weather']['code']} : {weather_json['data'][i]['weather']['description']}"})
    return jsonify(result)

    