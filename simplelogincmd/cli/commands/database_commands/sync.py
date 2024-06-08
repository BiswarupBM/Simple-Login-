import click

from simplelogincmd.cli import const


@click.command(
    "sync",
    short_help=const.HELP.DATABASE.SYNC.SHORT,
    help=const.HELP.DATABASE.SYNC.LONG,
    epilog=const.HELP.DATABASE.SYNC.EPILOG,
)
def sync() -> bool:
    """Populate the local db with SL's data"""
    from simplelogincmd.cli.commands.database_commands._sync import _sync

    return _sync()
