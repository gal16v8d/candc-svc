"""Common rest api assertions"""

from http import HTTPStatus
from typing import Any, Final
import requests


FAILED: Final = "FAILED"
PASSED: Final = "PASSED"


def assert_status(response: requests.Response, expected_status: HTTPStatus) -> None:
    """Assert status code from response"""
    assert (
        expected_status.value == response.status_code
    ), f"Expected {expected_status} but got {response.status_code}"


def assert_content_type(
    response: requests.Response, expected_content_type: str
) -> None:
    """Assert content type from response"""
    content_type = response.headers.get("Content-Type")
    assert (
        content_type is not None and expected_content_type in content_type
    ), f"Expected {expected_content_type} but got {content_type}"


def assert_path_exists(data: Any, json_path: str) -> None:
    """Asserts data["json_path"] exists"""
    assert (
        data.get(json_path) is not None
    ), f"Expected '{json_path}' to be in the response"


def assert_path_value(data: Any, json_path: str, expected_val: Any) -> None:
    """Asserts data["json_path"] compared with expected_val"""
    assert (
        data[json_path] == expected_val
    ), f"Expected {str(expected_val)} but got {str(data[json_path])}"
