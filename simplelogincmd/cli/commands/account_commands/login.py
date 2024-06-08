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
def login(email: str, password: str) -> bool:
    """Attempt to log in to SimpleLogin"""
    from simplelogincmd.cli.commands.account_commands._login import _login

    return _login(email, password)
