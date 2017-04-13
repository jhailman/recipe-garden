"""Application entry point"""
import os
import sqlite3.dbapi2 as sqlite3
from sqlalchemy import create_engine
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask_restful import Api

# These values are automatically added to the config
#DB_PATH = '/tmp/recipe-garden.sqlite'

app = Flask(__name__) # create the application instance
app.config.from_object(__name__) # load the values set above into config
app.secret_key = "super secret key"
app.config.from_envvar('RECIPE_GARDEN_SETTINGS', silent=True) # Override with env var
#api = Api(app) # Create REST API

global DATABASE_SET
DATABASE_SET = False

def create_db_engine():
    global DATABASE_SET
    if DATABASE_SET:
        return db_engine
    DATABASE_SET = True
    app.logger.info("Begin create_db_engine")
    with app.app_context():
        app.logger.info("In app get context")
        url = getattr(app.config, 'MYSQL_URL', None) if hasattr(app.config, 'MYSQL_URL') else None
        app.logger.info("Got a URL")
        if not url:
            app.logger.info("There is no URL")
            user = os.environ['RECIPE_GARDEN_MYSQL_USER'] if 'RECIPE_GARDEN_MYSQL_USER' in os.environ else 'root'
            password = os.environ['RECIPE_GARDEN_MYSQL_PASS'] if 'RECIPE_GARDEN_MYSQL_PASS' in os.environ else 'root'
            url = "mysql+pymysql://{user}:{password}@localhost/".format(
                user=user, password=password)
        app.logger.info("Creating engine with url %s", url)
        try:
            engine = create_engine(url) #, encoding = 'UTF-8')
        except Exception as ex:
            app.logger.error(ex)
        app.logger.info("Created engine")
        try:
            engine.execute("use recipe_schema")
        except Exception as e:
            app.logger.error(e)
            app.logger.debug("Could select database recipe_schema, assuming it must be created.")
            connection = engine.raw_connection()
            cursor = connection.cursor()
            with app.open_resource('schema.sql', mode='r') as schema:
                app.logger.info("Opened schema")
                cursor.execute(schema.read())
            cursor.close()
            cursor.commit()
            connection.close()
            connection.commit()
            app.logger.info("Created recipe_garden database from schema.")
        return engine


db_engine = create_db_engine()


def get_db():
    """Gets an application-context-specific DB connection"""
    if not hasattr(g, 'db'):
        setattr(g, 'db', db_engine.connect())
    return g.db


# Import stuff from common after creating `app` and `get_db`
from .common.user import User

# Set up database
@app.cli.command('initdb')
def run_db_schema():
    """Run the schema to reinitialize the database"""
    app.logger.info("Recreating recipe_garden from schema")
    connection = db_engine.raw_connection()
    cursor = connection.cursor()
    with app.open_resource('schema.sql', mode='r') as schema:
        cursor.execute(schema.read())
    cursor.close()
    connection.close()
    app.logger.info("Recreated recipe_garden database from schema.")

@app.teardown_appcontext
def shutdown_db(error):
    """Handler to close the DB at the end of application contexts"""
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def main_page():
    if 'email' in session:
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
        user = User.login(email, clearpass)
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
        try:
            user = User.register(username, email, clearpass)
            flash('Successfully registered')
            return redirect(url_for('login_page'))
        except Exception as err:
            flash(str(err))
            return redirect(url_for('registration_page'))
    else:
        return render_template("register.html")

#if __name__ == "recipe_garden.recipe_garden":
#    try:
#    except Exception as err:
        # do nothing
#        pass
