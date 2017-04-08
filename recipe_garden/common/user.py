from recipe_garden.database import db_session

class User():
    """User representation in DB"""
    def __init__(self, id=0, name=None, email=None):
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)

    def from_db(**table):
        User(table['id'], table['name'], table['email'])

class Users():
    """Queries to run on users"""

    @staticmethod
    def get_by_id(id):
        db_session.execute("select * from users where user.id = 1");
        return User(1)
        # return User(db_session.execute(
            # "select * from users where user.id = 1", id))
