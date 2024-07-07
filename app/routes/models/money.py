"""Money route handler"""

from http import HTTPStatus

from flask import jsonify, request, typing
from flask_restx import Namespace, Resource

from app.models.schemas import MoneySpendRequest
from app.models.swagger import get_money_model_response
from app.service.money_spend_service import MoneySpendService


money_ns = Namespace(
    "money",
    description="Helps to calculate how to spend money on game stuff",
    path="/api/money",
)
money_model = get_money_model_response(money_ns)
money_service = MoneySpendService()


@money_ns.route("/<model_type>")
@money_ns.param("model_type", "Model to fetch")
class MoneyResource(Resource):
    """Money check endpoints"""

    @money_ns.response(
        HTTPStatus.OK.value, "Return a way to spend the money building", money_model
    )
    def post(self, model_type: str) -> typing.ResponseReturnValue:
        """
        It can retrieve a random generated things to build given
        the faction_id and money amount
        :param model_type: model that we want to build
        """
        payload = request.get_json()
        money_request = MoneySpendRequest(**payload)
        result = money_service.spend_money_by_type(model_type, money_request)
        return jsonify(result)
