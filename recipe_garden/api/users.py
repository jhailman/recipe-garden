from flask import request
from flask_restful import Resource

class Users(Resource):
    def get(self, user_id):
        return { 'name': "User", 'id': user_id }
