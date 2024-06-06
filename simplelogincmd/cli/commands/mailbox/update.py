import click

from simplelogincmd.cli import const, util
from simplelogincmd.database.models import Mailbox


@click.command(
    "update",
    short_help=const.HELP.MAILBOX.UPDATE.SHORT,
    help=const.HELP.MAILBOX.UPDATE.LONG,
)
@click.argument(
    "id",
)
@click.option(
    "-e",
    "--email",
    help=const.HELP.MAILBOX.UPDATE.OPTION.EMAIL,
)
@click.option(
    "-d/-D",
    "--default/--no-default",
    default=None,
    help=const.HELP.MAILBOX.UPDATE.OPTION.DEFAULT,
)
@click.option(
    "-c/-C",
    "--cancel-email-change/--no-cancel-email-change",
    default=None,
    help=const.HELP.MAILBOX.UPDATE.OPTION.CANCEL_EMAIL_CHANGE,
)
@click.pass_obj
@util.authenticate
def update(
    obj,
    id: int,
    email: str | None,
    default: bool | None,
    cancel_email_change: bool | None,
) -> bool:
    """Modify a mailbox's attributes"""
    sl, db = obj.sl, obj.db
    id = util.resolve_id(db, Mailbox, id)
    success, msg = sl.update_mailbox(id, email, default, cancel_email_change)
    if not success:
        click.echo(msg)
        return False
    return True
