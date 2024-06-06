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


@click.command(
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
