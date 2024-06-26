"""Common constants in use by tests"""

from typing import Final, cast

import json

from werkzeug.test import TestResponse


UTF_8: Final[str] = "utf-8"


def assert_api_error(response: TestResponse, expected_code: int) -> None:
    """
    Check if response match expected code and data has
    the expected attributes defined for api model error response.
    :param response: Response from the api call
    :type response: class:`flask.testing.TestResponse`
    :param expected_code: Expected status code to match in the response
    :type expected_code: class:`int`
    """
    assert response.status_code == expected_code
    data_bytes: bytes = cast(bytes, response.data)
    data = json.loads(data_bytes.decode(UTF_8))
    assert data["message"] is not None
    assert data["path"] is not None
