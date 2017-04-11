from ..database import db_session
from ..recipe_garden import app

CREATE = "INSERT INTO favorites (user_id, recipe_id) VALUES (?, ?)"
GET_FOR_USER_ID = "SELECT * FROM favorites WHERE user_id = ?"
GET_FOR_RECIPE = "SELECT * FROM favorites WHERE recipe_id = ?"

GET_USER: "SELECT * FROM users WHERE id = ?"

class Favorite:
    """Instance of a user favoriting a recipe"""
    def __init__(self, *dbargs):
        self.id = dbargs[0]
        self.user_id = dbargs[1]
        self.recipe_id = dbargs[2]

    def get_user(self):
        """Gets the corresponding user of this favorite"""
        from .user import User
        return User.get_by_id(self.user_id)

    @staticmethod
    def create(user_id, recipe_id):
        """Create a new favorite"""
        return Favorite(db_session.execute(CREATE, (user_id, recipe_id)))
