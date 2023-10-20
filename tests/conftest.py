'''Test config module'''
import pytest
from app.configs.database_cfg import TestConfig


@pytest.fixture
def app():
    '''Init app fixture for route tests'''
    from app import create_app
    flask_app = create_app(TestConfig)
    with flask_app.app_context():
        yield flask_app
