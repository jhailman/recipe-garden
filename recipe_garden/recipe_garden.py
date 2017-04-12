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

def get_db():
    """Gets an application-context-specific DB connection"""
    if not hasattr(g, 'db'):
        setattr(g, 'db', sqlite3.connect(app.config['DB_PATH']))
        g.db.row_factory = sqlite3.Row
    return g.db


# Import stuff from common after creating `app` and `get_db`
from .common.user import User

# Set up database
def run_db_schema():
    """Run the schema to initialize the database"""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as schema:
        db.cursor().executescript(schema.read())
    db.commit()

@app.teardown_appcontext
def shutdown_db(error):
    """Handler to close the DB at the end of application contexts"""
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def main_page():
    if 'email' in session:
        # TODO: Look for the actual user
        user = User(1, session['email'], "foo@foo.com")
    else:
        user = None
    return render_template("home.html")

@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        clearpass = request.form['password']
        # TODO: Check credentials
        session['email'] = email
        return redirect(url_for('main_page'))
    else:
        return render_template("login.html")

@app.route('/registration', methods = ['GET', 'POST'])
def registration_page():
    if request.method == 'POST':
        username = request.form['username']
        clearpass = request.form['password']
        email = request.form['email']
        # TODO: Create new user in database here
        return redirect(url_for('login_page'))
    else:
        return render_template("register.html")

if __name__ == "recipe_garden.recipe_garden":
    try:
        run_db_schema()
    except Exception as err:
        # do nothing
        pass
