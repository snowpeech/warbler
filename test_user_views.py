"""Message View tests."""
import os
from unittest import TestCase
from flask import Flask, session

from models import db, connect_db, Message, User, Likes, Follows

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

    # def test_show_signup_user_page(self):
    #     """Can a new user sign up?"""
    #     with self.client as c:
    #         resp = c.get("/signup")
    #         html = resp.get_data(as_text=True)
            
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('<h2 class="join-message">Join Warbler today.</h2>', html)

    # def test_signup_user(self):
    #     """Can a new user sign up?"""
    #     with self.client as c:
    #         resp = c.post("/signup", data = {"username":"u1", "password":"test123","email":"u1@test.com"})
    #         self.assertEqual(resp.status_code, 302)
    #         q = User.query.all()
    #         self.assertEqual(len(q),2)

    # def test_login_user(self):
    #     """Test user login"""
    #     with self.client as c:
    #         resp = c.post("/login", data = {"username":"testuser", "password":"testuser"})

    #         self.assertEqual(resp.status_code, 302)
    #         self.assertEqual(session[CURR_USER_KEY], self.testuser.id)

# ***doesn't work below******************************************
    # def test_logout_user(self):
    #     """Test user logout"""
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser.id
    #         resp = c.get('/logout')
            
    #         self.assertIsNone(sess[CURR_USER_KEY])
# ***********************************************

    def test_user_profile(self):
        """Test user profile page and search"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp=c.get("/users?q=test")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<a href="/users/{self.testuser.id}">',html)
    
    def setup_users(self):
        """set up other users for testuser"""
        u1 = User(username="user1",email="user1@test.com",password="test123")
        u1.id=1111
        self.u1=u1

        u2=User(username='user2', email='user2@test.com',password='test123')
        u2.id=2222
        self.u2=u2
        db.session.add_all([u1,u2])
        db.session.commit()


    # def setup_likes(self):
    #     """set up messages with likes for testuser"""
    #     self.setup_users()

    #     m1 = Message(text="message 1 by me", user_id=self.testuser.id)
    #     m2 = Message(text="message 2 by someone else, u1", user_id=self.u1.id)
    #     m2.id =2000
    #     m3 = Message(text="message 3 by someone else", user_id=self.u1.id)
    #     m3.id=3000
    #     db.session.add_all([m1,m2,m3])
    #     db.session.commit()

    #     l1 = Likes(user_id=self.testuser.id, message_id=2000)
    #     db.session.add(l1)
    #     db.session.commit()
    
    # def test_like_users_message(self):
    #     """show user's liked messages"""
    #     self.setup_likes()
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser.id

    #         resp=c.post("/users/like/3333")
            
    #         self.assertEqual(resp.status_code, 302)
    #         likes = Likes.query.all()
    #         self.assertEqual(len(likes),2)
    #         self.assertEqual(likes[1].user_id, self.testuser.id)
            
    # def test_unlike_message(self):
    #     """un-like a message"""
    #     self.setup_likes()
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser.id
    #         resp=c.post("/users/like/2222")
    #         self.assertEqual(resp.status_code, 302)
    #         likes = Likes.query.all()
    #         self.assertEqual(len(likes),0)

    # def test_show_liked_messages(self):
    #     """show users liked messages"""
    #     self.setup_likes()
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser.id
    #         resp=c.get("/users/1111/liked_messages")
            
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('<a href="/users/1111">@user1</a>', html)
# ***********************************************
    
    def setup_follows(self):
        """setup followers/following for testuser"""
        self.setup_users()
        # i'm following u1. 
        f1 = Follows(user_being_followed_id=self.u1.id, user_following_id= self.testuser.id)

        #u2 follows me
        f2 = Follows(user_being_followed_id=self.testuser.id, user_following_id= self.u2.id)

        db.session.add_all([f1,f2])
        db.session.commit()

        self.testuser_id=1234

    def test_show_followers(self):
        """show users following testuser """
        self.setup_follows()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get("/users/1234/following")
            html = resp.get_data(as_text=True)

            self.assertEquals(resp.status_code,200)
            self.assertIn('@user1',html)
            self.assertIn('action="/users/stop-following/1111"',html)
    
    def test_show_following(self):
        """show users testuser is following"""
        self.setup_follows()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get("/users/1234/followers") 
            html = resp.get_data(as_text=True)

            self.assertEquals(resp.status_code,200)
            self.assertIn('@user2',html)
            self.assertIn('action="/users/follow/2222"',html)

    def test_follow_user(self):
        """follow a user"""
        self.setup_follows()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/users/follow/2222")
            self.assertEquals(resp.status_code,302)
            following = Follows.query.filter_by(user_following_id=self.testuser.id).all()
            self.assertEqual(len(following),2)       
    
    
    def test_stop_following_user(self):
        """stop following a user"""
        self.setup_follows()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/users/stop-following/1111")
            
            self.assertEquals(resp.status_code,302)
            following = Follows.query.filter_by(user_following_id=self.testuser.id).one_or_none()
            self.assertIsNone(following)

    #     # have user follow another user - need to have someone I'm not following (u2 is not in the follow pic)

    
    # def test_delete_user(self):
    #     """test deleting a user"""
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser.id
    #         resp=c.post('/users/delete')
    #         self.assertIsNone(g.user)
    #  NameError: "g" is not defined

