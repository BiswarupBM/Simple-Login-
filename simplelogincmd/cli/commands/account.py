"""
CLI commands regarding SimpleLogin's account endpoints

Subcommands:

- login
- mfa
- logout
"""

import click

from simplelogincmd.cli import const
from simplelogincmd.cli.lazy_group import LazyGroup, cmd_path


@click.group(
    "account",
    cls=LazyGroup,
    cmd_path=cmd_path(__file__, "account_commands"),
    short_help=const.HELP.ACCOUNT.SHORT,
    help=const.HELP.ACCOUNT.LONG,
)
def account():
    """Account-related commands"""
    pass
