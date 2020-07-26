"""Message View tests."""
import os
from unittest import TestCase
from flask import Flask, session

from models import db, connect_db, Message, User

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for user routes."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
        email="test@test.com",
        password="testuser",
        image_url=None)

        self.testuser.id=1234

        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_show_signup_user_page(self):
        """Can a new user sign up?"""
        with self.client as c:
            resp = c.get("/signup")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2 class="join-message">Join Warbler today.</h2>', html)

    def test_signup_user(self):
        """Can a new user sign up?"""
        with self.client as c:
            resp = c.post("/signup", data = {"username":"u1", "password":"test123","email":"u1@test.com"})
            self.assertEqual(resp.status_code, 302)
            q = User.query.all()
            self.assertEqual(len(q),2)

    def test_login_user(self):
        """Can a new user sign up?"""
        with self.client as c:
            resp = c.post("/login", data = {"username":"testuser", "password":"testuser"})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(session[CURR_USER_KEY], self.testuser.id)
    
            

        # # Since we need to change the session to mimic logging in, we need to use the changing-session trick:

        # with self.client as c:
        #     with c.session_transaction() as sess:
        #         sess[CURR_USER_KEY] = self.testuser.id

        #     # Now, that session setting is saved, so we can have
        #     # the rest of ours test

        #     resp = c.post("/messages/new", data={"text": "Hello"})

        #     # Make sure it redirects
        #     self.assertEqual(resp.status_code, 302)

        #     msg = Message.query.one()
        #     self.assertEqual(msg.text, "Hello")

