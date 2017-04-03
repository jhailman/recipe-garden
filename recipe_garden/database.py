from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

metadata = MetaData() # http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/

engine = create_engine('sqlite:////tmp/recipe-garden.db',
                       convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
metadata.create_all(bind=engine)

def run_db_schema():
    """Run the schema to initialize the database"""
    with app.open_resource('schema.sql', mode='r') as schema:
        engine.execute(schema.read())
    db.commit()
    print("Initialized the database")

def close_db():
    pass
