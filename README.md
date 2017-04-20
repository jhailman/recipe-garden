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

The user in question will need `INSERT,SELECT,DELETE,CREATE,DROP` permissions to the
`recipe_schema` database.

## The database

Flask setup found at http://flask.pocoo.org/docs/0.12/installation/
as well as the tutorial http://flask.pocoo.org/docs/0.12/tutorial/packaging/#tutorial-packaging

This project uses `virtualenv` to set up the dependencies. It's also
a pip package. This means the pyhton version and dependencies we use don't affect
the rest of your python installation.

1. Clone the repo

```
$ git clone ... project-dir
```
2. Set up virtualenv

Install `virtualenv` if you don't have it (may need sudo)

```
$ pip install virtualenv
```

Start the `virtualenv` folder for the project somewhere

```
$ cd project-dir

$ virtualenv .env # Create some folder somewhere for virtualenv to run in

$ . .env/bin/activate # Activate the virtualenv
```

This will wrap the shell prompt; you can leave `virtualenv` with

```
$ deactivate
```

3. Install Flask in the `virtualenv`

```
$ pip install Flask
```

4. Install the package in the `virtualenv`

The project works like a python package, running this will
install its dependencies (in the virtualenv) and let you run locally.

```
$ pip install --editable .
```

5. Run the server locally
The main file is located in `/recipe_garden/recipe_garden.py`.
```
python recipe_garden.py
```

See the source code for other flask commands we have registered.
