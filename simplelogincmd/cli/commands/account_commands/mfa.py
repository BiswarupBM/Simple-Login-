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
def mfa(mfa_token: str, mfa_key: str) -> bool:
    """Attempt to pass MFA during login"""
    from simplelogincmd.cli.commands.account_commands._mfa import _mfa

    return _mfa(mfa_token, mfa_key)
