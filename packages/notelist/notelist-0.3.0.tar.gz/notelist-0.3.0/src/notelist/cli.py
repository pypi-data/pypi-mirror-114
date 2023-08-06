"""CLI (Command Line Interface) module."""

from os.path import dirname, join
from typing import Optional

import click
from flask.cli import AppGroup

from notelist import tools
from notelist.models import User


# CLI objects
path_cli = AppGroup("path")
user_cli = AppGroup("user")


@path_cli.command("migrations")
def print_migrations_path():
    """Print the migrations directory full path."""
    print(join(dirname(__file__), "migrations"))


@user_cli.command("create")
@click.argument("username", type=str)
@click.argument("password", type=str)
@click.argument("admin", type=bool)
@click.argument("enabled", type=bool)
@click.argument("name", type=str, required=False)
@click.argument("email", type=str, required=False)
def create_user(
    username: str, password: str, admin: bool, enabled: bool,
    name: Optional[str] = None, email: Optional[str] = None
):
    """Create a user in the database.

    :param username: Username.
    :param password: Password.
    :param admin: Whether the user is an administrator or not.
    :param enabled: Whether the user is enabled or not.
    :param name: Name (optional).
    :param email: E-mail address (optional).
    """
    # Encrypt password
    password = tools.get_hash(password)

    user = User(
        username=username, password=password, admin=admin, enabled=enabled,
        name=name, email=email)

    user.save()
    print("User created")
