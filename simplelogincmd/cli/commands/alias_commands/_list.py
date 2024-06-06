import click

from simplelogincmd.cli import const, util


def _list(include, exclude, query):
    fields = util.get_display_fields_from_options(
        const.ALIAS_FIELD_ORDER, include, exclude
    )
    if len(fields) == 0:
        return
    cfg = util.init_cfg()
    sl = util.init_sl(cfg)
    db = util.init_db(cfg)
    aliases = sl.get_all_aliases(query)
    if len(aliases) == 0:
        click.echo("No aliases found.")
        return
    for alias in aliases:
        db.session.upsert(alias)
    db.session.commit()
    pager_threshold = cfg.get("display.pager-threshold")
    util.display_model_list(aliases, fields, pager_threshold)
