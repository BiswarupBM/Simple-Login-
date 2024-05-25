"""
CLI commands regarding SimpleLogin's account endpoints

Subcommands:

- login
- mfa
- logout
"""

import click

from simplelogincmd import config
from simplelogincmd.cli import const, util


def _save_api_key(api_key: str) -> bool:
    """
    Save the new api_key to disc

    :param api_key: The api_key which SimpleLogin provides
    :type api_key: str

    :return: Whether the save is successful
    :rtype: bool
    """
    cfg = config.load()
    cfg["API"]["api_key"] = api_key
    return config.save(cfg)


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
@util.pass_simplelogin
def login(sl, email: str, password: str) -> bool:
    """Attempt to log in to SimpleLogin"""
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
    _save_api_key(api_key)
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
@util.pass_simplelogin
def mfa(sl, mfa_token: str, mfa_key: str) -> bool:
    """Attempt to pass MFA during login"""
    success, msg = sl.mfa(mfa_token, mfa_key)
    if not success:
        click.echo(msg)
        return False
    api_key = sl.api_key
    _save_api_key(api_key)
    return True


@account.command(
    "logout",
    short_help=const.HELP.ACCOUNT.LOGOUT.SHORT,
    help=const.HELP.ACCOUNT.LOGOUT.LONG,
)
@util.pass_simplelogin
@util.authenticate
def logout(sl) -> None:
    """Log out of SimpleLogin"""
    success = sl.logout()
    if success:
        click.echo("logged out")
