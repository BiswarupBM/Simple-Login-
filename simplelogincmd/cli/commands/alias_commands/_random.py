import click

from simplelogincmd.cli.util import init, input


def _random(hostname, mode, note):
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    if note == "_EDIT":
        note = input.edit()
    success, obj = sl.create_random_alias(hostname, mode, note)
    if not success:
        click.echo(obj)
        return False
    db.session.upsert(obj)
    db.session.commit()
    click.echo(obj.email)
    return True
