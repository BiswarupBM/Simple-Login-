import click

from simplelogincmd.cli import const


@click.command(
    "custom",
    short_help=const.HELP.ALIAS.CUSTOM.SHORT,
    help=const.HELP.ALIAS.CUSTOM.LONG,
)
@click.option(
    "-o",
    "--hostname",
    help=const.HELP.ALIAS.CUSTOM.OPTION.HOSTNAME,
)
@click.option(
    "-p",
    "--prefix",
    help=const.HELP.ALIAS.CUSTOM.OPTION.PREFIX,
)
@click.option(
    "-m",
    "--mailbox",
    "mailboxes",
    required=True,
    multiple=True,
    help=const.HELP.ALIAS.CUSTOM.OPTION.MAILBOXES,
)
@click.option(
    "-n",
    "--note",
    is_flag=False,
    flag_value="_EDIT",
    help=const.HELP.ALIAS.CUSTOM.OPTION.NOTE,
)
@click.option(
    "-a",
    "--name",
    help=const.HELP.ALIAS.CUSTOM.OPTION.NAME,
)
@click.option(
    "-s",
    "--select-suffix",
    type=int,
    help=const.HELP.ALIAS.CUSTOM.OPTION.SELECT_SUFFIX,
)
@click.option(
    "-y",
    "--yes",
    "bypass_confirmation",
    is_flag=True,
    flag_value=True,
    default=False,
    help=const.HELP.ALIAS.CUSTOM.OPTION.YES,
)
def custom(
    hostname: str | None,
    prefix: str,
    mailboxes: tuple[str],
    note: str | None,
    name: str | None,
    select_suffix: int | None,
    bypass_confirmation: bool,
) -> bool:
    """Create a new custom alias"""
    from simplelogincmd.cli.commands.alias_commands._custom import _custom

    return _custom(
        hostname,
        prefix,
        mailboxes,
        note,
        name,
        select_suffix,
        bypass_confirmation,
    )
