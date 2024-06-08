import click

from simplelogincmd.cli import const


@click.command(
    "toggle",
    short_help=const.HELP.ALIAS.TOGGLE.SHORT,
    help=const.HELP.ALIAS.TOGGLE.LONG,
)
@click.argument(
    "id",
)
def toggle(id: str) -> bool:
    """Enable or disable an alias"""
    from simplelogincmd.cli.commands.alias_commands._toggle import _toggle

    return _toggle(id)
