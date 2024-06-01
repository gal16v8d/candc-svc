"""Define the actions to perform CRUD /api/{model} check"""

from http import HTTPStatus
from typing import Any, Dict

# pylint: disable=no-name-in-module
from behave import when, then
from requests import Response

# pylint: disable=import-error
from assertions.rest import RestAssertions
from generic_api_step import step_get_call_url
from features import constants


MODELS: Dict[str, Any] = {
    "boats": {
        "created_at": str,
        "updated_at": str,
        "boat_id": int,
        "base_cost": int,
        "name": str,
        "active": bool,
        "build_limit": bool,
        "is_special": bool,
        "target_air_unit": bool,
        "can_go_ground": bool,
    },
    "boatxfactions": {
        "active": bool,
        "boat_id": int,
        "created_at": str,
        "faction_id": int,
        "id": int,
    },
    "factions": {
        "active": bool,
        "created_at": str,
        "faction_id": int,
        "game_id": int,
        "name": str,
        "notes": str,
    },
    "games": {"active": bool, "created_at": str, "game_id": int, "name": str},
    "infantry": {
        "active": bool,
        "base_cost": int,
        "build_limit": bool,
        "can_fly": bool,
        "can_swim": bool,
        "created_at": str,
        "infantry_id": int,
        "is_special": bool,
        "is_stealth": bool,
        "name": str,
        "target_air_unit": bool,
        "updated_at": str,
    },
    "infantryxfactions": {
        "active": bool,
        "created_at": str,
        "faction_id": int,
        "id": int,
        "infantry_id": int,
    },
    "planes": {
        "active": bool,
        "base_cost": int,
        "build_limit": bool,
        "created_at": str,
        "is_special": bool,
        "is_stealth": bool,
        "name": str,
        "plane_id": int,
        "target_air_unit": bool,
    },
    "planexfactions": {
        "active": bool,
        "created_at": str,
        "faction_id": int,
        "id": int,
        "plane_id": int,
    },
    "structures": {
        "active": bool,
        "base_cost": int,
        "base_defense": bool,
        "build_limit": bool,
        "build_on_water": bool,
        "created_at": str,
        "is_special": bool,
        "is_stealth": bool,
        "name": str,
        "structure_id": int,
        "target_air_unit": bool,
    },
    "structurexfactions": {
        "active": bool,
        "created_at": str,
        "faction_id": int,
        "id": int,
        "structure_id": int,
    },
    "tanks": {
       "active": bool,
		"base_cost": int,
		"build_limit": bool,
		"can_swim": bool,
		"created_at": str,
		"is_special": bool,
		"is_stealth": bool,
		"name": str,
		"notes": str,
		"tank_id": int,
		"target_air_unit": bool 
    },
    "tankxfactions": {
        "active": bool,
		"created_at": str,
		"faction_id": int,
		"id": int,
		"tank_id": int
    }
}


@when("user call model endpoint as /api/'{path}'")
def step_when_call_model_endpoint(context: Any, path: str) -> None:
    """Calling GET /api/{path} on our api"""
    context.response = step_get_call_url(f"api/{path}")
    context.path = path


@then("response should match model validations")
def step_then_model_response_should_match(context: Any) -> None:
    """Check model response match status, and some body validations"""
    actual_response = context.response

    RestAssertions.assert_not_error(actual_response)
    safe_response: Response = actual_response
    RestAssertions.assert_status(safe_response, HTTPStatus.OK.value)
    RestAssertions.assert_content_type(safe_response, constants.JSON_TYPE)
    data = safe_response.json()
    RestAssertions.assert_is_list(data)
    if len(data) > 0:
        model = context.path if hasattr(context, "path") else ""
        arg_and_type = MODELS.get(model, {})
        RestAssertions.assert_data_elements(data[0], arg_and_type)
