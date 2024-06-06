import click

from simplelogincmd.cli import const, util
from simplelogincmd.database.models import Alias


@click.command(
    "delete",
    short_help=const.HELP.ALIAS.DELETE.SHORT,
    help=const.HELP.ALIAS.DELETE.LONG,
)
@click.argument(
    "id",
)
@click.option(
    "-y",
    "--yes",
    "bypass_confirmation",
    is_flag=True,
    flag_value=True,
    default=False,
    help=const.HELP.ALIAS.DELETE.OPTION.YES,
)
@click.pass_obj
@util.authenticate
def delete(obj, id: int, bypass_confirmation: bool) -> bool:
    """Delete an alias"""
    sl, db = obj.sl, obj.db
    id = util.resolve_id(db, Alias, id)
    if not bypass_confirmation:
        success, obj = sl.get_alias(id)
        if not success:
            # Clarify the somewhat vague error message for invalid ID
            msg = f"Unknown ID {id}" if "Unknown" in obj else obj
            click.echo(msg)
            return False
        click.confirm(f"Delete {obj.email}?", abort=True)
    success, msg = sl.delete_alias(id)
    if not success:
        # Clarify the somewhat vague error message
        msg = f"Unknown ID {id}" if msg == "Forbidden" else msg
        click.echo(msg)
        return False
    return True
