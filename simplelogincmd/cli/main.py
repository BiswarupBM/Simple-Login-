"""
CLI entrypoint
"""

import importlib.util
from pkgutil import iter_modules
from types import SimpleNamespace

import click
from trogon import tui

from simplelogincmd.cli import commands, const
from simplelogincmd.config import Config
from simplelogincmd.database import DatabaseAccessLayer
from simplelogincmd.rest import SimpleLogin


@tui(command="ui", help="Open terminal UI")
@click.group(
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


# Dynamically import and add any public Groups found in `commands` modules.
commands_path = commands.__path__
commands_prefix = f"{commands.__name__}."
for finder, name, is_pkg in iter_modules(commands_path, commands_prefix):
    spec = importlib.util.find_spec(name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for obj_name, obj in vars(module).items():
        if not obj_name.startswith("_") and isinstance(obj, click.core.Group):
            cli.add_command(obj)


if __name__ == "__main__":
    cli()
