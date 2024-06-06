import click

from simplelogincmd.cli import const


@click.command(
    "activity",
    short_help=const.HELP.ALIAS.ACTIVITY.SHORT,
    help=const.HELP.ALIAS.ACTIVITY.LONG,
    epilog=const.HELP.ALIAS.ACTIVITY.EPILOG,
)
@click.argument(
    "id",
)
@click.option(
    "-i",
    "--include",
    help=const.HELP.ALIAS.ACTIVITY.OPTION.INCLUDE,
)
@click.option(
    "-e",
    "--exclude",
    help=const.HELP.ALIAS.ACTIVITY.OPTION.EXCLUDE,
)
def activity(id: str, include: str | None, exclude: str | None) -> None:
    """Display alias activities in a tabular format"""
    from simplelogincmd.cli.commands.alias_commands._activity import _activity

    return _activity(id, include, exclude)
