'''Cache route handler'''
from http import HTTPStatus
from flask import Blueprint, Response, jsonify, make_response
from flasgger import swag_from
from app.service.cache_service import CacheService


cache_bp = Blueprint('cache', __name__)
cache_service = CacheService()


@cache_bp.route('/cache/keys', methods=['GET'])
@swag_from('../docs/cache_keys.yml')
def check_cache_keys() -> Response:
    '''Should retrieve all the keys in cache'''
    return jsonify(cache_service.get_cache_keys())


@cache_bp.route('/cache/clear', methods=['DELETE'])
@swag_from('../docs/cache_clear.yml')
def clear_cache() -> Response:
    '''Should clear app cache'''
    cache_service.clear_cache()
    return make_response('', HTTPStatus.NO_CONTENT.value)
