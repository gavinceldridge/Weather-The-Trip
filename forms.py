"""Forms for Weather The Trip app."""

from wtforms import SelectField, StringField, PasswordField
from flask_wtf import FlaskForm
from models import User
from wtforms.validators import InputRequired, Optional, Length


class TripForm(FlaskForm):
    start = StringField("Start Location", validators=[InputRequired()])
    end = StringField("End Location", validators=[InputRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""
    
    first_name = StringField('First Name', validators=[InputRequired(message='Enter your name please')])
    last_name = StringField('Last Name', validators=[InputRequired(message='Enter your name please')])
    email = StringField('Email', validators=[InputRequired(message='Please enter an Email')])
    password = PasswordField('Password', validators=[Length(min=6, message='Password must be at least 6 characters')])


class LoginForm(FlaskForm):
    """Login form."""

    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class EditUserForm(FlaskForm):
    """To edit an existing user"""
    first_name = StringField('First Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[Optional()])
    email = StringField('Email', validators=[Optional()])
    password = PasswordField('Password', validators=[InputRequired()])
