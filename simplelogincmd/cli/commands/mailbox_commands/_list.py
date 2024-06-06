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


def _list(include, exclude):
    fields = util.get_display_fields_from_options(
        const.MAILBOX_FIELD_ORDER, include, exclude
    )
    if len(fields) == 0:
        return
    cfg = util.init_cfg()
    sl = util.init_sl(cfg)
    mailboxes = sl.get_mailboxes()
    if len(mailboxes) == 0:
        return
    mailboxes.sort(key=_mailbox_sort_key)
    db = util.init_db(cfg)
    for mailbox in mailboxes:
        db.session.upsert(mailbox)
    db.session.commit()
    util.display_model_list(mailboxes, fields, pager_threshold=0)
