"""Money route handler"""

from flask import jsonify, request, typing
from flask_restx import Namespace, Resource, fields
from app.error.custom_exc import BadBodyException
from app.service.money_spend_service import MoneySpendService


money_ns = Namespace(
    "money",
    description="Helps to calculate how to spend money on game stuff",
    path="/api/money",
)
money_model = money_ns.model(
    "MoneyData",
    {"available_cash": fields.Integer(description="Money that was not spend")},
)
money_service = MoneySpendService()


@money_ns.route("/<model_type>")
@money_ns.param("model_type", "Model to fetch")
class MoneyResource(Resource):
    """Money check endpoints"""

    def post(self, model_type: str) -> typing.ResponseReturnValue:
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
        raise BadBodyException("money payload")
