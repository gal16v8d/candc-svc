'''Test for cache route'''
from http import HTTPStatus
import json
from flask import Flask


def test_check_cache_keys(app: Flask) -> None:
    '''Test case for check_cache_keys'''
    client = app.test_client()
    response = client.get('/api/cache/keys')
    assert response.status_code == HTTPStatus.OK.value
    data = json.loads(response.data.decode('utf-8'))
    assert data == []


def test_clear_cache(app: Flask) -> None:
    '''Test case for clear_cache'''
    client = app.test_client()
    response = client.delete('/api/cache/clear')
    assert response.status_code == HTTPStatus.NO_CONTENT.value
