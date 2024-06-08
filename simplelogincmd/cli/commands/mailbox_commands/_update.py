import click

from simplelogincmd.cli.util import init, input
from simplelogincmd.database.models import Mailbox


def _update(id, email, default, cancel_email_change):
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    id = input.resolve_id(db, Mailbox, id)
    success, msg = sl.update_mailbox(id, email, default, cancel_email_change)
    if not success:
        click.echo(msg)
        return False
    return True
