"""Notebook views module."""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt

from notelist.models.notebooks import Notebook
from notelist.schemas.notebooks import NotebookSchema
from notelist.tools import get_current_ts
from notelist.responses import (
    ResponseData, MV_USER_UNAUTHORIZED, MV_VALIDATION_ERROR, MT_OK,
    MT_ERROR_UNAUTHORIZED_USER, MT_ERROR_VALIDATION, MT_ERROR_ITEM_EXISTS,
    get_response_data)


# Message values
MV_NOTEBOOK_RETRIEVED_1 = "1 notebook retrieved"
MV_NOTEBOOK_RETRIEVED_N = "{} notebooks retrieved"
MV_NOTEBOOK_RETRIEVED = "Notebook retrieved"
MV_NOTEBOOK_CREATED = "Notebook created"
MV_NOTEBOOK_EXISTS = "The user already has a notebook with the same name"
MV_NOTEBOOK_UPDATED = "Notebook updated"
MV_NOTEBOOK_DELETED = "Notebook deleted"

# Schemas
notebook_list_schema = NotebookSchema(many=True)
notebook_schema = NotebookSchema()

# Blueprint object
bp = Blueprint("notebooks", __name__)


@bp.route("/notebooks", methods=["GET"])
@jwt_required()
def get_notebooks() -> ResponseData:
    """Get all the notebooks of the request user.

    This operation requires the following header with an access token:
        "Authorization: Bearer access_token"

    Response status codes:
        - 200 (Success)
        - 401 (Unauthorized)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.
        - result (list): Notebooks data.

    :return: Response data dictionary.
    """
    # JWT payload data
    uid = get_jwt()["user_id"]

    # Get all the notebooks of the request user
    notebooks = Notebook.get_all(uid)

    c = len(notebooks)
    mv = (
        MV_NOTEBOOK_RETRIEVED_1 if c == 1 else
        MV_NOTEBOOK_RETRIEVED_N.format(c))

    return get_response_data(
        mv, MT_OK, notebook_list_schema.dump(notebooks)), 200


@bp.route("/notebook/<notebook_id>", methods=["GET"])
@jwt_required()
def get_notebook(notebook_id: str) -> ResponseData:
    """Get an existing notebook's data.

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
        - result (object): Notebook data.

    :param notebook_id: Notebook ID.
    :return: Response data dictionary.
    """
    # JWT payload data
    uid = get_jwt()["user_id"]

    # Get the notebook
    notebook = Notebook.get_by_id(notebook_id)

    # Check if the notebook exists and the permissions
    if not notebook or uid != notebook.user_id:
        return get_response_data(
            MV_USER_UNAUTHORIZED, MT_ERROR_UNAUTHORIZED_USER), 403

    return get_response_data(
        MV_NOTEBOOK_RETRIEVED, MT_OK, notebook_schema.dump(notebook)), 200


@bp.route("/notebook", methods=["POST", "PUT"])
@jwt_required()
def create_notebook() -> ResponseData:
    """Create a new notebook.

    This operation requires the following header with an access token:
        "Authorization: Bearer access_token"

    Request data (JSON string):
        - name (string): Notebook name.

    Response status codes:
        - 201 (Success)
        - 400 (Bad Request)
        - 401 (Unauthorized)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.
        - result (object): Notebook ID.

    :return: Response data dictionary.
    """
    # JWT payload data
    uid = get_jwt()["user_id"]

    # Request data
    data = request.get_json() or {}

    # We validate the request data. If any of the Notebook model required
    # fields is missing, a "marshmallow.ValidationError" exception is
    # raised.
    notebook = notebook_schema.load(data)
    notebook.name = notebook.name.strip()

    if not notebook.name:
        return get_response_data(
            MV_VALIDATION_ERROR.format("name"), MT_ERROR_VALIDATION), 400

    # Check if the request user already has the notebook (based on the notebook
    # name).
    if Notebook.get_by_name(uid, notebook.name):
        return get_response_data(MV_NOTEBOOK_EXISTS, MT_ERROR_ITEM_EXISTS), 400

    # Save notebook
    notebook.user_id = uid
    notebook.save()
    result = {"id": notebook.id}

    return get_response_data(MV_NOTEBOOK_CREATED, MT_OK, result), 201


@bp.route("/notebook/<notebook_id>", methods=["PUT"])
@jwt_required()
def update_notebook(notebook_id: str) -> ResponseData:
    """Update an existing notebook.

    The user can call this operation only for their own notebooks. This
    operation requires the following header with an access token:
        "Authorization: Bearer access_token"

    Request parameters:
        - notebook_id (string): Notebook ID.

    Request data (JSON string):
        - name (string): Notebook name.

    Response status codes:
        - 200 (Success)
        - 400 (Bad Request)
        - 401 (Unauthorized)
        - 403 (Forbidden)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.

    :param notebook_id: Notebook ID.
    :return: Response data dictionary.
    """
    # JWT payload data
    uid = get_jwt()["user_id"]

    # Request data
    data = request.get_json() or {}

    # Get existing notebook
    notebook = Notebook.get_by_id(notebook_id)

    # Check if the notebook exists (based on its name) for the request user and
    # check the permissions (the request user must be the same as the notebook
    # user).
    if not notebook or uid != notebook.user_id:
        return get_response_data(
            MV_USER_UNAUTHORIZED, MT_ERROR_UNAUTHORIZED_USER), 403

    # Make a copy of the request data
    data = data.copy()

    # Check if a new name is provided and if the request user has already a
    # notebook with this name.
    if "name" in data:
        if type(data["name"]) != str or not data["name"].strip():
            return get_response_data(
                MV_VALIDATION_ERROR.format("name"), MT_ERROR_VALIDATION
            ), 400

        data["name"] = data["name"].strip()

        if (
            data["name"] != notebook.name and
            Notebook.get_by_name(uid, data["name"])
        ):
            return get_response_data(
                MV_NOTEBOOK_EXISTS, MT_ERROR_ITEM_EXISTS), 400
    else:
        data["name"] = notebook.name

    # We validate the request data. If any provided field is invalid, a
    # "marshmallow.ValidationError" exception is raised.
    new_notebook = notebook_schema.load(data)

    # Update notebook object
    notebook.name = new_notebook.name

    # Save notebook
    notebook.last_modified_ts = get_current_ts()
    notebook.save()

    return get_response_data(MV_NOTEBOOK_UPDATED, MT_OK), 200


@bp.route("/notebook/<notebook_id>", methods=["DELETE"])
@jwt_required()
def delete_notebook(notebook_id: str) -> ResponseData:
    """Delete an existing notebook.

    The user can call this operation only for their own notebooks. This
    operation requires the following header with a fresh access token:
        "Authorization: Bearer fresh_access_token"

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

    :param notebook_id: Notebook ID.
    :return: Response data dictionary.
    """
    # JWT payload data
    uid = get_jwt()["user_id"]

    # Get notebook
    notebook = Notebook.get_by_id(notebook_id)

    # Check if the notebook exists and the permissions (the request user can
    # only delete their own notebooks).
    if not notebook or uid != notebook.user.id:
        return get_response_data(
            MV_USER_UNAUTHORIZED, MT_ERROR_UNAUTHORIZED_USER), 403

    # Delete notebook
    notebook.delete()

    return get_response_data(MV_NOTEBOOK_DELETED, MT_OK), 200
