"""
Database setup, using the style of
http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/#manual-object-relational-mapping

"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

# Database engine object (just used for binding objects)
engine = create_engine('sqlite:////tmp/recipe-garden.db',
                       convert_unicode=True)
# ???
metadata = MetaData()
# Database object that is exported
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
metadata.create_all(bind=engine)

def init_db():
    metadata.create_all(bind=engine)
    db_session.execute("insert into users (id, email) values (1, `foo@foo.com`)")

def run_db_schema():
    """Run the schema to initialize the database"""
    with app.open_resource('schema.sql', mode='r') as schema:
        engine.execute(schema.read())

def close_db():
    pass
