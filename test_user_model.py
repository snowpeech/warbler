"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py

import os
from unittest import TestCase
from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database


os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app
from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
app.config['TESTING'] = True

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        user1 = User(email = "user1@u.com", username="user1", password="user123")
        user1id = 111
        user1.id=user1id
        user2 = User(email = "user2@u.com", username="user2", password="user123")
        user2id = 222
        user2.id = user2id
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()    

        u1 = User.query.get(user1id)
        u2 = User.query.get(user2id)

    #having u1 and u2 available on self makes it easier to test
        self.u1 = u1
        self.u2 = u2
        
        self.client = app.test_client()
    
    def tearDown(self):
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        
        db.session.rollback()


    def test_user_model(self):
        """Does basic model work?"""
        
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(u.image_url,"/static/images/default-pic.png")
        self.assertEqual(u.header_image_url,"/static/images/warbler-hero.jpg")
        self.assertEqual(repr(u),f"<User #{u.id}: {u.username}, {u.email}>")
        
    def test_user_following(self):
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertEqual(len(self.u2.following),0)
        self.assertEqual(len(self.u2.followers),1)
        self.assertTrue(self.u2.is_followed_by(self.u1))
        self.assertFalse(self.u2.is_following(self.u1))

        self.assertEqual(len(self.u1.following),1)
        self.assertEqual(len(self.u1.followers),0)
        self.assertFalse(self.u1.is_followed_by(self.u2))
        self.assertTrue(self.u1.is_following(self.u2))

        self.assertEqual(self.u2.followers[0].id, self.u1.id)
        self.assertEqual(self.u1.following[0].id, self.u2.id)

    def test_user_signup(self):
        q = User.query.filter_by(username="testname").first()
        self.assertIsNone(q)
        
        u = User.signup(username="testname", email="test@test.com", password="test123",image_url="testurl")
        
        q = User.query.filter_by(username="testname").first()
        self.assertIsNotNone(q)

    # def test_user_authenticates(self):
    #     a = User.authenticate(self.u1.username,"user123")
    #     self.assertIsNotNone(a)
    #   # invalid salt error. Not sure how to test this. Will return

    
        
    
        
