"""
CLI commands for managing the local database

Subcommands:

    - sync
"""

import click

from simplelogincmd.cli import const
from simplelogincmd.cli.lazy_group import LazyGroup, cmd_path


@click.group(
    "database",
    cls=LazyGroup,
    cmd_path=cmd_path(__file__, "database_commands"),
    short_help=const.HELP.DATABASE.SHORT,
    help=const.HELP.DATABASE.LONG,
)
def database():
    pass
