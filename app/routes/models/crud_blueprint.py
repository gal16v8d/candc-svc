'''Generic blueprint CRUD'''
from http import HTTPStatus
from typing import Any, List
from flask import Blueprint, Response, abort, jsonify, make_response, render_template, request
from flask_caching import Cache
from app.models.database import get_all, get_by_id, save, update, delete


def create_crud_blueprint(model: Any, cache: Cache):
    '''Generic blueprint to perform CRUD operations'''
    name = model.__name__
    data_not_found = f'{name} not found'
    data_should_be_json = f'{name} data should be json'
    crud_bp = Blueprint(name.lower(), __name__)
    path_name = 'infantry' if name == 'Infantry' else f'{name.lower()}s'

    def get_cache_key(item_id=None) -> str:
        '''get cache key for the model'''
        return path_name if item_id is None else f'{path_name}-{item_id}'

    def fetch_all_data() -> List[Any]:
        '''
        Attempts to lookup in the cache, 
        if not found go to db and put in cache
        '''
        cache_key = get_cache_key()
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        db_items = get_all(model)
        items = [i.to_dict() for i in db_items]
        cache.set(cache_key, items)
        return items

    def fetch_one_data(item_id: int) -> Any:
        cache_key = get_cache_key(item_id)
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        item = get_by_id(model, item_id)
        cache.set(cache_key, item)
        return item

    @crud_bp.route(f'/{path_name}', methods=['GET'])
    def get_all_items() -> Response:
        '''Get all items in db'''
        items = fetch_all_data()
        return jsonify(items)

    @crud_bp.route(f'/{path_name}/view', methods=['GET'])
    def get_all_items_view() -> Response:
        '''Get all items in db on templated view'''
        items = fetch_all_data()
        return render_template('table.html', data=items)

    @crud_bp.route(f'/{path_name}/<int:item_id>', methods=['GET'])
    def get_item_by_id(item_id: int) -> Response:
        '''Get a single item by id'''
        item = fetch_one_data(item_id)
        if item:
            return jsonify(item.to_dict())
        abort(HTTPStatus.NOT_FOUND.value, data_not_found)

    @crud_bp.route(f'/{path_name}', methods=['POST'])
    def create_item() -> Response:
        '''Allow to create an item'''
        payload = request.get_json()
        if payload:
            result = save(model, payload)
            cache.delete(get_cache_key())
            return make_response(jsonify(result.to_dict()), HTTPStatus.CREATED.value)
        abort(HTTPStatus.BAD_REQUEST.value, data_should_be_json)

    @crud_bp.route(f'/{path_name}/<int:item_id>', methods=['PUT'])
    def update_item(item_id: int) -> Response:
        '''Update item using id'''
        payload = request.get_json()
        if payload:
            item = get_by_id(model, item_id)
            if item:
                result = update(item, payload)
                cache.delete(get_cache_key())
                cache.delete(get_cache_key(item_id))
                return jsonify(result.to_dict())
            abort(HTTPStatus.NOT_FOUND.value, data_not_found)
        abort(HTTPStatus.BAD_REQUEST.value, data_should_be_json)

    @crud_bp.route(f'/{path_name}/<int:item_id>', methods=['DELETE'])
    def delete_item(item_id: int) -> Response:
        '''Allow to delete an item'''
        item = get_by_id(model, item_id)
        if item:
            delete(item)
            cache.delete(get_cache_key())
            cache.delete(get_cache_key(item_id))
            return make_response('', HTTPStatus.NO_CONTENT.value)
        abort(HTTPStatus.NOT_FOUND.value, data_not_found)

    return crud_bp
