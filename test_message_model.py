"""User message tests."""

import os
from unittest import TestCase
from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"
from app import app

app.config['TESTING'] = True

db.create_all()

class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        user1 = User(email = "user1@u.com", username="user1", password="user123")
        user1id = 111
        user1.id=user1id
        db.session.add(user1)
        db.session.commit()    

        self.u1 = User.query.get(user1id)
        
        self.client = app.test_client()
    
    def tearDown(self):
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        
        db.session.rollback()
    
    def test_create_message(self):
        m = Message(text="test", user_id = self.u1.id)
        db.session.add(m)
        db.session.commit()
        msg = Message.query.filter_by(user_id=self.u1.id).first()
        self.assertEqual(msg.text,'test')
        self.assertEqual(msg.user_id, self.u1.id)

    # def test_invalid_message(self):
    #     """ need to implement some error checking before trying this"""
    #     text = str([num for num in range(60)])
    #     m = Message(text=text, user_id=self.u1.id)
    #     db.session.add(m)
    #     db.session.commit()
    #     msg = Message.query.filter_by(user_id=self.u1.id).first()
        