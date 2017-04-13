from ..recipe_garden import get_db

CREATE = "INSERT INTO favorites (user_id, recipe_id) VALUES (?, ?)"
GET_USER = "SELECT * FROM users WHERE id = ?"

class Favorite:
    """Instance of a user favoriting a recipe"""
    def __init__(self, row):
        self.id = row['id']
        self.user_id = row['user_id']
        self.recipe_id = row['recipe_id']
        # Cached lookup fields
        self.recipe = None
        self.user = None

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

    @staticmethod
    def create(user_id, recipe_id):
        """Create a new favorite"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute(CREATE, (user_id, recipe_id))
        favorite_id = cursor.rowid
        cursor.close()
        db.commit()
        return Favorite({ "id": favorite_id, "user_id": user_id, "recipe_id": recipe_id })
