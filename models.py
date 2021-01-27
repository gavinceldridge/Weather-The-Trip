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

    id = db.Column(db.Integer, primary_key=True)

    starting_longitude = db.Column(db.Text, nullable=False)
    starting_latitude = db.Column(db.Text, nullable=False)
    ending_longitude = db.Column(db.Text, nullable=False)
    ending_latitude = db.Column(db.Text, nullable=False)

    # weathers = db.relationship(
    #     'Weather', secondary='trip_weathers', backref='trips')


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    trips = db.relationship('Trip', secondary='user_trips', backref='users')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Weather(db.Model):

    __tablename__ = 'weathers'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)


class TripWeather(db.Model):

    __tablename__ = 'trip_weathers'
    id = db.Column(db.Integer, primary_key=True)
    weather_id = db.Column(
        db.Integer, db.ForeignKey('weathers'), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips'), nullable=False)


class UserTrip(db.Model):
    '''relationship between users and trips'''
    __tablename__ = 'user_trips'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users'), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips'), nullable=False)
