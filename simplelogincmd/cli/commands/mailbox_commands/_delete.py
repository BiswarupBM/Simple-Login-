import click

from simplelogincmd.cli.util import init, input
from simplelogincmd.database.models import Mailbox


def _delete(id, transfer_aliases_to, bypass_confirm):
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    id = input.resolve_id(db, Mailbox, id)
    if transfer_aliases_to == -1 and not bypass_confirm:
        click.confirm(
            "This will delete all of the mailbox's aliases. Are you sure?", abort=True
        )
    success, msg = sl.delete_mailbox(id, transfer_aliases_to)
    if not success:
        click.echo(msg)
        return False
    return True
