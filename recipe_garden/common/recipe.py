from ..recipe_garden import get_db

GET_BY_ID = "SELECT * FROM recipe WHERE id = ?"

class Recipe:
    """Recipe"""
    def __init__(self, row):
        self.id = row['id']
        self.name = row['name']
        self.author_id = row['author_id']
        self.created = row['created']
        self.author = None

    def get_author(self):
        """Gets the corresponding author of this recipe"""
        from .user import User
        if not self.author:
            self.author = User.get_by_id(self.author_id)
        return self.author

    @staticmethod
    def get_by_id(recipe_id):
        """Gets a recipe with the corresponding ID"""
        pass

    @staticmethod
    def search_by_name(name):
        """Searches for recipes which are similar to the name"""
        pass

    def get_steps(self):
        """Gets the steps of the recipe"""
        pass

    def list_ingredients(self):
        """Gets all of the ingredients of the recipe"""
        pass

    def get_shopping_list(self):
        """
        Gets a list of all the ingredients needed to shop for the recipe.
        This can be saved with ShoppingList.save()
        """
        pass
