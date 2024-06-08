import click

from simplelogincmd.cli import const


@click.command(
    "logout",
    short_help=const.HELP.ACCOUNT.LOGOUT.SHORT,
    help=const.HELP.ACCOUNT.LOGOUT.LONG,
)
def logout() -> bool:
    """Log out of SimpleLogin"""
    from simplelogincmd.cli.commands.account_commands._logout import _logout

    return _logout()
