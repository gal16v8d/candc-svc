"""Basic health check route"""

from http import HTTPStatus
from flask import jsonify, typing
from flask_restx import Namespace, Resource, fields
from app.core.limiter import app_limiter


health_ns = Namespace("health", description="App status/readiness check")

health_model = health_ns.model(
    "Health", {"status": fields.String(required=True, description="UP if app is live")}
)


@health_ns.route("")
class HealthResource(Resource):
    """Namespace to expose the health check on api"""

    @app_limiter.exempt
    @health_ns.response(HTTPStatus.OK.value, "App Up and working", health_model)
    def get(self) -> typing.ResponseReturnValue:
        """Return UP if app is running"""
        return jsonify(status="UP")
