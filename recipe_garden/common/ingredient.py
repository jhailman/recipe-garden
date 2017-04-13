from ..recipe_garden import get_db

GET = "SELECT * FROM ingredient WHERE name = ?"
CREATE = "INSERT INTO ingredient (name) VALUES (?)"

class Ingredient:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


    @staticmethod
    def get_or_create(name):
        """Creates an ingredient if it does not exist"""
        name_lower = name.lower()
        db = get_db()
        cursor = db.cursor()
        prior = cursor.execute(GET, (name_lower,))
        if prior == None:
            cursor.execute(CREATE, (name_lower,))
            cursor.close()
            db.commit()
            return Ingredient(name_lower)
        else:
            cursor.close()
            return Ingredient(prior['name'])
