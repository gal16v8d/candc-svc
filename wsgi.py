"""File that allows wsgi gunicorn execution"""

from app import create_app

app = create_app()
