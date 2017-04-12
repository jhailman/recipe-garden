"""Application entry point"""

import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_restful import Api
from database import db_session
from common.user import User

app = Flask(__name__) # create the application instance
app.config.from_object(__name__) # load config from this file, recipe_garden.py
api = Api(app)
LOG = app.logger


# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE_PATH='/tmp/recipe-garden.db', #os.path.join(app.root_path, 'recipe-garden.db'),
    SECRET_KEY='wow-so-secret-very-key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('RECIPE_GARDEN_SETTINGS', silent=True)

# Set up database
def run_db_schema():
    """Run the schema to initialize the database"""
    with app.open_resource('schema.sql', mode='r') as schema:
        cursor = db_session.executescript(schema.read())
        db_session.commit()


@app.teardown_appcontext
def shutdown_db(error):
    app.logger.warn("Closing the database!!!")
    """Handler to close the DB"""
    db_session.close()

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
