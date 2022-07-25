"""User Task model"""
import uuid

from modules.main import MainModule


class UserTask(object):
    """User Task"""

    _collection_name = 'UserTask'

    def __init__(self, **args):
        self.id = args.get('id', uuid.uuid4().hex)
        self.name = args.get('name')
        self.user_id = args.get('user_id')

    def save(self):
        """Save User Task"""
        MainModule.get_firestore_db().collection(
            self._collection_name).document(self.id).set(self.to_dict())

    def to_dict(self):
        """Transform user task in dict format"""
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id
        }

    @classmethod
    def get_user_tasks(cls, user_id):
        """
        Get users tasks
        :params str user_id: User id
        """
        return MainModule.get_firestore_db().collection(
            cls._collection_name).where('user_id', u'==', user_id).limit(16).stream()
