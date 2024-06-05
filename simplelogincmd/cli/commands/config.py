"""
CLI commands regarding local app configuration

Subcommands:
"""

import click

from simplelogincmd.cli import const


def _display_config_value(key, value):
    if key == "api.api-key":
        # Obscure for security.
        value = "*" * 20
    click.echo(f"{key} = {value}")


def _restore_defaults(context, param, value):
    """Restore all config to default values"""
    if not value or context.resilient_parsing:
        return
    cfg = context.obj.cfg
    cfg.restore()
    cfg.save()
    context.exit()


def _list(context, param, value) -> None:
    """List all configuration values"""
    if not value or context.resilient_parsing:
        return
    all = context.obj.cfg.all()
    for k, v in all.items():
        _display_config_value(k, v)
    context.exit()


@click.group(
    "config",
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
    callback=_list,
    help=const.HELP.CONFIG.OPTION.LIST,
)
@click.option(
    "--restore-defaults",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=_restore_defaults,
    help=const.HELP.CONFIG.OPTION.RESTORE_DEFAULTS,
)
@click.argument(
    "key",
)
@click.argument(
    "value",
    required=False,
)
@click.pass_obj
def config(obj, key, value) -> None:
    """Manage app config"""
    cfg = obj.cfg
    key = key.lower()
    try:
        current = cfg.get(key)
    except KeyError:
        click.echo(f"Unknown config option '{key}'")
        return
    if value is None:
        _display_config_value(key, current)
        return
    setting = value.lower()
    if setting in ("true", "on", "yes"):
        setting = True
    elif setting in ("false", "off", "no"):
        setting = False
    else:
        try:
            setting = int(setting)
        except ValueError:
            # It's a normal string. Restore case.
            setting = value
    if (error := cfg.set(key, setting)) is not None:
        click.echo(error)
        return
    cfg.save()
