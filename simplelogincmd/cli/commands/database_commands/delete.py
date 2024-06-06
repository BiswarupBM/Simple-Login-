import click

from simplelogincmd.cli import const


@click.command(
    "delete",
    short_help=const.HELP.DATABASE.DELETE.SHORT,
    help=const.HELP.DATABASE.DELETE.LONG,
)
def delete() -> bool:
    """Delete the database"""
    from simplelogincmd.cli.commands.database_commands._delete import _delete

    return _delete()
