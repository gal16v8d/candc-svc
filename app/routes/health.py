"""Basic health check route"""

from http import HTTPStatus

from flask import jsonify, typing
from flask_restx import Namespace, Resource

from app.core.limiter import app_limiter
from app.models.swagger import get_health_model_response


health_ns = Namespace("health", description="App status/readiness check")
health_model = get_health_model_response(health_ns)


@health_ns.route("")
class HealthResource(Resource):
    """Namespace to expose the health check on api"""

    @app_limiter.exempt
    @health_ns.response(HTTPStatus.OK.value, "App Up and working", health_model)
    def get(self) -> typing.ResponseReturnValue:
        """Return UP if app is running"""
        return jsonify(status="UP")
