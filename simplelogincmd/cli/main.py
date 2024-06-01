"""
CLI entrypoint
"""

import click
import importlib.util
from pkgutil import iter_modules

from simplelogincmd import config
from simplelogincmd.cli import commands, const, util


@click.group(
    context_settings=const.CONTEXT_SETTINGS,
)
@click.version_option()
@util.pass_db_access
@util.pass_simplelogin
def cli(sl, db):
    """
    \f
    Application entrypoint
    """
    config.ensure_directory()
    db.initialize()
    # Silently log in if an API key is saved. If no API key is found,
    # don't prompt for credentials now because user may not be invoking
    # a command that requires authentication anyway. Later prompting
    # can be done via the `util.authenticate` command decorator.
    cfg = config.load()
    api_key = cfg["API"].get("api_key", "")
    if api_key != "":
        sl.api_key = api_key


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
