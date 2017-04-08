from ..recipe_garden import app, get_db

GET_BY_ID = "SELECT * FROM users WHERE id = ?"
FIND_BY_EMAIL = "SELECT * FROM users WHERE email = ?"
FIND_BY_NAME = "SELECT * FROM users WHERE name = ?"
CHECK_PASSWORD = ""

class User():
    """User representation in DB and static methods for access"""
    def __init__(self, row):
        self.id = row['id']
        self.name = row['name']
        self.email = row['email']

    def __repr__(self):
        return '<User %r (%r)>' % (self.name, self.email)

    @staticmethod
    def get_by_id(id_):
        """Gets a user with the given ID"""
        cursor = get_db().cursor()
        user_data = cursor.execute(GET_BY_ID, (id_,)).fetchone()
        cursor.close()
        return User(user_data)

    @staticmethod
    def find_by_email(email):
        cursor = get_db().cursor()
        user_data = cursor.execute(FIND_BY_EMAIL, (email,)).fetchone()
        cursor.close()
        return User(user_data)
