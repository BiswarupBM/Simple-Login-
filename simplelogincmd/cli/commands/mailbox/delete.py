import click

from simplelogincmd.cli import const, util
from simplelogincmd.database.models import Mailbox


@click.command(
    "delete",
    short_help=const.HELP.MAILBOX.DELETE.SHORT,
    help=const.HELP.MAILBOX.DELETE.LONG,
)
@click.argument(
    "id",
)
@click.option(
    "-t",
    "--transfer-aliases-to",
    default=-1,
    show_default=True,
    help=const.HELP.MAILBOX.DELETE.OPTION.TRANSFER_ALIASES_TO,
)
@click.option(
    "-y",
    "--yes",
    "bypass_confirm",
    is_flag=True,
    flag_value=True,
    default=False,
    help=const.HELP.MAILBOX.DELETE.OPTION.YES,
)
@click.pass_obj
@util.authenticate
def delete(obj, id: int, transfer_aliases_to: int, bypass_confirm: bool):
    """Delete a mailbox"""
    sl, db = obj.sl, obj.db
    id = util.resolve_id(db, Mailbox, id)
    if transfer_aliases_to == -1 and not bypass_confirm:
        click.confirm(
            "This will delete all of the mailbox's aliases. Are you sure?", abort=True
        )
    success, msg = sl.delete_mailbox(id, transfer_aliases_to)
    if not success:
        click.echo(msg)
        return False
    return True
