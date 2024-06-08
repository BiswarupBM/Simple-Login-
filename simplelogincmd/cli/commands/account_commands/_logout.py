import click

from simplelogincmd.cli.util import init


def _logout():
    cfg = init.cfg()
    sl = init.sl(cfg)
    success = sl.logout()
    if (error := cfg.set("api.api-key", "")) is not None:
        click.echo(error)
        return False
    cfg.save()
    return success
