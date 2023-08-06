"""Error handlers module."""

from flask import Flask
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound, MethodNotAllowed, InternalServerError

from notelist.responses import (
    ResponseData, MV_URL_NOT_FOUND, MV_METHOD_NOT_ALLOWED, MV_VALIDATION_ERROR,
    MV_INTERNAL_SERVER_ERROR, MT_ERROR_URL_NOT_FOUND,
    MT_ERROR_METHOD_NOT_ALLOWED, MT_ERROR_VALIDATION, MT_ERROR_INTERNAL_SERVER,
    get_response_data)


# Type
ValErrorData = dict[str, list[str]]


def not_found_handler(e: NotFound):
    """Handle 404 errors (Not Found) (callback function).

    :param e: Exception object.
    :return: Response data dictionary.
    """
    return get_response_data(MV_URL_NOT_FOUND, MT_ERROR_URL_NOT_FOUND), 404


def method_not_allowed_handler(e: MethodNotAllowed):
    """Handle 405 errors (Method Not Allowed) (callback function).

    :param e: Exception object.
    :return: Response data dictionary.
    """
    return get_response_data(
        MV_METHOD_NOT_ALLOWED, MT_ERROR_METHOD_NOT_ALLOWED), 405


def internal_server_error_handler(e: InternalServerError):
    """Handle 500 errors (Internal Server Error) (callback function).

    :param e: Exception object.
    :return: Response data dictionary.
    """
    return get_response_data(
        MV_INTERNAL_SERVER_ERROR, MT_ERROR_INTERNAL_SERVER), 500


def validation_error_handler(error: ValErrorData) -> ResponseData:
    """Handle validation errors (callback function).

    :param error: Object containing the error messages.
    :return: Response data dictionary.
    """
    fields = ", ".join([i for i in error.messages.keys()])
    return get_response_data(
        MV_VALIDATION_ERROR.format(fields), MT_ERROR_VALIDATION), 400


def register_error_handlers(app: Flask):
    """Register the error handlers.

    :param app: Flask application object.
    """
    for e, f in [
        (NotFound, not_found_handler),
        (MethodNotAllowed, method_not_allowed_handler),
        (InternalServerError, internal_server_error_handler),
        (ValidationError, validation_error_handler)
    ]:
        app.register_error_handler(e, f)
