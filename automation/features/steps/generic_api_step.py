"""Include all generic calls that can be reused by any step"""

from typing import Any, Dict, Union
import requests

# pylint: disable=no-name-in-module
from behave import given, then
from requests import Response

# pylint: disable=import-error
from features import config, constants
from features.assertions.rest import RestAssertions
from features.decorators.api_validator import rest_call_validator


@given("load request data from {request_file}")
def step_given_request_data(context: Any, request_file: str) -> None:
    """Load request json from a given file path"""
    context.request_data = config.load_json(request_file)


@then("user get error from api with code {status}")
def step_then_error_response_from_api(context: Any, status: str) -> None:
    """Check model response match status, and some body validations"""
    actual_response = context.response

    RestAssertions.assert_not_error(actual_response)
    safe_response: Response = actual_response
    RestAssertions.assert_status(safe_response, int(status))
    RestAssertions.assert_content_type(safe_response, constants.JSON_TYPE)
    data = safe_response.json()
    RestAssertions.assert_path_exists(data, constants.JSON_NODE_PATH)
    RestAssertions.assert_path_exists(data, constants.JSON_NODE_MESSAGE)


@rest_call_validator
def step_get_call_url(path: str) -> Any:
    """Generic GET call to the api appending the path"""
    return requests.get(
        f"{config.get_base_url()}/{path}", timeout=constants.REQUEST_TIMEOUT
    )


@rest_call_validator
def step_post_call_url(path: str, payload: Union[Dict[str, Any], None]) -> Any:
    """Generic POST call to the api appending the path"""
    return requests.post(
        f"{config.get_base_url()}/{path}",
        json=payload,
        timeout=constants.REQUEST_TIMEOUT,
    )
