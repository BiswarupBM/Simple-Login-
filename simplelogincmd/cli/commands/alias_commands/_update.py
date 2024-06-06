import click

from simplelogincmd.cli import util
from simplelogincmd.database.models import (
    Alias,
    Mailbox,
)


def _update(id, note, name, mailboxes, disable_pgp, pinned):
    cfg = util.init_cfg()
    sl = util.init_sl(cfg)
    db = util.init_db(cfg)
    id = util.resolve_id(db, Alias, id)
    mailbox_ids = {util.resolve_id(db, Mailbox, mb_id) for mb_id in mailboxes}
    if note == "_EDIT":
        note = util.edit()
    success, msg = sl.update_alias(
        alias_id=id,
        note=note,
        name=name,
        mailbox_ids=mailbox_ids,
        disable_pgp=disable_pgp,
        pinned=pinned,
    )
    if not success:
        click.echo(msg)
        return False
    return True
