"""Basic checks on health endpoint"""

from http import HTTPStatus
from typing import Dict
import requests

# pylint: disable=import-error
from assertions import rest
import config
import constants
from decorators.api_validator import rest_call_validator


class HealthSteps:
    """Health checker cases"""

    @staticmethod
    @rest_call_validator
    def check_health() -> Dict[str, str]:
        """Basic checks on health endpoint"""
        response = requests.get(
            f"{config.get_base_url()}/health", timeout=constants.REQUEST_TIMEOUT
        )
        response.raise_for_status()
        rest.assert_status(response, HTTPStatus.OK)
        rest.assert_content_type(response, constants.JSON_TYPE)
        data = response.json()
        rest.assert_path_value(data, "status", "UP")
