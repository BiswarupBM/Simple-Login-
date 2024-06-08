import click

from simplelogincmd.cli.util import init, input
from simplelogincmd.database.models import (
    Alias,
    Mailbox,
)


def _update(id, note, name, mailboxes, disable_pgp, pinned):
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    id = input.resolve_id(db, Alias, id)
    mailbox_ids = {input.resolve_id(db, Mailbox, mb_id) for mb_id in mailboxes}
    if note == "_EDIT":
        note = input.edit()
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
