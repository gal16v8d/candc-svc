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

Install any dependency you need:

```bash
poetry add lib_here
```

# Set up

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

```bash
flask run
```

# swagger docs (flasgger)

http://{host}:{port}/apidocs

## List of cool technologies in use here

- [Flask](https://flask.palletsprojects.com/en/2.3.x/)
- [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/)
- [FLask-Caching](https://flask-caching.readthedocs.io/en/latest/index.html)
- [Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/index.html)
- [SQLAlchemy](https://www.sqlalchemy.org/)

## License

[MIT licensed](LICENSE).

## Stay in touch

- Author - [gal16v8d](https://github.com/gal16v8d)