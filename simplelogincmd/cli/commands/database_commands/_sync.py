import click

from simplelogincmd.cli.util import init


def _sync():
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    objects = []
    click.echo("Retrieving mailboxes... ", nl=False)
    mailboxes = sl.get_mailboxes()
    objects.extend(mailboxes)
    click.echo("Done")
    click.echo("Retrieving aliases... ", nl=False)
    aliases = sl.get_all_aliases()
    objects.extend(aliases)
    click.echo("Done")
    click.echo("Refreshing local database... ", nl=False)
    db.clear()
    for obj in objects:
        db.session.upsert(obj)
    db.session.commit()
    click.echo("Done")
    click.echo("")
    click.echo("Local database synced successfully.")
    return True
