"""Application entry point"""

import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_restful import Api

app = Flask(__name__) # create the application instance
app.config.from_object(__name__) # load config from this file, recipe_garden.py
api = Api(app)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE='/tmp/recipe-garden.db', #os.path.join(app.root_path, 'recipe-garden.db'),
    SECRET_KEY='wow-so-secret-very-key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('RECIPE_GARDEN_SETTINGS', silent=True)

# Import submodules - the imports are written here because they're modifying the `app` global.

#from .database import *

# Set up resources
from api.recipes import RecipesById, RecipesByName
from api.users import Users

api.add_resource(RecipesByName, '/recipes/named/<string:recipe_name>')
api.add_resource(RecipesById, '/recipes/<int:recipe_id>')
api.add_resource(Users, '/users/<int:user_id>')

if __name__ == "__main__":
    app.run()
