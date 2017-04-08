from database import db_session
import recipe_garden.LOG as LOG

class User():
    """User representation in DB"""
    def __init__(self, id=0, name=None, email=None):
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)

    def from_db(**table):
        print("Creating user from %d", str(table))
        User(table['id'], table['name'], table['email'])

    @staticmethod
    def get_by_id(id_):
        return User(db_session.execute(
            "select * from users where user.id = ?", (id_,))
            .findone())
