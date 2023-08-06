"""About view module."""

from flask import Blueprint
from notelist.responses import ResponseData, MT_OK, get_response_data


# Message value
MV_API_INFO_RETRIEVED = "API information retrieved"

# API information
API_NAME = "Notelist"
API_VERSION = "0.3.0"
API_DESCRIPTION = "Tag based note taking REST API"
API_AUTHOR = "Jose A. Jimenez"

# Blueprint object
bp = Blueprint("about", __name__)


@bp.route("", methods=["GET"])
def about() -> ResponseData:
    """Get information about the API.

    Response status codes:
        - 200 (Success)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.
        - result (object): API data.

    :return: Response data dictionary.
    """
    info = {
        "name": API_NAME,
        "version": API_VERSION,
        "description": API_DESCRIPTION,
        "author": API_AUTHOR}

    return get_response_data(MV_API_INFO_RETRIEVED, MT_OK, info), 200
