import click

from simplelogincmd.cli import const, util
from simplelogincmd.database.models import Alias


def _activity(id, include, exclude):
    fields = util.output.get_display_fields_from_options(
        const.ACTIVITY_FIELD_ORDER, include, exclude
    )
    if len(fields) == 0:
        return
    cfg = util.init.cfg()
    sl = util.init.sl(cfg)
    db = util.init.db(cfg)
    id = util.input.resolve_id(db, Alias, id)
    activities = sl.get_all_alias_activities(id)
    if len(activities) == 0:
        click.echo("No activities found")
        return
    pager_threshold = cfg.get("display.pager-threshold")
    util.output.display_model_list(activities, fields, pager_threshold)
