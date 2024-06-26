"""Define the actions to perform /api/money/{model} check"""

from http import HTTPStatus
from typing import Any

# pylint: disable=no-name-in-module
from behave import when, then
from requests import Response

# pylint: disable=import-error
from assertions.rest import RestAssertions
from generic_api_step import step_post_call_url
from features import constants


@when("user call money endpoint as /api/money/{path}")
def step_when_call_money_endpoint(context: Any, path: str) -> None:
    """Calling POST /api/money/{path} on our api"""
    context.response = step_post_call_url(
        f"api/money/{path}",
        context.request_data if hasattr(context, "request_data") else {},
    )


@then("response should match money validations")
def step_then_money_response_should_match(context: Any) -> None:
    """Check money response match status and some body validations"""
    actual_response = context.response

    RestAssertions.assert_not_error(actual_response)
    safe_response: Response = actual_response
    RestAssertions.assert_status(safe_response, HTTPStatus.OK.value)
    RestAssertions.assert_content_type(safe_response, constants.JSON_TYPE)
    data = safe_response.json()
    RestAssertions.assert_path_exists(data, "available_cash")
    RestAssertions.assert_path_exists(data, "units")
