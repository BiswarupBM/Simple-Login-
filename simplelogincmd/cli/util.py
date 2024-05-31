"""
CLI application utilities
"""

from functools import wraps
from typing import Any, Type

import click

from simplelogincmd.cli.exceptions import NotLoggedInError
from simplelogincmd.database import DatabaseAccessLayer
from simplelogincmd.database.models import Object
from simplelogincmd.rest import SimpleLogin
from simplelogincmd.rest.exceptions import UnauthenticatedError


pass_db_access = click.make_pass_decorator(DatabaseAccessLayer, ensure=True)
pass_simplelogin = click.make_pass_decorator(SimpleLogin, ensure=True)


def authenticate(f):
    """
    Prompt the user to login if not already authenticated

    :param f: The function/method which requires the user be logged in
    :type f: Callable

    :raise NotLoggedInError: If the user fails to log in

    :return: Decorated function
    :rtype: Callable
    """

    @wraps(f)
    def wrapper(sl, *args, **kwargs):
        if not sl.is_authenticated():
            from simplelogincmd.cli.commands.account import login

            email = click.prompt("Email")
            password = click.prompt("Password", hide_input=True)
            context = click.get_current_context()
            success = context.invoke(login, email=email, password=password)
            if not success:
                # Click will handle this gracefully by itself.
                raise NotLoggedInError()
        return f(sl, *args, **kwargs)

    return wrapper


def _generate_model_list(models: list[Object], fields: list[str]):
    """
    Generate a table displaying the given fields of each item

    :param models: List of class:`simplelogincmd.rest.model.Object` to be
        included in the table
    :type models: list[Object]
    :param fields: The field names to be shown for each item
    :type fields: list[str]

    :return: A generator of each line of the table, including a heading
    :rtype: Generator
    """
    if len(models) == 0:
        return
    header = "|".join(fields)
    yield f"{header}\n"
    for model in models:
        properties = [model.get_string(field) for field in fields]
        entry = "|".join(properties)
        yield f"{entry}\n"


def display_model_list(
    models: list[Object],
    fields: list[str],
    use_pager: bool = True,
) -> None:
    """
    Print a simple table detailing each item to stdout

    :param models: Series of :class:`~simplelogincmd.database.models.Object` to
        be included in the output
    :type models: list[Object]
    :param fields: The field names to display for each item, in left-
        to-right order
    :type fields: list[str]
    :param use_pager: Whether to display the table in a pager, for easier
        viewing of long lists, defaults to True
    :type use_pager: bool, optional

    :rtype: None
    """
    table = _generate_model_list(models, fields)
    if use_pager:
        click.echo_via_pager(table)
        return
    for entry in table:
        # Entries come with newline appended, so suppress them here
        click.echo(entry, nl=False)


def edit(msg: str | None = None, *args, **kwargs) -> str | None:
    """
    Allow the user to enter a message via their editor of choice

    :param message: Default message to show in the temporary file. If
        not given, :data:`~simplelogincmd.cli.const.EDITOR_DEFAULT_MESSAGE`
        is used, defaults to None
    :type message: str, optional
    :param args: Passed directly on to :func:`click.edit`
    :param kwargs: Passed directly on to :func:`click.edit`

    :return: The message entered, with all blank and commented lines
        removed, or None if the user enters a blank message
    :rtype: str|None
    """
    msg = msg or (
        "\n\n# Provide your message above. Any line starting with "
        "\n# a `#` will be ignored. "
    )
    text = click.edit(msg, *args, **kwargs)
    if text is None:
        return text
    lines = text.splitlines()
    text = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line != "" and stripped_line[0] != "#":
            text.append(line)
    return "\n".join(text)


def get_display_fields_from_options(
    valid_fields: list[str],
    inclusions: str | None,
    exclusions: str | None,
) -> list[str]:
    """
    Make a list of valid fields based on which should be included and excluded

    Produce a list consisting of the valid items in `inclusions` (or
    those in `valid_fields` itself, if `inclusions` is empty), except
    for those found in `exclusions`. Comparisons are case-insensitive.

    :param valid_fields: All the possible valid fields
    :type valid_fields: list[str]
    :param inclusions: A comma-separated list of fields to be included.
        If empty, then assume all of `valid_fields` are to be included.
        Otherwise, include only the valid fields found in this list
    :type inclusions: str
    :param exclusions: Exclude any valid fields in this comma-separated
        list from the result
    :type exclusions: str

    :return: The valid fields as requested
    :rtype: list[str], might be empty
    """
    if inclusions is not None:
        inclusions = inclusions.lower()
        inclusions = inclusions.replace(" ", "")
        inclusions = inclusions.split(",")
        fields = [field for field in valid_fields if field in inclusions]
    else:
        fields = [field for field in valid_fields]
    if exclusions is not None:
        exclusions = exclusions.lower()
        exclusions = exclusions.replace(" ", "")
        exclusions = exclusions.split(",")
        fields = [field for field in fields if field not in exclusions]
    return fields


def prompt_choice(text: str, options: list) -> int:
    """
    Prompt the user to choose one of a list of items

    :param text: The prompt to display to the user, below the list of
        options
    :type text: str
    :param options: List of options from which the user can choose
    :type options: list

    :raise ValueError: if `options` is empty

    :return: The index of the item chosen
    :rtype: int
    """
    low, high = 1, len(options)
    if high == 0:
        raise ValueError("No options provided")
    int_range = click.IntRange(low, high)
    click.echo("")
    for index, option in enumerate(options):
        click.echo(f"{index + 1} - {option}")
    text = f"\n{text} ({low}-{high})"
    choice = click.prompt(text, type=int_range, show_choices=True)
    return choice - 1


def resolve_id(db: DatabaseAccessLayer, model_cls: Type, id: Any) -> int | Any:
    """
    Search for a single db object id given an identifier

    Call the model classes :meth:`~Object.resolve_identifier` method to
    locate db objects based on the given identifier, which can be any
    value. If multiple results match, ask the user to choose one and
    return the id of the selected object. If one result matches, return
    its id directly. If no matches were found, return the id as it was
    provided.

    :param db: The access layer instance to use for the lookup
    :type db: :class:`~simplelogincmd.database.DatabaseAccessLayer`
    :param model_cls: The type of db object for which to search
    :type model_cls: Type, subclass of
        :class:`~simplelogincmd.database.models.Object`
    :param id: The id to look up
    :type id: Any, usually int or str, as defined by the model class's
        :meth:`~simplelogincmd.database.models.Object.identifier_query`

    :return: The numeric id of the matched object, or the given id if
        none matched
    :rtype: int | type(id)
    """
    results = model_cls.resolve_identifier(db.session, id)
    count = len(results)
    if count == 0:
        return id
    if count == 1:
        return results[0].id
    choice = prompt_choice(f"Select {model_cls.__name__}", results)
    return results[choice].id
