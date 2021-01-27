"""Forms for Weather The Trip app."""

from wtforms import SelectField, StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional


class LocationForm(FlaskForm):
    """Form for adding playlists."""
    location = StringField("Location", validators=[InputRequired()])


class TripForm(FlaskForm):
    start = StringField("Start Location", validators=[InputRequired()])
    end = StringField("End Location", validators=[InputRequired()])


# class UserAddForm(FlaskForm):
#     """Form for adding users."""

#     username = StringField('Username', validators=[DataRequired()])
#     email = StringField('E-mail', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[Length(min=6)])
#     image_url = StringField('(Optional) Image URL')


# class LoginForm(FlaskForm):
#     """Login form."""

#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[Length(min=6)])


# class EditUserForm(FlaskForm):
#     """To edit an existing user"""
#     username = StringField('Username', validators=[Optional()])
#     email = StringField('Email', validators=[Optional()])
#     image_url = StringField('Image URL', validators=[Optional()])
#     header_image_url = StringField('Header Image URL', validators=[Optional()])
#     bio = StringField('Bio', validators=[Optional()])
#     password = PasswordField('Password', validators=[InputRequired()])
