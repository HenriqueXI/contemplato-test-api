""" User Task Module """
from models.user_task import UserTask


class UserTaskModule(object):
    """User task module"""

    @staticmethod
    def create(params, user_id):
        """
        Create new user task
        :param params: user task dict
        return user_task: UserTask
        """
        user_task = UserTask()
        user_task.name = params['name']
        user_task.user_id = user_id
        user_task.save()

        return user_task
