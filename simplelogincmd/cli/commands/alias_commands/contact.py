import click

from simplelogincmd.cli import const
from simplelogincmd.cli.lazy_group import LazyGroup, cmd_path


@click.group(
    "contact",
    cls=LazyGroup,
    cmd_path=cmd_path(__file__, "contact_commands"),
    short_help=const.HELP.ALIAS.CONTACT.SHORT,
    help=const.HELP.ALIAS.CONTACT.LONG,
)
def contact():
    """Contact commands"""
    pass
