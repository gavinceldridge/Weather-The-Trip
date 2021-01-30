"""Forms for Weather The Trip app."""

from wtforms import SelectField, StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional, Length


class LocationForm(FlaskForm):
    """Form for adding playlists."""
    location = StringField("Location", validators=[InputRequired()])


class TripForm(FlaskForm):
    start = StringField("Start Location", validators=[InputRequired()])
    end = StringField("End Location", validators=[InputRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


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
