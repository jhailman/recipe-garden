## Contributing & Setup

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
