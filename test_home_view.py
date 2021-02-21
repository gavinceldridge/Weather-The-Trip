"""Test Home Page"""


import os
from unittest import TestCase
from sqlalchemy import exc

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///test_weather_the_trip"


from app import app


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        with app.app_context():
                
            db.drop_all()
            db.create_all()

            u1 = User.signup("first", "last", "email1@email.com", "password")
            db.session.add(u1)
            db.session.commit()

            u1 = User.query.get(1)

            self.u1 = u1
            self.uid1 = 1

            self.client = app.test_client()

    def tearDown(self):
        with app.app_context():
                
            res = super().tearDown()
            db.session.rollback()
            return res

    def test_home_view(self):
        """Basic test to ensure that the home page is returning html"""
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        self.assertIn('<a class="navbar-brand" href="/">Weather The Trip</a>', html)

    def test_logged_in_user_can_click_old_trips(self):

        user = User.authenticate(self.u1.email, self.u1.password)
        with app.app_context():
            with app.session_transaction as sess:
                sess['email'] = user.email
        
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        self.assertIn("<a class='nav-link' href='#'>Old Trips</a>", html)


