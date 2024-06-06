import click

from simplelogincmd.cli import const, util
from simplelogincmd.database.models import Alias


@click.command(
    "toggle",
    short_help=const.HELP.ALIAS.TOGGLE.SHORT,
    help=const.HELP.ALIAS.TOGGLE.LONG,
)
@click.argument(
    "id",
)
@click.pass_obj
@util.authenticate
def toggle(obj, id: int) -> bool:
    """Enable or disable an alias"""
    sl, db = obj.sl, obj.db
    id = util.resolve_id(db, Alias, id)
    success, result = sl.toggle_alias(id)
    if not success:
        click.echo(result)
        return False
    click.echo("Enabled" if result else "Disabled")
    return True
