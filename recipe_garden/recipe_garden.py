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
    DATABASE_PATH='/tmp/recipe-garden.db', #os.path.join(app.root_path, 'recipe-garden.db'),
    SECRET_KEY='wow-so-secret-very-key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('RECIPE_GARDEN_SETTINGS', silent=True)

# Set up database
from database import db_session, run_db_schema
from common.user import Users

@app.teardown_appcontext
def shutdown_db(error):
    """Handler to close the DB"""
    db_session.remove()


@app.route('/')
def main_page():
    user = Users.get_by_id(1)
    return render_template("home.html.j2", user=user)

if __name__ == "__main__":
    init_db()
    run_db_schema()
    app.run()
