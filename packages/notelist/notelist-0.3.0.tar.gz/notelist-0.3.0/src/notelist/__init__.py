"""Notelist package.

Notelist is a tag based note taking REST API that can be used to manage
notebooks, tags and notes. Notelist is based on the Flask framework.

Project information:
- Version: 0.3.0
- Author: Jose A. Jimenez (jajimenezcarm@gmail.com)
- License: MIT License
- Repository: https://github.com/jajimenez/notelist
"""

from os import environ
from datetime import timedelta

from flask import Flask, render_template, abort
from flask.wrappers import Response
from flask_migrate import Migrate

from notelist.auth import jwt
from notelist.db import db, ma
from notelist.views import register_blueprints
from notelist.errors import register_error_handlers
from notelist.cli import path_cli, user_cli


__version__ = "0.3.0"

# Environment variables
SECRET_KEY = "NOTELIST_SECRET_KEY"
DB_URI = "NOTELIST_DB_URI"
AC_ALLOW_ORIGIN = "NOTELIST_AC_ALLOW_ORIGIN"
ROOT_DOC = "NOTELIST_ROOT_DOC"

# Application object
app = Flask(__name__)

app.config["JSON_SORT_KEYS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get(DB_URI)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

# CORS (Cross-Origin Resource Sharing):
#
# The value of the "Access-Control-Allow-Origin" response header determines
# which host is allow to make requests to the API from a front-end application
# (from JavaScript code).
#
# If this API is used through a front-end application and the API and the
# front-end application are in the same host, then it's not needed to set this
# header. If the API and the front-end are in different hosts, then the header
# must be set to the host of the front-end application (starting with
# "https://").
#
# The value "*" for the header allows a front-end from any host to make
# requests to the API but this is not recommended and is not supported by all
# browsers.
#
# In this API, we set the value of the header through the
# "NOTELIST_AC_ALLOW_ORIGIN" environment variable.
ac_allow_origin = environ.get(AC_ALLOW_ORIGIN)
ac_allow_headers = ["Accept", "Content-Type", "Authorization"]

# The Secret Key is used for storing session information specific to a user
# from one request to the next. This is implemented on top of cookies which are
# signed cryptographically with the secret key. This means that the user could
# look at the contents of the cookies but not modify it unless they knew the
# secret key. A secret key should be as random as possible.
app.secret_key = environ.get(SECRET_KEY)

# Database
db.init_app(app)
ma.init_app(app)
mig = Migrate(app, db)

# User authentication (JWT)
jwt.init_app(app)

# Blueprints (view groups)
register_blueprints(app)

# Error handlers
register_error_handlers(app)

# Flask commands
app.cli.add_command(path_cli)
app.cli.add_command(user_cli)


@app.route("/", methods=["GET"])
def index() -> str:
    """Return the API documentation page.

    The documentation page is returned only if the "NOTELIST_ROOT_DOC"
    environment variable is set and its value is "yes". Otherwise, a 404 error
    response is returned.
    """
    if environ.get(ROOT_DOC) != "yes":
        return abort(404)

    return render_template("index.html", version=__version__)


@app.after_request
def after_request(response: Response) -> Response:
    """Modify each request response before sending it.

    This function adds the "Access-Control-Allow-Origin" and
    "Access-Control-Allow-Headers" headers to every response of the API before
    sending it. These headers are related to CORS (Cross-Origin Resource
    Sharing).

    :param response: Original response.
    :return: Final response.
    """
    # Access Control Allow Origin
    if ac_allow_origin:
        response.access_control_allow_origin = ac_allow_origin

    # Access Control Allow Headers
    response.access_control_allow_headers = ac_allow_headers

    return response
