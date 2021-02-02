from flask import Blueprint, jsonify
from forms import TripForm
import requests
from pws import GOOGLE_MAPS_KEY

api = Blueprint('api', __name__, template_folder="templates")


@api.route("/directions")
def index():
    form = TripForm
    if form.validate_on_submit():
        origin = form.start.data
        destination = form.end.data
        result = requests.get(f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}?destination={destination}?key={GOOGLE_MAPS_KEY}')
        return result
    return jsonify({'result': 'Form Incomplete'})