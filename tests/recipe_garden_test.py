"""Application tests"""

import os
import tempfile

import pytest
from recipe_garden import recipe_garden

@pytest.fixture
def client(request):
    """Standard Flask client fixture, see minitwit's test example"""
    db_fd, recipe_garden.app.config['DB_PATH'] = tempfile.mkstemp()
    client = recipe_garden.app.test_client()
    with recipe_garden.app.app_context():
        recipe_garden.run_db_schema()

    def teardown():
        """Get rid of the database again after each test."""
        os.close(db_fd)
        os.unlink(recipe_garden.app.config['DB_PATH'])

    request.addfinalizer(teardown)
    return client
