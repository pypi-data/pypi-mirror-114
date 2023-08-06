"""Module with the tag schemas."""

from notelist.db import ma
from notelist.models.tags import Tag


class TagSchema(ma.SQLAlchemyAutoSchema):
    """Tag schema."""

    class Meta:
        """Tag schema metadata."""

        model = Tag
        include_fk = True
        dump_only = ["id", "created_ts", "last_modified_ts"]
        ordered = True
        load_instance = True
