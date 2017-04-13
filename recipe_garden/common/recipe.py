from ..recipe_garden import get_db
from sqlalchemy import text

GET_BY_ID = text("SELECT * FROM recipe WHERE id = :id")
SEARCH_BY_NAME = text("SELECT * FROM recipe WHERE name LIKE :name")
GET_INGREDIENTS = text("SELECT * FROM recipe_ingredient WHERE recipe_id = :id")
GET_STEPS = text("SELECT * FROM direction WHERE recipe_id = :id")


class Recipe:
    """Recipe"""
    def __init__(self, row):
        self.id = row['id']
        self.name = row['name']
        self.author_id = row['author_id']
        self.created = row['created']
        self.author = None
        self.steps = None
        self.ingredients = None

    def get_author(self):
        """Gets the corresponding author of this recipe"""
        from .user import User
        if not self.author:
            self.author = User.get_by_id(self.author_id)
        return self.author

    @staticmethod
    def get_by_id(recipe_id):
        """Gets a recipe with the corresponding ID"""
        return Recipe(get_db().execute(GET_BY_ID, id=recipe_id).fetchone())

    @staticmethod
    def search_by_name(name):
        """Searches for recipes which are similar to the name"""
        # TODO turn into %stuff% regex safely
        return Recipe(get_db().execute(SEARCH_BY_NAME, name=name))

    def get_directions(self):
        """Gets the steps of the recipe"""
        from .direction import Direction
        if not self.steps:
            self.steps = map(
                lambda step: Direction(step),
                get_db().execute(GET_STEPS, id=self.id).fetchall())
        return self.steps

    def get_ingredients(self):
        """Gets all of the ingredients of the recipe"""
        from .ingredient import RecipeIngredient
        if not self.ingredients:
            self.ingredients = map(
                lambda ingredient: RecipeIngredient(ingredient),
                get_db().execute(GET_INGREDIENTS, id=self.id).fetchall())
        return self.ingredients

    def get_shopping_list(self):
        """
        Gets a list of all the ingredients needed to shop for the recipe.
        This can be saved with ShoppingList.save()
        """
        pass
