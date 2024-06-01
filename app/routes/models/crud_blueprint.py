"""Generic blueprint CRUD"""

from http import HTTPStatus
from typing import Any, List, Type, Union
from flask import Blueprint, make_response, jsonify, render_template, request, typing
from pydantic import BaseModel
from sqlmodel import SQLModel
from app.error.custom_exc import BadBodyException, NotFoundException
from app.models.database import (
    get_all,
    get_by_id,
    get_by_query_args,
    delete,
    patch,
    save,
)
from app.service.cache_service import CacheService


def create_crud_blueprint(
    model: Type[SQLModel],
    schema: Type[BaseModel],
    schema_list: Union[Type[BaseModel], None] = None,
) -> Blueprint:
    """Generic blueprint to perform CRUD operations"""
    name = model.__name__
    path_name = "infantry" if name == "Infantry" else f"{name.lower()}s"
    crud_bp = Blueprint(name.lower(), __name__)
    cache_service = CacheService()

    def get_cache_key(item_id: Union[int, None] = None) -> str:
        """get cache key for the model"""
        return path_name if item_id is None else f"{path_name}-{item_id}"

    def fetch_all_data() -> List[Any]:
        """
        Fetch all data from db and transform in dict
        """
        return get_all(model)

    def fetch_one_data(item_id: int) -> Any:
        return get_by_id(model, item_id)

    def map_item_to_json(item: Any) -> typing.ResponseReturnValue:
        """Map a single item into json schema"""
        return schema(**item.to_dict()).dict(exclude_none=True)

    @crud_bp.route(f"/{path_name}", methods=["GET"])
    def get_all_items() -> typing.ResponseReturnValue:
        """Get all items in db"""
        if len(request.args) > 0:
            query_params = request.args.to_dict()
            items = get_by_query_args(model, query_params)
        else:
            items = cache_service.fetch_from_cache_or_else(
                get_cache_key(), fetch_all_data
            )
        if len(items) > 0 and schema_list is not None:
            result = schema_list(__root__=items).dict(exclude_none=True).get("__root__")
            return jsonify(result)
        raise NotFoundException(name)

    @crud_bp.route(f"/{path_name}/view", methods=["GET"])
    def get_all_items_view() -> typing.ResponseReturnValue:
        """Get all items in db on templated view"""
        if len(request.args) > 0:
            query_params = request.args.to_dict()
            items = get_by_query_args(model, query_params)
        else:
            items = fetch_all_data()
        items_schema = [schema(**i.to_dict()).dict() for i in items]
        return render_template("table.html", data=items_schema)

    @crud_bp.route(f"/{path_name}/<int:item_id>", methods=["GET"])
    def get_item_by_id(item_id: int) -> typing.ResponseReturnValue:
        """Get a single item by id"""
        item = cache_service.fetch_from_cache_or_else(
            get_cache_key(item_id), fetch_one_data, item_id=item_id
        )
        if item:
            return jsonify(map_item_to_json(item))
        raise NotFoundException(name)

    @crud_bp.route(f"/{path_name}", methods=["POST"])
    def create_item() -> typing.ResponseReturnValue:
        """Allow to create an item"""
        payload = request.get_json()
        if payload:
            model_schema = schema(**payload)
            result = save(model, model_schema.dict())
            cache_service.clear_cache_by_name(get_cache_key())
            data = map_item_to_json(result)
            return make_response(data, HTTPStatus.CREATED.value)
        raise BadBodyException(name)

    @crud_bp.route(f"/{path_name}/<int:item_id>", methods=["PATCH"])
    def patch_item(item_id: int) -> typing.ResponseReturnValue:
        """Patch item using id"""
        payload = request.get_json()
        if payload:
            item = get_by_id(model, item_id)
            if item:
                result = patch(item, payload)
                cache_service.clear_cache_by_name(get_cache_key())
                return jsonify(map_item_to_json(result))
            raise NotFoundException(name)
        raise BadBodyException(name)

    @crud_bp.route(f"/{path_name}/<int:item_id>", methods=["DELETE"])
    def delete_item(item_id: int) -> typing.ResponseReturnValue:
        """Allow to delete an item"""
        item = get_by_id(model, item_id)
        if item:
            delete(item)
            cache_service.clear_cache_by_name(get_cache_key())
            return make_response("", HTTPStatus.NO_CONTENT.value)
        raise NotFoundException(name)

    return crud_bp
