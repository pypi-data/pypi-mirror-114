"""Note views module."""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt

from notelist.models.notebooks import Notebook
from notelist.models.tags import Tag
from notelist.models.notes import Note
from notelist.schemas.notes import NoteSchema
from notelist.tools import get_current_ts
from notelist.responses import (
    ResponseData, MV_USER_UNAUTHORIZED, MV_VALIDATION_ERROR, MT_OK,
    MT_ERROR_UNAUTHORIZED_USER, MT_ERROR_VALIDATION, get_response_data)


# Message values
MV_NOTE_RETRIEVED_1 = "1 note retrieved"
MV_NOTE_RETRIEVED_N = "{} notes retrieved"
MV_NOTE_RETRIEVED = "Note retrieved"
MV_NOTE_CREATED = "Note created"
MV_NOTE_UPDATED = "Note updated"
MV_NOTE_DELETED = "Note deleted"

# Schemas
note_list_schema = NoteSchema(
    many=True, only=(
        "id", "active", "title", "created_ts", "last_modified_ts", "tags"))

note_schema = NoteSchema()

# Blueprint object
bp = Blueprint("notes", __name__)


@bp.route("/notes/<notebook_id>", methods=["POST"])
@jwt_required()
def get_notes(notebook_id: str) -> ResponseData:
    """Get all the notes of a notebook that match a filter.

    The user can call this operation only for their own notebooks. This
    operation requires the following header with an access token:
        "Authorization: Bearer access_token"

    Request parameters:
        - notebook_id (string): Notebook ID.

    Request data (JSON string):
        - active (boolean, optional): If `true`, only active notes are
            returned. If `false`, only archived (not active) notes are
            returned. If this item is not present in the request data, then no
            filter by state is applied and all notes are returned regardless
            their state.

        - tags (list, optional): List of strings containing the tag names to
            filter the notes by. If this item is present in the request data,
            only notes than have any of these tags are returned in the result.
            If this item is not present in the request data, then no filter by
            tags is applied and all notes are returned regardless their tags.

        - no_tags (boolean, optional): This item applies only if the "tags"
            item is present in the request data too. If `true`, notes with no
            tags are returned as well. If `false` or if this item is not
            present in the request data, notes with no tags are not returned.

        - last_mod (boolean, optional): If `true`, returned notes are sorted by
            their Last Modified timestamp. If `false` or if this item is not
            present in the request data, the notes are sorted by their Created
            timestamp.

        - asc (boolean, optional): If `true` or if this item is not present in
            the request data, the order of the returned notes is ascending. If
            `false`, the order is descending.

    Response status codes:
        - 200 (Success)
        - 400 (Bad Request)
        - 401 (Unauthorized)
        - 403 (Forbidden)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.
        - result (list): Notes data.

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

    # Request data
    fields = ["active", "tags", "no_tags", "last_mod", "asc"]
    data = request.get_json() or {}

    # Check if the request data contains any invalid field
    inv_fields = ", ".join([
        i for i in data if i not in fields])

    if inv_fields:
        return get_response_data(
            MV_VALIDATION_ERROR.format(inv_fields), MT_ERROR_VALIDATION
        ), 400

    # State filter (include active notes or not active notes)
    f = fields[0]

    if f in data:
        active = data[f]

        if type(active) != bool:
            return get_response_data(
                MV_VALIDATION_ERROR.format(f), MT_ERROR_VALIDATION), 400
    else:
        active = None

    # Tag filter (include notes that has any of these tags)
    f = fields[1]

    if f in data:
        tags = data[f]

        if (
            type(tags) != list or
            any(map(lambda t: type(t) != str or not t.strip(), tags))
        ):
            return get_response_data(
                MV_VALIDATION_ERROR.format(f), MT_ERROR_VALIDATION), 400

        tags = [t.strip() for t in tags]
    else:
        tags = None

    # Notes with No Tags filter (include notes with no tags). This filter
    # is only applicable if a tag filter has been provided, i.e. "tags" is
    # not None).
    f = fields[2]

    if f in data:
        no_tags = data[f]

        if tags is None or type(no_tags) != bool:
            return get_response_data(
                MV_VALIDATION_ERROR.format(f), MT_ERROR_VALIDATION), 400
    else:
        no_tags = None

    # Order by Last Modified timestamp
    f = fields[3]

    if f in data:
        last_mod = data[f]

        if last_mod is None or type(last_mod) != bool:
            return get_response_data(
                MV_VALIDATION_ERROR.format(f), MT_ERROR_VALIDATION), 400
    else:
        last_mod = False

    # Ascending order
    f = fields[4]

    if f in data:
        asc = data[f]

        if asc is None or type(asc) != bool:
            return get_response_data(
                MV_VALIDATION_ERROR.format(f), MT_ERROR_VALIDATION), 400
    else:
        asc = True

    notes = Note.get_by_filter(
        notebook_id, active, tags, no_tags, last_mod, asc)

    c = len(notes)
    mv = MV_NOTE_RETRIEVED_1 if c == 1 else MV_NOTE_RETRIEVED_N.format(c)

    return get_response_data(mv, MT_OK, note_list_schema.dump(notes)), 200


def _select_tag(notebook_id: str, name: str) -> Tag:
    """Return a new tag object giving the tag's name if the tag doesn't exist
    in a given notebook or the existing tag object otherwise.

    :param notebook_id: Notebook ID.
    :param name: Tag name.
    :return: Tag object.
    """
    tag = Tag.get_by_name(notebook_id, name)
    return tag if tag else Tag(notebook_id=notebook_id, name=name)


@bp.route("/note/<note_id>", methods=["GET"])
@jwt_required()
def get_note(note_id: str) -> ResponseData:
    """Get an existing note's data.

    The user can call this operation only for their own notebooks' notes.
    This operation requires the following header with an access token:
        "Authorization: Bearer access_token"

    Request parameters:
        - note_id (string): Note ID.

    Response status codes:
        - 200 (Success)
        - 401 (Unauthorized)
        - 403 (Forbidden)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.
        - result (object): Note data.

    :param note_id: Note ID.
    :return: Response data dictionary.
    """
    # JWT payload data
    uid = get_jwt()["user_id"]

    # Get the note
    note = Note.get(note_id)

    # Check if the note exists and the permissions
    if not note or uid != note.notebook.user_id:
        return get_response_data(
            MV_USER_UNAUTHORIZED, MT_ERROR_UNAUTHORIZED_USER), 403

    return get_response_data(
        MV_NOTE_RETRIEVED, MT_OK, note_schema.dump(note)), 200


@bp.route("/note", methods=["POST", "PUT"])
@jwt_required()
def create_note() -> ResponseData:
    """Create a new note.

    The user can call this operation only for their own notebooks. This
    operation requires the following header with an access token:
        "Authorization: Bearer access_token"

    Request data (JSON string):
        - notebook_id (string): Notebook ID.
        - active (string, optional): Whether this note is active (default) or
            not.
        - title (string, optional): Note title.
        - body (string, optional): Note body.
        - tags (list, optional): List of the names of the tags of the note.

    Response status codes:
        - 201 (Success)
        - 400 (Bad Request)
        - 401 (Unauthorized)
        - 403 (Forbidden)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.
        - result (object): Note ID.

    :return: Response data dictionary.
    """
    # JWT payload data
    uid = get_jwt()["user_id"]

    # Request data
    data = request.get_json() or {}

    # We validate the request data. If any of the Note model required
    # fields is missing, a "marshmallow.ValidationError" exception is
    # raised.
    note = note_schema.load(data)

    if note.title:
        note.title = note.title.strip()

    # Check if the note's notebook user is the same as the request user
    notebook = Notebook.get_by_id(note.notebook_id)

    if not notebook or uid != notebook.user_id:
        return get_response_data(
            MV_USER_UNAUTHORIZED, MT_ERROR_UNAUTHORIZED_USER), 403

    # For each request data tag, check if the tag already exists in the
    # notebook and if so, replace the request data tag by the existing tag.
    # This way, the request tags that already exist won't be created again,
    # as they will have their ID value defined (not None).
    note.tags = list(map(
        lambda t: _select_tag(note.notebook_id, t.name), note.tags))

    # Save note
    note.save()
    result = {"id": note.id}

    return get_response_data(MV_NOTE_CREATED, MT_OK, result), 201


@bp.route("/note/<note_id>", methods=["PUT"])
@jwt_required()
def update_note(note_id: str) -> ResponseData:
    """Update an existing note.

    The user can call this operation only for their own notebooks' notes
    and the notebook ID of the note cannot be changed. This operation
    requires the following header with an access token:
        "Authorization: Bearer access_token"

    Request parameters:
        - note_id (string): Note ID.

    Request data (JSON string):
        - active (string, optional): Whether this note is active or not.
        - title (string, optional): Note title.
        - body (string, optional): Note body.
        - tags (list, optional): List of the names of the tags of the note.

    Response status codes:
        - 200 (Success)
        - 400 (Bad Request)
        - 401 (Unauthorized)
        - 403 (Forbidden)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.

    :param note_id: Note ID.
    :return: Response data dictionary.
    """
    # JWT payload data
    uid = get_jwt()["user_id"]

    # Request data
    data = request.get_json() or {}

    # Get existing note
    note = Note.get(note_id)

    # Check if the note exists and the permissions
    if not note or uid != note.notebook.user_id:
        return get_response_data(
            MV_USER_UNAUTHORIZED, MT_ERROR_UNAUTHORIZED_USER), 403

    # Make a copy of the request data
    data = data.copy()

    # Check if a new value for the "notebook_id" field is provided,
    # which is not allowed.
    if "notebook_id" in data:
        return get_response_data(
            MV_VALIDATION_ERROR.format("notebook_id"), MT_ERROR_VALIDATION
        ), 400
    else:
        data["notebook_id"] = note.notebook_id

    # Check if new values for the state, the title, the body or the
    # tags are provided.
    if "active" not in data:
        data["active"] = note.active

    if "title" not in data:
        data["title"] = note.title

    if "body" not in data:
        data["body"] = note.body

    if "tags" not in data:
        data["tags"] = [t.name for t in note.tags]

    # We validate the request data. If any provided field is invalid,
    # a "marshmallow.ValidationError" exception is raised.
    new_note = note_schema.load(data)

    if new_note.title:
        new_note.title = new_note.title.strip()

    # For each tag, check if the tag already exists in the notebook and
    # if so, replace the tag object by the existing tag object (which
    # contains its ID). This way, the tags that already exist won't be
    # created again as they will have their ID value defined (not
    # None).
    tags = list(map(
        lambda t: _select_tag(new_note.notebook_id, t.name), new_note.tags))

    # Update note object. Note: we can't run "note.tags =
    # new_note.tags", as it would duplicate the note in the database
    # (that's why "tags" is a different list object).
    note.active = new_note.active
    note.title = new_note.title
    note.body = new_note.body
    note.tags = tags

    # Save note
    note.last_modified_ts = get_current_ts()
    note.save()

    return get_response_data(MV_NOTE_UPDATED, MT_OK), 200


@bp.route("/note/<note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id: str) -> ResponseData:
    """Delete an existing note.

    The user can call this operation only for their own notebooks' notes.
    This operation requires the following header with an access token:
        "Authorization: Bearer access_token"

    Request parameters:
        - note_id (string): Note ID.

    Response status codes:
        - 200 (Success)
        - 401 (Unauthorized)
        - 403 (Forbidden)
        - 422 (Unprocessable Entity)

    Response data (JSON string):
        - message (string): Message.
        - message_type (string): Message type.

    :param note_id: Note ID.
    :return: Response data dictionary.
    """
    # JWT payload data
    uid = get_jwt()["user_id"]

    # Get note
    note = Note.get(note_id)

    # Check if the note exists and the permissions (the request user must
    # be the same as the note's notebook user).
    if not note or uid != note.notebook.user_id:
        return get_response_data(
            MV_USER_UNAUTHORIZED, MT_ERROR_UNAUTHORIZED_USER), 403

    # Delete note
    note.delete()

    return get_response_data(MV_NOTE_DELETED, MT_OK), 200
