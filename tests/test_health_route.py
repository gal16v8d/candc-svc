"""Test for health route"""

import json
from flask import Flask


def test_health_check(app: Flask) -> None:
    """Test case for health_check"""
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data.decode("utf-8"))
    assert data == {"status": "UP"}
