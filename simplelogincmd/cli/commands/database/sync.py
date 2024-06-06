import click

from simplelogincmd.cli import const, util


@click.command(
    "sync",
    short_help=const.HELP.DATABASE.SYNC.SHORT,
    help=const.HELP.DATABASE.SYNC.LONG,
    epilog=const.HELP.DATABASE.SYNC.EPILOG,
)
@click.pass_obj
@util.authenticate
def sync(obj):
    """Populate the local db with SL's data"""
    sl, db = obj.sl, obj.db
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
