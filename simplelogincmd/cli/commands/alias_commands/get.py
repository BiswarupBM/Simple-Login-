import click

from simplelogincmd.cli import const


@click.command(
    "get",
    short_help=const.HELP.ALIAS.GET.SHORT,
    help=const.HELP.ALIAS.GET.LONG,
)
@click.argument(
    "id",
)
@click.option(
    "-i",
    "--include",
    help=const.HELP.ALIAS.GET.OPTION.INCLUDE,
)
@click.option(
    "-e",
    "--exclude",
    help=const.HELP.ALIAS.GET.OPTION.EXCLUDE,
)
def get(id: str, include: str | None, exclude: str | None) -> None:
    """Display a single alias in a tabular format"""
    from simplelogincmd.cli.commands.alias_commands._get import _get

    return _get(id, include, exclude)
