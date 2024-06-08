import click

from simplelogincmd.cli.util import init, input
from simplelogincmd.database.models import Alias


def _toggle(id):
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    id = input.resolve_id(db, Alias, id)
    success, result = sl.toggle_alias(id)
    if not success:
        click.echo(result)
        return False
    click.echo("Enabled" if result else "Disabled")
    return True
