"""
CLI commands regarding SimpleLogin's mailbox endpoints

Subcommands:

- create
- delete
- list
- update
"""

import click

from simplelogincmd.cli import const, util
from simplelogincmd.database.models import Mailbox


def _mailbox_sort_key(mailbox: Mailbox) -> tuple[int, str]:
    """
    Provide a sorting key for mailbox lists

    Sorts using the key will sort first by `nb_alias` descending, and then
    by `email` ascending.

    :param mailbox: The Mailbox to be sorted
    :type Mailbox: :class:`~simplelogincmd.database.models.Mailbox`

    :rtype: tuple[int, str]
    """
    return (mailbox.nb_alias * -1, mailbox.email)


@click.group(
    "mailbox", short_help=const.HELP.MAILBOX.SHORT, help=const.HELP.MAILBOX.LONG
)
def mailbox():
    """Mailbox commands"""
    pass


@mailbox.command(
    "create",
    short_help=const.HELP.MAILBOX.CREATE.SHORT,
    help=const.HELP.MAILBOX.CREATE.LONG,
    epilog=const.HELP.MAILBOX.CREATE.EPILOG,
)
@click.option(
    "-e",
    "--email",
    prompt=True,
    help=const.HELP.MAILBOX.CREATE.OPTION.EMAIL,
)
@click.pass_obj
@util.authenticate
def create(obj, email: str) -> bool:
    """Create a new mailbox"""
    sl = obj.sl
    success, msg = sl.create_mailbox(email)
    if not success:
        click.echo(msg)
        return False
    click.echo(f"A verification email has been sent to {email}.")
    return True


@mailbox.command(
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


@mailbox.command(
    "list",
    short_help=const.HELP.MAILBOX.LIST.SHORT,
    help=const.HELP.MAILBOX.LIST.LONG,
    epilog=const.HELP.MAILBOX.LIST.EPILOG,
)
@click.option(
    "-i",
    "--include",
    help=const.HELP.MAILBOX.LIST.OPTION.INCLUDE,
)
@click.option(
    "-e",
    "--exclude",
    help=const.HELP.MAILBOX.LIST.OPTION.EXCLUDE,
)
@click.pass_obj
@util.authenticate
def list(obj, include: str, exclude: str) -> None:
    """Display mailboxes in a tabular format"""
    sl, db = obj.sl, obj.db
    fields = util.get_display_fields_from_options(
        const.MAILBOX_FIELD_ORDER, include, exclude
    )
    if len(fields) == 0:
        return
    mailboxes = sl.get_mailboxes()
    if len(mailboxes) == 0:
        return
    mailboxes.sort(key=_mailbox_sort_key)
    for mailbox in mailboxes:
        db.session.upsert(mailbox)
    db.session.commit()
    util.display_model_list(mailboxes, fields, pager_threshold=0)


@mailbox.command(
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
