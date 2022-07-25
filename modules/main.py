"""Main module"""
from firebase_admin import firestore


class MainModule(object):
    """Main module"""

    @staticmethod
    def get_firestore_db():
        """Get firestore db instance"""
        return firestore.client()
