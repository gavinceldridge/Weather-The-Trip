from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
# from flask_wtf import FlaskForm
# from flask_mail import Message, Mail
# from threading import Thread

from models import db, connect_db, User, Trip, UserTrip, Weather, TripWeather
from forms import TripForm, LocationForm
from pws import GOOGLE_MAPS_KEY
import os


app = Flask(__name__)
# DEVELOPMENT
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///weather_the_trip'
db.init_app(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
# use secret key in production or default to our dev one
app.config['SECRET_KEY'] = 'verysecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  # DEVELOPMENT

db.init_app(app)

debug = DebugToolbarExtension(app)


@app.route('/')
def home():

    location_form = LocationForm()
    trip_form = TripForm()
    return render_template('home.html', GOOGLE_MAPS_KEY=GOOGLE_MAPS_KEY, location_form=location_form, trip_form=trip_form)