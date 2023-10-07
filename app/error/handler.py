'''Exception handling for app'''
from http import HTTPStatus
from flask import jsonify, request, Response
from werkzeug.exceptions import HTTPException


def http_exc_handler(exc: HTTPException) -> Response:
    '''Maps httpexception in a json structured response'''
    response = jsonify(path=request.path, message=exc.description)
    response.status_code = exc.code
    return response


def base_exc_handler(exc: Exception) -> Response:
    '''Maps exception in a json structured response'''
    response = jsonify(path=request.path, message=str(exc))
    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return response
