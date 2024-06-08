import click

from simplelogincmd.cli import const


@click.command(
    "list",
    short_help=const.HELP.ALIAS.CONTACT.LIST.SHORT,
    help=const.HELP.ALIAS.CONTACT.LIST.LONG,
    epilog=const.HELP.ALIAS.CONTACT.LIST.EPILOG,
)
@click.argument(
    "id",
)
@click.option(
    "-i",
    "--include",
    help=const.HELP.ALIAS.CONTACT.LIST.OPTION.INCLUDE,
)
@click.option(
    "-e",
    "--exclude",
    help=const.HELP.ALIAS.CONTACT.LIST.OPTION.EXCLUDE,
)
def list(id: str, include: str | None, exclude: str | None) -> None:
    """List contacts in a tabular format"""
    from simplelogincmd.cli.commands.alias_commands.contact_commands._list import _list

    return _list(id, include, exclude)
