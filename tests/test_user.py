"""Test user"""
import unittest

from main import app

from mock import patch
from mockfirestore import MockFirestore

from models.user import User
from modules.utils import encripty


class TestUser(unittest.TestCase):
    """Test user"""

    def setUp(self):
        self.mock_db = MockFirestore()
        self.patcher = patch(
            'modules.main.MainModule.get_firestore_db', return_value=self.mock_db)
        self.patcher.start()
        self.app = app.test_client()

    def tearDown(self):
        self.patcher.stop()
        self.mock_db.reset()

    @staticmethod
    def create_user(name, password):
        """
        Create user
        :params str name: User name
        :params str password: User password
        """
        user = User()
        user.name = name
        user.email = 'contemplato@contemplato.com'
        user.password = encripty(password)
        user.save()

    def test_save_and_get_user(self):
        """Test save and get user"""
        new_user = User()
        new_user.name = 'Henrique'
        new_user.password = encripty('123456')
        new_user.save()

        user = User.get_user(new_user.id)
        self.assertEqual(user.name, 'Henrique')
        self.assertEqual(user.password, '123456')
        self.assertEqual(user.id, new_user.id)

    def test_post_user(self):
        """ test post user """
        response = self.app.post(path='/users', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()['message'], "Bad request not params for user create")

        user_params = {
            'name': 'Herique Dellosso dos Santos',
            'email': 'henriquedellosso@gmail.com',
            'password': '12345'
        }

        response = self.app.post(path='/users', json=user_params)

        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        self.assertIsNotNone(response_json)
        self.assertIsNotNone(response_json['id'])
        self.assertEqual(response_json['name'], user_params['name'])
        self.assertEqual(response_json['email'], user_params['email'])
        self.assertEqual(
            response_json['password'], user_params['password'])

        response = self.app.post(path='/users', json=user_params)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()['message'], "E-mail already registered")

    def test_get_users(self):
        """ test get users """
        name = 'Henrique Dellosso'
        password = '12345'
        for _ in range(0, 2):
            self.create_user(name, password)
            name = "Roberto Silva"
            password = "54321"

        response = self.app.get(path='/users')
        self.assertEqual(len(response.get_json()['users']), 2)

    def test_user_sign_in(self):
        """ Test user sign in """
        user_params = {
            'name': 'Herique Dellosso dos Santos',
            'email': 'henriquedellosso@gmail.com',
            'password': '12345'
        }

        response = self.app.post('/user-sign-in', json=user_params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {})

        self.app.post(path='/users', json=user_params)
        response = self.app.post('/user-sign-in', json=user_params)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.get_json()['id'])
