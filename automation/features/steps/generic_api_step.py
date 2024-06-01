"""Include all generic calls that can be reused by any step"""

from typing import Any, Dict, Union
import requests

# pylint: disable=no-name-in-module
from behave import given

# pylint: disable=import-error
from features import config, constants
from features.decorators.api_validator import rest_call_validator


@given("load request data from '{request_file}'")
def step_given_request_data(context: Any, request_file: str) -> None:
    context.request_data = config.load_json(request_file)


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
