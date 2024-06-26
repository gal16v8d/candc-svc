"""Cache route handler"""

from http import HTTPStatus
from flask import jsonify, make_response, typing
from flask_restx import Namespace, Resource
from app.service.cache_service import CacheService


cache_ns = Namespace(
    "cache", description="App cache controller endpoints", path="/api/cache"
)
cache_service = CacheService()


@cache_ns.route("/keys")
@cache_ns.doc("Allows to retrieve all the keys in cache")
class CacheKeyResource(Resource):
    """Cache keys endpoints"""

    def get(self) -> typing.ResponseReturnValue:
        """Retrieve all the keys in cache"""
        return jsonify(cache_service.get_cache_keys())


@cache_ns.route("/clear")
@cache_ns.doc("Allows to retrieve all the keys in cache")
@cache_ns.response(HTTPStatus.NO_CONTENT.value, "Cache was cleared")
class CacheClearResource(Resource):
    """Cache clear endpoints"""

    def delete(self) -> typing.ResponseReturnValue:
        """Clear app cache"""
        cache_service.clear_cache()
        return make_response("", HTTPStatus.NO_CONTENT.value)
