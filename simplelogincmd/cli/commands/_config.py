import click

from simplelogincmd.cli.util import init


def _display_config_value(key, value):
    if key == "api.api-key":
        # Obscure for security.
        value = "*" * 20
    click.echo(f"{key} = {value}")


def _restore_defaults(context, param, value):
    cfg = init.cfg()
    cfg.restore()
    cfg.save()
    context.exit()


def _list_configs(context, param, value) -> None:
    cfg = init.cfg()
    all = cfg.all()
    for k, v in all.items():
        _display_config_value(k, v)
    context.exit()


def _config(key, value):
    cfg = init.cfg()
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
