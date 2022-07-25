"""Test user task"""
import unittest

from main import app

from mock import patch
from mockfirestore import MockFirestore

from models.user import User
from models.user_task import UserTask
from modules.utils import encripty


class TestUserTask(unittest.TestCase):
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

        return user

    @staticmethod
    def create_user_task(name, user_id):
        """
        Create user task
        :params str name: Task name
        :params str user_id: User id
        """
        user_task = UserTask()
        user_task.name = name
        user_task.user_id = user_id
        user_task.save()

    def test_post_user_task(self):
        """ test create user task """
        user = self.create_user('Herique Dellosso', '12345')
        task_params = {"name": "Concluir API"}

        response = self.app.post(
            path='/user-task/{}'.format(user.id), json=task_params)
        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        self.assertIsNotNone(response_json['id'])
        self.assertEqual(response_json['name'], task_params['name'])
        self.assertEqual(response_json['user_id'], user.id)

    def test_get_user_task(self):
        """ test get user task """
        user = self.create_user('Herique Dellosso', '12345')
        task_name = 'API'
        for _ in range(0, 2):
            self.create_user_task(task_name, user.id)
            task_name = 'client'

        response = self.app.get(path='/user-task/{}'.format(user.id))
        self.assertEqual(len(response.get_json()['user_tasks']), 2)

        response = self.app.get(path='/user-task/random_id')
        self.assertEqual(len(response.get_json()['user_tasks']), 0)
