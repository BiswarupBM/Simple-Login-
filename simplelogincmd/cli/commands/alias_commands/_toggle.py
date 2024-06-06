import click

from simplelogincmd.cli import util
from simplelogincmd.database.models import Alias


def _toggle(id):
    cfg = util.init_cfg()
    sl = util.init_sl(cfg)
    db = util.init_db(cfg)
    id = util.resolve_id(db, Alias, id)
    success, result = sl.toggle_alias(id)
    if not success:
        click.echo(result)
        return False
    click.echo("Enabled" if result else "Disabled")
    return True
