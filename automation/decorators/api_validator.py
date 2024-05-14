"""Decorator in use by the steps to validate and return PASSED/FAILED"""

import functools
from typing import Any, Callable, Dict, Union
import requests
# pylint: disable=import-error
import constants


def rest_call_validator(func: Callable) -> Callable:
    """Fun to annotate automation test cases"""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Dict[str, Union[str, Any]]:
        key = f"{func.__name__}_{args[0]}" if len(args) > 0 else func.__name__
        try:
            func(*args, **kwargs)
        except (
            requests.exceptions.RequestException,
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            AssertionError,
        ) as exc:
            return {key: constants.FAILED, "details": str(exc)}
        return {key: constants.PASSED}

    return wrapper
