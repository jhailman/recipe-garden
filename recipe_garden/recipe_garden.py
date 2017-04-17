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
            app.logger.info("Created engine")
        except Exception as ex:
            app.logger.error(ex)
        try:
            engine.execute("use recipe_schema")
        except Exception as e:
            try:
                app.logger.error(e)
                app.logger.debug("Could select database recipe_schema, assuming it must be created.")
                connection = engine.raw_connection()
                cursor = connection.cursor()
                schema = ""
                with app.open_resource('schema.sql', mode='r') as schema_file:
                    schema = schema_file.read()
                app.logger.info("Opened schema")
                cursor.execute(schema)
                app.logger.info("Created new database")
                cursor.close()
                connection.commit()
                connection.close()
                app.logger.info("Created recipe_garden database from schema.")
            except Exception as e:
                app.logger.error("Could not create the new database")
                app.logger.error(e)
        return engine


db_engine = create_db_engine()


def get_db():
    """Gets an application-context-specific DB connection"""
    if not hasattr(g, 'db'):
        setattr(g, 'db', db_engine.connect())
    return g.db


# Import stuff from common after creating `app` and `get_db`
from .common.user import User
from .common.recipe import Recipe

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
    return render_template("home.html")

@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        try:
            email = request.form['email']
            clearpass = request.form['password']

            # Check credentials
            user = User.login(email, clearpass)
            session['username'] = user.name
            session['email'] = user.email
            flash('Successfully logged in')
            return redirect(url_for('main_page'))
        except Exception as err:
            flash(str(err))
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route('/logout')
def logout_page():
    if 'username' in session:
        session.pop('username', None)
        session.pop('email', None)
        flash('Successfully logged out')
        return redirect(url_for('main_page'))

@app.route('/registration', methods = ['GET', 'POST'])
def registration_page():
    if request.method == 'POST':
        username = request.form['username']
        clearpass = request.form['password']
        email = request.form['email']

        # Create new user in database here
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
    try:
        recipes = Recipe.get_by_range(0, 20)
        return render_template('browse.html', recipes=recipes)
    except exception as err:
        flash("Error getting recipes")
        return render_template('browse.html')

@app.route('/new-recipe', methods = ['GET', 'POST'])
def new_recipe_page():
    if request.method == 'POST':
        try:
            # Add new recipe to database
            recipe_name = request.form['name']
            Recipe.create(recipe_name, User.find_by_email(session['email']),
                request.form['img-path'], request.form['directions'],
                request.form['ingredients'])

            # Display new recipe's page
            # new_recipe_id = (Recipe.search_by_name(recipe_name)).id
            new_recipe_id = 1
            flash("Recipe successfully created")
            return redirect(url_for('recipe_page', recipe_id=new_recipe_id))
        except Exception as err:
            flash(str(err))
            return render_template('new-recipe.html')
    else:
        if 'username' in session:
            return render_template('new-recipe.html')
        else:
            return redirect(url_for('main_page'))

@app.route('/recipe/<recipe_id>')
def recipe_page(recipe_id=None):
    recipe = Recipe.get_by_id(recipe_id)
    if recipe == None:
        flash("Recipe not found")
        return redirect(url_for('main_page'))

    return render_template('recipe.html', recipe=recipe)
