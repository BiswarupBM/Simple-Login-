"""
CLI commands regarding local app configuration

Subcommands:
"""

import click

from simplelogincmd.cli import const
from simplelogincmd.cli.lazy_group import LazyGroup, cmd_path


def list_configs(context, param, value):
    """Display all config values"""
    if not value or context.resilient_parsing:
        return
    from simplelogincmd.cli.commands._config import _list_configs

    return _list_configs(context, param, value)


def restore_defaults(context, param, value):
    """Restore all configs to default values"""
    if not value or context.resilient_parsing:
        return
    from simplelogincmd.cli.commands._config import _restore_defaults

    return _restore_defaults(context, param, value)


@click.group(
    "config",
    cls=LazyGroup,
    cmd_path=cmd_path(__file__, "config_commands"),
    invoke_without_command=True,
    short_help=const.HELP.CONFIG.SHORT,
    help=const.HELP.CONFIG.LONG,
    epilog=const.HELP.CONFIG.EPILOG,
)
@click.option(
    "-l",
    "--list",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=list_configs,
    help=const.HELP.CONFIG.OPTION.LIST,
)
@click.option(
    "--restore-defaults",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=restore_defaults,
    help=const.HELP.CONFIG.OPTION.RESTORE_DEFAULTS,
)
@click.argument(
    "key",
)
@click.argument(
    "value",
    required=False,
)
def config(key: str, value: str | None) -> None:
    from simplelogincmd.cli.commands._config import _config

    return _config(key, value)
