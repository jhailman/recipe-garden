from ..recipe_garden import get_db
from sqlalchemy import text
from datetime import datetime

GET_BY_ID = text("SELECT * FROM recipe WHERE id = :id")
SEARCH_BY_NAME = text("SELECT * FROM recipe WHERE name LIKE :name")
GET_INGREDIENTS = text("SELECT * FROM recipe_ingredient WHERE recipe_id = :id")
GET_STEPS = text("SELECT * FROM direction WHERE recipe_id = :id")
GET_RANGE = text("SELECT * FROM recipe ORDER BY created DESC LIMIT :start, :num")
GET_BY_AUTHOR = text("SELECT * FROM recipe WHERE author_id = :id")

CREATE = text("INSERT INTO recipe (name, author_id, image_path) VALUES (:name, :author_id, :image_path)")
ADD_STEP = text("INSERT INTO direction (recipe_id, description, ordernum) VALUES (:recipe_id, :description, :ordernum)")

class Recipe:
    """Recipe"""
    def __init__(self, row):
        self.id = row['id']
        self.name = row['name']
        self.author_id = row['author_id']
        self.created = row['created']
        self.image_path = row['image_path']
        self.author = None
        self.steps = None
        self.ingredients = None

    def __eq__(self, other):
        return self.id == other.id

    def get_author(self):
        """Gets the corresponding author of this recipe"""
        from .user import User
        if not self.author:
            self.author = User.get_by_id(self.author_id)
        return self.author

    @staticmethod
    def get_by_id(recipe_id):
        """Gets a recipe with the corresponding ID"""
        recipe_data = get_db().execute(GET_BY_ID, id=recipe_id).fetchone()
        if recipe_data:
            return Recipe(recipe_data)
        else:
            return None

    @staticmethod
    def search_by_name(name):
        """Searches for recipes which are similar to the name"""
        # TODO turn into %stuff% regex safely
        return Recipe(get_db().execute(SEARCH_BY_NAME, name=name))

    @staticmethod
    def get_by_range(start, num):
        """Gets a range of recipes, sorted by most recent first"""
        all_rows = get_db().execute(GET_RANGE, start=start, num=num).fetchall()
        all_recipes = []
        for row in all_rows:
            all_recipes.append(Recipe(row))
        return all_recipes

    @staticmethod
    def get_by_author(uid):
        all_rows = get_db().execute(GET_BY_AUTHOR, id=uid).fetchall()
        all_recipes = []
        for row in all_rows:
            all_recipes.append(Recipe(row))
        return all_recipes

    def create(name, author_id, image_path):
        id = get_db().execute(CREATE, author_id=author_id, name=name, image_path=image_path).lastrowid
        return Recipe({ 'id': id, 'author_id': author_id, 'name': name, 'image_path': image_path, 'created': datetime.now() })

    def add_ingredient(self, amount, ingredient):
        from .ingredient import RecipeIngredient
        RecipeIngredient.add_to_recipe(self.id, amount, ingredient)

    def add_step(self, description, count):
        get_db().execute(ADD_STEP, recipe_id=self.id, description=description, ordernum=count)

    def get_directions(self):
        """Gets the steps of the recipe"""
        from .direction import Direction
        if not self.steps:
            self.steps = map(
                lambda step: Direction(step),
                get_db().execute(GET_STEPS, id=self.id).fetchall())
        return self.steps

    def get_ingredients(self):
        """Gets all of the ingredients of the recipe"""
        from .ingredient import RecipeIngredient
        if not self.ingredients:
            self.ingredients = map(
                lambda ingredient: RecipeIngredient(ingredient),
                get_db().execute(GET_INGREDIENTS, id=self.id).fetchall())
        return self.ingredients
