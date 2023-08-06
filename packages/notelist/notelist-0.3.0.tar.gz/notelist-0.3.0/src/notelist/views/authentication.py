"""Authentication views module."""

from flask import Blueprint, request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    jwt_required, create_access_token, create_refresh_token, get_jwt,
    get_jwt_identity)

from notelist.auth import blocklist
from notelist.models.users import User
from notelist.schemas.users import UserSchema
from notelist.tools import get_hash
from notelist.responses import (
    ResponseData, MV_VALIDATION_ERROR, MT_OK, MT_ERROR_INVALID_CREDENTIALS,
    MT_ERROR_VALIDATION, get_response_data)


# Message values
MV_USER_LOGGED_IN = "User logged in"
MV_INVALID_CREDENTIALS = "Invalid credentials"
MV_TOKEN_REFRESHED = "Token refreshed"
MV_USER_LOGGED_OUT = "User logged out"

# Schemas
user_list_schema = UserSchema(many=True)
user_schema = UserSchema()

# Blueprint object
bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["POST"])
def login() -> ResponseData:
    """Log in.

    This operation returns a fresh access token and a refresh token. Any of the
    tokens can be provided to an API request in the following header:
        "Authorization: Bearer access_token"

    Request data (JSON string):
        - username (string): Username.
        - password (string): Password.

    Response status codes:
        - 200 (Success)
        - 400 (Bad Request)
        - 401 (Unauthorized)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.
        - result (object): User ID, access token and refresh token.

    :return: Response data dictionary.
    """
    # Request data
    data = request.get_json() or {}

    # Validate request data
    fields = ["username", "password"]

    inv_fields = ", ".join(
        [i for i in data.keys() if i not in fields] + [
            i for i in fields if (
                i not in data or type(data[i]) != str or
                not data[i].strip())])

    if inv_fields:
        return get_response_data(
            MV_VALIDATION_ERROR.format(inv_fields), MT_ERROR_VALIDATION
        ), 400

    # We get the hash of the request password, as passwords are stored
    # encrypted in the database.
    user = User.get_by_username(data[fields[0]].strip())
    req_pw = get_hash(data[fields[1]].strip())

    # Check password
    if user and user.enabled and safe_str_cmp(req_pw, user.password):
        # Create access and refresh tokens. The user ID is the Identity of the
        # tokens (not to be confused with the JTI (unique identifier) of the
        # tokens).
        result = {
            "user_id": user.id,
            "access_token": create_access_token(user.id, fresh=True),
            "refresh_token": create_refresh_token(user.id)}

        return get_response_data(MV_USER_LOGGED_IN, MT_OK, result), 200

    return get_response_data(
        MV_INVALID_CREDENTIALS, MT_ERROR_INVALID_CREDENTIALS), 401


@bp.route("/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh() -> ResponseData:
    """Get a new, not fresh, access token.

    Refreshing the access token is needed when the token is expired. This
    operation requires the following header with a refresh token:
        "Authorization: Bearer refresh_token"

    Response status codes:
        - 200 (Success)
        - 401 (Unauthorized)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.
        - result (object): New, not fresh, access token.

    :return: Response data dictionary.
    """
    # Get the request JWT Identity, which in this application is equal to the
    # ID of the request user.
    uid = get_jwt_identity()

    # Create a new, not fresh, access token
    result = {"access_token": create_access_token(uid, fresh=False)}

    return get_response_data(MV_TOKEN_REFRESHED, MT_OK, result), 200


@bp.route("/logout", methods=["GET"])
@jwt_required()
def logout() -> ResponseData:
    """Log out.

    This operation revokes an access token provided in the request. This
    operation requires the following header with the access token:
        "Authorization: Bearer access_token"

    Response status codes:
        - 200 (Success)
        - 401 (Unauthorized)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.

    :return: Response data dictionary.
    """
    # JWT payload data
    jti = get_jwt()["jti"]  # JTI (unique identifier)

    # Add the JTI of the JWT of the current request to the Block List in order
    # to revoke the JWT.
    blocklist.add(jti)

    return get_response_data(MV_USER_LOGGED_OUT, MT_OK), 200
