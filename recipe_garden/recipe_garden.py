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
app.config.from_envvar('RECIPE_GARDEN_SETTINGS', silent=True) # Override with env var
#api = Api(app) # Create REST API

def create_db_engine():
    url = getattr(app.config, 'MYSQL_URL', None)
    if not url:
        user = os.environ['RECIPE_GARDEN_MYSQL_USER'] or 'root'
        password = os.environ['RECIPE_GARDEN_MYSQL_PASS'] or 'root'
        url = "mysql+pymysql://{user}:{password}@localhost/".format(
            user=user, password=password)
    engine = create_engine(url, encoding = 'UTF-8')
    try:
        engine.execute("use recipe_garden")
    except:
        app.logger.info("Could select database recipe_garden, assuming it must be created.")
        connection = engine.raw_connection()
        cursor = connection.cursor()
        with app.open_resource('schema.sql', mode='r') as schema:
            cursor.execute(schema.read())
        cursor.close()
        connection.close()
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
    user = User.get_by_id(1)
    return render_template("home.html.j2", user=user)
