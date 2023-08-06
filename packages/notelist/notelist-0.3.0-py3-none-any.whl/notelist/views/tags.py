"""Tag views module."""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt

from notelist.models.notebooks import Notebook
from notelist.models.tags import Tag
from notelist.schemas.tags import TagSchema
from notelist.tools import get_current_ts
from notelist.responses import (
    ResponseData, MV_USER_UNAUTHORIZED, MV_VALIDATION_ERROR, MT_OK,
    MT_ERROR_UNAUTHORIZED_USER, MT_ERROR_VALIDATION, MT_ERROR_ITEM_EXISTS,
    get_response_data)


# Message values
MV_TAG_RETRIEVED_1 = "1 tag retrieved"
MV_TAG_RETRIEVED_N = "{} tags retrieved"
MV_TAG_RETRIEVED = "Tag retrieved"
MV_TAG_CREATED = "Tag created"
MV_TAG_UPDATED = "Tag updated"
MV_TAG_DELETED = "Tag deleted"
MV_TAG_EXISTS = "A tag with the same name already exists in the notebook"

# Schemas
tag_list_schema = TagSchema(
    many=True, only=("id", "name", "color", "created_ts", "last_modified_ts"))

tag_schema = TagSchema()

# Blueprint object
bp = Blueprint("tags", __name__)


@bp.route("/tags/<notebook_id>", methods=["GET"])
@jwt_required()
def get_tags(notebook_id: int) -> ResponseData:
    """Get all the tags of a notebook.

    The user can call this operation only for their own notebooks. This
    operation requires the following header with an access token:
        "Authorization: Bearer access_token"

    Request parameters:
        - notebook_id (string): Notebook ID.

    Response status codes:
        - 200 (Success)
        - 401 (Unauthorized)
        - 403 (Forbidden)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.
        - result (list): Tags data.

    :param notebook_id: Notebook ID.
    :return: Response data dictionary.
    """
    # JWT payload data
    uid = get_jwt()["user_id"]

    # Get notebook
    notebook = Notebook.get_by_id(notebook_id)

    # Check if the notebook exists and the permissions
    if not notebook or uid != notebook.user_id:
        return get_response_data(
            MV_USER_UNAUTHORIZED, MT_ERROR_UNAUTHORIZED_USER), 403

    # Get notebook tags
    tags = sorted(notebook.tags, key=lambda t: t.name)
    c = len(tags)
    mv = MV_TAG_RETRIEVED_1 if c == 1 else MV_TAG_RETRIEVED_N.format(c)

    return get_response_data(mv, MT_OK, tag_list_schema.dump(tags)), 200


@bp.route("/tag/<tag_id>", methods=["GET"])
@jwt_required()
def get_tag(tag_id: str) -> ResponseData:
    """Get an existing tag's data.

    The user can call this operation only for their own notebooks' tags. This
    operation requires the following header with an access token:
        "Authorization: Bearer access_token"

    Request parameters:
        - tag_id (string): Tag ID.

    Response status codes:
        - 200 (Success)
        - 401 (Unauthorized)
        - 403 (Forbidden)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.
        - result (object): Tag data.

    :param tag_id: Tag ID.
    :return: Response data dictionary.
    """
    # JWT payload data
    uid = get_jwt()["user_id"]

    # Get tag
    tag = Tag.get_by_id(tag_id)

    # Check if the tag exists and the permissions
    if not tag or uid != tag.notebook.user_id:
        return get_response_data(
            MV_USER_UNAUTHORIZED, MT_ERROR_UNAUTHORIZED_USER), 403

    return get_response_data(
        MV_TAG_RETRIEVED, MT_OK, tag_schema.dump(tag)), 200


@bp.route("/tag", methods=["POST", "PUT"])
@jwt_required()
def create_tag() -> ResponseData:
    """Create a new tag.

    The user can call this operation only for their own notebooks. This
    operation requires the following header with an access token:
        "Authorization: Bearer access_token"

    Request data (JSON string):
        - notebook_id (string): Notebook ID.
        - name (string): Tag name.
        - color (string, optional): Tag color. E.g. "#00ff00".

    Response status codes:
        - 201 (Success)
        - 400 (Bad Request)
        - 401 (Unauthorized)
        - 403 (Forbidden)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.
        - result (object): Tag ID.

    :return: Response data dictionary.
    """
    # JWT payload data
    uid = get_jwt()["user_id"]

    # Request data
    data = request.get_json() or {}

    # We validate the request data. If any of the Tag model required fields is
    # missing, a "marshmallow.ValidationError" exception is raised.
    tag = tag_schema.load(data)
    tag.name = tag.name.strip()

    if not tag.name:
        return get_response_data(
            MV_VALIDATION_ERROR.format("name"), MT_ERROR_VALIDATION), 400

    # Check if the notebook exists and the permissions (the request user must
    # be the same as the notebook's user).
    notebook = Notebook.get_by_id(tag.notebook_id)

    if not notebook or uid != notebook.user_id:
        return get_response_data(
            MV_USER_UNAUTHORIZED, MT_ERROR_UNAUTHORIZED_USER), 403

    # Check if the notebook already has the tag (based on the tag name)
    if Tag.get_by_name(notebook.id, tag.name):
        return get_response_data(MV_TAG_EXISTS, MT_ERROR_ITEM_EXISTS), 400

    # Save tag
    tag.save()
    result = {"id": tag.id}

    return get_response_data(MV_TAG_CREATED, MT_OK, result), 201


