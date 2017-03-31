from flask import request
from flask_restful import Resource

class RecipeResource(Resource):
    def get(self):
        return { 'name': 'MyRecipe' }
