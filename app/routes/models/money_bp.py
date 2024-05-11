"""Money route handler"""

from http import HTTPStatus
from flask import Blueprint, Response, abort, jsonify, request, typing
from app.service.money_spend_service import MoneySpendService


money_bp = Blueprint("money", __name__)
money_service = MoneySpendService()


@money_bp.route("/money/<model_type>", methods=["POST"])
def money_to_spend(model_type: str) -> typing.ResponseReturnValue:
    """
    It can retrieve a random generated planes quantity given
    the faction_id and money amount
    """
    payload = request.get_json()
    if payload:
        result = money_service.spend_money_by_type(
            model_type, payload["faction_id"], payload["money"]
        )
        return jsonify(result)
    abort(HTTPStatus.BAD_REQUEST.value, "data_should_be_json")
