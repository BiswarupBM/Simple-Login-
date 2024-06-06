import click

from simplelogincmd.cli import const


@click.command(
    "list",
    short_help=const.HELP.ALIAS.LIST.SHORT,
    help=const.HELP.ALIAS.LIST.LONG,
    epilog=const.HELP.ALIAS.LIST.EPILOG,
)
@click.option(
    "-i",
    "--include",
    help=const.HELP.ALIAS.LIST.OPTION.INCLUDE,
)
@click.option(
    "-e",
    "--exclude",
    help=const.HELP.ALIAS.LIST.OPTION.EXCLUDE,
)
@click.option(
    "-p",
    "--pinned",
    "query",
    flag_value="pinned",
    help=const.HELP.ALIAS.LIST.OPTION.PINNED,
)
@click.option(
    "-n",
    "--enabled",
    "query",
    flag_value="enabled",
    help=const.HELP.ALIAS.LIST.OPTION.ENABLED,
)
@click.option(
    "-d",
    "--disabled",
    "query",
    flag_value="disabled",
    help=const.HELP.ALIAS.LIST.OPTION.DISABLED,
)
def list(include: str | None, exclude: str | None, query: str | None) -> None:
    """Display aliases in a tabular format"""
    from simplelogincmd.cli.commands.alias_commands._list import _list

    return _list(include, exclude, query)
