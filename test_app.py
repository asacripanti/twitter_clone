from app import app, db
import unittest
from models import User
from flask import session

class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        # self._db = db.get_db()

        db.create_all()
        User.query.delete()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_signup(self):

        with self.client as client:
            response = client.post('/signup', data={
                'username': 'testuser',
                'password': 'testpassword',
                'email': 'test@example.com',
                "image_url": "/static/images/default-pic.png"
            }, follow_redirects=True)


            self.assertEqual(response.status_code, 200)

    def test_login(self):

        with self.client as client:
            response = client.post('/login', data={
                'username': 'testuser',
                'password': 'testpassword'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)

    def test_logout(self):

        with self.client as client:

            client.post('/login', data={
                'username': 'testuser',
                'password': 'testpassword'
            }, follow_redirects=True)

            response = client.post('/logout', follow_redirects=True)

            self.assertEqual(response.status_code, 405)

if __name__ == "__main__":
    unittest.main()