import click

from simplelogincmd.cli import const


@click.command(
    "random",
    short_help=const.HELP.ALIAS.RANDOM.SHORT,
    help=const.HELP.ALIAS.RANDOM.LONG,
    epilog=const.HELP.ALIAS.RANDOM.EPILOG,
)
@click.option(
    "-o",
    "--hostname",
    help=const.HELP.ALIAS.RANDOM.OPTION.HOSTNAME,
)
@click.option(
    "-u",
    "--uuid",
    "mode",
    flag_value="uuid",
    help=const.HELP.ALIAS.RANDOM.OPTION.UUID,
)
@click.option(
    "-w",
    "--word",
    "mode",
    flag_value="word",
    help=const.HELP.ALIAS.RANDOM.OPTION.WORD,
)
@click.option(
    "-n",
    "--note",
    is_flag=False,
    flag_value="_EDIT",
    help=const.HELP.ALIAS.RANDOM.OPTION.NOTE,
)
def random(hostname: str | None, mode: str | None, note: str | None) -> bool:
    """Create a new random alias"""
    from simplelogincmd.cli.commands.alias_commands._random import _random

    return _random(hostname, mode, note)
