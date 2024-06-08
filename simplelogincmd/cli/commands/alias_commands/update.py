import click

from simplelogincmd.cli import const


@click.command(
    "update",
    short_help=const.HELP.ALIAS.UPDATE.SHORT,
    help=const.HELP.ALIAS.UPDATE.LONG,
)
@click.argument(
    "id",
)
@click.option(
    "-n",
    "--note",
    is_flag=False,
    flag_value="_EDIT",
    help=const.HELP.ALIAS.UPDATE.OPTION.NOTE,
)
@click.option(
    "-a",
    "--name",
    help=const.HELP.ALIAS.UPDATE.OPTION.NAME,
)
@click.option(
    "-m",
    "--mailbox",
    "mailboxes",
    required=True,
    multiple=True,
    help=const.HELP.ALIAS.UPDATE.OPTION.MAILBOXES,
)
@click.option(
    "-d/-D",
    "--disable-pgp/--no-disable-pgp",
    default=None,
    help=const.HELP.ALIAS.UPDATE.OPTION.DISABLE_PGP,
)
@click.option(
    "-p/-P",
    "--pinned/--no-pinned",
    default=None,
    help=const.HELP.ALIAS.UPDATE.OPTION.PINNED,
)
def update(
    id: str,
    note: str | None,
    name: str | None,
    mailboxes: tuple[str],
    disable_pgp: bool | None,
    pinned: bool | None,
) -> bool:
    """Modify an alias's fields"""
    from simplelogincmd.cli.commands.alias_commands._update import _update

    return _update(id, note, name, mailboxes, disable_pgp, pinned)
