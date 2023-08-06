"""User views module."""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt

from notelist.models.users import User
from notelist.schemas.users import UserSchema
from notelist.tools import get_current_ts
from notelist.responses import (
    ResponseData, MV_USER_UNAUTHORIZED, MV_VALIDATION_ERROR, MT_OK,
    MT_ERROR_UNAUTHORIZED_USER, MT_ERROR_VALIDATION, MT_ERROR_ITEM_EXISTS,
    MT_ERROR_ITEM_NOT_FOUND, get_response_data)


# Message values
MV_USER_RETRIEVED_1 = "1 user retrieved"
MV_USER_RETRIEVED_N = "{} users retrieved"
MV_USER_RETRIEVED = "User retrieved"
MV_USER_NOT_FOUND = "User not found"
MV_USER_CREATED = "User created"
MV_USER_EXISTS = "A user with the same username already exists"
MV_USER_UPDATED = "User updated"
MV_USER_DELETED = "User deleted"

# Schemas
user_list_schema = UserSchema(many=True)
user_schema = UserSchema()

# Blueprint object
bp = Blueprint("users", __name__)


@bp.route("/users", methods=["GET"])
@jwt_required()
def get_users() -> ResponseData:
    """Get all existing users.

    This operation requires administrator permissions and the following header
    with an access token:
        "Authorization: Bearer access_token"

    Response status codes:
        - 200 (Success)
        - 401 (Unauthorized)
        - 403 (Forbidden)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.
        - result (list): Users data.

    :return: Response data dictionary.
    """
    # JWT payload data
    admin = get_jwt()["admin"]

    # Check permissions
    if not admin:
        return get_response_data(
            MV_USER_UNAUTHORIZED, MT_ERROR_UNAUTHORIZED_USER), 403

    # Get all users
    users = User.get_all()

    c = len(users)
    mv = MV_USER_RETRIEVED_1 if c == 1 else MV_USER_RETRIEVED_N.format(c)

    return get_response_data(mv, MT_OK, user_list_schema.dump(users)), 200


