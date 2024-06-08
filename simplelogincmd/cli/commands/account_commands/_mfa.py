import click

from simplelogincmd.cli.util import init
from simplelogincmd.rest import SimpleLogin


def _mfa(mfa_token, mfa_key):
    context = click.get_current_context()
    sl = context.ensure_object(SimpleLogin)
    success, msg = sl.mfa(mfa_token, mfa_key)
    if not success:
        click.echo(msg)
        return False
    cfg = init.cfg()
    api_key = sl.api_key
    if (error := cfg.set("api.api-key", api_key)) is not None:
        click.echo(error)
        return False
    cfg.save()
    return True
