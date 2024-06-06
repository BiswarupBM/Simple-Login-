import click

from simplelogincmd.cli import util
from simplelogincmd.database.models import Alias


def _create(id, email):
    cfg = util.init_cfg()
    sl = util.init_sl(cfg)
    db = util.init_db(cfg)
    id = util.resolve_id(db, Alias, id)
    success, obj = sl.create_contact(id, email)
    if not success:
        click.echo(obj)
        return False
    db.session.upsert(obj)
    db.session.commit()
    click.echo(obj.reverse_alias_address)
    return True
