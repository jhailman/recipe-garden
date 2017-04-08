"""User tests"""

from recipe_garden import recipe_garden
from recipe_garden.common import User

def test_register_and_login(client):
    registered = User.register("Mrs. Example", "mrs-example@example.com", "mrs_example")
    assert registered != None
    logged_in = User.login("mrs-example@email.com", "mrs_example")
    assert logged_in == registered
