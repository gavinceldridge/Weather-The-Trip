"""Seed file to generate basic data in DB"""

from models import User, Trip, Weather, UserTrip, TripWeather, db
from app import app

with app.app_context():

    # Create all tables
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    # User.query.delete()
    # Trip.query.delete()
    # Weather.query.delete()
    # UserTrip.query.delete()
    # TripWeather.query.delete()

    # Weather types: Rain, lightning, hail, snow,

    # Add users
    squirtle = User.signup(first_name='Squirtle', last_name='Gang',
                           email='test@test.com', password='password')

    squirtle_trip = Trip(
        starting_latitude='start lat',
        starting_longitude='start lon',
        ending_latitude='ending lat',
        ending_longitude='ending lon'
    )

    db.session.add_all([squirtle, squirtle_trip])

    db.session.commit()

    user_trip = UserTrip(user_id=squirtle.id, trip_id=squirtle_trip.id)

    db.session.add(user_trip)
    db.session.commit()

# pokemon_post=Post(title="Why Pokemon is sick", content="""
# Pokemon is a sicc game cuz it allows for you to grow with your pokemon and their success will mean your success.
# My favorite pokemon is squirtle.
# """, user_id=2)

# jakes_post = Post(title="Join State Farm!", content="If you join State Farm, I will give you all your capitalistic needs.", user_id=3)

# db.session.add_all([pokemon_post, jakes_post])
# db.session.commit()
