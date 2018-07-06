import unittest
import uuid
import json, os, sys
from passlib.hash import sha256_crypt
from base import BaseTestCase

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import models


class authTestCase(BaseTestCase):

    def setUp(self):
        models.db.drop_all()
        models.db.create_all()

        self.role = models.Role(name="regular")
        self.role.save()

        self.user_1 = models.User(
            name="Joseph Cobhams",
            email="joseph.cobhams@andela.com",
            password=sha256_crypt.hash('andela')
        )
        self.user_1.save()

    def test_user_created_successfully(self):
        response = self.client.post('/api/v1/auth/signup', data=json.dumps({
            "name": "usman baba",
            "email": "usman.baba@andela.com",
            "password": "andela"
        }), content_type="application/json")
        response_data = json.loads(response.data)

        self.assertEqual(response_data['data']['user']['name'], "usman baba")
        self.assert_status(response, 201)

    def test_user_logged_in_successfully(self):
        response = self.client.post('/api/v1/auth/login', data=json.dumps({
            "email": "joseph.cobhams@andela.com",
            "password": "andela"
        }), content_type="application/json")
        response_data = json.loads(response.data)

        self.assertTrue('access_token' in response_data['data'])
        self.assertEqual(response_data['data']['message'], "User loggedin successfully")
        self.assert_status(response, 200)



if __name__ == '__main__':
    unittest.main()