from flask import Flask, request, redirect, render_template, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
# from flask_wtf import FlaskForm
# from flask_mail import Message, Mail
# from threading import Thread

from models import db, connect_db, User, Trip, UserTrip, Weather, TripWeather
from forms import TripForm, LocationForm, LoginForm
from api import api
import os
try:
    from pws import GOOGLE_MAPS_KEY
except:
    GOOGLE_MAPS_KEY = os.environ.get('GOOGLE_MAPS_KEY')

app = Flask(__name__)
app.register_blueprint(api)
# DEVELOPMENT
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///weather_the_trip')
db.init_app(app)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_ECHO'] = True
# use secret key in production or default to our dev one
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'backupkey')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  # DEVELOPMENT
debug = DebugToolbarExtension(app)

db.init_app(app)



@app.before_request
def before_request():
    if 'email' in session:
        g.user = User.query.filter(User.email == session['email']).first()
    else:
        g.user = None


@app.route('/')
def home():
    login_form = LoginForm()
    directions_form = TripForm()
    return render_template('home.html', directions_form=directions_form, login_form=login_form, GOOGLE_MAPS_KEY=GOOGLE_MAPS_KEY, user=g.user)


@app.route('/login', methods=['POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = User.authenticate(email, password)

        if(user):
            session['email'] = user.email
        else:
            flash('Incorrect email or password!', 'danger')

    return redirect('/')


@app.route('/logout')
def logout():
    session['email'] = None
    return redirect('/')
