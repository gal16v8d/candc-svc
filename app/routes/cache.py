"""Cache route handler"""

from http import HTTPStatus

from flask import jsonify, make_response, typing
from flask_restx import Namespace, Resource

from app.models.swagger import get_cache_model_response
from app.service.cache_service import CacheService


cache_ns = Namespace(
    "cache", description="App cache controller endpoints", path="/api/cache"
)
cache_model = get_cache_model_response()
cache_service = CacheService()


@cache_ns.route("/keys")
@cache_ns.doc("Allows to retrieve all the keys in cache")
class CacheKeyResource(Resource):
    """Cache keys endpoints"""

    @cache_ns.response(HTTPStatus.OK.value, "Cache keys in use", cache_model)
    def get(self) -> typing.ResponseReturnValue:
        """Retrieve all the keys in cache"""
        return jsonify(cache_service.get_cache_keys())


@cache_ns.route("/clear")
@cache_ns.doc("Allows to retrieve all the keys in cache")
class CacheClearResource(Resource):
    """Cache clear endpoints"""

    @cache_ns.response(HTTPStatus.NO_CONTENT.value, "Cache was cleared")
    def delete(self) -> typing.ResponseReturnValue:
        """Clear app cache"""
        cache_service.clear_cache()
        return make_response("", HTTPStatus.NO_CONTENT.value)
