"""Basic health check route"""

from flask import Blueprint, jsonify, typing
from flask_limiter import Limiter
from flasgger import swag_from


def create_health_bp(limiter: Limiter) -> Blueprint:
    """Blueprint to expose the health check on api"""
    health_bp = Blueprint("health", __name__)

    @health_bp.route("/health", methods=["GET"])
    @limiter.exempt
    @swag_from("../docs/health.yml")
    def health_check() -> typing.ResponseReturnValue:
        """Return UP if app is running"""
        return jsonify(status="UP")

    return health_bp
