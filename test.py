import unittest
from main import app


# 200 - auth isnt required
# 302 - auth is required
class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_Home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'Redirecting...', response.data)


    def test_Login(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_Logout(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'Redirecting...', response.data)

    def test_Sign_Up(self):
        response = self.app.get('/sign-up')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)    

if __name__ == '__main__':
    unittest.main()