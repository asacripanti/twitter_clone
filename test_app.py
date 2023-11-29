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
                'email': 'test@example.com'
            }, follow_redirects=True)

            self.assertIn('curr_user', session)

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'100 most recent messages', response.data)

    def test_login(self):

        user = User.signup(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )
        db.session.commit()

        with self.client as client:
            response = client.post('/login', data={
                'username': 'testuser',
                'password': 'testpassword'
            }, follow_redirects=True)

            self.assertIn('curr_user', session)

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'100 most recent messages', response.data)

    def test_logout(self):

        user = User.signup(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )

        db.session.commit()

        with self.client as client:

            client.post('/login', data={
                'username': 'testuser',
                'password': 'testpassword'
            }, follow_redirects=True)

            response = client.get('/logout', follow_redirects=True)

            self.assertNotIn('curr_user', session)

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Log in to Warbler', response.data)

if __name__ == "__main__":
    unittest.main()