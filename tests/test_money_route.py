'''Test for money route'''
from http import HTTPStatus
import json
from flask import Flask


def test_money_to_spend(app: Flask) -> None:
    '''Test case for money_to_spend'''
    client = app.test_client()
    response = client.post('/api/money/boats', json={'money': 5000, 'faction_id': 1})
    assert response.status_code == HTTPStatus.OK.value
    data = json.loads(response.data.decode('utf-8'))
    assert data['available_cash'] is not None
    assert data['units'] is not None


def test_money_to_spend_bad_type(app: Flask) -> None:
    '''Test case for money_to_spend'''
    client = app.test_client()
    response = client.post('/api/money/not_supported', json={'money': 5000, 'faction_id': 1})
    assert response.status_code == HTTPStatus.BAD_REQUEST.value
    data = json.loads(response.data.decode('utf-8'))
    assert data['path'] is not None
    assert data['message'] is not None


def test_money_to_spend_error(app: Flask) -> None:
    '''Test case for money_to_spend'''
    client = app.test_client()
    response = client.post('/api/money/not_supported', json={'money': 5000})
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value
    data = json.loads(response.data.decode('utf-8'))
    assert data['path'] is not None
    assert data['message'] is not None


def test_money_to_spend_no_payload(app: Flask) -> None:
    '''Test case for money_to_spend'''
    client = app.test_client()
    response = client.post('/api/money/boats', json={})
    assert response.status_code == HTTPStatus.BAD_REQUEST.value
