from werkzeug.security import check_password_hash, generate_password_hash
from ..recipe_garden import get_db

GET_BY_ID = "SELECT * FROM users WHERE id = ?"
FIND_BY_EMAIL = "SELECT * FROM users WHERE email = ?"
FIND_BY_NAME = "SELECT * FROM users WHERE name = ?"
REGISTER = "INSERT INTO users (name, email, password) VALUES (?, ?, ?)"

class User:
    """User representation in DB and static methods for access"""
    def __init__(self, row):
        self.id = row['id']
        self.name = row['name']
        self.email = row['email']
        self.password = row['password']

    def __repr__(self):
        return '<User %r (%r)>' % (self.name, self.email)

    @staticmethod
    def get_by_id(id_):
        """Gets a user with the given ID"""
        cursor = get_db().cursor()
        user_data = cursor.execute(GET_BY_ID, (id_,)).fetchone()
        cursor.close()
        if user_data:
            return User(user_data)
        else:
            return None

    @staticmethod
    def find_by_email(email):
        cursor = get_db().cursor()
        user_data = cursor.execute(FIND_BY_EMAIL, (email,)).fetchone()
        cursor.close()
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
        cursor = get_db().cursor()
        cursor.execute(REGISTER, (name, email, hashed_pass))
        inserted_id = cursor.lastrowid
        cursor.close()
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
