'''Test config module'''
import pytest


@pytest.fixture
def app():
    '''Init app fixture for route tests'''
    from app import create_app
    flask_app = create_app()
    with flask_app.app_context():
        yield flask_app
