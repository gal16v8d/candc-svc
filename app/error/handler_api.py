"""Exception handling for app"""

from http import HTTPStatus
from typing import Any
import logging

from flask import request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from app.configs.log_cfg import LOG_NAME
from app.models.schemas import ApiErrorResponse
from app.error import custom_exc


log = logging.getLogger(LOG_NAME)
BAD_REQUEST_CLASSES = [
    custom_exc.BadArgException,
    custom_exc.BadModelException,
    custom_exc.UnpatchableFieldException,
]


def http_exc_handler(exc: HTTPException) -> tuple[dict[str, str | None], int]:
    """
    Maps httpexception in a json structured response
    :param exc: exception raised in the app
    :type exc: class:`werkzeug.exceptions.HTTPException`
    :return: create a common structure with error data
    :rtype: Tuple
    """
    log.warning("HTTPException -> %s", str(exc), exc_info=exc)
    code = exc.code or HTTPStatus.INTERNAL_SERVER_ERROR.value
    response = ApiErrorResponse(
        path=request.path,
        message=(
            exc.description
            if isinstance(exc.description, str)
            else str(exc.description)
        ),
    )
    return response.model_dump(), code


def val_exc_handler(exc: ValidationError) -> tuple[dict[str, Any], int]:
    """Maps validationerror in a json structured response"""
    log.warning("ValidationError -> %s", str(exc), exc_info=exc)
    response = ApiErrorResponse(
        path=request.path,
        message=exc.errors() if isinstance(exc.errors(), list) else str(exc.errors()),
    )
    return response.model_dump(), HTTPStatus.BAD_REQUEST.value


def sqlalchemy_exc_handler(
    exc: IntegrityError,
) -> tuple[dict[str, str | None], int]:
    """Maps validationerror in a json structured response"""
    log.warning("IntegrityError -> %s", str(exc), exc_info=exc)
    response = ApiErrorResponse(
        path=request.path,
        message=str(exc.orig) if hasattr(exc, "orig") else str(exc),
    )
    return response.model_dump(), HTTPStatus.BAD_REQUEST.value


def base_exc_handler(exc: Exception) -> tuple[dict[str, str], int]:
    """Maps exception in a json structured response"""
    log.warning("Exception -> %s", str(exc), exc_info=exc)
    response = ApiErrorResponse(
        path=request.path,
        message=str(exc),
    )
    if any(isinstance(exc, clazz) for clazz in BAD_REQUEST_CLASSES):
        code = HTTPStatus.BAD_REQUEST.value
    elif isinstance(exc, custom_exc.NotFoundException):
        code = HTTPStatus.NOT_FOUND.value
    else:
        code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    return response.model_dump(), code
