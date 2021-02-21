"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///test_weather_the_trip"



from app import app


class UserModelTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""
        with app.app_context():
                
            db.drop_all()
            db.create_all()

            u1 = User.signup("first", "last", "email1@email.com", "password")
            u1.id = 1

            u2 = User.signup("first", "last", "email2@email.com", "password")
            u2.id = 2
            db.session.commit()

            u1 = User.query.get(1)
            u2 = User.query.get(2)

            self.u1 = u1
            self.uid1 = 1

            self.u2 = u2
            self.uid2 = 2

            self.client = app.test_client()

    def tearDown(self):
        with app.app_context():
                
            res = super().tearDown()
            db.session.rollback()
            return res


    def test_user_model_pw_encryption(self):
        """Does basic model work?"""
        with app.app_context():
                
            user = User.signup(
                first_name="firstname",
                last_name="lastname",
                email="test@test.com",
                password="HASHED_PASSWORD"
            )

            db.session.add(user)
            db.session.commit()
            self.assertNotEqual('HASHED_PASSWORD', user.password)



        




        

