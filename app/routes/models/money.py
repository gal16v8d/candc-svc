'''Money route handler'''
from http import HTTPStatus
from flask import Blueprint, Response, abort, jsonify, request
from flask_caching import Cache
from app.service.db_service.money_spend import MoneySpendService


def create_money_bp(cache: Cache) -> Blueprint:
    '''Blueprint for money spend services on api'''
    money_bp = Blueprint('money', __name__)
    money_service = MoneySpendService(cache)

    @money_bp.route('/money/<model_type>', methods = ['POST'])
    def money_to_spend(model_type: str) -> Response:
        '''
        It can retrieve a random generated planes quantity given
        the faction_id and money amount
        '''
        payload = request.get_json()
        if payload:
            result = money_service.spend_money_by_type(model_type, payload['faction_id'], payload['money'])
            return jsonify(result)
        abort(HTTPStatus.BAD_REQUEST.value, 'data_should_be_json')

    return money_bp