@bp.route("/tag/<tag_id>", methods=["PUT"])
@jwt_required()
def update_tag(tag_id: str) -> ResponseData:
    """Update an existing tag.

    The user can call this operation only for their own notebooks' tags and the
    notebook ID of the tag cannot be changed. This operation requires the
    following header with an access token:
        "Authorization" = "Bearer access_token"

    Request parameters:
        - tag_id (string): Tag ID.

    Request data (JSON string):
        - name (string, optional): Tag name.
        - color (string, optional): Tag color. E.g. "#00ff00".

    Response status codes:
        - 200 (Success)
        - 400 (Bad Request)
        - 401 (Unauthorized)
        - 403 (Forbidden)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.

    :param tag_id: Tag ID.
    :return: Dictionary with the message.
    """
    # JWT payload data
    uid = get_jwt()["user_id"]

    # Request data
    data = request.get_json() or {}

    # Get existing tag
    tag = Tag.get_by_id(tag_id)

    # Check if the tag exists and the permissions
    if not tag or uid != tag.notebook.user_id:
        return get_response_data(
            MV_USER_UNAUTHORIZED, MT_ERROR_UNAUTHORIZED_USER), 403

    # Make a copy of the request data
    data = data.copy()

    # Check if a new value for the "notebook_id" field is provided, which is
    # not allowed.
    if "notebook_id" in data:
        return get_response_data(
            MV_VALIDATION_ERROR.format("notebook_id"), MT_ERROR_VALIDATION
        ), 400
    else:
        data["notebook_id"] = tag.notebook_id

    # Check if a new value for the name is provided and if the notebook has
    # already a tag with this name.
    if "name" in data:
        if type(data["name"]) != str or not data["name"].strip():
            return get_response_data(
                MV_VALIDATION_ERROR.format("name"), MT_ERROR_VALIDATION
            ), 400

        data["name"] = data["name"].strip()

        if (
            data["name"] != tag.name and
            Tag.get_by_name(tag.notebook_id, data["name"])
        ):
            return get_response_data(
                MV_TAG_EXISTS, MT_ERROR_ITEM_EXISTS), 400
    else:
        data["name"] = tag.name

    # Check if a new value for the color is provided
    if "color" not in data:
        data["color"] = tag.color

    # We validate the request data. If any provided field is invalid, a
    # "marshmallow.ValidationError" exception is raised.
    new_tag = tag_schema.load(data)

    # Update tag object
    tag.name = new_tag.name
    tag.color = new_tag.color

    # Save tag
    tag.last_modified_ts = get_current_ts()
    tag.save()

    return get_response_data(MV_TAG_UPDATED, MT_OK), 200


@bp.route("/tag/<tag_id>", methods=["DELETE"])
@jwt_required()
def delete_tag(tag_id: str) -> ResponseData:
    """Delete an existing tag.

    The user can call this operation only for their own notebooks' tags. This
    operation requires the following header with an access token:
        "Authorization: Bearer access_token"

    Request parameters:
        - tag_id (string): Tag ID.

    Response status codes:
        - 200 (Success)
        - 401 (Unauthorized)
        - 403 (Forbidden)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.

    :param tag_id: Tag ID.
    :return: Response data dictionary.
    """
    # JWT payload data
    uid = get_jwt()["user_id"]

    # Get tag
    tag = Tag.get_by_id(tag_id)

    # Check if the tag exists and the permissions (the request user must be the
    # same as the tag's notebook user).
    if not tag or uid != tag.notebook.user_id:
        return get_response_data(
            MV_USER_UNAUTHORIZED, MT_ERROR_UNAUTHORIZED_USER), 403

    # Delete tag
    tag.delete()

    return get_response_data(MV_TAG_DELETED, MT_OK), 200
