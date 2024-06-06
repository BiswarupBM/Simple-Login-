import click

from simplelogincmd.cli import const


@click.command(
    "mfa",
    hidden=True,
    short_help=const.HELP.ACCOUNT.MFA.SHORT,
    help=const.HELP.ACCOUNT.MFA.LONG,
    epilog=const.HELP.ACCOUNT.MFA.EPILOG,
)
@click.option(
    "-p",
    "--otp",
    "mfa_token",
    prompt="OTP",
    hide_input=True,
    help=const.HELP.ACCOUNT.MFA.OPTION.OTP,
)
@click.option(
    "-k",
    "--mfa-key",
    prompt="MFA key",
    hide_input=True,
    help=const.HELP.ACCOUNT.MFA.OPTION.MFA_KEY,
)
@click.pass_obj
def mfa(obj, mfa_token: str, mfa_key: str) -> bool:
    """Attempt to pass MFA during login"""
    sl, cfg = obj.sl, obj.cfg
    success, msg = sl.mfa(mfa_token, mfa_key)
    if not success:
        click.echo(msg)
        return False
    api_key = sl.api_key
    if (error := cfg.set("api.api-key", api_key)) is not None:
        click.echo(error)
        return False
    cfg.save()
    return True
