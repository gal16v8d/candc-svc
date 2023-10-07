'''Generic blueprint CRUD'''
from http import HTTPStatus
from flask import Blueprint, Response, abort, jsonify, make_response, request
from app.models.database import get_all, get_by_id, save, update, delete


def create_crud_blueprint(model):
    '''Generic blueprint to perform CRUD operations'''
    name = model.__name__
    data_not_found = f'{name} not found'
    data_should_be_json = f'{name} data should be json'
    crud_bp = Blueprint(name.lower(), __name__)
    path_name = 'infantry' if name == 'Infantry' else f'{name.lower()}s'

    @crud_bp.route(f'/{path_name}', methods=['GET'])
    def get_all_items() -> Response:
        '''Get all items in db'''
        items = get_all(model)
        return jsonify([i.to_dict() for i in items])

    @crud_bp.route(f'/{path_name}/<int:item_id>', methods=['GET'])
    def get_item_by_id(item_id: int) -> Response:
        '''Get a single item by id'''
        item = get_by_id(model, item_id)
        if item:
            return jsonify(item.to_dict())
        abort(HTTPStatus.NOT_FOUND.value, data_not_found)

    @crud_bp.route(f'/{path_name}', methods=['POST'])
    def create_item() -> Response:
        '''Allow to create an item'''
        payload = request.get_json()
        if payload:
            result = save(model, payload)
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
                return jsonify(result.to_dict())
            abort(HTTPStatus.NOT_FOUND.value, data_not_found)
        abort(HTTPStatus.BAD_REQUEST.value, data_should_be_json)

    @crud_bp.route(f'/{path_name}/<int:item_id>', methods=['DELETE'])
    def delete_item(item_id: int) -> Response:
        '''Allow to delete an item'''
        item = get_by_id(model, item_id)
        if item:
            delete(item)
            return make_response('', HTTPStatus.NO_CONTENT.value)
        abort(HTTPStatus.NOT_FOUND.value, data_not_found)

    return crud_bp
