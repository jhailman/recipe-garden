import sqlite3

def start_db(path):
    """Open a database connection (SQLite from the tutorial)"""
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def handler_close_db(error):
    """Closes the database at the end of the request"""
    if hasattr(g, 'db'):
        g.sqlite_db.close()

@app.cli.command('initdb')
def command_init_db():
    """CLI command to create the database by running the schema"""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as schema:
        db.cursor().executescript(schema.read())
    db.commit()
    print("Initialized the database")

# TODO
#g.get_db = lambda: g.db if hasattr(g, 'db') else connect_db(app.config['DATABASE'])
