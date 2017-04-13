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
        return get_db().execute(GET_BY_ID, id=recipe_id).fetchone()

    @staticmethod
    def search_by_name(name):
        """Searches for recipes which are similar to the name"""
        # TODO turn into %stuff% regex safely
        return get_db().execute(SEARCH_BY_NAME, name=name)

    def get_steps(self):
        """Gets the steps of the recipe"""
        if not self.steps:
            self.steps = get_db().execute(GET_STEPS, id=self.id).findmany()
        return self.steps

    def list_ingredients(self):
        """Gets all of the ingredients of the recipe"""
        if not self.ingredients:
            self.ingredients = get_db().execute(GET_INGREDIENTS, id=self.id).findmany()
        return self.ingredients

    def get_shopping_list(self):
        """
        Gets a list of all the ingredients needed to shop for the recipe.
        This can be saved with ShoppingList.save()
        """
        pass
