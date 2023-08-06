"""Responses module."""

from typing import Optional, Union


# Types
Result = Optional[Union[dict, list[dict]]]
ResponseData = dict[str, Union[str, dict]]

# Messages
MV_URL_NOT_FOUND = "The requested URL was not found"
MV_METHOD_NOT_ALLOWED = "The method is not allowed for the requested URL"
MV_MISSING_TOKEN = "Missing token"
MV_INVALID_TOKEN = "Invalid token"
MV_NOT_FRESH_TOKEN = "Not fresh token"
MV_EXPIRED_TOKEN = "Expired token"
MV_REVOKED_TOKEN = "Revoked token"
MV_USER_UNAUTHORIZED = "User unauthorized"
MV_VALIDATION_ERROR = "Validation error: {}"
MV_INTERNAL_SERVER_ERROR = "Internal server error"

# Message types
MT_OK = "ok"
MT_ERROR_URL_NOT_FOUND = "error_url_not_found"
MT_ERROR_METHOD_NOT_ALLOWED = "method_not_allowed"
MT_ERROR_INVALID_CREDENTIALS = "error_invalid_credentials"
MT_ERROR_MISSING_TOKEN = "error_missing_token"
MT_ERROR_INVALID_TOKEN = "error_invalid_token"
MT_ERROR_NOT_FRESH_TOKEN = "error_not_fresh_token"
MT_ERROR_EXPIRED_TOKEN = "error_expired_token"
MT_ERROR_REVOKED_TOKEN = "error_revoked_token"
MT_ERROR_UNAUTHORIZED_USER = "error_unauthorized_user"
MT_ERROR_VALIDATION = "error_validation"
MT_ERROR_ITEM_EXISTS = "error_item_exists"
MT_ERROR_ITEM_NOT_FOUND = "error_item_not_found"
MT_ERROR_INTERNAL_SERVER = "internal_server_error"


def get_response_data(
    message: str, message_type: str, result: Result = None
) -> ResponseData:
    """Return the response data of a given request.

    The value returned is a dictionary intended to be serialized as a JSON
    string and to be sent as the response data of a given request.

    :param message: Message.
    :param message_type: Message type.
    :param result: Result (optional).
    :return: Dictionary with the response data.
    """
    data = {"message": message, "message_type": message_type}

    if result is not None:
        data["result"] = result

    return data
