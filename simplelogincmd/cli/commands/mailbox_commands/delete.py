import click

from simplelogincmd.cli import const


@click.command(
    "delete",
    short_help=const.HELP.MAILBOX.DELETE.SHORT,
    help=const.HELP.MAILBOX.DELETE.LONG,
)
@click.argument(
    "id",
)
@click.option(
    "-t",
    "--transfer-aliases-to",
    default=-1,
    show_default=True,
    help=const.HELP.MAILBOX.DELETE.OPTION.TRANSFER_ALIASES_TO,
)
@click.option(
    "-y",
    "--yes",
    "bypass_confirm",
    is_flag=True,
    flag_value=True,
    default=False,
    help=const.HELP.MAILBOX.DELETE.OPTION.YES,
)
def delete(id: str, transfer_aliases_to: int, bypass_confirm: bool) -> bool:
    """Delete a mailbox"""
    from simplelogincmd.cli.commands.mailbox_commands._delete import _delete

    return _delete(id, transfer_aliases_to, bypass_confirm)
