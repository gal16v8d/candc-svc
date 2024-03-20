'''Test config module'''
import pytest
from app.configs.lazy_cfg_loader import LazyImporter


@pytest.fixture
def app():
    '''Init app fixture for route tests'''
    app_module = LazyImporter('app').get_module()
    flask_app = app_module.create_app()
    with flask_app.app_context():
        yield flask_app
