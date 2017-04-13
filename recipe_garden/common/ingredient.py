from ..recipe_garden import get_db
from sqlalchemy import text

GET = text("SELECT * FROM ingredient WHERE name = :name")
CREATE = text("INSERT INTO ingredient (name) VALUES (:name)")

class Ingredient:
    def __init__(self, row):
        self.name = row['name']

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @staticmethod
    def get_or_create(name):
        """Creates an ingredient if it does not exist"""
        name_lower = name.lower()
        db = get_db()
        prior = db.execute(GET, name=name_lower).fetchone()
        if prior == None:
            db.execute(CREATE, name=name_lower)
            return Ingredient(name_lower)
        else:
            return Ingredient(prior['name'])
