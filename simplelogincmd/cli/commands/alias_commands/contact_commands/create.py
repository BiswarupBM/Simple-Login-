import click

from simplelogincmd.cli import const


@click.command(
    "create",
    short_help=const.HELP.ALIAS.CONTACT.CREATE.SHORT,
    help=const.HELP.ALIAS.CONTACT.CREATE.LONG,
)
@click.argument(
    "id",
)
@click.option(
    "-e",
    "--email",
    help=const.HELP.ALIAS.CONTACT.CREATE.OPTION.EMAIL,
)
def create(id: str, email: str) -> bool:
    """Create a new contact"""
    from simplelogincmd.cli.commands.alias_commands.contact_commands._create import (
        _create,
    )

    return _create(id, email)
