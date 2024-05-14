"""Basic checks on money spend endpoint"""

from http import HTTPStatus
from typing import Dict
import requests

# pylint: disable=import-error
from assertions import rest
import config
import constants
from decorators.api_validator import rest_call_validator


class MoneySteps:
    """Health checker cases"""

    @staticmethod
    @rest_call_validator
    def check_money_spend_ok(
        model_type: str, faction_id: int, money: int
    ) -> Dict[str, str]:
        """Basic checks on money spend endpoint""" ""
        payload: Dict[str, int] = {"faction_id": faction_id, "money": money}
        response = requests.post(
            f"{config.get_base_url()}/api/money/{model_type}",
            json=payload,
            timeout=constants.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        rest.assert_status(response, HTTPStatus.OK)
        rest.assert_content_type(response, constants.JSON_TYPE)
        data = response.json()
        rest.assert_path_exists(data, "available_cash")
        rest.assert_path_exists(data, "units")

    @staticmethod
    @rest_call_validator
    def check_money_spend_no_payload(model_type: str) -> Dict[str, str]:
        """Check with no payload"""
        response = requests.post(
            f"{config.get_base_url()}/api/money/{model_type}",
            json={},
            timeout=constants.REQUEST_TIMEOUT,
        )
        rest.assert_status(response, HTTPStatus.BAD_REQUEST)
        rest.assert_content_type(response, constants.JSON_TYPE)
        data = response.json()
        rest.assert_path_exists(data, "path")
        rest.assert_path_exists(data, "message")
