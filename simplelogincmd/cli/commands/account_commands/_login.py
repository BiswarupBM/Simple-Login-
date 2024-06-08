import click

from simplelogincmd.cli.util import init
from simplelogincmd.rest import SimpleLogin


def _login(email, password):
    context = click.get_current_context()
    sl = context.ensure_object(SimpleLogin)
    success, msg = sl.login(email, password)
    if not success:
        click.echo(msg)
        return False
    if sl.is_mfa_waiting():
        from simplelogincmd.cli.commands.account.mfa import mfa

        mfa_key = sl.mfa_key
        mfa_token = click.prompt("OTP", type=int, hide_input=True)
        context = click.get_current_context()
        return context.invoke(mfa, mfa_token=mfa_token, mfa_key=mfa_key)

    cfg = init.cfg()
    api_key = sl.api_key
    if (error := cfg.set("api.api-key", api_key)) is not None:
        click.echo(error)
        return False
    cfg.save()
    return True
