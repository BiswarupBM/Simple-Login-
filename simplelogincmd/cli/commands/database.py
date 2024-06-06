"""
CLI commands for managing the local database

Subcommands:

    - sync
"""

import click

from simplelogincmd.cli import const, util


@click.group(
    "database",
    short_help=const.HELP.DATABASE.SHORT,
    help=const.HELP.DATABASE.LONG,
)
def group_db():
    pass


@group_db.command(
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


@group_db.command(
    "delete",
    short_help=const.HELP.DATABASE.DELETE.SHORT,
    help=const.HELP.DATABASE.DELETE.LONG,
)
@click.pass_obj
def delete(obj) -> bool:
    """Delete the database"""
    db = obj.db
    if not db.destroy():
        click.echo("Failed to delete database.")
        return False
    return True
