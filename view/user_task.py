"""Users tasks view"""
from flask_restful import Resource
from flask import request
from models.user_task import UserTask
from modules.user_task import UserTaskModule


class UserTasksHandler(Resource):
    """Users Tasks handler"""

    def get(self, user_id):
        """Get User tasks"""
        try:
            response = {"user_tasks": []}
            user_tasks = UserTask.get_user_tasks(user_id)

            for task in user_tasks:
                response['user_tasks'].append(task.to_dict())

            return response

        except Exception as error:
            return {
              'message': 'Error on get Users Tasks',
              'details': str(error)
            }, 500

    def post(self, user_id):
        """Create a new user task"""
        try:
            if not request.json:
                return {"message": "Bad request not params for user task create"}, 400

            user_task = UserTaskModule.create(request.json, user_id)

            return user_task.to_dict()

        except Exception as error:
            return {
              'message': 'Error on create a new user task',
              'details': str(error)
            }, 500
