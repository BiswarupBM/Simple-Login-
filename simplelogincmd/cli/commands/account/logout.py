import click

from simplelogincmd.cli import const, util


@click.command(
    "logout",
    short_help=const.HELP.ACCOUNT.LOGOUT.SHORT,
    help=const.HELP.ACCOUNT.LOGOUT.LONG,
)
@click.pass_obj
@util.authenticate
def logout(obj) -> bool:
    """Log out of SimpleLogin"""
    sl, cfg = obj.sl, obj.cfg
    success = sl.logout()
    if (error := cfg.set("api.api-key", "")) is not None:
        click.echo(error)
        return False
    cfg.save()
    return success
