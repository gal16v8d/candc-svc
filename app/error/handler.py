'''Exception handling for app'''
from http import HTTPStatus
import logging
from flask import jsonify, request, Response
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException
from app.configs.log_cfg import LOG_NAME
from app.error.bad_arg_exc import BadArgException
from app.error.bad_model_exc import BadModelException


log = logging.getLogger(LOG_NAME)


def http_exc_handler(exc: HTTPException) -> Response:
    '''Maps httpexception in a json structured response'''
    log.warning('HTTPException -> %s', str(exc), exc_info=exc)
    response = jsonify(path=request.path, message=exc.description)
    response.status_code = exc.code
    return response


def val_exc_handler(exc: ValidationError) -> Response:
    '''Maps validationerror in a json structured response'''
    log.warning('ValidationError -> %s', str(exc), exc_info=exc)
    response = jsonify(path=request.path, message=exc.errors())
    response.status_code = HTTPStatus.BAD_REQUEST
    return response


def sqlalchemy_exc_handler(exc: IntegrityError) -> Response:
    '''Maps validationerror in a json structured response'''
    log.warning('IntegrityError -> %s', str(exc), exc_info=exc)
    response = jsonify(path=request.path, message=str(exc.orig))
    response.status_code = HTTPStatus.BAD_REQUEST
    return response


def base_exc_handler(exc: Exception) -> Response:
    '''Maps exception in a json structured response'''
    log.warning('Exception -> %s', str(exc), exc_info=exc)
    response = jsonify(path=request.path, message=str(exc))
    if isinstance(exc, BadModelException) or isinstance(exc, BadArgException):
        response.status_code = HTTPStatus.BAD_REQUEST
    else:
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return response
