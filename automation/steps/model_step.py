"""Basic checks on crud endpoints"""

from http import HTTPStatus
from typing import Any, Dict, Final
import requests

# pylint: disable=import-error
from assertions.rest import RestAssertions
from assertions.model_verifier import ModelVerifier
import config
import constants
from decorators.api_validator import rest_call_validator


MODELS: Final = [
    ModelVerifier(
        "boats",
        {
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
    )
]


class ModelSteps:
    """Model related steps"""

    @staticmethod
    @rest_call_validator
    def check_get_all(model_type: str, arg_and_type: Dict[str, Any]) -> Dict[str, str]:
        """Check list all the data for model type"""
        response = requests.get(
            f"{config.get_base_url()}/api/{model_type}",
            timeout=constants.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        RestAssertions.assert_status(response, HTTPStatus.OK)
        RestAssertions.assert_content_type(response, constants.JSON_TYPE)
        data = response.json()
        RestAssertions.assert_is_list(data)
        if len(data) > 0:
            RestAssertions.assert_data_elements(data[0], arg_and_type)
