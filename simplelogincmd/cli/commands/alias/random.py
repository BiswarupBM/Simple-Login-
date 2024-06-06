import click

from simplelogincmd.cli import const, util


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
@click.pass_obj
@util.authenticate
def random(
    obj,
    hostname: str | None,
    mode: str | None,
    note: str | None,
) -> bool:
    """Create a new random alias"""
    sl, db = obj.sl, obj.db
    if note == "_EDIT":
        note = util.edit()
    success, obj = sl.create_random_alias(hostname, mode, note)
    if not success:
        click.echo(obj)
        return False
    db.session.upsert(obj)
    db.session.commit()
    click.echo(obj.email)
    return True
