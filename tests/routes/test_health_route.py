"""Test for health route"""

from http import HTTPStatus
import json
from typing import cast

from flask import Flask

import tests.test_helper as helper


def test_health_check(app: Flask) -> None:
    """Test case for health_check"""
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == HTTPStatus.OK.value
    data_bytes: bytes = cast(bytes, response.data)
    data = json.loads(data_bytes.decode(helper.UTF_8))
    assert data == {"status": "UP"}
