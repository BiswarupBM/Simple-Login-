import click

from simplelogincmd.cli.util import init, input
from simplelogincmd.database.models import Alias


def _delete(id, bypass_confirmation):
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    id = input.resolve_id(db, Alias, id)
    if not bypass_confirmation:
        success, obj = sl.get_alias(id)
        if not success:
            # Clarify the somewhat vague error message for invalid ID
            msg = f"Unknown ID {id}" if "Unknown" in obj else obj
            click.echo(msg)
            return False
        click.confirm(f"Delete {obj.email}?", abort=True)
    success, msg = sl.delete_alias(id)
    if not success:
        # Clarify the somewhat vague error message
        msg = f"Unknown ID {id}" if msg == "Forbidden" else msg
        click.echo(msg)
        return False
    return True
