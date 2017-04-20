## Recipe Garden

Recipe Garden is a website where users can create and share recipes, with shopping lists 
so they can cook the recipes they like.

## Setup

Recipe Garden is written in Python using Flask and MySQL. It requires Python 3.6. 

We recommend using virtualenv (https://virtualenv.pypa.io/en/stable/) to install the 
dependencies (flask, SQLAlchemy, etc.) and keep the setup separate from the rest of 
your system. In particular, we had `import` issues that seemed to differ between
Python 2.7, Python 3.4, and Python 3.6. Because of this, we ask you use virtualenv to
setup Python 3.6, even if you do not use it for other applications.

## Setup

### Clone the repository

```
$ git clone https://github.com/jhailman/recipe-garden.git

$ cd recipe-garden
```

### Install virtualenv

Virtualenv(https://virtualenv.pypa.io/en/stable) can be installed through `pip` or your
distribution's package manager (where it is usually called `python-virtualenv` or
`python3.6-virtualenv`, etc.). Follow [virtualenv's instructions](https://virtualenv.pypa.io/en/stable/installation/)
to install otherwise.

### Using virtualenv

Virtualenv will create a folder to install a specific instance of Python (i.e. Python 3.6)
and various dependencies (i.e. Flask). This means that you'll be able to run recipe-garden
without worrying about affecting any other software on your machine.

First, we will create a folder for this process. We'll call it `.env` and leave it in the git folder's
root.

```
$ virtualenv .env
```

Next, we need to make sure that commands like `pip` and `python` use the Python installed in `.env`.
To do this, virtualenv works with the shell (bash, zsh, fish, and more are supported).

```
$ . .env/bin/activate
```

The `.` on bash or zsh will cause the comands to redirect. Virtualenv should have affected your
shell prompt as well. Please consult the [virtualenv docs](https://virtualenv.pypa.io/en/stable/userguide/#activate-script) if this does not work.

At this point you're ready for the installation.

## Install dependencies

Recipe-garden is set up to be a python package, so `pip` will be able to install its
dependencies automatically. If you set up virtualenv they will be installed there.

```
$ pip install --editable .
```

This will install all the required dependencies (`flask`, `pymysql`, `sqlalchemy`).

## Environment variables

Running the app will require setting some environment variables:

- `RECIPE_GARDEN_MYSQL_USER`: MySQL user account (defaults to `root`).
- `RECIPE_GARDEN_MYSQL_PASS`: MySQL user password (defaults to `root` as well).
- `FLASK_APP="recipe_garden/recipe_garden.py"`: Flask requires this variable to be
the relative path to the app's main python file. This value works when running from
the Git project root.
- `FLASK_DEBUG=true` This is optional to help with debugging.

## The database

The user specified by the environment variables will need `INSERT,SELECT,DELETE,CREATE,DROP` 
permissions to the `recipe_schema` database.

The `recipe_schema` database will automatically be created if it does not exist. The database
and tables will be populated with some example recipes and an example user.

## Running the project

Once the project is installed and environment variables are set, the site can be run with
`flask run`. It will show up at http://localhost:5000/. The default user is `email@example.com`
with password `password`.

## References

- virtualenv 1.9: https://virtualenv.pypa.io/en/stable/
- Flask 0.12: http://flask.pocoo.org/docs/0.12/installation/
- SQLAlchemy 1.1.9 http://www.sqlalchemy.org/
