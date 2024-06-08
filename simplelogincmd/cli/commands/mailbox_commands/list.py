import click

from simplelogincmd.cli import const


@click.command(
    "list",
    short_help=const.HELP.MAILBOX.LIST.SHORT,
    help=const.HELP.MAILBOX.LIST.LONG,
    epilog=const.HELP.MAILBOX.LIST.EPILOG,
)
@click.option(
    "-i",
    "--include",
    help=const.HELP.MAILBOX.LIST.OPTION.INCLUDE,
)
@click.option(
    "-e",
    "--exclude",
    help=const.HELP.MAILBOX.LIST.OPTION.EXCLUDE,
)
def list(include: str, exclude: str) -> None:
    """Display mailboxes in a tabular format"""
    from simplelogincmd.cli.commands.mailbox_commands._list import _list

    return _list(include, exclude)
