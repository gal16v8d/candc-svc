"""Allow to generate a resource that can be reused to expose several crud models"""

from http import HTTPStatus
from typing import Any, Dict, List, Type, Union
from flask import make_response, jsonify, render_template, request, typing
from flask_restx import Namespace, Resource
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


def create_crud_resource(
    ns: Namespace,
    model: Type[SQLModel],
    schema: Type[BaseModel],
    schema_list: Union[Type[BaseModel], None] = None,
) -> List:
    """Boilerplate code to create a crud resource"""
    name = model.__name__
    path_name = "infantry" if name == "Infantry" else f"{name.lower()}s"
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

    @ns.route("")
    class CrudBaseResource(Resource):
        """Base path crud resource"""

        def get(self) -> typing.ResponseReturnValue:
            """Get all items in db"""
            if len(request.args) > 0:
                query_params = request.args.to_dict()
                items = get_by_query_args(model, query_params)
            else:
                items = cache_service.fetch_from_cache_or_else(
                    get_cache_key(), fetch_all_data
                )
            if len(items) > 0 and schema_list is not None:
                result = (
                    schema_list(__root__=items).dict(exclude_none=True).get("__root__")
                )
                return jsonify(result)
            raise NotFoundException(name)

        def post(self) -> typing.ResponseReturnValue:
            """Allow to create an item"""
            payload = request.get_json()
            if payload:
                model_schema = schema(**payload)
                result = save(model, model_schema.dict())
                cache_service.clear_cache_by_name(get_cache_key())
                data = map_item_to_json(result)
                return make_response(data, HTTPStatus.CREATED.value)
            raise BadBodyException(name)

    @ns.route("/<item_id>")
    @ns.param("item_id", f"{path_name}'s id to fetch data")
    class CrudIdResource(Resource):
        """All the actions on id based resource path"""

        def get(self, item_id: int) -> typing.ResponseReturnValue:
            """Get a single item by id"""
            item = cache_service.fetch_from_cache_or_else(
                get_cache_key(item_id), fetch_one_data, item_id=item_id
            )
            if item:
                return jsonify(map_item_to_json(item))
            raise NotFoundException(name)

        def patch(self, item_id: int) -> typing.ResponseReturnValue:
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

        def delete(self, item_id: int) -> typing.ResponseReturnValue:
            """Allow to delete an item"""
            item = get_by_id(model, item_id)
            if item:
                delete(item)
                cache_service.clear_cache_by_name(get_cache_key())
                return make_response("", HTTPStatus.NO_CONTENT.value)
            raise NotFoundException(name)

    @ns.route("/view")
    class CrudViewResource(Resource):
        """Resource to render a template"""

        def get(self) -> typing.ResponseReturnValue:
            """Get all items in db on templated view"""
            if len(request.args) > 0:
                query_params = request.args.to_dict()
                items = get_by_query_args(model, query_params)
            else:
                items = fetch_all_data()
            items_schema = [schema(**i.to_dict()).dict() for i in items]
            return render_template("table.html", data=items_schema)

    return [CrudBaseResource, CrudIdResource, CrudViewResource]


def crud_route_ns(routes: List[Dict[str, Any]]) -> List[Namespace]:
    """Add all the relevant routes to create the namespaces"""
    ns_list = []
    for route in routes:
        model_name = route.get("name")
        ns = Namespace(
            model_name,
            description=f"Crud service for {model_name} entity",
            path=f"/api/{model_name}",
        )
        resources = create_crud_resource(
            ns, route.get("model"), route.get("schema"), route.get("schema_list")
        )
        # Append all the given path resources under the single namespace
        for resource in resources:
            ns.add_resource(resource)
        ns_list.append(ns)
    return ns_list
