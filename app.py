from flask import Flask, request, redirect, render_template, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Trip, UserTrip, Weather, TripWeather
from forms import TripForm, LoginForm, UserAddForm
from api import api
import os

app = Flask(__name__)
app.register_blueprint(api)


# DEVELOPMENT
# from pws import GOOGLE_MAPS_KEY

# PRODUCTION
GOOGLE_MAPS_KEY = os.environ.get('GOOGLE_MAPS_KEY')


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///test_weather_the_trip')
db.init_app(app)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'backupkey')
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  # DEVELOPMENT
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


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    login_form = LoginForm()
    signup_form = UserAddForm()
    if signup_form.validate_on_submit():
        email = signup_form.email.data
        password = signup_form.password.data
        first_name = signup_form.first_name.data
        last_name = signup_form.last_name.data
        new_user = User.signup(first_name, last_name, email, password)
        is_email_taken = User.query.filter(User.email == email).all()
        if(is_email_taken == []):

            db.session.add(new_user)
            db.session.commit()
            flash(f'Thanks for signing up, {first_name}', 'success')
            return redirect('/')
        else:
            flash('Email already taken, try again', 'danger')

    return render_template('signup.html', signup_form=signup_form, login_form=login_form)


@app.route('/logout')
def logout():
    session['email'] = None
    return redirect('/')
