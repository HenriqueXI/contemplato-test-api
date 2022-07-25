""" User Module """
from models.user import User
from modules.utils import encripty


class UserModule(object):
    """User module"""

    @staticmethod
    def create(params):
        """
        Create new user
        :param params: user dict
        return user: User
        """
        user = User()
        user.name = params['name']
        user.email = params['email']

        enc_password = encripty(params['password'])
        user.password = enc_password

        user.save()

        return user
