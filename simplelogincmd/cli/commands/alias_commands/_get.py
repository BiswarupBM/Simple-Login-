import click

from simplelogincmd.cli import const, util
from simplelogincmd.database.models import Alias


def _get(id, include, exclude):
    fields = util.output.get_display_fields_from_options(
        const.ALIAS_FIELD_ORDER, include, exclude
    )
    if len(fields) == 0:
        return
    cfg = util.init.cfg()
    sl = util.init.sl(cfg)
    db = util.init.db(cfg)
    id = util.input.resolve_id(db, Alias, id)
    success, obj = sl.get_alias(id)
    if not success:
        click.echo(obj)
        return None
    db.session.upsert(obj)
    db.session.commit()
    util.output.display_model_list([obj], fields, pager_threshold=0)
