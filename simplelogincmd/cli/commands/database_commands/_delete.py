import click

from simplelogincmd.cli.util import init


def _delete():
    cfg = init.cfg()
    db = init.db(cfg)
    if not db.destroy():
        click.echo("Failed to delete database.")
        return False
    return True
