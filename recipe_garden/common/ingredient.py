from ..recipe_garden import get_db, app
from sqlalchemy import text

GET_BY_ID = text("SELECT * FROM recipe_ingredient WHERE id = :id")
ENSURE_INGREDIENT = text("INSERT IGNORE INTO ingredient (name) VALUES (:ingredient)")
ADD_INGREDIENT = text("INSERT INTO recipe_ingredient (recipe_id, ingredient, amount) VALUES (:recipe_id, :ingredient, :amount)")

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

    @staticmethod
    def add_to_recipe(recipe_id, amount, ingredient):
        db = get_db()
        db.execute(ENSURE_INGREDIENT, ingredient=ingredient)
        db.execute(ADD_INGREDIENT, recipe_id=recipe_id, amount=amount, ingredient=ingredient)

    def get_recipe(self):
        from .recipe import Recipe
        if not self.recipe:
            self.recipe = Recipe.get_by_id(self.recipe_id)
        return self.recipe
