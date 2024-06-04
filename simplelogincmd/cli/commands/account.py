"""
CLI commands regarding SimpleLogin's account endpoints

Subcommands:

- login
- mfa
- logout
"""

import click

from simplelogincmd.cli import const, util


@click.group(
    "account",
    short_help=const.HELP.ACCOUNT.SHORT,
    help=const.HELP.ACCOUNT.LONG,
)
def account():
    """Account-related commands"""
    pass


@account.command(
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


@account.command(
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


@account.command(
    "logout",
    short_help=const.HELP.ACCOUNT.LOGOUT.SHORT,
    help=const.HELP.ACCOUNT.LOGOUT.LONG,
)
@click.pass_obj
@util.authenticate
def logout(obj) -> bool:
    """Log out of SimpleLogin"""
    sl, cfg = obj.sl, obj.cfg
    success = sl.logout()
    if (error := cfg.set("api.api-key", "")) is not None:
        click.echo(error)
        return False
    cfg.save()
    return success
