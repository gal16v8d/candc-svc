"""Common rest api assertions"""

from http import HTTPStatus
from typing import Any, Dict, Final
import requests


FAILED: Final = "FAILED"
PASSED: Final = "PASSED"


class RestAssertions:
    """Assertions to implement in the rest calls"""

    @staticmethod
    def assert_status(response: requests.Response, expected_status: HTTPStatus) -> None:
        """Assert status code from response"""
        assert (
            expected_status.value == response.status_code
        ), f"Expected {expected_status} but got {response.status_code}"

    @staticmethod
    def assert_content_type(
        response: requests.Response, expected_content_type: str
    ) -> None:
        """Assert content type from response"""
        content_type = response.headers.get("Content-Type")
        assert (
            content_type is not None and expected_content_type in content_type
        ), f"Expected {expected_content_type} but got {content_type}"

    @staticmethod
    def assert_path_exists(data: Any, json_path: str) -> None:
        """Asserts data["json_path"] exists"""
        assert (
            data.get(json_path) is not None
        ), f"Expected '{json_path}' to be in the response"

    @staticmethod
    def assert_path_value(data: Any, json_path: str, expected_val: Any) -> None:
        """Asserts data["json_path"] compared with expected_val"""
        assert (
            data[json_path] == expected_val
        ), f"Expected {str(expected_val)} but got {str(data[json_path])}"

    @staticmethod
    def assert_is_list(data: Any) -> None:
        """Assert data object is actually a list"""
        assert isinstance(data, list), "Data is not a list"

    @staticmethod
    def assert_data_elements(
        data: Dict[str, Any], arg_and_type: Dict[str, Any]
    ) -> None:
        """
        Verify data element has all of the keys provided
        on arg_and_type attribute, plus also matching the
        provided value as instance/type
        """
        error_list = []
        for key, val in arg_and_type.items():
            if not isinstance(data.get(key), val):
                error_list.append(f"{key} should be {val}")
        assert len(error_list) == 0, ", ".join(error_list)
