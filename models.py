from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Trip(db.Model):

    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    starting_longitude = db.Column(db.Text, nullable=False)
    starting_latitude = db.Column(db.Text, nullable=False)
    ending_longitude = db.Column(db.Text, nullable=False)
    ending_latitude = db.Column(db.Text, nullable=False)
    user = db.relationship('User', secondary='user_trips', backref='trips')


class Weather(db.Model):

    __tablename__ = 'weathers'
    code = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)


class TripWeather(db.Model):

    __tablename__ = 'trip_weathers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    weather_code = db.Column(db.Integer, db.ForeignKey(
        'weathers.code'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    weather = db.relationship('Weather')
    trip = db.relationship('Trip')


class UserTrip(db.Model):
    '''relationship between users and trips'''
    __tablename__ = 'user_trips'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    user = db.relationship('User')
    trip = db.relationship('Trip')


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    first_name = db.Column(
        db.Text,
        nullable=False
    )

    last_name = db.Column(
        db.Text,
        nullable=False
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.Text,
        nullable=False
    )
    

    def __repr__(self):
        return f"<User #{self.id}: {self.first_name}, {self.last_name}, {self.email}>"

    @classmethod
    def signup(cls, first_name, last_name, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        # import pdb
        # pdb.set_trace()

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_pwd
        )

        return user

    @classmethod
    def authenticate(cls, email, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
