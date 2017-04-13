from sqlalchemy import text
from ..recipe_garden import get_db

class Direction:
    """A step to making a recipe"""
    def __init__(self, row):
        self.id = row['id']
        self.recipe_id = row['recipe_id']
        self.description = row['description']
        self.ordernum = row['ordernum']

        self.recipe = None

    def __str__(self):
        return self.description

    def get_recipe(self):
        """Gets the recipe this direction is for"""
        from .recipe import Recipe
        if not self.recipe:
            self.recipe = Recipe.get_by_id(self.recipe)
        return self.recipe
