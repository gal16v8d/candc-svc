# C&C service

<p align="center">
  <img width="200" src="flask-logo.png" alt="Flask logo">
  <p align="center">
    Flask + SQLAlchemy + PostgreSQL REST API for C&C Wiki
  </p>
</p>


This project was created using [Poetry](https://python-poetry.org/).
Basically, its a really basic API wiki view for all the data related to C&C games.
This is still WIP, so it may get some data updates soon.

# Get started

## Unix

Install poetry:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Init repo:

```bash
poetry new candc-svc
```

Create the virtual env folder:

```bash
mkdir .venv
```

Install all the dependencies in the project (clean-state):

```bash
poetry install
```

Install any dependency you need:

```bash
poetry add lib_here
```

Remove a dependency you don't need:

```bash
poetry remove lib_here
```

Update all (updatable) libs

```bash
poetry update
```

# Set up

# env

Activate using the command:

```bash
source .venv/bin/activate
```

Exit virtual env:

```bash
exit
```

or

```bash
deactivate
```

# sqlalchemy

For init db:

```bash
flask db init
```

Migrate:

```bash
flask db migrate
```

Confirm/apply in db:

```bash
flask db upgrade
```

# launch

Dev mode:

```bash
flask run
```

Prod run:

```bash
gunicorn --workers {# workers here} --bind 0.0.0.0:{port here} wsgi:app
```

# test

```bash
pytest --cov
```

# automation

Run the server using the command on launch section
Then open another console, activate the env and go to automation folder
Once there run the tests using:

```bash
behave
```

You can see the console output with several features, scenarios and steps and its status as passed, failed or skipped.

# Advanced use cases

If multiple python versions are found in the operative system, then
- use pyenv to handle the versions
- if needed set the local python for this project, like
```bash
pyenv local 3.12.1
```
- you can confirm all good by checking
```bash
pyenv which python
```
- set the specific python version like
```bash
poetry env use $USER_HOME/.pyenv/versions/3.12.1/bin/python
```
- then install using commands like the ones in the previous section

# Formatter

Using `black` as code formatter
Can be used this way:
```bash
poetry run black .
```

# Type checking
Using `mypy` for type checking
Can be used this way:
```bash
poetry run mypy app tests
```

# swagger docs (flasgger)

http://{host}:{port}/apidocs

# Web deployment

This app can be hosted in [Railway](https://railway.app), folder that helps with it is `.ci` folder.

## List of cool technologies in use here

- [Behave](https://behave.readthedocs.io/en/latest/)
- [Flask](https://flask.palletsprojects.com/en/2.3.x/)
- [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/)
- [FLask-Caching](https://flask-caching.readthedocs.io/en/latest/index.html)
- [Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/index.html)
- [poetry](https://python-poetry.org/)
- [pyenv](https://github.com/pyenv/pyenv)
- [SQLAlchemy](https://www.sqlalchemy.org/)

## License

[MIT licensed](LICENSE).

## Stay in touch

- Author - [gal16v8d](https://github.com/gal16v8d)