from ..recipe_garden import get_db
from sqlalchemy import text

GET_BY_ID = text("SELECT * FROM favorite WHERE id = :id")
CREATE = text("INSERT INTO favorite (user_id, recipe_id) VALUES (:user_id, :recipe_id)")

class Favorite:
    """Instance of a user favoriting a recipe"""
    def __init__(self, row):
        self.id = row['id']
        self.user_id = row['user_id']
        self.recipe_id = row['recipe_id']
        # Cached lookup fields
        self.recipe = None
        self.user = None

    @staticmethod
    def get_by_id(id):
        return Favorite(get_db().execute(GET_BY_ID, id=id).fetchone())

    @staticmethod
    def create(user_id, recipe_id):
        """Create a new favorite"""
        favorite_id = get_db().execute(CREATE, user_id=user_id, recipe_id=recipe_id).rowid
        return Favorite({ "id": favorite_id, "user_id": user_id, "recipe_id": recipe_id })

    def get_user(self):
        """Gets the corresponding user of this favorite"""
        from .user import User
        if not self.user:
            self.user = User.get_by_id(self.user_id)
        return self.user

    def get_recipe(self):
        """Gets the corresponding recipe of this favorite"""
        from .recipe import Recipe
        if not self.recipe:
            self.recipe = Recipe.get_by_id(self.recipe_id)
        return self.recipe
