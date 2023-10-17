'''Exception handling for app'''
from http import HTTPStatus
import logging
from flask import jsonify, request, Response
from werkzeug.exceptions import HTTPException
from app.configs.log_cfg import LOG_NAME
from app.error.bad_model_exc import BadModelException


log = logging.getLogger(LOG_NAME)


def http_exc_handler(exc: HTTPException) -> Response:
    '''Maps httpexception in a json structured response'''
    log.warning('HTTPException -> %s', str(exc), exc_info=exc)
    response = jsonify(path=request.path, message=exc.description)
    response.status_code = exc.code
    return response


def base_exc_handler(exc: Exception) -> Response:
    '''Maps exception in a json structured response'''
    log.warning('Exception -> %s', str(exc), exc_info=exc)
    response = jsonify(path=request.path, message=str(exc))
    if isinstance(exc, BadModelException):
        response.status_code = HTTPStatus.BAD_REQUEST
    else:
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return response
