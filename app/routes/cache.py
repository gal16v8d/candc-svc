'''Cache route handler'''
from http import HTTPStatus
from flask import Blueprint, Response, jsonify, make_response
from flask_caching import Cache
from flasgger import swag_from


def create_cache_bp(cache: Cache):
    '''Cache related methods'''
    cache_bp = Blueprint('cache', __name__)

    @cache_bp.route('/cache/keys', methods=['GET'])
    @swag_from('../docs/cache_keys.yml')
    def check_cache_keys() -> Response:
        '''Shouild retrieve all the keys in cache'''
        cache_keys = [key for key in cache.cache._cache.keys()]
        return jsonify(cache_keys)

    @cache_bp.route('/cache/clear', methods=['DELETE'])
    @swag_from('../docs/cache_clear.yml')
    def clear_cache() -> Response:
        '''Should clear app cache'''
        cache.clear()
        return make_response('', HTTPStatus.NO_CONTENT.value)

    return cache_bp
