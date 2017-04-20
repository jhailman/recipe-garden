from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text
from ..recipe_garden import get_db
from recipe import Recipe

GET_BY_ID = text("SELECT * FROM user WHERE id = :id")

FIND_BY_EMAIL = text("SELECT * FROM user WHERE email = :email")
FIND_BY_NAME = text("SELECT * FROM user WHERE name = :name")
REGISTER = text("INSERT INTO user (name, email, password) VALUES (:name, :email, :password)")

GET_RECIPES = text("SELECT * FROM recipe WHERE user_id = :user_id")
GET_FAVORITES = text("SELECT * FROM favorites WHERE user_id = :user_id")
GET_SHOPPING_LIST = text("SELECT * FROM shopping_list WHERE user_id = :user_id")

INSERT_FAVORITE = text("INSERT INTO favorites (user_id, recipe_id) VALUES (:uid, :rid)")
DELETE_FAVORITE = text("DELETE FROM favorites WHERE recipe_id = :recipe_id")

class User:
    """User representation in DB and static methods for access"""
    def __init__(self, row):
        self.id = row['id']
        self.name = row['name']
        self.email = row['email']
        self.password = row['password']
        # Cached fields
        self.recipes = None
        self.favorites = None
        self.shopping_list = None

    def __repr__(self):
        return '<User %r (%r)>' % (self.name, self.email)

    def __eq__(self, other):
        return self.id == other.id

    @staticmethod
    def get_by_id(id_):
        """Gets a user with the given ID"""
        user_data = get_db().execute(GET_BY_ID, id=id_ ).fetchone()
        if user_data:
            return User(user_data)
        else:
            return None

    @staticmethod
    def find_by_email(email):
        user_data = get_db().execute(FIND_BY_EMAIL, email= email).fetchone()
        if user_data:
            return User(user_data)
        else:
            return None

    @staticmethod
    def register(name, email, clearpass):
        """
        Attempts to register a user with the given name, email, and passsword.
        Throws an `Exception` if a user with that email already exists.
        """
        if User.find_by_email(email):
            raise Exception("A user with that email already exists.")

        hashed_pass = generate_password_hash(clearpass)
        db = get_db()
        inserted_id = db.execute(REGISTER, name=name, email=email, password=hashed_pass).lastrowid
        return User({ "id": inserted_id, "name": name, "email": email, "password": "" })

    @staticmethod
    def login(email, clearpass):
        """
        Attempts to authenticate as a user with given email and password.
        Returns the `User` object if the password is correct.
        Throws an `Exception` for invalid email or invalid password.
        The difference between the two should be kept secret from the user, however.
        """
        user = User.find_by_email(email)
        if not user:
            raise Exception("Invalid email %s" % email)
        if not check_password_hash(user.password, clearpass):
            raise Exception("Invalid password for %s" % email)
        return user

    def get_recipes(self):
        """Gets the recipes created by the user"""
        if not self.recipes:
            self.recipes = get_db().execute(GET_RECIPES, user_id=self.id).fetchall()
        return self.recipes

    def get_favorites(self):
        """Gets the user's favorite recipes"""
        if not self.favorites:
            self.favorites = []
            all_rows = get_db().execute(GET_FAVORITES, user_id=self.id).fetchall()
            for row in all_rows:
                self.favorites.append(Recipe.get_by_id(row['recipe_id']))
        return self.favorites

    def add_favorite(self, recipe_id):
        """Adds a recipe to a user's favorite recipes"""
        if not self.favorites:
            self.favorites = [Recipe.get_by_id(recipe_id)]
        else:
            self.favorites.append(recipe_id)

        get_db().execute(INSERT_FAVORITE, uid=self.id, rid=recipe_id)

    def remove_favorite(self, recipe_id):
        """Removes a recipe from a user's favorite recipes"""
        self.get_favorites()
        self.favorites.remove(Recipe.get_by_id(recipe_id))
        get_db().execute(DELETE_FAVORITE, recipe_id=recipe_id)

    def get_shopping_list(self):
        """Gets the user's shopping list"""
        if not self.shopping_list:
            self.shopping_list = get_db().execute(GET_SHOPPING_LIST, user_id=self.id).fetchall()
        return self.shopping_list
