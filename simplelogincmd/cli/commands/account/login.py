import click

from simplelogincmd.cli import const


@click.command(
    "login",
    short_help=const.HELP.ACCOUNT.LOGIN.SHORT,
    help=const.HELP.ACCOUNT.LOGIN.LONG,
)
@click.option(
    "-e",
    "--email",
    prompt=True,
    help=const.HELP.ACCOUNT.LOGIN.OPTION.EMAIL,
)
@click.option(
    "-p",
    "--password",
    prompt=True,
    hide_input=True,
    help=const.HELP.ACCOUNT.LOGIN.OPTION.PASSWORD,
)
@click.pass_obj
def login(obj, email: str, password: str) -> bool:
    """Attempt to log in to SimpleLogin"""
    sl, cfg = obj.sl, obj.cfg
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
    api_key = sl.api_key
    if (error := cfg.set("api.api-key", api_key)) is not None:
        click.echo(error)
        return False
    cfg.save()
    return True
