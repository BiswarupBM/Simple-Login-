import click

from simplelogincmd.cli import util


def _random(hostname, mode, note):
    cfg = util.init_cfg()
    sl = util.init_sl(cfg)
    db = util.init_db(cfg)
    if note == "_EDIT":
        note = util.edit()
    success, obj = sl.create_random_alias(hostname, mode, note)
    if not success:
        click.echo(obj)
        return False
    db.session.upsert(obj)
    db.session.commit()
    click.echo(obj.email)
    return True
