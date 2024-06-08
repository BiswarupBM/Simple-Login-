"""
CLI commands regarding SimpleLogin's alias endpoints

Subcommands:

- activity
- contact
    - create
    - list
- custom
- delete
- get
- list
- random
- toggle
- update
"""

import click

from simplelogincmd.cli import const
from simplelogincmd.cli.lazy_group import LazyGroup, cmd_path


@click.group(
    "alias",
    cls=LazyGroup,
    cmd_path=cmd_path(__file__, "alias_commands"),
    short_help=const.HELP.ALIAS.SHORT,
    help=const.HELP.ALIAS.LONG,
)
def alias():
    """Alias commands"""
    pass
