"""Arquivo main da API"""
import firebase_admin

from flask import Flask
from flask_restful import Resource, Api
from flask import request
from flask_cors import CORS
from view.user import UserSignInHandler, UsersHandler
from view.user_task import UserTasksHandler


app = Flask(__name__)
CORS(app)
API = Api(app)

cred = firebase_admin.credentials.Certificate(
    './contemplato-tec-test-firebase-adminsdk-lqwt0-2075194858.json')
firebase_admin.initialize_app(credential=cred)

@app.before_request
def start_request():
    """Start api request"""
    if request.method == 'OPTIONS':
        return '', 200
    if not request.endpoint:
        return 'Sorry, Nothign at this URL.', 404


class Index(Resource):
    """ class return API index """

    def get(self):
        """return API"""
        return {"API": "Contemplato-tec-test"}


API.add_resource(Index, '/', endpoint='index')
API.add_resource(UsersHandler, '/users', endpoint='users')
API.add_resource(UserTasksHandler, '/user-task/<user_id>', endpoint='user-task')
API.add_resource(UserSignInHandler, '/user-sign-in', endpoint='user-sign-in')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
