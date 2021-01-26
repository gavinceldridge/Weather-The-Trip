
from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
# from flask_wtf import FlaskForm
# from flask_mail import Message, Mail
# from threading import Thread

from models import db, connect_db, User, Trip, UserTrip, Weather, TripWeather
# from forms import RegisterForm, LoginForm, ForgotPasswordForm, EditUserForm, ResetPasswordForm, AdminForm, BanAppealForm
# from pws import admin_pw, email_pw
# from time import time
from pws import GOOGLE_MAPS_KEY
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgres:///')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///weather_the_trip'#DEVELOPMENT
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
# use secret key in production or default to our dev one
app.config['SECRET_KEY'] = 'verysecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False#DEVELOPMENT


debug = DebugToolbarExtension(app)


@app.route('/')
def home():
    return render_template('home.html', GOOGLE_MAPS_KEY=GOOGLE_MAPS_KEY)