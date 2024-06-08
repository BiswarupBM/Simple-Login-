"""
CLI commands regarding SimpleLogin's mailbox endpoints

Subcommands:

- create
- delete
- list
- update
"""

import click

from simplelogincmd.cli import const
from simplelogincmd.cli.lazy_group import LazyGroup, cmd_path


@click.group(
    "mailbox",
    cls=LazyGroup,
    cmd_path=cmd_path(__file__, "mailbox_commands"),
    short_help=const.HELP.MAILBOX.SHORT,
    help=const.HELP.MAILBOX.LONG,
)
def mailbox():
    """Mailbox commands"""
    pass
