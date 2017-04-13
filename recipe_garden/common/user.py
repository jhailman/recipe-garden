from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text
from ..recipe_garden import get_db

GET_BY_ID = text("SELECT * FROM user WHERE id = :id")

FIND_BY_EMAIL = text("SELECT * FROM user WHERE email = :email")
FIND_BY_NAME = text("SELECT * FROM user WHERE name = :name")
REGISTER = text("INSERT INTO user (name, email, password) VALUES (:name, :email, :password)")

GET_RECIPES = text("SELECT * FROM recipe WHERE user_id = :user_id")
GET_FAVORITES = text("SELECT * FROM favorite WHERE user_id = :user_id")
GET_SHOPPING_LISTS = text("SELECT * FROM shopping_list WHERE user_id = :user_id")

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
        self.shopping_lists = None

    def __repr__(self):
        return '<User %r (%r)>' % (self.name, self.email)

    @staticmethod
    def get_by_id(id_):
        """Gets a user with the given ID"""
        db = get_db()
        user_data = db.execute(GET_BY_ID, id=id_ ).fetchone()
        if user_data:
            return User(user_data)
        else:
            return None

    @staticmethod
    def find_by_email(email):
        db = get_db()
        user_data = db.execute(FIND_BY_EMAIL, email= email).fetchone()
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
        result = db.execute(REGISTER, name=name, email=email, password=hashed_pass)
        inserted_id = result.lastrowid
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
        pass

    def get_favorites(self):
        pass

    def get_shopping_lists(self):
        pass
