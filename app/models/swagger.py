"""Swagger models and examples"""

from flask_restx import Namespace, Model, OrderedModel, fields


def get_cache_model_response() -> Model | OrderedModel:
    """Build namespace model for cache keys response"""
    return fields.List(fields.String, description="List of keys", example=["boats"])


def get_health_model_response(ns: Namespace) -> Model | OrderedModel:
    """Build namespace model for health response"""
    return ns.model(
        "Health",
        {"status": fields.String(description="UP if app is live", example="UP")},
    )


def get_money_model_response(ns: Namespace) -> Model | OrderedModel:
    """Build namespace model for money response"""
    units_model = ns.model(
        "UnitsData", {"units": fields.Raw(example={"Aegis Cruiser": 2, "Dolphin": 4})}
    )
    money_model = ns.model(
        "MoneyData",
        {
            "available_cash": fields.Integer(
                description="Money that was not spend", example=100
            ),
            "units": fields.Nested(units_model),
        },
    )
    return money_model
