import click

from simplelogincmd.cli import util


def _delete():
    cfg = util.init_cfg()
    db = util.init_db(cfg)
    if not db.destroy():
        click.echo("Failed to delete database.")
        return False
    return True
