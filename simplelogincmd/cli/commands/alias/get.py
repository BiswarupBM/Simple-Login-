import click

from simplelogincmd.cli import const, util
from simplelogincmd.database.models import Alias


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
@click.pass_obj
@util.authenticate
def get(obj, id: int, include: str | None, exclude: str | None) -> None:
    """Display a single alias in a tabular format"""
    sl, db = obj.sl, obj.db
    fields = util.get_display_fields_from_options(
        const.ALIAS_FIELD_ORDER, include, exclude
    )
    if len(fields) == 0:
        return
    id = util.resolve_id(db, Alias, id)
    success, obj = sl.get_alias(id)
    if not success:
        click.echo(obj)
        return None
    db.session.upsert(obj)
    db.session.commit()
    util.display_model_list([obj], fields, pager_threshold=0)
