"""Application entry point"""

import sqlite3.dbapi2 as sqlite3

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
from flask_restful import Api

# These values are automatically added to the config
DB_PATH = '/tmp/recipe-garden.sqlite'

app = Flask(__name__) # create the application instance
app.config.from_object(__name__) # load the values set above into config
app.secret_key = "super secret key"
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
    if 'username' in session:
        # TODO: Look for the actual user
        # user = User(1, session['email'], "foo@foo.com"
        pass
    else:
        user = None
    return render_template("home.html")

@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        clearpass = request.form['password']
        # TODO: Check credentials
        # user = User.login(email, clearpass)
        user = User({ "id": 1, "name": "ari", "email": "ari@test.com", "password": "asdf" })
        session['username'] = user.name
        flash('Successfully logged in')
        return redirect(url_for('main_page'))
    else:
        return render_template("login.html")

@app.route('/logout')
def logout_page():
    if 'username' in session:
        session.pop('username', None)
        flash('Successfully logged out')
        return redirect(url_for('main_page'))

@app.route('/registration', methods = ['GET', 'POST'])
def registration_page():
    if request.method == 'POST':
        username = request.form['username']
        clearpass = request.form['password']
        email = request.form['email']
        # TODO: Create new user in database here
        try:
            user = User.register(username, email, clearpass)
            flash('Successfully registered')
            return redirect(url_for('login_page'))
        except Exception as err:
            flash(str(err))
            return redirect(url_for('registration_page'))
    else:
        return render_template("register.html")

@app.route('/browse')
def browse_page():
    return render_template('browse.html')

@app.route('/new-recipe', methods = ['GET', 'POST'])
def new_recipe_page():
    if 'username' in session:
        return render_template('new-recipe.html')
    else:
        return redirect(url_for('main_page'))

@app.route('/recipe/<recipe_id>')
def recipe_page(recipe_id=None):
    # TODO: Implement Recipe database functions
    # try:
    #     recipe = Recipe.get_by_id(recipe_id)
    #     render_template('recipe.html', recipe=recipe)
    # except Exception as err:
    #     flash(str(err))
    #     return redirect(url_for('main_page'))

    # TODO: Temporary
    return render_template('recipe.html', recipe="test")


if __name__ == "recipe_garden.recipe_garden":
    try:
        run_db_schema()
    except Exception as err:
        # do nothing
        pass
