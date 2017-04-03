from flask import request
from flask_restful import Resource

class RecipesById(Resource):
    def get(self, recipe_id):
        return { 'name': 'MyRecipe', 'id': recipe_id }

class RecipesByName(Resource):
    def get(self, recipe_name):
        return { 'name': recipe_name }
