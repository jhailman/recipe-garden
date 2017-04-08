"""
Database setup and teardown routines
"""

from sqlite3 import connect

DB_LOCATION = "/tmp/recipe-garden.sqlite"

db_session = connect(DB_LOCATION)
