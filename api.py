from flask import Blueprint, jsonify, request
from forms import TripForm
import requests
from pws import GOOGLE_MAPS_KEY

api = Blueprint('api', __name__, template_folder="templates")


try:
    from pws import WEATHER_KEY
except:
    WEATHER_KEY = os.environ.get('WEATHER_KEY')


@api.route("/directions")
def index():
    form = TripForm
    if form.validate_on_submit():
        origin = form.start.data
        destination = form.end.data
        result = requests.get(f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}?destination={destination}?key={GOOGLE_MAPS_KEY}')
        return result
    return jsonify({'result': 'Form Incomplete'})

@api.route('/get-weather-report', methods=['POST'])
def weather():
    # latitude = request.args.get('lat')
    # longitude = request.args.get('lon')
    # expected_time = request.args.get('time')
    result = dict()
    json = request.get_json('response')
    for time in json['times']:
        print(json['times'][f'{time}'])

    import pdb
    pdb.set_trace()
    return jsonify(result)

    