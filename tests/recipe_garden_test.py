"""Application tests"""

import os
import tempfile

import pytest
from recipe_garden import recipe_garden

@pytest.fixture
def client(request):
    """Standard Flask client fixture, see minitwit's test example"""
    db_fd, recipe_garden.app.config['DB_PATH'] = tempfile.mkstemp()
    recipe_garden.app.config['TESTING'] = True
    client = recipe_garden.app.test_client()
    with recipe_garden.app.app_context():
        recipe_garden.get_db()
        recipe_garden.run_db_schema()

    def teardown():
        """Get rid of the database again after each test."""
        os.close(db_fd)
        os.unlink(recipe_garden.app.config['DB_PATH'])

    request.addfinalizer(teardown)
    return client


# Users

def test_register_and_login(client):
    with recipe_garden.app.app_context():
        registered = recipe_garden.User.register(
            "Mrs. Example", "mrs-example@example.com", "mrs_example")
        assert registered != None
        logged_in = recipe_garden.User.login(
            "mrs-example@example.com", "mrs_example")
        assert logged_in.email == registered.email and logged_in.name == registered.name


def test_login_bad_email(client):
    with pytest.raises(Exception):
        with recipe_garden.app.app_context():
            registered = recipe_garden.User.register(
                "mrs. example", "mrs-example@example.com", "mrs_example")
            assert registered != None
            recipe_garden.user.login(
                "mr-example@example.com", "mrs_example")


def test_login_bad_password(client):
    with pytest.raises(Exception):
        with recipe_garden.app.app_context():
            registered = recipe_garden.User.register(
                "mrs. example", "mrs-example@example.com", "mrs_example")
            assert registered != None
            recipe_garden.user.login(
                "mrs-example@example.com", "mr_example")
