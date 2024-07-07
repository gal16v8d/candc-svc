"""Test for cache route"""

from http import HTTPStatus
import json
from typing import cast

from flask import Flask

import tests.test_helper as helper


def test_get_all(app: Flask) -> None:
    """Test case for get all"""
    client = app.test_client()
    response = client.get("/api/boats")
    assert response.status_code == HTTPStatus.OK.value
    data_bytes: bytes = cast(bytes, response.data)
    data = json.loads(data_bytes.decode(helper.UTF_8))
    assert len(data) > 0


def test_get_all_filter(app: Flask) -> None:
    """Test case for get all using filter"""
    client = app.test_client()
    response = client.get("/api/boats?boat_id=16")
    assert response.status_code == HTTPStatus.OK.value
    data_bytes: bytes = cast(bytes, response.data)
    data = json.loads(data_bytes.decode(helper.UTF_8))
    assert len(data) == 1


def test_get_all_wrong_filter(app: Flask) -> None:
    """Test case for get all using bad filter"""
    client = app.test_client()
    response = client.get("/api/boats?non-valid-field=Test")
    helper.assert_api_error(response, HTTPStatus.BAD_REQUEST.value)


def test_get_all_not_found(app: Flask) -> None:
    """Test case for get all not found scenario"""
    client = app.test_client()
    response = client.get("/api/boats?boat_id=9999")
    helper.assert_api_error(response, HTTPStatus.NOT_FOUND.value)


def test_get_by_id_not_found(app: Flask) -> None:
    """Test case for get by id not found scenario"""
    client = app.test_client()
    response = client.get("/api/boats/9999")
    helper.assert_api_error(response, HTTPStatus.NOT_FOUND.value)


def test_get_by_id(app: Flask) -> None:
    """Test case for get by id"""
    client = app.test_client()
    response = client.get("/api/boats/1")
    assert response.status_code == HTTPStatus.OK.value
    data_bytes: bytes = cast(bytes, response.data)
    data = json.loads(data_bytes.decode(helper.UTF_8))
    assert isinstance(data["name"], str)
    assert isinstance(data["active"], bool)
    assert isinstance(data["base_cost"], int)


def test_create_not_valid(app: Flask) -> None:
    """Test case for create empty payload"""
    client = app.test_client()
    response = client.post("/api/boats")
    helper.assert_api_error(response, HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value)


def test_create_missing_data(app: Flask) -> None:
    """Test case for create bad payload"""
    client = app.test_client()
    response = client.post("/api/boats", json={"name": "Test Boat"})
    assert response.status_code == HTTPStatus.BAD_REQUEST.value
    data_bytes: bytes = cast(bytes, response.data)
    data = json.loads(data_bytes.decode(helper.UTF_8))
    assert isinstance(data["message"], list)
    assert data["path"] is not None


def test_patch_item_not_valid(app: Flask) -> None:
    """Test case for patch empty payload"""
    client = app.test_client()
    response = client.patch("/api/boats/1")
    helper.assert_api_error(response, HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value)


def test_patch_item_not_updatable_created(app: Flask) -> None:
    """Test case for patch empty payload"""
    client = app.test_client()
    response = client.patch(
        "/api/boats/1", json={"created_at": "2023-11-03T22:48:48.938506"}
    )
    helper.assert_api_error(response, HTTPStatus.BAD_REQUEST.value)


def test_patch_item_not_updatable_updated(app: Flask) -> None:
    """Test case for patch empty payload"""
    client = app.test_client()
    response = client.patch(
        "/api/boats/1", json={"updated_at": "2023-11-03T22:48:48.938506"}
    )
    helper.assert_api_error(response, HTTPStatus.BAD_REQUEST.value)


def test_patch_item_not_found(app: Flask) -> None:
    """Test case for patch not found"""
    client = app.test_client()
    response = client.patch("/api/boats/9999", json={"name": "Test Boat"})
    helper.assert_api_error(response, HTTPStatus.NOT_FOUND.value)


def test_delete_item_not_found(app: Flask) -> None:
    """Test case for delete empty payload"""
    client = app.test_client()
    response = client.delete("/api/boats/9999")
    helper.assert_api_error(response, HTTPStatus.NOT_FOUND.value)
