"""Test config module"""

from typing import Any
import pytest

from app.configs.lazy_cfg_loader import LazyImporter


@pytest.fixture
def app() -> Any:
    """Init app fixture for route tests"""
    app_module = LazyImporter("app").get_module()
    flask_app = app_module.create_app()
    with flask_app.app_context():
        yield flask_app
