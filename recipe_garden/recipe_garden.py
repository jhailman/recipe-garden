"""Application entry point"""

import sqlite3.dbapi2 as sqlite3

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
from flask_restful import Api

# These values are automatically added to the config
DB_PATH = '/tmp/recipe-garden.sqlite'

app = Flask(__name__) # create the application instance
app.config.from_object(__name__) # load the values set above into config
app.config.from_envvar('RECIPE_GARDEN_SETTINGS', silent=True) # Override with env var
api = Api(app) # Create REST API

def get_db(): # See flask tutorial `minitwit`
    """Gets an application-context-specific DB connection"""
    top = _app_ctx_stack.top
    if not hasattr(top, 'db'):
        top.db = sqlite3.connect(app.config['DB_PATH'])
        top.db.row_factory = sqlite3.Row
    return top.db


# Import stuff from common after creating `app` and `get_db`
from .common.user import User

# Set up database
def run_db_schema():
    """Run the schema to initialize the database"""
    app.logger.info("Initializing the database")
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as schema:
        db.executescript(schema.read())
    db.commit()

@app.teardown_appcontext
def shutdown_db(error):
    """Handler to close the DB at the end of application contexts"""
    get_db().close()

@app.route('/')
def main_page():
    user = User.get_by_id(1)
    return render_template("home.html.j2", user=user)

if __name__ == "recipe_garden.recipe_garden":
    # try:
    #     run_db_schema()
    # except Exception as err:
    #     # do nothing
    #     pass
    pass
