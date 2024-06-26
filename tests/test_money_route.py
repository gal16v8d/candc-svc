"""Test for money route"""

from http import HTTPStatus
import json
from flask import Flask
import tests.test_helper as helper


def test_money_to_spend(app: Flask) -> None:
    """Test case for money_to_spend"""
    client = app.test_client()
    response = client.post("/api/money/boats", json={"money": 5000, "faction_id": 1})
    assert response.status_code == HTTPStatus.OK.value
    data = json.loads(response.data.decode(helper.UTF_8))
    assert data["available_cash"] is not None
    assert data["units"] is not None


def test_money_to_spend_bad_type(app: Flask) -> None:
    """Test case for money_to_spend"""
    client = app.test_client()
    response = client.post(
        "/api/money/not_supported", json={"money": 5000, "faction_id": 1}
    )
    helper.assert_api_error(response, HTTPStatus.BAD_REQUEST.value)


def test_money_to_spend_error(app: Flask) -> None:
    """Test case for money_to_spend"""
    client = app.test_client()
    response = client.post("/api/money/not_supported", json={"money": 5000})
    helper.assert_api_error(response, HTTPStatus.INTERNAL_SERVER_ERROR.value)


def test_money_to_spend_no_payload(app: Flask) -> None:
    """Test case for money_to_spend"""
    client = app.test_client()
    response = client.post("/api/money/boats", json={})
    helper.assert_api_error(response, HTTPStatus.BAD_REQUEST.value)
