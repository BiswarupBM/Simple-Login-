import click

from simplelogincmd.cli import const, util
from simplelogincmd.database.models import (
    Alias,
    Mailbox,
)


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
@click.pass_obj
@util.authenticate
def update(
    obj,
    id: int,
    note: str | None,
    name: str | None,
    mailboxes: tuple[str],
    disable_pgp: bool | None,
    pinned: bool | None,
) -> bool:
    """Modify an alias's fields"""
    sl, db = obj.sl, obj.db
    id = util.resolve_id(db, Alias, id)
    mailbox_ids = {util.resolve_id(db, Mailbox, mb_id) for mb_id in mailboxes}
    if note == "_EDIT":
        note = util.edit()
    success, msg = sl.update_alias(
        alias_id=id,
        note=note,
        name=name,
        mailbox_ids=mailbox_ids,
        disable_pgp=disable_pgp,
        pinned=pinned,
    )
    if not success:
        click.echo(msg)
        return False
    return True
