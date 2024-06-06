import click

from simplelogincmd.cli import util


def _logout():
    cfg = util.init_cfg()
    sl = util.init_sl(cfg)
    success = sl.logout()
    if (error := cfg.set("api.api-key", "")) is not None:
        click.echo(error)
        return False
    cfg.save()
    return success
