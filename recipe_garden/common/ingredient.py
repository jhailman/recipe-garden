from ..recipe_garden import get_db, app
from sqlalchemy import text

GET_BY_ID = text("SELECT * FROM recipe_ingredient WHERE id = :id")

class RecipeIngredient:
    def __init__(self, row):
        app.logger.debug(row)
        self.id = row['id']
        self.recipe_id = row['recipe_id']
        self.ingredient = row['ingredient']
        self.amount = row['amount']

        self.recipe = None

    def __repr__(self):
        return "%s %s" % (self.amount, self.ingredient)

    @staticmethod
    def get_by_id(id):
        return RecipeIngredient(get_db().execute(GET_BY_ID, id=id).fetchone())

    def get_recipe(self):
        from .recipe import Recipe
        if not self.recipe:
            self.recipe = Recipe.get_by_id(self.recipe_id)
        return self.recipe