@bp.route("/user/<user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id: str) -> ResponseData:
    """Get an existing user's data.

    The user can call this operation only for their own data, unless they are
    an administrator. This operation requires the following header with an
    access token:
        "Authorization: Bearer access_token"

    Request parameters:
        - user_id (string): User ID.

    Response status codes:
        - 200 (Success)
        - 401 (Unauthorized)
        - 403 (Forbidden)
        - 404 (Not Found)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.
        - result (object): User data.

    :param user_id: User ID.
    :return: Response data dictionary.
    """
    # JWT payload data
    jwt = get_jwt()
    uid = jwt["user_id"]
    admin = jwt["admin"]

    # Check permissions
    if not admin and uid != user_id:
        return get_response_data(
            MV_USER_UNAUTHORIZED, MT_ERROR_UNAUTHORIZED_USER), 403

    # Get the user
    user = User.get_by_id(user_id)

    # Check if the user doesn't exist
    if not user:
        return get_response_data(
            MV_USER_NOT_FOUND, MT_ERROR_ITEM_NOT_FOUND), 404

    return get_response_data(
        MV_USER_RETRIEVED, MT_OK, user_schema.dump(user)), 200


@bp.route("/user", methods=["POST", "PUT"])
@jwt_required()
def create_user() -> ResponseData:
    """Create a new user.

    This operation requires administrator permissions and the following header
    with an access token:
        "Authorization: Bearer access_token"

    Request data (JSON string):
        - username (string): Username.
        - password (string): Password. It must have 8-100 characters.
        - admin (boolean, optional): Whether the user is an administrator or
            not (default).
        - enabled (boolean, optional): Whether the user is enabled or not
            (default).
        - name (string, optional): Full name.
        - email (string, optional): E-mail address.

    Response status codes:
        - 201 (Success)
        - 400 (Bad Request)
        - 401 (Unauthorized)
        - 403 (Forbidden)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.
        - result (object): User ID.

    :return: Response data dictionary.
    """
    # JWT payload data
    admin = get_jwt()["admin"]

    # Check permissions
    if not admin:
        return get_response_data(
            MV_USER_UNAUTHORIZED, MT_ERROR_UNAUTHORIZED_USER), 403

    # Request data
    data = request.get_json() or {}

    # We validate the request data. If any of the User model required fields is
    # missing, a "marshmallow.ValidationError" exception is raised.
    user = user_schema.load(data)
    user.username = user.username.strip()

    if not user.username:
        return get_response_data(
            MV_VALIDATION_ERROR.format("username"), MT_ERROR_VALIDATION
        ), 400

    # Check if the user already exists (based on its username)
    if User.get_by_username(user.username):
        return get_response_data(MV_USER_EXISTS, MT_ERROR_ITEM_EXISTS), 400

    # Save the user
    user.save()
    result = {"id": user.id}

    return get_response_data(MV_USER_CREATED, MT_OK, result), 201


@bp.route("/user/<user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id: str) -> ResponseData:
    """Update an existing user.

    The user, if they aren't an administrator, can call this operation only to
    update their own data, except the "username", "admin" or "enabled" fields.
    This operation requires the following header with an access token:
        "Authorization: Bearer access_token"

    Request parameters:
        - user_id (string): User ID.

    Request data (JSON string):
        - username (string, optional): Username.
        - password (string, optional): Password. It must have 8-100 characters.
        - admin (boolean, optional): Whether the user is an administrator or
            not (default).
        - enabled (boolean, optional): Whether the user is enabled or not
            (default).
        - name (string, optional): Full name.
        - email (string, optional): E-mail address.

    Response status codes:
        - 200 (Success)
        - 400 (Bad Request)
        - 401 (Unauthorized)
        - 403 (Forbidden)
        - 404 (Not Found)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.

    :param user_id: User ID.
    :return: Response data dictionary.
    """
    # JWT payload data
    jwt = get_jwt()
    uid = jwt["user_id"]
    admin = jwt["admin"]

    # Request data
    data = request.get_json() or {}

    # Get existing user
    user = User.get_by_id(user_id)

    # Check if the user exists and the permissions. "username", "admin" and
    # "enabled" are the fields that not administrator users aren't allowed to
    # modify.
    if (
        not admin and (
            not user or uid != user.id or "username" in data
            or "admin" in data or "enabled" in data)
    ):
        return get_response_data(
            MV_USER_UNAUTHORIZED, MT_ERROR_UNAUTHORIZED_USER), 403
    elif admin and not user:
        return get_response_data(
            MV_USER_NOT_FOUND, MT_ERROR_ITEM_NOT_FOUND), 404

    # Make a copy of the request data
    data = data.copy()

    # Check if a new username is provided and if there is already a user with
    # this username.
    if "username" in data:
        if (
            type(data["username"]) != str or
            not data["username"].strip()
        ):
            return get_response_data(
                MV_VALIDATION_ERROR.format("username"), MT_ERROR_VALIDATION
            ), 400

        data["username"] = data["username"].strip()

        if (
            data["username"] != user.username and
            User.get_by_username(data["username"])
        ):
            return get_response_data(
                MV_USER_EXISTS, MT_ERROR_ITEM_EXISTS), 400
    else:
        data["username"] = user.username

    # Check if new values for "enabled", "admin", "name" or "email" are
    # provided.
    if "enabled" not in data:
        data["enabled"] = user.enabled

    if "admin" not in data:
        data["admin"] = user.admin

    if "name" not in data:
        data["name"] = user.name

    if "email" not in data:
        data["email"] = user.email

    # Check if a new value for the password is provided. If not, we need to
    # temporarily store the current encrypted password and recover it later as
    # "user_schema.load" will encrypt again the password.
    password = user.password if "password" not in data else None

    # We validate the request data. If any provided field is invalid, a
    # "marshmallow.ValidationError" exception is raised.
    new_user = user_schema.load(data)

    # Update user object
    user.username = new_user.username
    user.admin = new_user.admin
    user.enabled = new_user.enabled
    user.name = new_user.name
    user.email = new_user.email
    user.password = password if password else new_user.password

    # Save user
    user.last_modified_ts = get_current_ts()
    user.save()

    return get_response_data(MV_USER_UPDATED, MT_OK), 200


@bp.route("/user/<user_id>", methods=["DELETE"])
@jwt_required(fresh=True)
def delete_user(user_id: str) -> ResponseData:
    """Delete an existing user.

    This operation requires administrator permissions and the following header
    with a fresh access token:
        "Authorization: Bearer fresh_access_token"

    Request parameters:
        - user_id (string): User ID.

    Response status codes:
        - 200 (Success)
        - 401 (Unauthorized)
        - 403 (Forbidden)
        - 404 (Not Found)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.

    :param user_id: User ID.
    :return: Dictionary with the message.
    """
    # JWT payload data
    admin = get_jwt()["admin"]

    # Check permissions (only administrator users can delete users)
    if not admin:
        return get_response_data(
            MV_USER_UNAUTHORIZED, MT_ERROR_UNAUTHORIZED_USER), 403

    # Get user
    user = User.get_by_id(user_id)

    # Check if the user doesn't exist
    if not user:
        return get_response_data(
            MV_USER_NOT_FOUND, MT_ERROR_ITEM_NOT_FOUND), 404

    # Delete user
    user.delete()

    return get_response_data(MV_USER_DELETED, MT_OK), 200
