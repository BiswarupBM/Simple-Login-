"""
CLI entrypoint
"""

from types import SimpleNamespace

import click

from simplelogincmd.cli import const
from simplelogincmd.cli.lazy_group import LazyGroup, cmd_path
from simplelogincmd.config import Config
from simplelogincmd.database import DatabaseAccessLayer
from simplelogincmd.rest import SimpleLogin


@click.group(
    cls=LazyGroup,
    cmd_path=cmd_path(__file__, "commands"),
    context_settings=const.CONTEXT_SETTINGS,
)
@click.version_option()
@click.pass_context
def cli(context):
    """
    \f
    Application entrypoint
    """
    cfg = Config()
    sl = SimpleLogin()
    db = DatabaseAccessLayer()
    cfg.ensure_directory()
    db.initialize()
    # Silently log in if an API key is saved. If no API key is found,
    # don't prompt for credentials now because user may not be invoking
    # a command that requires authentication anyway. Later prompting
    # can be done via the `util.authenticate` command decorator.
    if (api_key := cfg.get("api.api-key")) != "":
        sl.api_key = api_key
    context.obj = SimpleNamespace(
        cfg=cfg,
        sl=sl,
        db=db,
    )


if __name__ == "__main__":
    cli()
