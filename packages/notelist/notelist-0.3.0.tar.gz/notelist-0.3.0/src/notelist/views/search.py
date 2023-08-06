"""Search view module."""

from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt

from notelist.responses import (
    ResponseData, MV_VALIDATION_ERROR, MT_OK, MT_ERROR_VALIDATION,
    get_response_data)
from notelist.models.notebooks import Notebook
from notelist.schemas.notebooks import NotebookSchema
from notelist.schemas.tags import TagSchema
from notelist.schemas.notes import NoteSchema


# Message values
MV_ITEM_RETRIEVED_1 = "1 item retrieved"
MV_ITEM_RETRIEVED_N = "{} items retrieved"

# Schemas
notebook_list_schema = NotebookSchema(many=True)
tag_list_schema = TagSchema(many=True)

note_list_schema = NoteSchema(
    many=True, only=(
        "id", "notebook_id", "active", "title", "created_ts",
        "last_modified_ts", "tags"))

# Blueprint object
bp = Blueprint("search", __name__)


@bp.route("/<search>", methods=["GET"])
@jwt_required()
def search(search: str) -> ResponseData:
    """Get all the notebooks, tags and notes of the request user that match a
    a text.

    This operation requires the following header with an access token:
        "Authorization: Bearer access_token"

    Request parameters:
        - search (string): Search text.

    Response status codes:
        - 200 (Success)
        - 400 (Bad Request)
        - 401 (Unauthorized)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.
        - result (object): Data of the notebooks, tags and notes found.

    :param search: Search text.
    :return: Response data dictionary.
    """
    # JWT payload data
    uid = get_jwt()["user_id"]

    # Check search string
    search = search.strip().lower()

    if len(search) < 2:
        return get_response_data(
            MV_VALIDATION_ERROR.format("search"), MT_ERROR_VALIDATION), 400

    # Notebooks
    notebooks = Notebook.get_all(uid)
    res_notebooks = [n for n in notebooks if search in n.name.lower()]

    # Notes and tags
    res_tags = []
    res_notes = []

    for nb in notebooks:
        res_tags += [
            t for t in nb.tags if (
                search in t.name.lower() or
                (t.color and search in t.color.lower()))]

        res_notes += [
            n for n in nb.notes if (
                (n.title and search in n.title.lower()) or
                (n.body and search in n.body.lower()) or
                (any(map(lambda t: search in t.name.lower(), n.tags))))]

    result = {
        "notebooks": notebook_list_schema.dump(res_notebooks),
        "tags": tag_list_schema.dump(res_tags),
        "notes": note_list_schema.dump(res_notes)}

    c = len(res_notebooks) + len(res_notes) + len(res_tags)
    mv = MV_ITEM_RETRIEVED_1 if c == 1 else MV_ITEM_RETRIEVED_N.format(c)

    return get_response_data(mv, MT_OK, result), 200
