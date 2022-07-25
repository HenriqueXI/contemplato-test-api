"""User model"""
import uuid

from modules.main import MainModule
from modules.utils import decrypt


class User(object):
    """User"""

    _collection_name = 'User'

    def __init__(self, **args):
        self.id = args.get('id', uuid.uuid4().hex)
        self.name = args.get('name')
        self.email = args.get('email')
        self.password = args.get('password')

    def save(self):
        """Save User"""
        MainModule.get_firestore_db().collection(
            self._collection_name).document(self.id).set(self.to_dict())

    def to_dict(self):
        """Transform user in dict format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': decrypt(self.password)
        }

    @classmethod
    def get_user(cls, user_id):
        """Get User"""
        user = MainModule.get_firestore_db().collection(
            cls._collection_name).document(user_id).get()
        if user.exists:
            return User(**user.to_dict())
        return None

    @classmethod
    def get_user_by_email(cls, email):
        """Get User by params"""
        user = MainModule.get_firestore_db().collection(
            cls._collection_name).where(u'email', u'==', email).stream()
        return user

    @classmethod
    def get_users(cls):
        """Get users"""
        return MainModule.get_firestore_db().collection(
            cls._collection_name).limit(16).stream()
