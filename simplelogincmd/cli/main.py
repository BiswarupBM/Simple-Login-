"""
CLI entrypoint
"""

import click

from simplelogincmd.cli import const
from simplelogincmd.cli.lazy_group import LazyGroup, cmd_path


@click.group(
    cls=LazyGroup,
    cmd_path=cmd_path(__file__, "commands"),
    context_settings=const.CONTEXT_SETTINGS,
)
@click.version_option()
def cli():
    """
    \f
    Application entrypoint
    """
    pass


if __name__ == "__main__":
    cli()
