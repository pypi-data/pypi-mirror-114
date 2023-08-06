"""Views package."""

from flask import Flask

from notelist.views.authentication import bp as auth_bp
from notelist.views.users import bp as users_bp
from notelist.views.notebooks import bp as notebooks_bp
from notelist.views.tags import bp as tags_bp
from notelist.views.notes import bp as notes_bp
from notelist.views.search import bp as search_bp
from notelist.views.about import bp as about_bp


def register_blueprints(app: Flask):
    """Register the API blueprints (view groups).

    :param app: Flask application object.
    """
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(notebooks_bp, url_prefix="/notebooks")
    app.register_blueprint(tags_bp, url_prefix="/tags")
    app.register_blueprint(notes_bp, url_prefix="/notes")
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(about_bp, url_prefix="/about")
