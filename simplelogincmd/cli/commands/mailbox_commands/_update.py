import click

from simplelogincmd.cli import util
from simplelogincmd.database.models import Mailbox


def _update(id, email, default, cancel_email_change):
    cfg = util.init_cfg()
    sl = util.init_sl(cfg)
    db = util.init_db(cfg)
    id = util.resolve_id(db, Mailbox, id)
    success, msg = sl.update_mailbox(id, email, default, cancel_email_change)
    if not success:
        click.echo(msg)
        return False
    return True
