import click

from simplelogincmd.cli import const


@click.command(
    "create",
    short_help=const.HELP.MAILBOX.CREATE.SHORT,
    help=const.HELP.MAILBOX.CREATE.LONG,
    epilog=const.HELP.MAILBOX.CREATE.EPILOG,
)
@click.option(
    "-e",
    "--email",
    prompt=True,
    help=const.HELP.MAILBOX.CREATE.OPTION.EMAIL,
)
def create(email: str) -> bool:
    """Create a new mailbox"""
    from simplelogincmd.cli.commands.mailbox_commands._create import _create

    return _create(email)
