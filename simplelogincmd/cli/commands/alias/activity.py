import click

from simplelogincmd.cli import const, util
from simplelogincmd.database.models import Alias


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
@click.pass_obj
@util.authenticate
def activity(obj, id: int, include: str | None, exclude: str | None) -> None:
    """Display alias activities in a tabular format"""
    sl, db, cfg = obj.sl, obj.db, obj.cfg
    fields = util.get_display_fields_from_options(
        const.ACTIVITY_FIELD_ORDER, include, exclude
    )
    if len(fields) == 0:
        return
    id = util.resolve_id(db, Alias, id)
    activities = sl.get_all_alias_activities(id)
    if len(activities) == 0:
        click.echo("No activities found")
        return
    pager_threshold = cfg.get("display.pager-threshold")
    util.display_model_list(activities, fields, pager_threshold)
