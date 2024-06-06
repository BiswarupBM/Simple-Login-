import click

from simplelogincmd.cli import const


@click.command(
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
